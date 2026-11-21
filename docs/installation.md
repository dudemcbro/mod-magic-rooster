# Installation, updating and rollback

How to install mod-magic-rooster, what its SQL changes, and how to update or remove it.

- [Requirements](#requirements)
- [1. Get the module](#1-get-the-module)
- [2. Re-run CMake and rebuild](#2-re-run-cmake-and-rebuild)
- [3. Start worldserver](#3-start-worldserver)
- [Applying the SQL by hand](#applying-the-sql-by-hand)
- [Updating](#updating)
- [Upgrading from a manual install](#upgrading-from-a-manual-install)
- [Rollback](#rollback)

## Requirements

* An AzerothCore WotLK server. For the automatic SQL import you build it from
  source, with the module in its `modules/` folder.
* To apply the SQL by hand instead: access to the world database
  (`acore_world` by default) with the `mysql` command line client.
* For the optional client patch: Python 3.8 or newer and the `Spell.dbc` of
  your own 3.3.5a (build 12340) client. This repository contains no Blizzard
  files. See [the client patch](client-patch.md).

## 1. Get the module

Clone it into the `modules/` folder of your AzerothCore source:

```sh
cd <path to your AzerothCore source>/modules
git clone https://github.com/dudemcbro/mod-magic-rooster.git
```

Keep the folder name `mod-magic-rooster`, since the core expects the module's
script loader to be named after the folder. The module has no scripts and the
loader in [`src/`](../src/) is empty, but it is needed: the core puts a module on
its module list only when the module has a `src/` folder, and worldserver
imports SQL only for modules on that list.

## 2. Re-run CMake and rebuild

Re-run CMake and rebuild the server as you normally do, for example with
`./acore.sh compiler build`. This adds the module to the module list that is
built into worldserver. Until then, worldserver does not import the module's
SQL.

## 3. Start worldserver

On start, worldserver imports the SQL in
[`data/sql/world/`](../data/sql/world/) into the world database (the module
has no characters or auth database SQL), as long as `Updates.EnableDatabases`
in `worldserver.conf` includes the world database (flag 4, included in the
default of 7). It records each file in the world database's `updates` table
and applies it again only when the file changes. The import runs before the
world data loads, so this one start is enough.

The folder is called `world` rather than the skeleton module's `db-world` on
purpose: cores built before AzerothCore's April 2026 change to module SQL
folder matching
([azerothcore-wotlk#25372](https://github.com/azerothcore/azerothcore-wotlk/pull/25372))
only import folders named exactly `world`, `characters` and `auth`, and newer
cores import both.

The SQL:

* updates item 46778 in `item_template` (level 1, no skill requirement),
* gives item 46778 to every row of `playercreateinfo` through
  `playercreateinfo_item`, after removing any starter rows for 46778 and
  49290 (the other Magic Rooster Egg),
* removes spells 23161, 23214 and 34767 from `playercreateinfo_spell_custom`,
* removes the `spell_magic_rooster_speed` script binding that an earlier
  version of this module added, if it is present.

## Applying the SQL by hand

If `Updates.EnableDatabases` leaves out the world database, or you do not want
to rebuild, apply the files in `data/sql/world/` by hand in name order
(currently there is one), then restart worldserver:

```sh
mysql -u <user> -p acore_world < mod-magic-rooster/data/sql/world/mod_magic_rooster_mounts.sql
```

Use your own world database name if it is not `acore_world`. The file can be
run again safely, for example after an update. Applied this way, the module
does not need to be inside `modules/` and needs no rebuild.

## Updating

```sh
cd mod-magic-rooster
git pull
```

If the update changed anything in `src/`, re-run CMake and rebuild. Then
restart worldserver; it applies the files in `data/sql/world/` again if
they changed. If you apply the SQL by hand, apply the files in
`data/sql/world/` again in name order and restart worldserver. If
`scripts/build_client_patch.py` changed, rebuild and reinstall the
[client patch](client-patch.md) as well.

If you are updating from the version that set the rooster to 60%: re-run CMake
and rebuild once so the old script is dropped from `worldserver`. The install
SQL removes the old script binding when it runs.

## Upgrading from a manual install

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

## Rollback

1. Undo the SQL changes. This restores the stock item requirements and stops
   giving the egg to new characters:

   ```sh
   mysql -u <user> -p acore_world < mod-magic-rooster/data/sql/rollback/world/mod_magic_rooster_rollback.sql
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
