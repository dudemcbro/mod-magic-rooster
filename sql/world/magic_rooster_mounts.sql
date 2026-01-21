-- Magic Rooster starter mount setup
-- Everyone starts with the Magic Rooster egg, and class mounts are removed from new characters.

DELETE FROM `playercreateinfo_spell_custom`
WHERE `Spell` IN (23161, 23214, 34767);

DELETE FROM `playercreateinfo_item`
WHERE `itemid` IN (46778, 49290);

INSERT INTO `playercreateinfo_item` (`race`, `class`, `itemid`, `amount`, `Note`)
VALUES (0, 0, 46778, 1, 'Magic Rooster Egg');
