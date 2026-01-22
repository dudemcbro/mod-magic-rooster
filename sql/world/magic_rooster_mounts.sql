-- Magic Rooster starter mount setup
-- Everyone starts with the Magic Rooster egg, and class mounts are removed from new characters.

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

