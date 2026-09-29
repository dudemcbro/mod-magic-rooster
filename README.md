# AzerothCore: Magic Rooster Starter Mount

An [AzerothCore](https://www.azerothcore.org/) (WotLK 3.3.5a) module that makes
the Magic Rooster the starter mount for every new character and turns it into a
60% ground mount.

## What It Does

After installation:

* Every character created from then on starts with one Magic Rooster Egg
  (item 46778) in its bags, for every race and class combination listed in
  `playercreateinfo`. Existing characters are not changed.
* The egg can be used from level 1 without Riding skill (stock: level 60 and
  Riding 150). Using it teaches the Magic Rooster mount (spell 65917) and uses
  up the egg.
* The Magic Rooster is a ground mount with 60% mounted speed, the speed of an
  Apprentice Riding mount (stock: 100%). The speed is fixed: it does not change
  with Riding skill, and the rooster never flies. Other mounted speed bonuses
  apply as they do on any other 60% mount.
* The 60% speed applies to every Magic Rooster on the realm, including ones
  learned before the module was installed.
* The egg's description no longer says "This is a very fast mount."
* The class mount spells 23161, 23214 and 34767 are removed from
  `playercreateinfo_spell_custom`. This only matters if you enable
  `PlayerStart.CustomSpells` in `worldserver.conf`; by default characters do
  not get those spells at creation.

An optional client patch makes the in-game tooltips agree with the server:
the Magic Rooster buff reads "Increases speed by 60%." and the spell no longer
calls itself a very fast mount.

### How the speed change works

Casting Magic Rooster (65917) makes the core cast spell 66122 through
`spell_linked_spell`. That spell, like its model variants 66123 and 66124,
holds the mount aura and a mounted speed aura of 100%. The module's spell
script ([`src/mod_magic_rooster.cpp`](src/mod_magic_rooster.cpp)) sets that
speed aura to 60% when it is applied, and the core calculates the mounted
speed from it as for any other mount. No core changes and no server DBC
changes are needed.

## Requirements

* An AzerothCore WotLK source checkout that you build yourself.
* Access to the world database (`acore_world` by default) with the `mysql`
  command line client.
* For the optional client patch: Python 3.8 or newer and the `Spell.dbc` of
  your own 3.3.5a (build 12340) client. This repository contains no Blizzard
  files.

## Installation

### 1. Add the module and build

Clone the module into the `modules/` folder of your AzerothCore source tree:

```sh
cd <azerothcore>/modules
git clone https://github.com/dudemcbro/mod-magic-rooster.git
```

Re-run CMake in your build directory with the options you normally use, then
build and install:

```sh
cd <azerothcore>/build
cmake ..
make -j"$(nproc)"
make install
```

The spell script is compiled into `worldserver`.

### 2. Apply the SQL to the world database

The SQL lives in [`sql/world/`](sql/world/). AzerothCore's database updater
only imports module SQL from folders under the module's `data/sql/`, so these
files are **not** applied automatically. Apply the install file by hand:

```sh
mysql -u <user> -p acore_world < <azerothcore>/modules/mod-magic-rooster/sql/world/magic_rooster_mounts.sql
```

Use your own world database name if it is not `acore_world`. The file can be
run again safely, for example after an update.

The file:

* updates item 46778 in `item_template` (level 1, no skill requirement, new
  description),
* gives item 46778 to every row of `playercreateinfo` through
  `playercreateinfo_item`, after removing any starter rows for 46778 and
  49290 (the other Magic Rooster Egg),
* removes spells 23161, 23214 and 34767 from `playercreateinfo_spell_custom`,
* binds spells 66122, 66123 and 66124 to the script
  `spell_magic_rooster_speed` in `spell_script_names`. Without these rows the
  rooster keeps its stock 100% speed.

### 3. Restart worldserver

The new rows and the script are loaded at startup.

## Client Patch (Optional)

The server does not need the client patch. Without it the game still works
and the rooster still runs at 60%, but the tooltips show the stock text
("Increases speed by 100%." and "This is a very fast mount.").

### Build it

[`scripts/build_client_patch.py`](scripts/build_client_patch.py) patches a
copy of your own `Spell.dbc` and packs it into an MPQ. It needs no extra
Python packages.

Use the `Spell.dbc` that matches your client, for example the one the
AzerothCore extractor wrote to the `dbc/` folder of your server's `DataDir`
(it comes from your client), or one you extract yourself from your client's
MPQ files. The input file is only read.

```sh
cd <azerothcore>/modules/mod-magic-rooster
python3 scripts/build_client_patch.py --dbc-in <path to your Spell.dbc>
```

This writes:

```
data/client/DBFilesClient/Spell.dbc   patched Spell.dbc
data/client/patch-9.MPQ               MPQ holding DBFilesClient\Spell.dbc
```

Use `--dbc-out` and `--mpq-out` to write somewhere else, and `--help` for all
options. Both outputs contain Blizzard data and are ignored by git; do not
commit or publish them.

The script checks that every field it changes still holds its stock value and
stops if it does not. If you knowingly give it a `Spell.dbc` that another tool
already changed in those fields, add `--force`.

What the script changes in `Spell.dbc`:

| Spell | Change |
| --- | --- |
| 65917 Magic Rooster | effects 1 and 2 target the caster; effect 2 becomes a mounted speed aura of 60% |
| 66122, 66123, 66124 Magic Rooster | mounted speed aura changed from 100% to 60% |
| 65917, 66122, 66123, 66124 | enUS description loses "This is a very fast mount." |

Descriptions in other client languages are left unchanged.

### Install it

Copy `data/client/patch-9.MPQ` into the `Data/` folder of the client:

```
World of Warcraft/Data/patch-9.MPQ
```

If you already use a `patch-9.MPQ`, give this one a free patch name instead.

Then delete the client's `Cache/` folder (at least `Cache/WDB`) so the item and
spell text is loaded fresh, and restart the client.

### Using it with other Spell.dbc patches

The client reads `Spell.dbc` from only one archive, so two patches that each
ship a full `Spell.dbc` cannot both take effect. To combine them, build one
`Spell.dbc` that has every change: run the other patcher first, give its
patched `Spell.dbc` to this script as `--dbc-in`, and install only the MPQ
this script writes.

## Rollback

1. Undo the SQL changes. This restores the stock item requirements and
   description, stops giving the egg to new characters and removes the script
   binding:

   ```sh
   mysql -u <user> -p acore_world < <azerothcore>/modules/mod-magic-rooster/sql/world/magic_rooster_rollback.sql
   ```

2. Remove `modules/mod-magic-rooster`, re-run CMake and rebuild.
3. Remove the client MPQ from `World of Warcraft/Data/` and delete the
   client's `Cache/` folder.
4. Restart worldserver.

Characters keep eggs and mounts they already have; after the rollback those
roosters are 100% mounts again. The rollback does not re-add rows to
`playercreateinfo_spell_custom`, since the stock database has none for these
spells.

## Updating

```sh
cd <azerothcore>/modules/mod-magic-rooster
git pull
```

Then rebuild (installation step 1), apply
`sql/world/magic_rooster_mounts.sql` again (step 2) and restart worldserver.
If `scripts/build_client_patch.py` changed, rebuild and reinstall the client
patch as well.

## Module Layout

```
scripts/build_client_patch.py   Builds the client Spell.dbc and MPQ from your own Spell.dbc
sql/world/                      World database SQL (install and rollback, applied by hand)
src/mod_magic_rooster.cpp       Spell script that sets the rooster speed to 60%
```

## Contributing

Bug reports and suggestions are welcome as
[GitHub issues](https://github.com/dudemcbro/mod-magic-rooster/issues).
For changes, fork the repository, make your change on a branch and open a pull
request that says what changed and how you tested it. Please do not add
Blizzard files (DBC, MPQ or other client data) to the repository.

## License

This module is released under the GNU General Public License v3.0. See
[LICENSE](LICENSE).
