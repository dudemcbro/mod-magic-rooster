-- Magic Rooster starter mount rollback (acore_world)
-- Restores the stock AzerothCore values changed by magic_rooster_mounts.sql.
-- The playercreateinfo_spell_custom rows it deletes are not stock rows, so
-- there is nothing to restore there.

-- Stop granting the egg to new characters
DELETE FROM `playercreateinfo_item`
WHERE `itemid` = 46778 AND `Note` = 'Magic Rooster Egg';

-- Stock requirements: level 60, Riding (762) 150
UPDATE `item_template`
SET
  `RequiredLevel` = 60,
  `RequiredSkill` = 762,
  `RequiredSkillRank` = 150
WHERE `entry` = 46778;
