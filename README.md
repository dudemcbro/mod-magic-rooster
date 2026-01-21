# AzerothCore - Magic Rooster Starter Mounts

This module makes the Magic Rooster the only starter mount:
- All new characters start with the Magic Rooster Egg (item 46778).
- Class mount spells are removed from new characters (paladin/warlock).
- Magic Rooster tooltip shows 100% with the provided DBC patch.

## Installation

1) Apply the SQL to the world database:
   - `data/sql/db-world/magic_rooster_mounts.sql`

2) Server DBC (for speed + spell data):
   - Copy `patch-contents/dbc/Spell.dbc` to your server `DataDir/dbc/Spell.dbc`.
   - `DataDir` is defined in `worldserver.conf` (example: `/data/wow335`).

3) Client DBC (for tooltip text):
   - Copy `patch-9.MPQ` to the client `World of Warcraft/Data/` folder.
   - If you use locale MPQs, rename to `patch-<locale>-9.MPQ` (e.g. `patch-enUS-9.MPQ`) and place it under `World of Warcraft/Data/<locale>/`.
   - Alternative: use loose DBC by copying `patch-contents/DBFilesClient/Spell.dbc` to:
     - `World of Warcraft/Data/DBFilesClient/Spell.dbc` and/or
     - `World of Warcraft/Data/<locale>/DBFilesClient/Spell.dbc`

4) Clear client cache:
   - Delete `World of Warcraft/Cache/` (or at least `Cache/WDB`).

5) Restart worldserver so it reloads the DBC.

## Optional: remove already learned class mounts

If you want to remove class mounts from existing characters:

```
DELETE FROM character_spell WHERE spell IN (23161, 23214, 34767);
```

## Files

- `data/sql/db-world/magic_rooster_mounts.sql`
- `patch-contents/dbc/Spell.dbc`
- `patch-contents/DBFilesClient/Spell.dbc`
- `patch-9.MPQ`
