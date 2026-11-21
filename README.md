# mod-magic-rooster

<img src="icon.png" alt="" width="64" align="right">

An [AzerothCore](https://www.azerothcore.org/) (WotLK 3.3.5a) module that makes
the Magic Rooster the starter mount for every new character. Each new character
starts with a Magic Rooster Egg it can use from level 1. The module is data
only: no scripts and no core changes.

- **Author:** [dudemcbro](https://github.com/dudemcbro)
- **License:** [GNU GPL v3.0](LICENSE)
- **Works with:** An AzerothCore WotLK server (3.3.5a, build 12340 client for the optional patch)

## Features

- **An egg in every new character's bags.** Every character created from then
  on starts with one Magic Rooster Egg (item 46778) in its bags, for every race
  and class combination listed in `playercreateinfo`. Existing characters are
  not changed.
- **Usable from level 1.** The egg can be used from level 1 without Riding
  skill (stock: level 60 and Riding 150). Using it teaches the Magic Rooster
  mount (spell 65917) and uses up the egg.
- **Your server's mount speed.** The rooster keeps whatever mount speed your
  server gives it. The module does not change mount speeds; if you run a mount
  speed module or profile, the rooster follows it like any other mount.
- **No class mount spells at creation.** The class mount spells 23161, 23214
  and 34767 are removed from `playercreateinfo_spell_custom`. This only matters
  if you enable `PlayerStart.CustomSpells` in `worldserver.conf`; by default
  characters do not get those spells at creation.
- **An optional client patch.** It fixes the Magic Rooster spell tooltip,
  which in the stock client shows no mount speed at all.

## Quick start

1. Clone into your AzerothCore `modules/` folder (keep the name `mod-magic-rooster`):
   ```sh
   cd <azerothcore>/modules
   git clone https://github.com/dudemcbro/mod-magic-rooster.git
   ```
2. Re-run CMake, build and install the core.
3. Start `worldserver`. It imports the SQL in `data/sql/world/` into the world
   database, as long as `Updates.EnableDatabases` includes the world database
   (flag 4, part of the default of 7).
4. Optional: build the client patch from your own `Spell.dbc` and give
   `patch-9.MPQ` to your players:
   ```sh
   python3 scripts/build_client_patch.py --dbc-in <path to your Spell.dbc>
   ```

The full steps, requirements, applying the SQL by hand, updating and rollback
are in [docs/installation.md](docs/installation.md).

## Documentation

| Page | What's in it |
| --- | --- |
| [Installation](docs/installation.md) | Requirements, install, what the SQL changes, applying it by hand, updating, upgrading from a manual install, rollback |
| [The client patch](docs/client-patch.md) | Building and installing the optional tooltip patch, combining it with other `Spell.dbc` patches |
| [Contributing](docs/contributing.md) | How to help, and the module layout |

## Contributing

Bug reports and suggestions are welcome as
[GitHub issues](https://github.com/dudemcbro/mod-magic-rooster/issues).
For changes, fork the repository, make your change on a branch and open a pull
request that says what changed and how you tested it. Please do not add
Blizzard files (DBC, MPQ or other client data) to the repository. The module
layout is in [docs/contributing.md](docs/contributing.md).

## License

This module is released under the GNU General Public License v3.0. See
[LICENSE](LICENSE).
