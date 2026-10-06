# AzerothCore: Magic Rooster Starter Mount

An [AzerothCore](https://www.azerothcore.org/) (WotLK 3.3.5a) module that makes
the Magic Rooster the starter mount for every new character. It is data only:
no scripts and no core changes.

## What It Does

After installation:

* Every character created from then on starts with one Magic Rooster Egg
  (item 46778) in its bags, for every race and class combination listed in
  `playercreateinfo`. Existing characters are not changed.
* The egg can be used from level 1 without Riding skill (stock: level 60 and
  Riding 150). Using it teaches the Magic Rooster mount (spell 65917) and uses
  up the egg.
* The rooster keeps whatever mount speed your server gives it. The module
  does not change mount speeds; if you run a mount speed module or profile,
  the rooster follows it like any other mount.
* The class mount spells 23161, 23214 and 34767 are removed from
  `playercreateinfo_spell_custom`. This only matters if you enable
  `PlayerStart.CustomSpells` in `worldserver.conf`; by default characters do
  not get those spells at creation.

An optional client patch fixes the Magic Rooster spell tooltip, which in the
stock client shows no mount speed at all.

## Requirements

* An AzerothCore WotLK server. For the automatic SQL import you build it from
  source, with the module in its `modules/` folder.
* To apply the SQL by hand instead: access to the world database
  (`acore_world` by default) with the `mysql` command line client.
* For the optional client patch: Python 3.8 or newer and the `Spell.dbc` of
  your own 3.3.5a (build 12340) client. This repository contains no Blizzard
  files.

## Installation

### 1. Get the module

Clone it into the `modules/` folder of your AzerothCore source:

```sh
cd <path to your AzerothCore source>/modules
git clone https://github.com/dudemcbro/mod-magic-rooster.git
```

Keep the folder name `mod-magic-rooster`, since the core expects the module's
script loader to be named after the folder. The module has no scripts and the
loader in [`src/`](src/) is empty, but it is needed: the core puts a module on
its module list only when the module has a `src/` folder, and worldserver
imports SQL only for modules on that list.

### 2. Re-run CMake and rebuild

Re-run CMake and rebuild the server as you normally do, for example with
`./acore.sh compiler build`. This adds the module to the module list that is
built into worldserver. Until then, worldserver does not import the module's
SQL.

### 3. Start worldserver

On start, worldserver imports the SQL in
[`data/sql/db-world/`](data/sql/db-world/) into the world database (the module
has no characters or auth database SQL), as long as `Updates.EnableDatabases`
in `worldserver.conf` includes the world database (flag 4, included in the
default of 7). It records each file in the world database's `updates` table
and applies it again only when the file changes. The import runs before the
world data loads, so this one start is enough.

The SQL:

* updates item 46778 in `item_template` (level 1, no skill requirement),
* gives item 46778 to every row of `playercreateinfo` through
  `playercreateinfo_item`, after removing any starter rows for 46778 and
  49290 (the other Magic Rooster Egg),
* removes spells 23161, 23214 and 34767 from `playercreateinfo_spell_custom`,
* removes the `spell_magic_rooster_speed` script binding that an earlier
  version of this module added, if it is present.

### Applying the SQL by hand

If `Updates.EnableDatabases` leaves out the world database, or you do not want
to rebuild, apply the files in `data/sql/db-world/` by hand in name order
(currently there is one), then restart worldserver:

```sh
mysql -u <user> -p acore_world < mod-magic-rooster/data/sql/db-world/mod_magic_rooster_mounts.sql
```

Use your own world database name if it is not `acore_world`. The file can be
run again safely, for example after an update. Applied this way, the module
does not need to be inside `modules/` and needs no rebuild.

## Client Patch (Optional)

The server does not need the client patch. Without it the game works the
same; only the Magic Rooster spell tooltip lacks its speed line.

### Build it

[`scripts/build_client_patch.py`](scripts/build_client_patch.py) patches a
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

### Install it

Copy `data/client/patch-9.MPQ` into the `Data/` folder of the client:

```
World of Warcraft/Data/patch-9.MPQ
```

If you already use a `patch-9.MPQ`, give this one a free patch name instead.
Then delete the client's `Cache/` folder (at least `Cache/WDB`) and restart
the client.

### Using it with other Spell.dbc patches

The client reads `Spell.dbc` from only one archive, so two patches that each
ship a full `Spell.dbc` cannot both take effect. To combine them (for example
with a mount speed tooltip profile), build one `Spell.dbc` that has every
change: run the other patcher first, give its patched `Spell.dbc` to this
script as `--dbc-in`, and install only the MPQ this script writes.

## Rollback

1. Undo the SQL changes. This restores the stock item requirements and stops
   giving the egg to new characters:

   ```sh
   mysql -u <user> -p acore_world < mod-magic-rooster/data/sql/rollback/db-world/mod_magic_rooster_rollback.sql
   ```

   Files in `data/sql/rollback/` are never imported automatically. If
   worldserver imported the install SQL, also remove its row from the world
   database's `updates` table, so that a later reinstall imports it again:

   ```sql
   DELETE FROM `updates` WHERE `name` = 'mod_magic_rooster_mounts.sql';
   ```

2. If the module is in your `modules/` folder, remove it so worldserver does
   not import the install SQL again, then re-run CMake and rebuild.
3. Remove the client MPQ from `World of Warcraft/Data/` and delete the
   client's `Cache/` folder.
4. Restart worldserver.

Characters keep eggs and mounts they already have. The rollback does not
re-add rows to `playercreateinfo_spell_custom`, since the stock database has
none for these spells.

## Updating

```sh
cd mod-magic-rooster
git pull
```

If the update changed anything in `src/`, re-run CMake and rebuild. Then
restart worldserver; it applies the files in `data/sql/db-world/` again if
they changed. If you apply the SQL by hand, apply the files in
`data/sql/db-world/` again in name order and restart worldserver. If
`scripts/build_client_patch.py` changed, rebuild and reinstall the client
patch as well.

If you are updating from the version that set the rooster to 60%: re-run CMake
and rebuild once so the old script is dropped from `worldserver`. The install
SQL removes the old script binding when it runs.

### Upgrading from a manual install

Earlier versions kept the SQL in `sql/world/` and had you apply it by hand.
After you install this version as described above, worldserver sees
`mod_magic_rooster_mounts.sql` as a new file and applies it once on the next
start. That is safe: the file is written to be run more than once, and on a
database where it already ran it changes nothing, unless you edited its rows by
hand since.

To skip that run, mark the file as applied in the world database before you
start worldserver:

```sql
INSERT INTO `updates` (`name`, `hash`, `state`) VALUES ('mod_magic_rooster_mounts.sql', '', 'MODULE');
```

On the next start, worldserver only stores the file's hash and does not run it
(this needs `Updates.AllowRehash`, on by default). Only do this if the SQL you
applied by hand is the current version. If you are coming from the 60%
version, let the file run so it removes the old script binding.

## Module Layout

```
data/sql/db-world/                World database SQL, imported by worldserver
data/sql/rollback/db-world/       World database rollback, applied by hand
scripts/build_client_patch.py     Builds the client Spell.dbc and MPQ from your own Spell.dbc
src/mod_magic_rooster_loader.cpp  Empty script loader, needed for the SQL import
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
