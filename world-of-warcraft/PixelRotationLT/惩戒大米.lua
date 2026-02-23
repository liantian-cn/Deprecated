if not Prop("玩家在战斗中") then
    return Idle("玩家不在战斗")
end

if Prop("在坐骑上") then
    return Idle("在坐骑上")
end

if Prop("目标是玩家") then
    return Idle("目标是玩家")
end

if Prop("目标为空") then
    return Idle("目标为空")
end

-- /dump C_Spell.GetSpellInfo("自动攻击")
--
-- 技能可用
--local isUsable, insufficientPower = C_Spell.IsSpellUsable(spellIdentifier)
--return isUsable or insufficientPower

local AOE = Prop("在AOE")
local Single = not AOE
local Power = Prop("神圣能量")

if CoolDown("责难") then
    if Prop("与玩家敌对", "focus") and Prop("技能在施法距离", "责难", "focus") and Prop("应当打断", "focus") then
        return Cast("责难焦点")
    end

    if Prop("与玩家敌对", "target") and Prop("技能在施法距离", "责难", "target") and Prop("应当打断", "target") then
        return Cast("责难目标")
    end
end

if (Prop("玩家血量") < 60) and (Power >= 3) then
    return Cast("荣耀圣令/自己")
end

if (Prop("玩家血量") < 20) and CoolDown("圣疗术", 300) and not (Prop("玩家存在Debuff", "自律")) then
    return Cast("圣疗术/自己")
end

if (Prop("玩家血量") < 15) and CoolDown("圣盾术", 300) and not (Prop("玩家存在Debuff", "自律")) then
    return Cast("圣盾术/自己")
end


-- /dump C_Spell.IsSpellInRange(6603, "target")
-- /dump C_Spell.IsSpellInRange(184575, "target")
-- 如果在近战
if not C_Item.IsItemInRange(32321, "target") then
    return Idle("目标不在近战范围")
end
-- Cast 神圣之锤
if (Power >= 3) and Prop("技能可用", "神圣之锤") and CoolDown("神圣之锤", 400) then
    return Cast("神圣之锤")
end

-- 处决宣判
if Prop("技能可用", "处决宣判") and CoolDown("处决宣判", 400) then
    return Cast("处决宣判")
end

-- Cast [最终清算] if you have at least 3 Holy Power and [灰烬觉醒] is on cooldown.
--if Prop("技能可用", "最终清算") and CoolDown("最终清算", 400) and (Prop("冷却剩余", "灰烬觉醒") > 5) then
if Prop("技能可用", "最终清算") and CoolDown("最终清算", 400)  then
    return Cast("最终清算")
end
--惩戒圣光之锤可用
--local slot = FindSpellBookSlotBySpellID( 427453 )
--if not slot then return false end
--local spellBookItemInfo = C_SpellBook.GetSpellBookItemInfo(slot, 0)
--if spellBookItemInfo.spellID == 427453 then
--    local isUsable, insufficientPower = C_Spell.IsSpellUsable(427453)
--    return isUsable
--else
--    return false
--end

-- 如果惩戒圣光之锤可用，释放圣光之锤
if (Power >= 5) and Prop("惩戒圣光之锤可用") then
    return Cast("圣光之锤")
end

-- AOE: Cast [神圣风暴] if you have 5 Holy Power.
if AOE and (Power == 5) then
    return Cast("神圣风暴")
end

-- Single: Cast  [神圣风暴] if you have an [苍穹之力] proc and 5 Holy Power.
if Single and Prop("Buff存在", "苍穹之力") and (Power == 5) then
    return Cast("神圣风暴")
end

-- Single: Cast [最终审判] if you have 5 Holy Power.
if Single and Prop("技能可用", "最终审判") and (Power == 5) then
    return Cast("最终审判")
end

--    目标Debuff剩余时间
--    local aura  = C_UnitAuras.GetAuraDataBySpellName("target", debuff_name,"HARMFUL|PLAYER")
--    if aura  then
--        local remaining = aura.expirationTime - GetTime()
--        return math.max(remaining, 0)
--    end
--    return 0

-- 技能充能
--local spellInfo = C_Spell.GetSpellInfo(spell_name)
--local chargeInfo = C_Spell.GetSpellCharges(spellInfo.spellID)
--
--if chargeInfo.currentCharges == chargeInfo.maxCharges then
--    return chargeInfo.currentCharges
--else
--    local gcd
--    if cooldownLimit == nil then
--        gcd = PixelRotationLT.GcdRemaining()
--    else
--        gcd = cooldownLimit/1000
--    end
--    local cd = chargeInfo.cooldownStartTime + chargeInfo.cooldownDuration - GetTime()
--    if (cd > gcd) then
--        return chargeInfo.currentCharges
--    else
--        return chargeInfo.currentCharges+1
--    end
--end

-- Single: Cast [公正之剑] if [异端逐除] is not active.
if Single and Prop("技能充能", "公正之剑", 400) >= 1 and Prop("目标Debuff剩余时间", "异端逐除") < 0.5 then
    return Cast("公正之剑")
end



--local spellInfo = C_Spell.GetSpellInfo("灰烬觉醒")
--if not spellInfo then
--    return false
--end
--
--local spellCooldownInfo = C_Spell.GetSpellCooldown(255937)
--
--if spellCooldownInfo.duration == 0 then
--    return true
--else
--    local remaining = spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
--    return remaining < 0.7
--end

-- Cast [灰烬觉醒]
if Prop("灰烬觉醒可用") then
    return Cast("灰烬觉醒")
end

--Single:Cast Divine Toll Icon Divine Toll if you have 3 or less Holy Power.
--AOE: Cast Divine Toll Icon Divine Toll if you have 1 or less Holy Power.
if CoolDown("圣洁鸣钟", 400) then
    if Single and (Power <= 3) then
        return Cast("圣洁鸣钟")
    end
    if AOE and (Power <= 1) then
        return Cast("圣洁鸣钟")
    end
end

-- Cast  [神圣风暴] if you have an [苍穹之力] .
if Prop("Buff存在", "苍穹之力") then
    return Cast("神圣风暴")
end

-- Single:Cast [最终审判] with 3-4 Holy Power.
-- Aoe: Cast[神圣风暴] with 3-4 Holy Power.
if Single and (Power >= 3) and Prop("技能可用", "最终审判") then
    return Cast("最终审判")
end

if AOE and (Power >= 3) then
    return Cast("神圣风暴")
end

-- Single:Cast [审判] if you have 3 or less Holy Power.
-- Single:Cast [公正之剑] if you have 3 or less Holy Power.
-- AOE顺序颠倒，所以无所谓了

if CoolDown("审判", 400) and Power <= 3 then
    return Cast("审判")
end

if Prop("技能充能", "公正之剑", 400) and Power <= 3 then
    return Cast("公正之剑")
end

if Prop("技能可用", "愤怒之锤") and CoolDown("愤怒之锤", 1000) then
    return Cast("愤怒之锤")
end

return Idle("无事可做")
