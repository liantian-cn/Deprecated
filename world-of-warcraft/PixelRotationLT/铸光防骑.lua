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

if (Prop("神圣能量") >= 3) and (Prop("Buff剩余时间", "正义盾击") < 7) then
    return Cast("正义盾击")
end

if (Prop("奉献图腾剩余时间") < 1.5) or (not Prop("Buff存在", "奉献")) then
    if CoolDown("奉献",300) and (Prop("当前移动速度") == 0) then
        return Cast("奉献")
    end
end


-- 避免浪费白送的圣令
if ((1.0 < Prop("Buff剩余时间", "神圣壁垒")) and (Prop("Buff剩余时间", "神圣壁垒")  < 4.0) ) or( (1.0 < Prop("Buff剩余时间", "神圣壁垒")) and  ( Prop("Buff剩余时间", "神圣壁垒")< 4.0)) then
    if (Prop("Buff层数",327510) == 2) and (Prop("玩家蓝量") >= 250000) then
        return Cast("荣耀圣令")
    end
end

if Prop("玩家血量") < 30 then
    if Prop("工程护腕可用") then
        return Cast("工程护腕")
    end
end

if (Prop("玩家血量") < 70) and (Prop("Buff层数",327510) >= 1) and (Prop("玩家蓝量") >= 250000) then
    return Cast("荣耀圣令")
end

if Prop("尖刺释放") and Prop("Buff存在", 327510) and (Prop("玩家蓝量") >= 250000) then
    if (Prop("Buff剩余时间", "圣盾术") < 1) and
            (Prop("Buff剩余时间", "保护祝福") < 1) and
            (Prop("Buff剩余时间", "炽热防御者") < 1) and
            (Prop("Buff剩余时间", "戍卫") < 1) and
            (Prop("Buff剩余时间", "信仰圣光") < 1) then
        return Cast("荣耀圣令")
    end
end


if CoolDown("复仇者之盾", 500) then
    if Prop("与玩家敌对","focus") and Prop("技能在施法距离", "复仇者之盾", "focus") and Prop("可以打断", "focus") and (not Prop("是自己","focustarget")) then
        return Cast("复仇者之盾焦点")
    end

    if Prop("与玩家敌对","target") and Prop("技能在施法距离", "复仇者之盾", "target") and Prop("可以打断", "focus") and Prop("是自己","targettarget") then
        return Cast("复仇者之盾目标")
    end
end

if CoolDown("责难") then
    if Prop("与玩家敌对","focus") and Prop("技能在施法距离", "责难", "focus") and Prop("应当打断", "focus") then
        return Cast("责难焦点")
    end

    if Prop("与玩家敌对","target") and Prop("技能在施法距离", "责难", "target") and Prop("应当打断", "target") then
        return Cast("责难目标")
    end
end

if Prop("鼠标指向为小队或团队玩家") then
    if Prop("鼠标指向目标存在可驱散异常状态", "Poison") or Prop("鼠标指向目标存在可驱散异常状态", "Disease") then
        if CoolDown("清毒术", 200) then
            return Cast("鼠标指向清毒术")
        end
    end

    if Prop("鼠标指向已死亡") and (Prop("神圣能量") >= 3) and Prop("技能可用","代祷") and CoolDown("代祷",200) then
        return Cast("鼠标指向代祷")
    end
end

if Prop("在爆发中") then
    if Prop("特定范围内特定血量以上敌人数量",10,30000000) >= 5  then
        if CoolDown("圣洁鸣钟", 200) then
            return Cast("圣洁鸣钟")
        end
    end

    if Prop("特定范围内特定血量以上敌人数量",10,30000000) >= 5  then
        if Prop("技能充能","神圣壁垒") == 2 then
            if CoolDown("神圣壁垒", 200) then
                return Cast("神圣军备")

            end
        end
        if Prop("技能充能","神圣壁垒") > 0 then
            if (not Prop("Buff存在", "神圣壁垒")) and (not Prop("Buff存在", "神圣壁垒")) then
                if CoolDown("神圣壁垒", 200) then
                    return Cast("神圣军备")
                end
            end
        end
    end
end

if CoolDown("复仇者之盾",200)  and Prop("技能在施法距离", "复仇者之盾", "target") then
    if not Prop("Buff存在", "信仰壁垒") then
        if (Prop("Buff剩余时间", "正义盾击") < 7) then
            return Cast("复仇者之盾目标/盾击")
        end
        return Cast("复仇者之盾目标")
    end
end

if Prop("技能可用","愤怒之锤") and CoolDown("愤怒之锤",200) and Prop("技能在施法距离", "愤怒之锤", "target") then
    if (Prop("Buff剩余时间", "正义盾击") < 7) then
        return Cast("愤怒之锤/盾击")
    end
    return Cast("愤怒之锤")
end

if ((Prop("技能充能","审判") >= 1) or CoolDown("审判",300)) and Prop("技能在施法距离", "审判", "target") then
    if (Prop("Buff剩余时间", "正义盾击") < 7) then
        return Cast("审判/盾击")
    end
    return Cast("审判")
end

if (Prop("技能充能","祝福之锤") >= 1)  or CoolDown("祝福之锤",300) then
    return Cast("祝福之锤")
end



if Prop("神圣能量") == 5  then
    return Cast("正义盾击")
end

return Idle("无事可做")
