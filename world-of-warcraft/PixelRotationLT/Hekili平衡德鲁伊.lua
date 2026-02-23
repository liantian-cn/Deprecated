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


if Hekili.DB.profile.enabled == false then
    Hekili:Toggle()
end

if Hekili.DB.profile.toggles.mode.value ~= "automatic" then
    Hekili.DB.profile.toggles.mode.value = "automatic"
    Hekili:UpdateDisplayVisibility()
    Hekili:ForceUpdate("HEKILI_TOGGLE", true)
end

local ability_id, err, info = Hekili_GetRecommendedAbility("Primary", 1)  -- luacheck: ignore
if ability_id == nil then
    return Idle("没有推荐技能")
end
if ability_id <= 0 then
    ability_id, err, info = Hekili_GetRecommendedAbility("Primary", 2)  -- luacheck: ignore
    if ability_id <= 0 then
        ability_id, err, info = Hekili_GetRecommendedAbility("Primary", 3)  -- luacheck: ignore
        if ability_id <= 0 then
            return Idle("没有推荐技能")
        end
    end
end


if ability_id == 1126 then
    return Cast("野性印记")
elseif ability_id == 24858 then
    return Cast("枭兽形态")
elseif ability_id == 102793 then
    return Cast("乌索尔旋风")
elseif ability_id == 5487 then
    return Cast("熊形态")
elseif ability_id == 8921 then
    return Cast("月火术")
elseif ability_id == 194153 then
    return Cast("星火术")
elseif ability_id == 202425 then
    return Cast("艾露恩的战士")
elseif ability_id == 93402 then
    return Cast("阳炎术")
elseif ability_id == 190984 then
    return Cast("愤怒")
elseif ability_id == 102560 then
    return Cast("超凡之盟")
elseif ability_id == 194223 then
    return Cast("超凡之盟")
elseif ability_id == 391528 then
    return Cast("万灵之召")
elseif ability_id == 191034 then
    return Cast("星辰坠落")
elseif ability_id == 202770 then
    return Cast("艾露恩之怒")
elseif ability_id == 274281 then
    return Cast("新月")
elseif ability_id == 274282 then
    return Cast("新月")
elseif ability_id == 274283 then
    return Cast("新月")
elseif ability_id == 20484 then
    return Cast("复生")
elseif ability_id == 78674 then
    return Cast("星涌术")
elseif ability_id == 78675 then
    return Cast("日光术")
elseif ability_id == 29166 then
    return Cast("激活")
elseif ability_id == 108238 then
    return Cast("甘霖")
elseif ability_id == 2782 then
    return Cast("清除腐蚀")
elseif ability_id == 22812 then
    return Cast("树皮术")
elseif ability_id == 8936 then
    return Cast("愈合")
elseif ability_id == 2908 then
    return Cast("安抚")
elseif ability_id == 774 then
    return Cast("回春术")
elseif ability_id == 88747 then
    return Cast("野性蘑菇")
elseif ability_id == 124974 then
    return Cast("自然的守护")
elseif ability_id == 205636 then
    return Cast("自然之力")
elseif ability_id == 202347 then
    return Cast("星辰耀斑")
elseif ability_id == 209749 then
    return Cast("精灵虫群")
end


-- /dump Hekili_GetRecommendedAbility("Primary", 1)
