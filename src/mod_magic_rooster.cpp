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
    MagicRoosterSpeed() : PlayerScript("MagicRoosterSpeed") {}

    void OnUpdate(Player* player, uint32 /*diff*/) override
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

        if (player->GetSpeedRate(MOVE_RUN) < ROOSTER_RUN_RATE)
        {
            player->SetSpeedRate(MOVE_RUN, ROOSTER_RUN_RATE);
            player->UpdateSpeed(MOVE_RUN, true);
        }
    }
};

void Addmod_magic_roosterScripts()
{
    new MagicRoosterSpeed();
}
