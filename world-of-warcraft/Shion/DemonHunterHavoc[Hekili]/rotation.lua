-- 打断部分
local MeleeDPSInterruptSpellList = {}; -- 打断技能清单
local MeleeDPSInterruptBlacklist = {}; -- 打断技能黑名单


-- 打断判断
local function InterruptCast(target)
    if not UnitExists(target) then
        return 0
    end
    local name, _, _, _, _, _, _, notIncorruptible, spellId = UnitCastingInfo(target)
    if name == nil then
        return 0
    end
    if MeleeDPSInterruptBlacklist[spellId] then
        return 0
    end
    if notIncorruptible then
        return 0
    end
    if MeleeDPSInterruptSpellList[spellId] then
        return 2
    end
    return 1
end

local function InterruptChannel(target)
    if not UnitExists(target) then
        return 0
    end
    local name, _, _, _, _, _, notIncorruptible, spellId, _, _ = UnitChannelInfo(target)
    if name == nil then
        return 0
    end
    if MeleeDPSInterruptBlacklist[spellId] then
        return 0
    end
    if notIncorruptible then
        return 0
    end
    if MeleeDPSInterruptSpellList[spellId] then
        return 2
    end
    return 1
end

local function CanInterrupt(target)
    return (InterruptCast(target) > 0) or (InterruptChannel(target) > 0)
end

local function ShouldInterrupt(target)
    return (InterruptCast(target) > 1) or (InterruptChannel(target) > 1)
end



-- 玩家在战斗中
local function checkInCombat(targetUnit)
    return UnitAffectingCombat(targetUnit)
end

--在坐骑上
local function checkMounted()
    return IsMounted()
end

--目标是玩家
local function checkTargetIsPlayer(targetUnit)
    return UnitIsPlayer(targetUnit)
end

--目标为空
local function checkTargetIsEmpty(targetUnit)
    return not UnitExists(targetUnit)
end

--玩家血量
local function getPlayerHealthPercentage()
    return UnitHealth("player") / UnitHealthMax("player") * 100
end

--玩家在施法读条
local function checkPlayerIsCasting()
    local name, _, _, _, endTimeMs, _, _, _, _, _ = UnitChannelInfo("player")
    if name then
        return (GetTime() * 1000 + (SpellQueueWindow / 2)) < endTimeMs
    end

    name, _, _, _, endTimeMs, _, _, _, _ = UnitCastingInfo("player")
    if name then
        return (GetTime() * 1000 + (SpellQueueWindow / 2)) < endTimeMs
    end
    return false

end

--与玩家敌对
local function checkIsEnemy(targetUnit)
    return UnitCanAttack("player", targetUnit)
end

local function NumberOfEnemyInRange(mob_range, mob_health)
    local function isUnitInRange(unit, range)
        local getRange = {
            { 5, 37727 },
            { 6, 63427 },
            { 8, 34368 },
            { 10, 32321 },
            { 15, 33069 },
            { 20, 10645 },
            { 25, 24268 },
            { 30, 835 },
            { 35, 24269 },
            { 40, 28767 },
            { 45, 23836 },
            { 50, 116139 },
            { 60, 32825 },
            { 70, 41265 },
            { 80, 35278 },
            { 100, 33119 },
        }
        for _, rangeData in ipairs(getRange) do
            local maxRange, itemID = unpack(rangeData)
            if maxRange == range then
                return C_Item.IsItemInRange(itemID, unit)
            end
        end
        return false
    end

    local inRange, unitID = 0
    for _, plate in pairs(C_NamePlate.GetNamePlates()) do
        unitID = plate.namePlateUnitToken
        if UnitCanAttack("player", unitID) and (not UnitIsDeadOrGhost(unitID)) then
            if isUnitInRange(unitID, mob_range) and (UnitHealth(unitID) > mob_health) then
                inRange = inRange + 1
            end
        end
    end
    return inRange
end



-- ------------------------------
-- 爆发控制
-- 爆发控制
local burst_time = GetTime();
local function IsBurst()
    return GetTime() <= burst_time
end

local function SetBurst(time)
    burst_time = GetTime() + time
end

local function ClearBurst()
    burst_time = GetTime() - 30
end

--ShionVars["AutoBurst"] = true;
--local function ToggleAutoBurst()
--    ShionVars["AutoBurst"] = not ShionVars["AutoBurst"];
--    ShionCB["AutoBurst"]:SetChecked(ShionVars["AutoBurst"]);
--end
--CreateLine("自动爆发", "AutoBurst", ToggleAutoBurst)
--
--ShionVars["AlwaysBurst"] = false;
--local function ToggleAlwaysBurst()
--    ShionVars["AlwaysBurst"] = not ShionVars["AlwaysBurst"];
--    ShionCB["AlwaysBurst"]:SetChecked(ShionVars["AlwaysBurst"]);
--    if ShionVars["AutoBurst"] then
--        ShionVars["AutoBurst"] = not ShionVars["AutoBurst"];
--        ShionCB["AutoBurst"]:SetChecked(ShionVars["AutoBurst"]);
--    end
--    if ShionVars["AlwaysBurst"] then
--        SetBurst(9999);
--    else
--        ClearBurst();
--    end
--end
--CreateLine("持续爆发", "AlwaysBurst", ToggleAlwaysBurst)


-- 不使用眼棱
--ShionVars["NotEyeBeam"] = false;
--local function ToggleNotEyeBeam()
--    ShionVars["NotEyeBeam"] = not ShionVars["NotEyeBeam"];
--    ShionCB["NotEyeBeam"]:SetChecked(ShionVars["NotEyeBeam"]);
--end
--CreateLine("不用眼棱/追击", "NotEyeBeam", ToggleNotEyeBeam)
--
---- 移动中眼棱
--ShionVars["EyeBeamWhenMoving"] = false;
--local function ToggleEyeBeamWhenMoving()
--    ShionVars["EyeBeamWhenMoving"] = not ShionVars["EyeBeamWhenMoving"];
--    ShionCB["EyeBeamWhenMoving"]:SetChecked(ShionVars["EyeBeamWhenMoving"]);
--end
--CreateLine("移动中眼棱/追击", "EyeBeamWhenMoving", ToggleEyeBeamWhenMoving)
--
--ShionVars["AlwaysAOE"] = false;
--local function ToggleAlwaysAOE()
--    ShionVars["AlwaysAOE"] = not ShionVars["AlwaysAOE"];
--    ShionCB["AlwaysAOE"]:SetChecked(ShionVars["AlwaysAOE"]);
--    if ShionVars["AlwaysSingle"] and ShionVars["AlwaysAOE"] then
--        ShionVars["AlwaysSingle"] = false;
--        ShionCB["AlwaysSingle"]:SetChecked(false)
--    end
--end
--CreateLine("总是AOE", "AlwaysAOE", ToggleAlwaysAOE)
--
--ShionVars["AlwaysSingle"] = false;
--local function ToggleAlwaysSingle()
--    ShionVars["AlwaysSingle"] = not ShionVars["AlwaysSingle"];
--    ShionCB["AlwaysSingle"]:SetChecked(ShionVars["AlwaysSingle"]);
--    if ShionVars["AlwaysSingle"] and ShionVars["AlwaysAOE"] then
--        ShionVars["AlwaysAOE"] = false;
--        ShionCB["AlwaysAOE"]:SetChecked(false)
--    end
--end
--CreateLine("总是单体", "AlwaysSingle", ToggleAlwaysSingle)

--local function checkIsAOE()
--    if ShionVars["AlwaysAOE"] then
--        return true
--    end
--    if ShionVars["AlwaysSingle"] then
--        return false
--    end
--    return (NumberOfEnemyInRange(10, 80000000) > 1)
--end

local VDH_eventFrame = CreateFrame("Frame")
VDH_eventFrame:RegisterEvent("PLAYER_LEAVE_COMBAT")
VDH_eventFrame:RegisterEvent("PLAYER_ENTER_COMBAT")
VDH_eventFrame:RegisterEvent("PLAYER_STARTED_MOVING")
VDH_eventFrame:RegisterEvent("PLAYER_STOPPED_MOVING")
VDH_eventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, ...)
end)

function VDH_eventFrame:PLAYER_LEAVE_COMBAT()
    if ShionVars["AutoBurst"] then
        ClearBurst();
    end
end

function VDH_eventFrame:PLAYER_ENTER_COMBAT()
    if ShionVars["AutoBurst"] then
        SetBurst(25);
    end
end

local moving_time = 0

function VDH_eventFrame:PLAYER_STARTED_MOVING()
    moving_time = GetTime() + 360
end

function VDH_eventFrame:PLAYER_STOPPED_MOVING()
    moving_time = GetTime()
end

local function checkIsMoving()
    return GetTime() < moving_time + 1
end

-- 恶魔之怒
local function getFury()
    return UnitPower("player", Enum.PowerType.Fury)
end

local function getFuryDeficit()
    return UnitPowerMax("player", Enum.PowerType.Fury) - UnitPower("player", Enum.PowerType.Fury)
end





-- 排气臂铠可用
local function checkVentingVambracesReady()
    local itemId = GetInventoryItemID("player", 9)
    if itemId ~= 221806 then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(221806)
    return (enable == 1) and (duration == 0)

end

local function checkTargetIsBoss()
    if UnitExists("target") then
        if (UnitLevel("target") == -1) or (UnitLevel("target") >= 82) then
            if UnitHealth("target") > 100000000 then
                return true
            end
        end
    end

    return false
end

local function Ticket13Usable()
    local itemId = GetInventoryItemID("player", 13)
    local usable, noMana = C_Item.IsUsableItem(itemId)
    if (not usable) or noMana then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(itemId)
    if (enable ~= 1) or (duration ~= 0) then
        return false
    end
    return true
end

local function Ticket14Usable()
    local itemId = GetInventoryItemID("player", 14)
    local usable, noMana = C_Item.IsUsableItem(itemId)
    if (not usable) or noMana then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(itemId)
    if (enable ~= 1) or (duration ~= 0) then
        return false
    end
    return true
end

--技能在施法距离
local function checkSkillInRange(spell_id, targetUnit)
    if not UnitExists(targetUnit) then
        return false
    end
    return C_Spell.IsSpellInRange(spell_id, targetUnit) or false
end

local function main_rotation()
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()
    if not (classFilename == "DEMONHUNTER" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    --local TargetIn5Yard = checkSkillInRange(162794, "target") -- 使用[混乱打击]判断是否属于近战
    --local TargetIsBoss = checkTargetIsBoss()
    --local IsMoving = checkIsMoving()
    --local IsAOE = checkIsAOE()


    -- 不在战斗，则不做任何事
    local isPlayerInCombat = checkInCombat("player")
    if not isPlayerInCombat then
        return Idle("玩家不在战斗")
    end

    local mapInfo = C_Map.GetMapInfo(C_Map.GetBestMapForUnit("player"))
    if (not checkInCombat("target")) and (mapInfo.mapType == 4) then
        return Idle("目标不在战斗")
    end

    -- 在坐骑上，则不做任何事
    local isPlayerOnMount = checkMounted()
    if isPlayerOnMount then
        return Idle("玩家在坐骑上")
    end

    -- 目标是玩家，则不做任何事
    local PlayerTargetIsPlayer = checkTargetIsPlayer("target")
    if PlayerTargetIsPlayer then
        return Idle("目标是玩家")
    end

    -- 目标为空，则不做任何事
    local PlayerTargetIsEmpty = checkTargetIsEmpty("target")
    if PlayerTargetIsEmpty then
        return Idle("目标为空")
    end

    -- 血量小于25%，工程护腕可用，则用工程护腕救急。
    local PlayerHP = getPlayerHealthPercentage()
    local VentingVambracesReady = checkVentingVambracesReady() -- 皮甲工程护腕
    if (PlayerHP < 25) and VentingVambracesReady then
        return Cast("排气臂铠护腕")
    end

    -- 在读条，则不做任何事
    local PlayerIsCasting = checkPlayerIsCasting()
    if PlayerIsCasting then
        return Idle("玩家在施法读条")
    end

    -- 10码内没有敌人，则不做任何事
    local IsRanged = NumberOfEnemyInRange(10, 1) > 0
    if not IsRanged and (mapInfo.mapType == 4) then
        return Idle("10码内没有敌人")
    end

    -- 打断判断
    local DisruptIsCooldown = CoolDown(183752, 0) -- 瓦解在冷却
    local TargetIsEnemy = checkIsEnemy("target") -- 目标敌对
    local DisruptInRangeTarget = checkSkillInRange(183752, "target") -- 瓦解在目标施法距离
    local TargetShouldInterrupt = ShouldInterrupt("target")
    if DisruptIsCooldown and TargetIsEnemy and DisruptInRangeTarget and TargetShouldInterrupt then
        return Cast("瓦解目标")
    end

    local FocusIsEnemy = checkIsEnemy("focus")  -- 焦点敌对
    local DisruptInRangeFocus = checkSkillInRange(183752, "focus") -- 瓦解在焦点施法距离
    local FocusShouldInterrupt = ShouldInterrupt("focus")
    if DisruptIsCooldown and FocusIsEnemy and DisruptInRangeFocus and FocusShouldInterrupt then
        return Cast("瓦解焦点")
    end

    if Hekili.DB.profile.toggles.mode.value ~= "automatic" then
        Hekili.DB.profile.toggles.mode.value = "automatic"
        Hekili:UpdateDisplayVisibility()
        Hekili:ForceUpdate("HEKILI_TOGGLE", true)
    end
    if Hekili.DB.profile.enabled == false then
        Hekili:Toggle()
    end

    local ability_id1, err1, info1 = Hekili_GetRecommendedAbility("Primary", 1)  -- luacheck: ignore
    local ability_id2, err2, info2 = Hekili_GetRecommendedAbility("Primary", 2)  -- luacheck: ignore
    local ability_id3, err3, info3 = Hekili_GetRecommendedAbility("Primary", 3)  -- luacheck: ignore
    local ability_id = ability_id1
    if ability_id == nil then
        return Idle("没有推荐技能")
    end

    if ability_id == 204596 then
        return Cast("烈焰咒符脚下")
    elseif ability_id == 389810 then
        return Cast("烈焰咒符")
    elseif ability_id == 258920 then
        return Cast("献祭光环")
    elseif (ability_id < 0) and Ticket13Usable() then
        return Cast("13号饰品")
    elseif (ability_id < 0) and Ticket14Usable() then
        return Cast("14号饰品")
    elseif ability_id == 370965 then
        return Cast("恶魔追击")
    elseif ability_id == 198013 then
        return Cast("眼棱")
    elseif ability_id == 195072 then
        return Cast("邪能冲撞")
    elseif ability_id == 162794 then
        return Cast("混乱打击")
    elseif ability_id == 188499 then
        return Cast("刃舞")
    elseif ability_id == 179057 then
        return Cast("混乱新星")
    elseif ability_id == 232893 then
        return Cast("邪能之刃")
    elseif ability_id == 191427 then
        return Cast("恶魔变身原地")
    elseif ability_id == 258860 then
        return Cast("精华破碎")
    elseif ability_id == 390163 then
        return Cast("怨念咒符脚下")
    elseif ability_id == 389815 then
        return Cast("怨念咒符")
    elseif ability_id == 278326 then
        return Cast("吞噬魔法")
    elseif ability_id == 198589 then
        return Cast("疾影")
    elseif ability_id == 210152 then
        return Cast("死亡横扫")
    elseif ability_id == 201427 then
        return Cast("毁灭")
    elseif ability_id == 442294 then
        return Cast("收割者战刃")
    elseif ability_id == 198793 then
        return Cast("复仇回避")
    elseif ability_id == 185123 then
        return Cast("投掷利刃")
    else
        local spell_info = C_Spell.GetSpellInfo(ability_id)
        local spell_name = ""
        if spell_info then
            spell_name = spell_info.name
        end
        print("未知的技能ID：" .. ability_id .. " 技能名称：" .. spell_name)
    end

    return Idle("无事可做")
end



