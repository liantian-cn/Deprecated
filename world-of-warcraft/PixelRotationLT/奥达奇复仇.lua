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

-- /dump  UnitPower("player", Enum.PowerType.Fury)
-- /dump  UnitPower("player", Enum.PowerType.Pain)
-- /dump C_Spell.GetSpellInfo("幽魂炸弹")
-- /dump C_Spell.GetSpellInfo("灵魂爆裂")




if Prop("尖刺释放") then
    if (Prop("技能充能", "恶魔尖刺") >= 1) then
        if not Prop("Buff存在", "恶魔尖刺") then
            return Cast("恶魔尖刺")
        end
    end
end

--local itemId = GetInventoryItemID("player", 9)
--if itemId ~= 221806 then
--    return false
--end
--local _, duration, enable = C_Container.GetItemCooldown(221806)
--return (enable == 1) and (duration == 0)


if Prop("玩家血量") < 25 then
    if Prop("排气臂铠可用") then
        return Cast("排气臂铠护腕")   --/use 9 护腕
    end
end

if Prop("玩家在施法读条", 300) then
    return Idle("玩家在施法读条")
end

if (Prop("技能充能", "恶魔尖刺") == 2) then
    return Cast("恶魔尖刺")
end

if CoolDown("瓦解") then
    if Prop("与玩家敌对", "focus") and Prop("技能在施法距离", "瓦解", "focus") and Prop("应当打断", "focus") then
        return Cast("瓦解焦点")
    end

    if Prop("与玩家敌对", "target") and Prop("技能在施法距离", "瓦解", "target") and Prop("应当打断", "target") then
        return Cast("瓦解目标")
    end
end


--## 思路
--你的目标是尽可能多地生成灵魂碎片，以便可以频繁施放[收割者战刃]。
--浪费怒气比失去潜在的[破裂]充能次数要好。
--始终在施放[收割者战刃]后，将[破裂]引导到[灵魂裂劈]。
--在拥有4-5个灵魂碎片时及时使用[幽魂炸弹]，避免灵魂碎片浪费。
--始终优先在技能冷却结束时立即施放技能，避免资源闲置。


-- # 复仇恶魔猎手输出技能优先级
--
-- 1. 冷却结束时施放[恶魔追击]以触发[战刃绝技]
-- 2. 冷却结束时施放[收割者战刃]，无论是被动触发还是通过[恶魔追击]施放
-- 3. 始终将[破裂]作为[收割者战刃]的第一个增强技能施放
-- 4. 始终将[灵魂裂劈]作为[收割者战刃]的第二个增强技能施放
-- 5. 冷却结束时施放[烈火烙印]以触发[天赋:炽烈灭亡]的伤害
-- 6. 如果[单目标]则：在灵魂碎片达到4-5时优先用于[幽魂炸弹]
-- 7. 如果[多目标]则：在灵魂碎片达到4-5时全力施放[幽魂炸弹]
-- 8. 冷却结束时施放[烈焰咒符]
-- 9. 冷却结束时施放[献祭光环]
-- 10. 如果拥有2次充能且不需要保留移动资源，施放[地狱火撞击]
-- 11. 冷却结束时施放[邪能毁灭]
-- 12. 如果携带[怨念咒符]天赋则施放
-- 13. 尽可能多地施放[灵魂裂劈]
-- 14. 如果不会怒气溢出，施放[邪能之刃]
-- 15. 如果不会灵魂碎片或怒气溢出，施放[破裂]
-- 16. 无其他选择时使用[投掷利刃]填充

-- 差异处理说明：当单/多目标处理方式不同时，使用独立条目标示；技能顺序1-15中仅有第6条存在表述差异，其他条目处理逻辑完全一致。特别说明[幽魂炸弹]在多目标环境需要更主动施放。


-- 1. 冷却结束时施放[恶魔追击]以触发[战刃绝技]
-- 手动释放


-- 5. 冷却结束时施放[烈火烙印]以触发[天赋:炽烈灭亡]的伤害
-- 手动提前
if Prop("爆发或BOSS") then
    if CoolDown("烈火烙印", 700) and Prop("技能在施法距离", "烈火烙印", "target") then
        return Cast("烈火烙印")
    end
end



-- 2. 冷却结束时施放[收割者战刃]，无论是被动触发还是通过[恶魔追击]施放
if Prop("技能可用", "收割者战刃") then
    if Prop("技能在施法距离", "收割者战刃", "target") then
        return Cast("收割者战刃")
    end
end

-- 3. 始终将[破裂]作为[收割者战刃]的第一个增强技能施放
-- 释放收割者[收割者战刃]后，获得撕裂猛击，442442，该buff强化了破裂
-- /dump  C_UnitAuras.GetAuraDataBySpellName("player", "撕裂猛击" , "HELPFUL|PLAYER")
-- /dump C_UnitAuras.GetPlayerAuraBySpellID(442442)
-- /dump type("撕裂猛击")
-- /dump PixelRotationLT["p_xrvXijCa"]("撕裂猛击")

-- 自然而然的使用，所以注释了

--if Prop("Buff存在", "撕裂猛击") then
--    if (Prop("技能充能", "破裂") >= 1) then
--        return Cast("破裂")
--    end
--end


-- 4. 始终将[灵魂裂劈]作为[收割者战刃]的第二个增强技能施放
-- 释放收割者[收割者战刃]后，获得战刃乱舞，442435，该buff强化了灵魂裂劈
--if (not Prop("Buff存在", "撕裂猛击")) and Prop("Buff存在", "战刃乱舞") then
--    if (Prop("恶魔之怒") >= 30) and Prop("技能在施法距离", "灵魂裂劈", "target") then
--        return Cast("灵魂裂劈")
--    end
--end




-- 11. 不要浪费破裂

if Prop("技能在施法距离", "破裂", "target") and (Prop("技能充能", "破裂",300) == 2) then
    return Cast("破裂")
end


-- 6. 如果[单目标]则：在灵魂碎片达到4-5时优先用于[幽魂炸弹]
-- 7. 如果[多目标]则：在灵魂碎片达到4-5时全力施放[幽魂炸弹]
-- /dump C_Spell.IsSpellUsable("幽魂炸弹")

if Prop("技能可用", "幽魂炸弹") then
    if (Prop("恶魔之怒") > 40) and (Prop("灵魂残片") >= 4) then
        return Cast("幽魂炸弹")
    end
end
-- 8. 冷却结束时施放[烈焰咒符]
if Prop("爆发或BOSS") and (Prop("当前移动速度") == 0) then
    if Prop("目标Debuff剩余时间", "烈焰咒符") < 1 then
        if (Prop("技能充能", "烈焰咒符") >= 1) then
            if Prop("技能在施法距离", "破裂", "target") and (Prop("恶魔之怒空挡") >= 30) then
                return Cast("烈焰咒符脚下")
            end
        end
    end
end

if (Prop("技能充能", "烈焰咒符") >= 2) then
    if Prop("技能在施法距离", "破裂", "target") and (Prop("恶魔之怒空挡") >= 30) then
        return Cast("烈焰咒符脚下")
    end
end

-- 9. 冷却结束时施放[献祭光环]
if CoolDown("献祭光环", 700) then
    if (Prop("恶魔之怒") <= 150) then
        return Cast("献祭光环")
    end
end


-- 10. 如果拥有2次充能且不需要保留移动资源，施放[地狱火撞击]
-- 手动释放


-- 11. 不要浪费破裂

if Prop("技能在施法距离", "破裂", "target") and (Prop("技能充能", "破裂",300) == 2) then
    return Cast("破裂")
end




-- 11. 冷却结束时施放[邪能毁灭]
if Prop("爆发或BOSS") then
    if CoolDown("邪能毁灭", 700) then
        if (Prop("恶魔之怒") >= 50) then
            if Prop("技能在施法距离", "邪能之刃", "target") then
                if (not Prop("Buff存在", "恶魔变形")) then
                    return Cast("邪能毁灭")
                end
            end
        end
    end
end


-- 12. 如果携带[怨念咒符]天赋则施放

if Prop("爆发或BOSS") then
    if Prop("技能可用", "怨念咒符") then
        if CoolDown("怨念咒符", 700) then
            if Prop("技能在施法距离", "破裂", "target") then
                return Cast("怨念咒符脚下")
            end
        end
    end
end

-- 13. 尽可能多地施放[灵魂裂劈]

if (Prop("恶魔之怒") >= 50)  and (Prop("灵魂残片") >= 2) and Prop("技能在施法距离", "灵魂裂劈", "target") then
    if not Prop("Buff存在", "撕裂猛击") then
        return Cast("灵魂裂劈")
    end
end

-- 14. 如果不会怒气溢出，施放[邪能之刃]

if Prop("技能在施法距离", "破裂", "target") then
    if CoolDown("邪能之刃", 700) and (Prop("恶魔之怒空挡") >= 40) then
        return Cast("邪能之刃")
    end
end

-- 15. 如果不会灵魂碎片或怒气溢出，施放[破裂]
if Prop("技能在施法距离", "破裂", "target") and (Prop("技能充能", "破裂",300) >= 1) then
    return Cast("破裂")
end


-- 16. 无其他选择时使用[投掷利刃]填充
if Prop("技能充能", "投掷利刃") >= 1 then
    return Cast("投掷利刃")
end

return Idle("无事可做")

