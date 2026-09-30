-- Magic Rooster starter mount setup (acore_world)
-- Everyone starts with the Magic Rooster Egg, the rooster runs at 60% mounted
-- speed, and class mounts are removed from new characters.
-- This file is safe to run more than once.

-- Remove class mount spells from new characters
DELETE FROM `playercreateinfo_spell_custom`
WHERE `Spell` IN (23161, 23214, 34767);

-- Remove any existing starter mount items to keep this idempotent
DELETE FROM `playercreateinfo_item`
WHERE `itemid` IN (46778, 49290);

-- Make the Magic Rooster Egg usable at level 1 without riding skill, and drop
-- the "very fast mount" text since the rooster is a 60% mount here
UPDATE `item_template`
SET
  `RequiredLevel` = 1,
  `RequiredSkill` = 0,
  `RequiredSkillRank` = 0,
  `description` = 'Teaches you how to summon this mount.'
WHERE `entry` = 46778;

-- Give the Magic Rooster Egg to all valid race and class combinations
INSERT INTO `playercreateinfo_item` (`race`, `class`, `itemid`, `amount`, `Note`)
SELECT `race`, `class`, 46778, 1, 'Magic Rooster Egg'
FROM `playercreateinfo`;

-- Bind the Magic Rooster mount auras to the module's speed script
-- (src/mod_magic_rooster.cpp), which sets their mounted speed to 60%
DELETE FROM `spell_script_names`
WHERE `ScriptName` = 'spell_magic_rooster_speed';

INSERT INTO `spell_script_names` (`spell_id`, `ScriptName`) VALUES
(66122, 'spell_magic_rooster_speed'),
(66123, 'spell_magic_rooster_speed'),
(66124, 'spell_magic_rooster_speed');
