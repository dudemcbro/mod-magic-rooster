# AzerothCore – Magic Rooster Starter Mounts

This is a data only AzerothCore module.

It makes the Magic Rooster the only starter mount:

* All new characters start with the Magic Rooster Egg (item 46778)
* Class mount spells are removed from new characters (paladin and warlock)
* Magic Rooster tooltip shows 100 percent speed using a DBC patch

No server code and no core patches are required.

## Server Installation

1. SQL import (world database)

Apply the SQL file to your world database:

```
sql/world/magic_rooster_mounts.sql
```

2. Server DBC (spell data and speed)

Copy the server DBC file to your DataDir:

```
data/client/patch-contents/dbc/Spell.dbc
```

Destination example:

```
<DataDir>/dbc/Spell.dbc
```

DataDir is defined in worldserver.conf.

Restart worldserver after copying.

## Client Installation

Copy the MPQ to the client data directory:

```
data/client/patch-9.MPQ
```

Destination:

```
World of Warcraft/Data/
```

If using locale MPQs, rename accordingly, for example:

```
patch-enUS-9.MPQ
```

and place it under:

```
World of Warcraft/Data/enUS/
```

## Client Cache

After installing client files, delete:

```
World of Warcraft/Cache/
```

or at least:

```
Cache/WDB
```

## Module Layout

```
data/client/        Client DBC and MPQ files

```

