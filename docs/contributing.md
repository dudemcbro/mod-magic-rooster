# Contributing

How to report problems or send changes, and how the module is laid out.

## How to help

Bug reports and suggestions are welcome as
[GitHub issues](https://github.com/dudemcbro/mod-magic-rooster/issues).
For changes, fork the repository, make your change on a branch and open a pull
request that says what changed and how you tested it. Please do not add
Blizzard files (DBC, MPQ or other client data) to the repository.

## Module layout

```
data/sql/world/                World database SQL, imported by worldserver
data/sql/rollback/world/       World database rollback, applied by hand
scripts/build_client_patch.py     Builds the client Spell.dbc and MPQ from your own Spell.dbc
src/mod_magic_rooster_loader.cpp  Empty script loader, needed for the SQL import
```

The loader in `src/` is empty but needed; see
[installation](installation.md#1-get-the-module) for why.
