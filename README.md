# AzerothCore: Magic Rooster Starter Mounts

An AzerothCore (WotLK 3.3.5a) module that makes the Magic Rooster the starter
mount for every new character.

* All new characters start with the Magic Rooster Egg (item 46778), usable at
  level 1 without Riding skill.
* Class mount spells (23161, 23214, 34767) are removed from
  `playercreateinfo_spell_custom`. This only matters if you enable
  `PlayerStart.CustomSpells` in `worldserver.conf`; stock characters do not get
  these spells at creation.
* A small server script (`src/mod_magic_rooster.cpp`) keeps the Magic Rooster
  at a minimum of 60% mounted run speed.
* A client patch (`data/client/patch-9.MPQ`) carries a patched `Spell.dbc` for
  the Magic Rooster tooltip.

No core patches are required. No server DBC files are required.

## Server Installation

1. Place the module in the `modules/` folder of your AzerothCore source tree,
   re-run CMake and rebuild. The server script is compiled into worldserver.

2. Import the SQL into the world database. The file lives in `sql/world/` and
   is NOT picked up by the AzerothCore DB auto-updater (it only reads
   `data/sql/db-world/` inside a module), so apply it manually:

   ```
   mysql -u <user> -p acore_world < sql/world/magic_rooster_mounts.sql
   ```

   The file is re-runnable.

3. Restart worldserver.

To undo the SQL changes:

```
mysql -u <user> -p acore_world < sql/world/magic_rooster_rollback.sql
```

## Client Installation

Copy the MPQ to the client data directory:

```
data/client/patch-9.MPQ  ->  World of Warcraft/Data/
```

If you already use a `patch-9.MPQ`, rename this one to a free patch number.
If using locale MPQs, rename it accordingly, for example `patch-enUS-9.MPQ`,
and place it under `World of Warcraft/Data/enUS/`.

After installing client files, delete `World of Warcraft/Cache/` (or at least
`Cache/WDB`).

## Module Layout

```
data/client/   Client MPQ (patched Spell.dbc)
sql/world/     World database SQL (install and rollback)
src/           Server script
```
