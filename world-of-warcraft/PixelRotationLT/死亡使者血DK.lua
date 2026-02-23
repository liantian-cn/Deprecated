if Prop("玩家存在Debuff", "抓握之血") then
    return Idle("闲置")
end

if Prop("在坐骑上") then
    return Idle("在坐骑上")
end

if Prop("目标是玩家") then
    return Idle("目标是玩家")
end

if not Prop("玩家在战斗中") then
    return Idle("玩家不在战斗")
end

if Prop("目标为空") then
    return Idle("目标为空")
end

if Prop("玩家血量") < 30 then
    if Prop("工程护腕可用") then
        return Cast("工程护腕")
    end
end

if Prop("尖刺释放") then
    if Prop("玩家血量") < 80 then
        if Prop("符文能量") > 40 then
            return Cast("灵界打击")
        end
    end
end

if Prop("玩家血量") < 50 then
    if Prop("玩家血量") < 80 then
        if Prop("符文能量") > 40 then
            return Cast("灵界打击")
        end
    end
end

if Prop("应当打断", "focus") and Prop("与玩家敌对", "focus") then
    if CoolDown("心灵冰冻") and Prop("技能在施法距离", "心灵冰冻", "focus") then
        return Cast("心灵冰冻焦点")
    end
end

if Prop("应当打断", "target") and Prop("与玩家敌对", "target") then
    if CoolDown("心灵冰冻") and Prop("技能在施法距离", "心灵冰冻", "target") then
        return Cast("心灵冰冻目标")
    end
end

-- 攻略在：https://maxroll.gg/wow/class-guides/blood-death-knight-mythic-plus-guide#gear-header

--Never drop your Bone Shield! Use Marrowrend or Death's Caress to keep it active.
--永远不要断档白骨之盾（Bone Shield）！使用骨髓分裂（Marrowrend）或死亡之抚（Death's Caress）维持层数。
--Maintain 5+ Stacks of Bone Shield to make use of Ossuary, dropping below 5 is ok if Dancing Rune Weapon is coming up soon.
--通过墓石（Ossuary）天赋保持5层以上白骨之盾，若符文刃舞（Dancing Rune Weapon）即将就绪，允许短暂低于5层。


if (Prop("Buff层数", "白骨之盾") < 5) or (Prop("Buff剩余时间", "白骨之盾") < 6) then

    if CoolDown("死神印记", 300) and (not Prop("玩家存在Buff", "破灭")) then
        return Cast("死神印记")
    end

    if Prop("技能在施法距离", "死神的抚摩", "target") and CoolDown("死神的抚摩", 300) then
        return Cast("死神的抚摩")
    end

    if Prop("玩家存在Buff", "破灭") and Prop("技能在施法距离", "精髓分裂", "target") and Prop("目标血量") > 10 then
        return Cast("精髓分裂")
    end

    if Prop("技能在施法距离", "精髓分裂", "target") then
        return Cast("精髓分裂")
    end


end

--Cast Abomination Limb + Raise Dead on cooldown unless a fight requires you to hold it.
-- 冷却完毕立即施放畸变肢解（Abomination Limb）+ 亡者复生（Raise Dead）（需要预留技能的特殊战斗除外）。
-- 大巴掌手动释放
-- 亡者复生不占gcd，好了就放。
if CoolDown("亡者复生", 200) then
    return Cast("亡者复生")
end

-- Keep up your Death and Decay buff, check out the Deep Dive section for more info.
-- 保持死亡凋零（Death and Decay）增益，详情参阅进阶指南（Deep Dive）章节。

if not Prop("玩家存在Buff", "枯萎凋零") then
    if Prop("玩家存在Buff", "赤色天灾") then
        return Cast("枯萎凋零")
    end

    if Prop("技能充能", "枯萎凋零", 3000) == 2 then
        return Cast("枯萎凋零")
    end

    if (Prop("当前移动速度") == 0) then
        return Cast("枯萎凋零")
    end
end

--Use Reaper's Mark on cooldown.
--冷却完毕立即使用"死神印记"。
--Consume your Exterminate buffs before casting the next Reaper's Mark.
--施放下一个"死神印记"前，先消耗"破灭"（Exterminate）增益。

if CoolDown("死神印记", 300) and (not Prop("玩家存在Buff", "破灭")) then
    return Cast("死神印记")
end

-- Cast Soul Reaper if the Target is below 35% HP.
-- 在以下情况施放灵魂收割（Soul Reaper）：目标生命值低于35%
-- Or you have the buff Reaper of Souls from your Reaper's Mark application.
-- 或你拥有收割者印记触发的收割之魂（Reaper of Souls）增益时。

if Prop("技能可用", "灵魂收割") then
    if CoolDown("灵魂收割", 300) then
        if (Prop("目标血量") < 35) then
            return Cast("灵魂收割")
        end
    end
end

-- Cast Dancing Rune Weapon on cooldown.
-- 冷却完毕立即施放符文刃舞（Dancing Rune Weapon）。
-- 手动释放



--Cast Tombstone on cooldown under the following conditions:
--在下列条件下冷却完毕施放墓碑（Tombstone）：
--✓ You are standing in Death and Decay for Shattering Bone.
--✓ 处于死亡凋零范围内（触发碎骨/Shattering Bone）
--✓ You have 5+ Stacks of Bone Shield.
--✓ 白骨之盾≥5层
--✓ Your Insatiable Blade talent provides you with 20/25 seconds of cooldown reduction for Dancing Rune Weapon.
--✓ 饥渴之刃（Insatiable Blade）天赋使符文刃舞冷却缩减20/25秒
if Prop("玩家存在Buff", "枯萎凋零") then
    if Prop("Buff层数", "白骨之盾") >= 5 then
        if Prop("符文刃舞的CD") > 25 then
            if (Prop("符文能量") < 90) then
                if CoolDown("墓石", 300) then
                    return Cast("墓石")
                end
            end
        end
    end
end

-- Cast Bonestorm on cooldown under the following conditions:
-- 在下列条件下冷却完毕施放白骨风暴（Bonestorm）：
--✓ You are standing in Death and Decay for Shattering Bone.
--✓ 处于死亡凋零范围内（触发碎骨/Shattering Bone）
--✓ You have 5+ Stacks of Bone Shield.
--✓ 白骨之盾≥5
--✓ Your Insatiable Blade talent provides you with 20/25 seconds of cooldown reduction for Dancing Rune Weapon.
--✓ 饥渴之刃天赋使符文刃舞冷却缩减20/25秒

if Prop("玩家存在Buff", "枯萎凋零") then
    if Prop("Buff层数", "白骨之盾") >= 5 then
        if Prop("符文刃舞的CD") > 25 then
            if CoolDown("白骨风暴", 300) then
                return Cast("白骨风暴")
            end
        end
    end
end


-- Spend Runic Power on Death Strike when you are about to overcap or Coagulopathy is about to fade.
--在以下情况使用灵界打击（Death Strike）消耗符文能量：
--when you are about to overcap
--符文能量即将溢出
--or Coagulopathy is about to fade.
--或 凝血（Coagulopathy）效果即将消失

if Prop("符文能量") > 100 then
    return Cast("灵界打击")
end

if (Prop("Buff剩余时间", "凝血") < 2) and Prop("符文能量") > 80 then
    return Cast("灵界打击")
end

-- Cast Consumption on cooldown.
-- 冷却完毕立即施放吞噬（Consumption）。
if Prop("玩家存在Buff", "吸血鬼之血") then
    if Prop("目标Debuff剩余时间", "血之疫病") > 6 then
        if CoolDown("吞噬", 300) then
            return Cast("吞噬")
        end
    end
end

if Prop("吸血鬼之血的CD") > 30 then
    if Prop("目标Debuff剩余时间", "血之疫病") > 6 then
        if CoolDown("吞噬", 300) then
            return Cast("吞噬")
        end
    end
end

-- Cast Blood Boil to avoid overcapping on stacks.
--使用血液沸腾（Blood Boil）避免层数溢出。

if Prop("技能充能", "血液沸腾", 300) >= 1 then
    if Prop("特定范围内特定血量以上敌人数量", 5, 100000) > 0 then
        return Cast("血液沸腾")
    end
end

-- Cast Heart Strike to consume runes as a filler.
--使用心脏打击（Heart Strike）作为填充技能消耗符文。

if (Prop("Buff层数", "白骨之盾") <= 8) then
    if Prop("技能在施法距离", "死神的抚摩", "target") and CoolDown("死神的抚摩", 300) then
        return Cast("死神的抚摩")
    end
    return Cast("精髓分裂")
end

if Prop("符文数") >= 1 then
    return Cast("心脏打击")
end

return Idle("无事可做")