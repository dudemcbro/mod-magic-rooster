# The client patch (optional)

Building and installing the optional patch that fixes the Magic Rooster spell tooltip.

The server does not need the client patch. Without it the game works the
same; only the Magic Rooster spell tooltip lacks its speed line. In the stock
client the tooltip shows no mount speed at all.

You need Python 3.8 or newer and the `Spell.dbc` of your own 3.3.5a (build
12340) client. This repository contains no Blizzard files.

## Build it

[`scripts/build_client_patch.py`](../scripts/build_client_patch.py) patches a
copy of your own `Spell.dbc` and packs it into an MPQ. It needs no extra
Python packages.

Use the `Spell.dbc` that matches your client, for example the one the
AzerothCore extractor wrote to the `dbc/` folder of your server's `DataDir`
(it comes from your client), or one you extract yourself from your client's
MPQ files. The input file is only read.

```sh
cd mod-magic-rooster
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
| 65917 Magic Rooster | effects 1 and 2 target the caster; effect 2 becomes a mounted speed aura of 100%, the rooster's real speed |

## Install it

Copy `data/client/patch-9.MPQ` into the `Data/` folder of the client:

```
World of Warcraft/Data/patch-9.MPQ
```

If you already use a `patch-9.MPQ`, give this one a free patch name instead.
Then delete the client's `Cache/` folder (at least `Cache/WDB`) and restart
the client.

## Using it with other Spell.dbc patches

The client reads `Spell.dbc` from only one archive, so two patches that each
ship a full `Spell.dbc` cannot both take effect. To combine them (for example
with a mount speed tooltip profile), build one `Spell.dbc` that has every
change: run the other patcher first, give its patched `Spell.dbc` to this
script as `--dbc-in`, and install only the MPQ this script writes.

## Removing it

Remove the client MPQ from `World of Warcraft/Data/` and delete the client's
`Cache/` folder. The full rollback is in [installation](installation.md#rollback).
