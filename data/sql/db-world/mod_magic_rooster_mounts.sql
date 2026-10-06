-- Magic Rooster starter mount setup (acore_world)
-- Everyone starts with the Magic Rooster Egg and class mounts are removed from
-- new characters. The rooster keeps whatever mount speed your server gives it.
-- This file is safe to run more than once.

-- Remove class mount spells from new characters
DELETE FROM `playercreateinfo_spell_custom`
WHERE `Spell` IN (23161, 23214, 34767);

-- Remove any existing starter mount items to keep this idempotent
DELETE FROM `playercreateinfo_item`
WHERE `itemid` IN (46778, 49290);

-- Make the Magic Rooster Egg usable at level 1 without riding skill
UPDATE `item_template`
SET
  `RequiredLevel` = 1,
  `RequiredSkill` = 0,
  `RequiredSkillRank` = 0
WHERE `entry` = 46778;

-- Give the Magic Rooster Egg to all valid race and class combinations
INSERT INTO `playercreateinfo_item` (`race`, `class`, `itemid`, `amount`, `Note`)
SELECT `race`, `class`, 46778, 1, 'Magic Rooster Egg'
FROM `playercreateinfo`;

-- Remove the speed script binding added by an earlier version of this module
-- (the module no longer changes the rooster's speed)
DELETE FROM `spell_script_names`
WHERE `ScriptName` = 'spell_magic_rooster_speed';
