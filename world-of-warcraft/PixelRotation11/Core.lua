PixelRotation11 = {}

local pr = PixelRotation11

local talent = {  }
local spell = {  }
local buff = {  }
local item = {  }






-- 判断天赋是否启用
function pr.TalentEnabled(talent_name)
    return IsPlayerSpell(talent[talent_name])
end

function pr.TalentDisabled(talent_name)
    return not IsPlayerSpell(talent[talent_name])
end


-- gcd_remaining
-- 返回gcd的剩余时间，单位为秒。
-- /dump C_Spell.GetSpellCooldown(61304)
-- /dump PixelRotation11.GcdRemaining()

function pr.GcdRemaining()
    local spellCooldownInfo = C_Spell.GetSpellCooldown(spell["global_cooldown"])
    if spellCooldownInfo.duration == 0 then
        return 0
    else
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end


-- SpellInRange(439843, "target")

function pr.SpellInRange(spell_name, unit)
    return C_Spell.IsSpellInRange(spell[spell_name], unit)
end












-- 通用

spell["global_cooldown"] = 61304




-- 死亡骑士
talent["死神印记"] = 439843