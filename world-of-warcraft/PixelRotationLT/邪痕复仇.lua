if not Prop("玩家在战斗中") then
    return Idle("玩家不在战斗")
end

if Prop("玩家存在Debuff", "抓握之血") then
    return Idle("闲置")
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

--if Prop("玩家血量") < 30 then
--    if Prop("工程护腕可用") then
--        return Cast("工程护腕")
--    end
--end

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


--1. 冷却完毕立即施放【烈火烙印】用于减伤效果和触发烈焰毁灭伤害
--这是个长CD技能，所以仅在爆发模式使用

if Prop("爆发或BOSS") then
    if CoolDown("烈火烙印", 200) and Prop("技能在施法距离", "烈火烙印", "target") then
        return Cast("烈火烙印")
    end
end

--2. 冷却完毕立即施放【烈焰咒符】
-- 在爆发模式下，目标没有烈焰咒符buff，则施放【烈焰咒符】
if Prop("爆发或BOSS") then
    if Prop("目标Debuff剩余时间", "烈焰咒符") < 1 then
        if (Prop("技能充能", "烈焰咒符") >= 1) then
            if Prop("技能在施法距离", "破裂", "target") and (Prop("恶魔之怒") <= 120) then
                return Cast("烈焰咒符脚下")
            end
        end
    end
end
-- 非爆发模式下，两层烈焰咒符时，施放【烈焰咒符】
if (Prop("技能充能", "烈焰咒符") >= 2) then
    if Prop("技能在施法距离", "破裂", "target") and (Prop("恶魔之怒") <= 120) then
        return Cast("烈焰咒符脚下")
    end
end

--3. 冷却完毕立即施放【献祭光环】
if CoolDown("献祭光环", 400) then
    if (Prop("恶魔之怒") <= 150) then
        return Cast("献祭光环")
    end
end

--4. 冷却完毕立即施放【邪能毁灭】进入恶魔变形并强化技能
--这是个长CD技能，所以仅在爆发模式使用
if Prop("爆发或BOSS") then
    if CoolDown("邪能毁灭", 200) then
        if (Prop("恶魔之怒") >= 50) then
            if Prop("技能在施法距离", "破裂", "target") then
                if (not Prop("Buff存在", "恶魔变形")) then
                    return Cast("邪能毁灭")
                end
            end
        end
    end
end

--冷却完毕立即施放【邪能荒芜】
if Prop("技能可用", "邪能荒芜") then
    if Prop("技能在施法距离", "破裂", "target") then
        if (Prop("恶魔之怒") >= 50) and CoolDown("邪能荒芜",300) then
            return Cast("邪能毁灭")
        end
    end
end
--冷却完毕立即施放【吞噬烈焰】
if Prop("技能可用", "吞噬之焰") then
    if CoolDown("吞噬之焰", 400) then
        return Cast("献祭光环")
    end
end

--使用【灵魂迸发】叠加恶魔涌动增伤
if Prop("技能可用", "灵魂爆裂") then
    if (Prop("恶魔之怒") >= 40) and (Prop("灵魂残片") >= 3) and Prop("技能在施法距离", "灵魂裂劈", "target") then
        return Cast("幽魂炸弹")
    end
end

--使用【灵魂割裂】叠加恶魔涌动增伤
if Prop("技能可用", "灵魂割裂") then
    if (Prop("恶魔之怒") >= 30) and Prop("技能在施法距离", "灵魂裂劈", "target") then
        return Cast("灵魂裂劈")
    end
end

--7. 施放【恶魔变形】通过恶魔之怒强度重置技能并强化效果
-- 暂时手动

--8. 冷却完毕立即施放【厄运符咒】_但需间隔施放以维持苦痛研习增益覆盖_
if Prop("技能可用", "末日咒符") then
    if (Prop("技能充能", "末日咒符") >= 1) then
        return Cast("烈焰咒符脚下")
    end
end


--11. 使用【恶魔追击】技能
-- 这个手动

--12. 若已点选天赋则施放【怨念咒符】
-- 爆发才用
if Prop("爆发或BOSS") then
    if Prop("技能可用", "怨念咒符") then
        if CoolDown("怨念咒符", 400) then
            if Prop("技能在施法距离", "破裂", "target") then
                return Cast("怨念咒符脚下")
            end
        end
    end
end

--13. 尽可能频繁地用5个灵魂施放【幽魂炸弹】
if Prop("幽魂炸弹可用") then
    if (Prop("特定范围内特定血量以上敌人数量", 8, 1000000) >= 5) then
        if (Prop("恶魔之怒") > 40) and (Prop("灵魂残片") >= 4) then
            return Cast("幽魂炸弹")
        end
    end
end

--14. 当灵魂残片或怒气未达上限时使用【破裂】
if Prop("技能在施法距离", "破裂", "target") then
    if (Prop("技能充能", "破裂") >= 1)  then
        if (Prop("灵魂残片") <= 3) then
            return Cast("破裂")
        end
        if (Prop("恶魔之怒") <= 130) then
            return Cast("破裂")
        end
    end
end

--15. 当充能达到2层且无需保留位移时使用【地狱火撞击】
-- 手动释放位移
--16. 尽可能多地施放【灵魂裂劈】

if (Prop("恶魔之怒") >= 80) and Prop("技能在施法距离", "灵魂裂劈", "target") then
    return Cast("灵魂裂劈")
end


if Prop("玩家血量") < 80 then
    if (Prop("恶魔之怒") >= 50) and Prop("技能在施法距离", "灵魂裂劈", "target") then
        return Cast("灵魂裂劈")
    end
end


--17. 不超过怒气上限时使用【邪能之刃】

if Prop("技能在施法距离", "破裂", "target") then
    if CoolDown("邪能之刃", 400) and (Prop("恶魔之怒") <= 110) then
        return Cast("邪能之刃")
    end
end

--18. 作为填充技或远离目标时使用【投掷战刃】
if Prop("技能充能", "投掷利刃") >= 1 then
    return Cast("投掷利刃")
end


return Idle("无事可做")