-- Magic Rooster starter mount rollback (acore_world)
-- Restores the stock AzerothCore values changed by mod_magic_rooster_mounts.sql
-- in data/sql/world/. The playercreateinfo_spell_custom rows it deletes are
-- not stock rows, so there is nothing to restore there.
-- Apply this file by hand: worldserver never imports data/sql/rollback/.

-- Stop granting the egg to new characters
DELETE FROM `playercreateinfo_item`
WHERE `itemid` = 46778 AND `Note` = 'Magic Rooster Egg';

-- Stock requirements (level 60, Riding (762) 150) and description
UPDATE `item_template`
SET
  `RequiredLevel` = 60,
  `RequiredSkill` = 762,
  `RequiredSkillRank` = 150,
  `description` = '"Teaches you how to summon this mount. This is a very fast mount."'
WHERE `entry` = 46778;

-- Remove the speed script binding, if an earlier version of the module added it
DELETE FROM `spell_script_names`
WHERE `ScriptName` = 'spell_magic_rooster_speed';
