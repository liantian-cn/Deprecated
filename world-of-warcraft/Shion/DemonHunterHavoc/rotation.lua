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


--技能充能
local function checkSkillCharges(spell_id, cooldownLimit)
    --local spellInfo = C_Spell.GetSpellInfo(spell_name)
    local chargeInfo = C_Spell.GetSpellCharges(spell_id)

    if chargeInfo.currentCharges == chargeInfo.maxCharges then
        return chargeInfo.currentCharges
    else
        local gcd
        if cooldownLimit == nil then
            gcd = SpellQueueWindow / 1000
        else
            gcd = cooldownLimit / 1000
        end
        local cd = chargeInfo.cooldownStartTime + chargeInfo.cooldownDuration - GetTime()
        if (cd > gcd) then
            return chargeInfo.currentCharges
        else
            return chargeInfo.currentCharges + 1
        end
    end
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

--技能在施法距离
local function checkSkillInRange(spell_id, targetUnit)
    if not UnitExists(targetUnit) then
        return false
    end
    return C_Spell.IsSpellInRange(spell_id, targetUnit) or false
end


--玩家Buff存在
local function checkPlayerAuraExists(buff_id)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(buff_id)

    if aura then
        return true
    end
    return false
end

local function getPlayerAuraRemainingTime(buff_id)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(buff_id)
    if aura then
        local remaining = aura.expirationTime - GetTime()
        return math.max(remaining, 0)
    end
    return 0
end

-- /dump getTargetDebuffRemainingTime("target",204598,"HARMFUL|PLAYER")
local function getTargetDebuffRemainingTime(targetUnit, buff_id, filter)
    function getAuraInfo(targetUnit, buff_id, filter)
        local i = 1
        while true do
            local auraInfo = C_UnitAuras.GetAuraDataByIndex(targetUnit, i, filter)
            if not auraInfo then
                return nil
            end
            if auraInfo.spellId == buff_id then
                return auraInfo
            end
            i = i + 1
        end
    end

    local auraInfo = getAuraInfo(targetUnit, buff_id, filter)

    if auraInfo then
        local remaining = auraInfo.expirationTime - GetTime()
        return math.max(remaining, 0)
    end
    return 0
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



ShionVars["AutoBurst"] = true;
local function ToggleAutoBurst()
    ShionVars["AutoBurst"] = not ShionVars["AutoBurst"];
    ShionCB["AutoBurst"]:SetChecked(ShionVars["AutoBurst"]);
end
CreateLine("自动爆发", "AutoBurst", ToggleAutoBurst)


ShionVars["AlwaysBurst"] = false;
local function ToggleAlwaysBurst()
    ShionVars["AlwaysBurst"] = not ShionVars["AlwaysBurst"];
    ShionCB["AlwaysBurst"]:SetChecked(ShionVars["AlwaysBurst"]);
    if ShionVars["AutoBurst"] then
        ShionVars["AutoBurst"] = not ShionVars["AutoBurst"];
        ShionCB["AutoBurst"]:SetChecked(ShionVars["AutoBurst"]);
    end
    if ShionVars["AlwaysBurst"] then
        SetBurst(9999);
    else
        ClearBurst();
    end
end
CreateLine("持续爆发", "AlwaysBurst", ToggleAlwaysBurst)


-- 不使用眼棱
ShionVars["NotEyeBeam"] = false;
local function ToggleNotEyeBeam()
    ShionVars["NotEyeBeam"] = not ShionVars["NotEyeBeam"];
    ShionCB["NotEyeBeam"]:SetChecked(ShionVars["NotEyeBeam"]);
end
CreateLine("不用眼棱/追击", "NotEyeBeam", ToggleNotEyeBeam)

-- 移动中眼棱
ShionVars["EyeBeamWhenMoving"] = false;
local function ToggleEyeBeamWhenMoving()
    ShionVars["EyeBeamWhenMoving"] = not ShionVars["EyeBeamWhenMoving"];
    ShionCB["EyeBeamWhenMoving"]:SetChecked(ShionVars["EyeBeamWhenMoving"]);
end
CreateLine("移动中眼棱/追击", "EyeBeamWhenMoving", ToggleEyeBeamWhenMoving)

ShionVars["AlwaysAOE"] = false;
local function ToggleAlwaysAOE()
    ShionVars["AlwaysAOE"] = not ShionVars["AlwaysAOE"];
    ShionCB["AlwaysAOE"]:SetChecked(ShionVars["AlwaysAOE"]);
    if ShionVars["AlwaysSingle"] and ShionVars["AlwaysAOE"] then
        ShionVars["AlwaysSingle"] = false;
        ShionCB["AlwaysSingle"]:SetChecked(false)
    end
end
CreateLine("总是AOE", "AlwaysAOE", ToggleAlwaysAOE)

ShionVars["AlwaysSingle"] = false;
local function ToggleAlwaysSingle()
    ShionVars["AlwaysSingle"] = not ShionVars["AlwaysSingle"];
    ShionCB["AlwaysSingle"]:SetChecked(ShionVars["AlwaysSingle"]);
    if ShionVars["AlwaysSingle"] and ShionVars["AlwaysAOE"] then
        ShionVars["AlwaysAOE"] = false;
        ShionCB["AlwaysAOE"]:SetChecked(false)
    end
end
CreateLine("总是单体", "AlwaysSingle", ToggleAlwaysSingle)

local function checkIsAOE()
    if ShionVars["AlwaysAOE"] then
        return true
    end
    if ShionVars["AlwaysSingle"] then
        return false
    end
    return (NumberOfEnemyInRange(10, 80000000) > 1)
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
    local usable, noMana  = C_Item.IsUsableItem(itemId)
    if (not usable) or noMana then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(itemId)
    if (enable ~= 1) or (duration ~= 0 ) then
        return false
    end
    return true
end

local function Ticket14Usable()
    local itemId = GetInventoryItemID("player", 14)
    local usable, noMana  = C_Item.IsUsableItem(itemId)
    if (not usable) or noMana then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(itemId)
    if (enable ~= 1) or (duration ~= 0 ) then
        return false
    end
    return true
end




local function main_rotation()
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()
    if not (classFilename == "DEMONHUNTER" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    local TargetIn5Yard = checkSkillInRange(162794, "target") -- 使用[混乱打击]判断是否属于近战
    local TargetIsBoss = checkTargetIsBoss()
    local IsMoving = checkIsMoving()
    local IsAOE = checkIsAOE()

    -- DH
    local fury = getFury()
    local furyDeficit = getFuryDeficit()


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
    if not IsRanged  and (mapInfo.mapType == 4) then
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

    -- 在精华破碎期间，尽量打出死亡横扫和毁灭
    -- Single1.Cast  Death Sweep during  Essence Break.
    -- Single2. Cast  Annihilation during  Essence Break.
    local TargetEssenceBreakDebuffRemaining = getTargetDebuffRemainingTime("target", 320338, "HARMFUL|PLAYER") -- 精华破碎在目标的buff剩余时间
    local DeathSweepUsable = IsSpellKnownOrOverridesKnown(210152) -- [死亡横扫] = [恶魔变身]后的[刃舞]，当技能被覆盖时
    local DeathSweepCoolDown = false
    if DeathSweepUsable then
        DeathSweepCoolDown = CoolDown(210152)  -- 死亡横扫的冷却冷却
    end
    local AnnihilationUsable = IsSpellKnownOrOverridesKnown(201427) --[毁灭] = [恶魔变身]后的[混乱打击]，当技能被覆盖时
    if TargetEssenceBreakDebuffRemaining > 0 then
        if DeathSweepUsable and DeathSweepCoolDown and TargetIn5Yard and (fury > 35) then
            --DebugRecord("01")
            return Cast("死亡横扫")
        end
        if AnnihilationUsable and (fury > 40) and TargetIn5Yard then
            --DebugRecord("02")
            return Cast("毁灭")
        end
    end

    --AOE:AOE中，总要先打出强化的混乱打击
    local PlayerHaveRendingStrikeBuff = checkPlayerAuraExists(442442) -- 撕裂猛击，强化[混乱打击]
    if IsAOE then
        if (fury > 35) and PlayerHaveRendingStrikeBuff and TargetIn5Yard then
            --DebugRecord("03")
            return Cast("混乱打击")
        end
    end

    -- AOE： 献祭光环2层时，优先打
    local ImmolationAuraCharges = checkSkillCharges(258920) -- 献祭光环可用次数
    if IsAOE and (ImmolationAuraCharges > 1) then
        --DebugRecord("04")
        return Cast("献祭光环")
    end

    -- Single3.Cast  Reaver's Glaive.
    -- 收割者战刃
    local ReaverGlaiveUsable = IsSpellKnownOrOverridesKnown(442294) -- [收割者战刃]可用
    local ReaverGlaiveInRange = checkSkillInRange(442294, "target") -- 在施法距离
    local PlayerThrillOfTheFightBuffRemaining = getPlayerAuraRemainingTime(442688) --酣战热血剩余时间
    local PlayerHaveGlaiveFlurryBuff = checkPlayerAuraExists(442435) -- 战刃乱舞，强化[灵魂裂劈]
    if ReaverGlaiveUsable
            and ReaverGlaiveInRange
            and (not PlayerHaveGlaiveFlurryBuff) and (not PlayerHaveRendingStrikeBuff)
            and (PlayerThrillOfTheFightBuffRemaining < 3)
            and (UnitHealth("target") > 30000000)     then
        --DebugRecord("05")
        return Cast("收割者战刃")
    end

    -- Single4.Cast  Sigil of Spite.
    local SigilOfSpiteIsCooldown = CoolDown(390163) -- [怨念咒符]冷却
    if TargetIsBoss or IsBurst() or IsAOE then
        if (not IsMoving) then
            if SigilOfSpiteIsCooldown then
                --DebugRecord("06")
                return Cast("怨念咒符脚下")
            end
        end
    end

    -- Single5. Cast  The Hunt if you do NOT have a  Reaver's Glaive charge ready.
    local HuntUsable = IsSpellKnownOrOverridesKnown(370965) -- [恶魔追击]可用
    local HuntCooldown = CoolDown(370965) -- [恶魔追击]冷却

    if not ShionVars["NotEyeBeam"] then
        if (not IsMoving) or ShionVars["EyeBeamWhenMoving"] and (not PlayerHaveGlaiveFlurryBuff) and (not PlayerHaveRendingStrikeBuff) then
            if HuntUsable and HuntCooldown then
                --DebugRecord("07")
                return Cast("恶魔追击")
            end
        end
    end

    -- Single6.Cast  Essence Break while in  Metamorphosis.
    -- 在恶魔变身中使用[精华破碎]
    local PlayerInMetamorphosis = checkPlayerAuraExists(162264) -- 在[恶魔变身]中
    local KnownEssenceBreak = IsSpellKnownOrOverridesKnown(258860) -- 点了[精华破碎]天赋
    local EssenceBreakCooldown = CoolDown(258860) -- [精华破碎]冷却
    if PlayerInMetamorphosis and KnownEssenceBreak and EssenceBreakCooldown then
        --DebugRecord("08")
        return Cast("精华破碎")
    end

    --Single7.Cast  Death Sweep.
    if DeathSweepUsable and DeathSweepCoolDown and TargetIn5Yard and (fury > 35) then
        --DebugRecord("09")
        return Cast("死亡横扫")
    end

    -- Single8. Cast Metamorphosis if  Eye Beam is on cooldown.
    local EyeBeamCooldownIn5S = CoolDown(198013, 5000) -- [眼棱]将要在5秒内冷却
    local MetamorphosisCooldown = CoolDown(191427) -- [恶魔变身]冷却
    if (not EyeBeamCooldownIn5S) and MetamorphosisCooldown and (IsBurst() or TargetIsBoss) then
        return Cast("恶魔变身原地")
    end

    --print("===========")
    --print(Ticket13Usable())
    --print(Ticket14Usable())
    --Single9. Cast  Eye Beam.
    local EyeBeamCooldown = CoolDown(198013) -- [眼棱]冷却
    if not ShionVars["NotEyeBeam"] then
        if (not IsMoving) or ShionVars["EyeBeamWhenMoving"] then
            if EyeBeamCooldown and (fury > 30) then
                --DebugRecord("10")
                if Ticket13Usable() then
                    return Cast("13号饰品")
                end
                if Ticket14Usable() then
                    return Cast("14号饰品")
                end
                return Cast("眼棱")
            end
        end
    end

    -- Single10.Cast  Blade Dance.
    local BladeDanceCooldown = CoolDown(188499) -- [刃舞]冷却
    if BladeDanceCooldown and (fury > 35) and TargetIn5Yard then
        --DebugRecord("11")
        return Cast("刃舞")
    end

    -- AOE10.Cast  Immolation Aura.
    if IsAOE then
        if (ImmolationAuraCharges > 0) and TargetIn5Yard then
            --DebugRecord("12")
            return Cast("献祭光环")
        end
    end


    -- Single211.Cast  Sigil of Flame if under 90 Fury.
    local SigilOfFlameCharges = checkSkillCharges(204596) -- [烈焰咒符]的充能
    if (SigilOfFlameCharges > 0) and (furyDeficit > 30) then
        --DebugRecord("13")
        return Cast("烈焰咒符脚下")
    end

    -- Single12.Cast  Annihilation.
    if AnnihilationUsable and (fury > 40) and TargetIn5Yard then
        --DebugRecord("14")
        return Cast("毁灭")
    end

    --Single13. Cast [混乱打击] if [撕裂猛击] proc for  [混乱打击] needs to be used.
    if (fury > 40) and PlayerHaveRendingStrikeBuff and TargetIn5Yard then
        --DebugRecord("15")
        return Cast("混乱打击")
    end

    -- Single14. Cast  Felblade if under 80 Fury.
    local FelbladeIsCooldown = CoolDown(232893) -- 邪能之刃
    if (furyDeficit > 40) and FelbladeIsCooldown and TargetIn5Yard then
        --DebugRecord("16")
        return Cast("邪能之刃")
    end

    -- Single15. Cast  Chaos Strike.
    if (fury > 40) and TargetIn5Yard then
        --DebugRecord("17")
        return Cast("混乱打击")
    end

    -- Single16. Cast  Immolation Aura.
    if not IsAOE then
        if (ImmolationAuraCharges > 0) and TargetIn5Yard then
            --DebugRecord("18")
            return Cast("献祭光环")
        end
    end

    -- Single17. Cast  Throw Glaive if no other buttons are available.
    -- AOE 15
    local ThrowGlaiveCharges = checkSkillCharges(185123) -- 投掷利刃
    if (not ReaverGlaiveUsable) and (ThrowGlaiveCharges >= 1) then
        return Cast("投掷利刃")
    end

    return Idle("无事可做")
end


