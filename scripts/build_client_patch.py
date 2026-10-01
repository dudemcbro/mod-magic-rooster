#!/usr/bin/env python3
"""Build the Magic Rooster client patch from your own WotLK 3.3.5a Spell.dbc.

The module does not ship any Blizzard files. This script reads a Spell.dbc
that you supply (--dbc-in), fixes the Magic Rooster spell tooltip, and writes:

  * the patched Spell.dbc (--dbc-out), and
  * a single-file MPQ that holds it as DBFilesClient\\Spell.dbc (--mpq-out),
    ready to copy into the client's Data folder.

In the stock client the learned spell 65917 has no speed effect of its own
(the server casts the real mount aura, 66122, through spell_linked_spell), so
its tooltip shows no mount speed. This script gives 65917 the same mounted
speed aura the rooster really has (100%, unchanged), so the tooltip reads
correctly. Changes to Spell.dbc (3.3.5a build 12340 layout, 234 fields):

  65917 Magic Rooster:
    - effect 1 and 2 implicit target A: 0 -> 1 (TARGET_UNIT_CASTER)
    - effect 2 aura: 4 (DUMMY) -> 32 (MOD_INCREASE_MOUNTED_SPEED)
    - effect 2 base points: -1 -> 99 (tooltip value $s2 = 100)

The rooster's speed itself is not changed. The server does not read the client
Spell.dbc; mount speeds are whatever your server gives them.

Only one Spell.dbc is used by the client, taken from the highest priority MPQ.
If another tool also patches Spell.dbc (for example a mount speed profile),
run the patchers one after another (use one patcher's output as the next
one's --dbc-in) and install one MPQ.
"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

# The rooster's stock mounted speed, in percent.
SPEED_PCT = 100

# Spell.dbc 3.3.5a layout
FIELD_COUNT = 234
RECORD_SIZE = FIELD_COUNT * 4

F_ID = 0
F_EFFECT_BASE_POINTS = (80, 81, 82)
F_IMPLICIT_TARGET_A = (86, 87, 88)
F_EFFECT_AURA = (95, 96, 97)
F_NAME_ENUS = 136

TARGET_UNIT_CASTER = 1
SPELL_AURA_DUMMY = 4
SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED = 32

SPELL_MAGIC_ROOSTER = 65917

# (spell id, field index, stock value, new value)
FIELD_CHANGES = [
    (SPELL_MAGIC_ROOSTER, F_IMPLICIT_TARGET_A[0], 0, TARGET_UNIT_CASTER),
    (SPELL_MAGIC_ROOSTER, F_IMPLICIT_TARGET_A[1], 0, TARGET_UNIT_CASTER),
    (SPELL_MAGIC_ROOSTER, F_EFFECT_AURA[1], SPELL_AURA_DUMMY, SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED),
    (SPELL_MAGIC_ROOSTER, F_EFFECT_BASE_POINTS[1], -1, SPEED_PCT - 1),
]


class Dbc:
    """Minimal WDBC reader and writer."""

    def __init__(self, path: Path):
        data = path.read_bytes()
        if len(data) < 20 or data[:4] != b"WDBC":
            raise SystemExit(f"{path}: not a WDBC file")
        count, fields, size, strings = struct.unpack_from("<4I", data, 4)
        if fields != FIELD_COUNT or size != RECORD_SIZE:
            raise SystemExit(
                f"{path}: {fields} fields of {size} bytes per record, expected "
                f"{FIELD_COUNT} fields of {RECORD_SIZE} bytes. Is this a 3.3.5a Spell.dbc?"
            )
        end = 20 + count * size
        if len(data) < end + strings:
            raise SystemExit(f"{path}: file is truncated")
        self.count = count
        self.records = bytearray(data[20:end])
        self.strings = bytearray(data[end:end + strings])
        self.offsets = {}
        for i in range(count):
            spell_id = struct.unpack_from("<I", self.records, i * RECORD_SIZE)[0]
            self.offsets[spell_id] = i * RECORD_SIZE

    def get(self, spell_id: int, field: int) -> int:
        return struct.unpack_from("<i", self.records, self._pos(spell_id, field))[0]

    def set(self, spell_id: int, field: int, value: int) -> None:
        struct.pack_into("<i", self.records, self._pos(spell_id, field), value)

    def get_string(self, spell_id: int, field: int) -> str:
        start = struct.unpack_from("<I", self.records, self._pos(spell_id, field))[0]
        end = self.strings.index(b"\0", start)
        return self.strings[start:end].decode("utf-8")

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as out:
            out.write(b"WDBC")
            out.write(struct.pack("<4I", self.count, FIELD_COUNT, RECORD_SIZE, len(self.strings)))
            out.write(self.records)
            out.write(self.strings)

    def _pos(self, spell_id: int, field: int) -> int:
        if spell_id not in self.offsets:
            raise SystemExit(f"Spell {spell_id} is missing from the input Spell.dbc")
        return self.offsets[spell_id] + field * 4


def patch_spell_dbc(dbc: Dbc, force: bool) -> None:
    name = dbc.get_string(SPELL_MAGIC_ROOSTER, F_NAME_ENUS)
    if name and name != "Magic Rooster":
        raise SystemExit(f"Spell {SPELL_MAGIC_ROOSTER} is named {name!r}, expected 'Magic Rooster'")

    for spell_id, field, stock, new in FIELD_CHANGES:
        current = dbc.get(spell_id, field)
        if current not in (stock, new) and not force:
            raise SystemExit(
                f"Spell {spell_id} field {field} is {current}, expected the stock value {stock}. "
                "The input Spell.dbc is not stock here; use --force to patch it anyway."
            )
        if current != new:
            dbc.set(spell_id, field, new)
            print(f"  spell {spell_id} field {field}: {current} -> {new}")



# MPQ writer (pure Python, same approach as the other client patch builders
# used with this core): format version 0, one uncompressed single-unit file,
# 16-entry hash table (the 3.3.5a client needs at least 16 entries).

def _build_crypt_table() -> list:
    table = [0] * 0x500
    seed = 0x00100001
    for i in range(0x100):
        for j in range(5):
            seed = (seed * 125 + 3) % 0x2AAAAB
            high = (seed & 0xFFFF) << 16
            seed = (seed * 125 + 3) % 0x2AAAAB
            low = seed & 0xFFFF
            table[i + j * 0x100] = (high | low) & 0xFFFFFFFF
    return table


CRYPT_TABLE = _build_crypt_table()


def hash_string(text: str, hash_type: int) -> int:
    seed1, seed2 = 0x7FED7FED, 0xEEEEEEEE
    for ch in text.upper().replace("/", "\\"):
        value = CRYPT_TABLE[(hash_type << 8) + ord(ch)]
        seed1 = (value ^ (seed1 + seed2)) & 0xFFFFFFFF
        seed2 = (ord(ch) + seed1 + seed2 + ((seed2 << 5) & 0xFFFFFFFF) + 3) & 0xFFFFFFFF
    return seed1


def encrypt_table(data: bytes, key: int) -> bytes:
    seed1, seed2 = key & 0xFFFFFFFF, 0xEEEEEEEE
    out = bytearray()
    for i in range(0, len(data), 4):
        value = struct.unpack_from("<I", data, i)[0]
        seed2 = (seed2 + CRYPT_TABLE[0x400 + (seed1 & 0xFF)]) & 0xFFFFFFFF
        out += struct.pack("<I", (value ^ (seed1 + seed2)) & 0xFFFFFFFF)
        seed1 = (((~seed1) << 21) + 0x11111111 | (seed1 >> 11)) & 0xFFFFFFFF
        seed2 = (value + seed2 + ((seed2 << 5) & 0xFFFFFFFF) + 3) & 0xFFFFFFFF
    return bytes(out)


def build_mpq(mpq_path: Path, payload: bytes, internal_name: str) -> None:
    hash_entries = 16
    header_size = 32
    hash_table_offset = header_size
    block_table_offset = hash_table_offset + hash_entries * 16
    file_offset = block_table_offset + 16
    archive_size = file_offset + len(payload)

    hash_raw = bytearray(b"\xff" * (hash_entries * 16))
    slot = hash_string(internal_name, 0) % hash_entries
    hash_raw[slot * 16:(slot + 1) * 16] = struct.pack(
        "<IIHHI", hash_string(internal_name, 1), hash_string(internal_name, 2), 0, 0, 0
    )
    hash_table = encrypt_table(bytes(hash_raw), hash_string("(hash table)", 3))

    flags = 0x80000000 | 0x01000000  # MPQ_FILE_EXISTS | MPQ_FILE_SINGLE_UNIT
    block_table = encrypt_table(
        struct.pack("<IIII", file_offset, len(payload), len(payload), flags),
        hash_string("(block table)", 3),
    )

    header = struct.pack(
        "<4sIIHHIIII",
        b"MPQ\x1a",
        header_size,
        archive_size,
        0,  # format version
        3,  # sector size shift
        hash_table_offset,
        block_table_offset,
        hash_entries,
        1,  # block table entries
    )

    mpq_path.parent.mkdir(parents=True, exist_ok=True)
    with mpq_path.open("wb") as out:
        out.write(header)
        out.write(hash_table)
        out.write(block_table)
        out.write(payload)


MODULE_DIR = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--dbc-in", required=True, type=Path,
        help="your client's Spell.dbc (3.3.5a); it is only read, never changed",
    )
    parser.add_argument(
        "--dbc-out", type=Path, default=MODULE_DIR / "data/client/DBFilesClient/Spell.dbc",
        help="patched Spell.dbc output (default: %(default)s)",
    )
    parser.add_argument(
        "--mpq-out", type=Path, default=MODULE_DIR / "data/client/patch-9.MPQ",
        help="client MPQ output (default: %(default)s)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="patch even if a changed field does not hold its stock value",
    )
    args = parser.parse_args()

    if not args.dbc_in.is_file():
        raise SystemExit(f"Spell.dbc not found: {args.dbc_in}")
    if args.dbc_out.resolve() == args.dbc_in.resolve():
        raise SystemExit("--dbc-out must not be the same file as --dbc-in")

    print(f"Reading {args.dbc_in}")
    dbc = Dbc(args.dbc_in)
    print("Patching Magic Rooster records:")
    patch_spell_dbc(dbc, args.force)

    dbc.write(args.dbc_out)
    print(f"Wrote {args.dbc_out}")

    build_mpq(args.mpq_out, args.dbc_out.read_bytes(), "DBFilesClient\\Spell.dbc")
    print(f"Wrote {args.mpq_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
