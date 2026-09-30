/*
 * mod-magic-rooster: Magic Rooster starter mount.
 *
 * The Magic Rooster (item 46778, spell 65917) is a 100% ground mount in the
 * stock game. This module turns it into a 60% ground mount, the speed of an
 * Apprentice Riding mount, so it can be given to new characters.
 *
 * How the stock spells fit together in AzerothCore:
 *   - 65917 is the spell the player learns and casts. SpellInfoCorrections.cpp
 *     wipes its two aura effects, so it never applies a mount aura itself.
 *   - spell_linked_spell (65917 -> 66122) casts 66122 on the caster. 66122,
 *     66123 and 66124 are the actual mount auras (they only differ by the
 *     creature model): EFFECT_0 is SPELL_AURA_MOUNTED and EFFECT_1 is
 *     SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED with an amount of 100.
 *
 * The script below lowers that EFFECT_1 amount to 60 when the aura is created.
 * Unit::UpdateSpeed() then computes the mounted run speed from the aura as for
 * any other mount, so other mounted speed bonuses (for example a Riding Crop or
 * Crusader Aura) still apply on top in the usual way. The speed does not
 * change with Riding skill.
 *
 * The spells are bound to the script by spell_script_names rows in
 * sql/world/magic_rooster_mounts.sql.
 */

#include "ScriptMgr.h"
#include "SpellAuraEffects.h"
#include "SpellScript.h"
#include "SpellScriptLoader.h"

namespace
{
    // Apprentice Riding speed, in percent. Keep in sync with SPEED_PCT in
    // scripts/build_client_patch.py so the client tooltip shows the same value.
    constexpr int32 MAGIC_ROOSTER_SPEED_PCT = 60;
}

// 66122, 66123, 66124 - Magic Rooster (mount aura)
class spell_magic_rooster_speed : public AuraScript
{
    PrepareAuraScript(spell_magic_rooster_speed);

    void CalculateSpeed(AuraEffect const* /*aurEff*/, int32& amount, bool& /*canBeRecalculated*/)
    {
        amount = MAGIC_ROOSTER_SPEED_PCT;
    }

    void Register() override
    {
        DoEffectCalcAmount += AuraEffectCalcAmountFn(spell_magic_rooster_speed::CalculateSpeed, EFFECT_1, SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED);
    }
};

void Addmod_magic_roosterScripts()
{
    RegisterSpellScript(spell_magic_rooster_speed);
}
