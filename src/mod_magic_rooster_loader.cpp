/*
 * mod-magic-rooster has no scripts: it is SQL plus an optional client patch.
 *
 * The core only puts a folder in modules/ on its module list when the folder
 * has a src/ directory, and worldserver only imports the data/sql/ folders of
 * modules on that list. The generated script loader calls
 * Add<folder name>Scripts() (with '-' replaced by '_') for every listed
 * module, so this empty loader is what lets the module's SQL be imported
 * automatically. Keep the folder name mod-magic-rooster to match it.
 */

void Addmod_magic_roosterScripts()
{
}
