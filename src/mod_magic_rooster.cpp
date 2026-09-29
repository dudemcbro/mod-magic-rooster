#include "ScriptMgr.h"
#include "Player.h"
#include "SpellAuraEffects.h"

namespace
{
    constexpr uint32 SPELL_MAGIC_ROOSTER = 65917;
    constexpr float  ROOSTER_RUN_RATE    = 1.6f; // Journeyman 60%
}

class MagicRoosterSpeed final : public PlayerScript
{
public:
    MagicRoosterSpeed() : PlayerScript("MagicRoosterSpeed", { PLAYERHOOK_ON_UPDATE }) {}

    void OnPlayerUpdate(Player* player, uint32 /*diff*/) override
    {
        if (!player || !player->IsMounted())
            return;

        bool rooster = false;
        for (auto const* ae : player->GetAuraEffectsByType(SPELL_AURA_MOUNTED))
        {
            if (ae && ae->GetBase() && ae->GetBase()->GetId() == SPELL_MAGIC_ROOSTER)
            {
                rooster = true;
                break;
            }
        }

        if (!rooster)
            return;

        // SetSpeed() stores the rate and sends the forced speed change to the client.
        // (UpdateSpeed() would recompute the rate from auras and undo the change.)
        if (player->GetSpeedRate(MOVE_RUN) < ROOSTER_RUN_RATE)
            player->SetSpeed(MOVE_RUN, ROOSTER_RUN_RATE, true);
    }
};

void Addmod_magic_roosterScripts()
{
    new MagicRoosterSpeed();
}
