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
    --if (not checkInCombat("target")) and (mapInfo.mapType == 4) then
    --    return Idle("目标不在战斗")
    --end

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
    local DisruptIsCooldown = CoolDown(47528, 0) -- 瓦解在冷却
    local TargetIsEnemy = checkIsEnemy("target") -- 目标敌对
    local DisruptInRangeTarget = checkSkillInRange(47528, "target") -- 瓦解在目标施法距离
    local TargetShouldInterrupt = ShouldInterrupt("target")
    if DisruptIsCooldown and TargetIsEnemy and DisruptInRangeTarget and TargetShouldInterrupt then
        return Cast("心灵冰冻目标")
    end

    local FocusIsEnemy = checkIsEnemy("focus")  -- 焦点敌对
    local DisruptInRangeFocus = checkSkillInRange(47528, "focus") -- 瓦解在焦点施法距离
    local FocusShouldInterrupt = ShouldInterrupt("focus")
    if DisruptIsCooldown and FocusIsEnemy and DisruptInRangeFocus and FocusShouldInterrupt then
        return Cast("心灵冰冻焦点")
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

    if ability_id == 49039 then
        return Cast("巫妖之躯")
    elseif ability_id == 48792 then
        return Cast("冰封之韧")
    elseif ability_id == 47528 then
        return Cast("心灵冰冻")
    elseif (ability_id < 0) and Ticket13Usable() then
        return Cast("13号饰品")
    elseif (ability_id < 0) and Ticket14Usable() then
        return Cast("14号饰品")
    elseif ability_id == 47541 then
        return Cast("凋零缠绕")
    elseif ability_id == 383269 then
        return Cast("憎恶附肢")
    elseif ability_id == 61999 then
        return Cast("复活盟友")
    elseif ability_id == 49998 then
        return Cast("灵界打击")
    elseif ability_id == 46584 then
        return Cast("亡者复生")
    elseif ability_id == 207317 then
        return Cast("扩散")
    elseif ability_id == 207289 then
        return Cast("邪恶突袭")
    elseif ability_id == 152280 then
        return Cast("亵渎")
    elseif ability_id == 77575 then
        return Cast("爆发")
    elseif ability_id == 63560 then
        return Cast("黑暗突变")
    elseif ability_id == 55090 then
        return Cast("天灾打击")
    elseif ability_id == 85948 then
        return Cast("脓疮打击")
    elseif ability_id == 458128 then
        return Cast("脓疮毒镰")

    elseif ability_id == 433895 then
        return Cast("吸血鬼打击")
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



