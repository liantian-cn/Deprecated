-- 打断部分
local VDHInterruptSpellList = {}; -- 打断技能清单
local VDHInterruptBlacklist = {}; -- 打断技能黑名单
local  ReaverGlaiveTargetHp = 30000000;

-- 打断判断
local function InterruptCast(target)
    if not UnitExists(target) then
        return 0
    end
    local name, _, _, _, _, _, _, notIncorruptible, spellId = UnitCastingInfo(target)
    if name == nil then
        return 0
    end
    if VDHInterruptBlacklist[spellId] then
        return 0
    end
    if notIncorruptible then
        return 0
    end
    if VDHInterruptSpellList[spellId] then
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
    if VDHInterruptBlacklist[spellId] then
        return 0
    end
    if notIncorruptible then
        return 0
    end
    if VDHInterruptSpellList[spellId] then
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


-- 坦克减伤逻部分

local VDHTankOutburstDamage = {};  -- 坦克尖刺伤害
local VDHTankSustainedDamage = {}; -- 坦克减伤技能或增益坦克减伤技能或增

local TankOutburstDamageTimeStamp = GetTime(); -- 创建一个时间戳，当当前时间小于这个时间戳，则认为有怪在释放增益

local function isTankOutburstDamage()
    return (TankOutburstDamageTimeStamp - GetTime()) > 0
end

local function checkTargetIsTankOutburstDamage(event, spell_id)
    if VDHTankOutburstDamage[spell_id] then
        if ShionVars["GlobalDEBUG"] then
            print("通过事件" .. event .. "技能" .. spell_id .. "检测到尖刺伤害")
        end
        TankOutburstDamageTimeStamp = GetTime() + 2
    end
end

local function clearTargetIsTankOutburstDamage(event, spell_id)
    if VDHTankSustainedDamage[spell_id] then
        if ShionVars["GlobalDEBUG"] then
            print("通过事件" .. event .. "技能" .. spell_id .. "清除坦克尖刺伤害")
        end
        TankOutburstDamageTimeStamp = GetTime() - 2
    end
end



---- 移动判断
--local moving_time = 0
--
--local function checkIsMoving()
--    return GetTime() < moving_time + 1
--end


-- 常用函数

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

ShionVars["NotUseFelDevastation"] = false;
local function ToggleNotUseFelDevastation()
    ShionVars["NotUseFelDevastation"] = not ShionVars["NotUseFelDevastation"];
    ShionCB["NotUseFelDevastation"]:SetChecked(ShionVars["NotUseFelDevastation"]);
end
CreateLine("不用邪能毁灭", "NotUseFelDevastation", ToggleNotUseFelDevastation)



-- 恶魔之怒
local function getFury()
    return UnitPower("player", Enum.PowerType.Fury)
end

local function getFuryDeficit()
    return UnitPowerMax("player", Enum.PowerType.Fury) - UnitPower("player", Enum.PowerType.Fury)
end


--尖刺释放


-- 排气臂铠可用
local function checkVentingVambracesReady()
    local itemId = GetInventoryItemID("player", 9)
    if itemId ~= 221806 then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(221806)
    return (enable == 1) and (duration == 0)

end

-- [圣光虔敬魔典]
local function checkTomeOfLightDevotion()
    -- 判断标准
    -- 栏位13必须是[圣光虔敬魔典]
    local itemId = GetInventoryItemID("player", 13)
    if itemId ~= 219309 then
        return false
    end
    -- 必须是[圣光虔敬魔典]的CD
    local _, duration, enable = C_Container.GetItemCooldown(219309)
    if (enable ~= 1) or (duration ~= 0) then
        return false
    end
    -- 必须有[450706的]的buff
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(450706)
    if aura then
        return true
    else
        return false
    end
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

-- 灵魂残片
local function getSoulFragmentsNum()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(203981)
    if aura then
        return aura.applications
    else
        return 0
    end
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

local function checkEnemyIn5Yard()
    if checkSkillInRange(263642, "target") then
        -- 使用破裂判断是否属于近战
        return true
    end
    return (NumberOfEnemyInRange(5, -1) > 0)
end

local function main_rotation()
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()
    if not (classFilename == "DEMONHUNTER" and currentSpec == 2) then
        return Idle("专精不匹配")
    end

    local PlayerHP = getPlayerHealthPercentage()

    local TargetIn5Yard = checkSkillInRange(263642, "target") -- 使用破裂判断是否属于近战
    local TargetIn10Yard = checkSkillInRange(183752, "target") -- 瓦解=10码
    local TargetIn30Yard = checkSkillInRange(204021, "target") -- 使用[烈火烙印]判断是否属于近战
    local TargetIsBoss = checkTargetIsBoss()
    --local IsMoving = checkIsMoving()
    local IsMoving = GetUnitSpeed("player") > 0
    local IsAOE = (NumberOfEnemyInRange(10, 80000000) > 3)
    local EnemyIn5Yard = checkEnemyIn5Yard()

    -- DH
    local fury = getFury()
    local furyDeficit = getFuryDeficit()
    local soulNum = getSoulFragmentsNum()

    local isPlayerInCombat = checkInCombat("player")
    if not isPlayerInCombat then
        return Idle("玩家不在战斗")
    end

    local isPlayerOnMount = checkMounted()
    if isPlayerOnMount then
        return Idle("玩家在坐骑上")
    end

    local PlayerTargetIsPlayer = checkTargetIsPlayer("target")
    if PlayerTargetIsPlayer then
        return Idle("目标是玩家")
    end

    local PlayerTargetIsEmpty = checkTargetIsEmpty("target")
    if PlayerTargetIsEmpty then
        return Idle("目标为空")
    end

    local VentingVambracesReady = checkVentingVambracesReady() -- 皮甲工程护腕
    if (PlayerHP < 25) and VentingVambracesReady then
        return Cast("排气臂铠护腕")
    end

    local PlayerIsCasting = checkPlayerIsCasting()
    if PlayerIsCasting then
        return Idle("玩家在施法读条")
    end

    -- 有两层恶魔尖刺，则用，不浪费。实际上恶魔尖刺应该绑定了宏，很快用掉。
    local DemonSpikesCharges = checkSkillCharges(203720) -- 恶魔尖刺
    if DemonSpikesCharges == 2 then
        return Cast("恶魔尖刺")
    end




    -- 减伤逻辑
    -- 如果在变身中，那就无视
    -- 如果可用邪能毁灭，就用邪能毁灭
    -- 其次使用烈火烙印
    -- 然后使用14号饰品
    -- 最后使用[恶魔变形]
    local PlayerInMetamorphosis = checkPlayerAuraExists(187827) -- 在[恶魔变身]中
    local FelDevastationIsCooldown = CoolDown(212084) -- 邪能毁灭
    local FieryBrandIsCooldown = CoolDown(204021) -- 烈火烙印
    local MetamorphosisCooldown = CoolDown(187827) -- [恶魔变形]

    if isTankOutburstDamage() then
        if not PlayerInMetamorphosis then
            if (not IsMoving) and (fury >= 50) and FelDevastationIsCooldown then
                return Cast("邪能毁灭")
            end
            if FieryBrandIsCooldown and TargetIn30Yard then
                return Cast("烈火烙印")
            end
            if Ticket14Usable() then
                return Cast("14号饰品")
            end
            if MetamorphosisCooldown then
                return Cast("恶魔变形")
            end
        end
    end

    local DisruptIsCooldown = CoolDown(183752) -- 瓦解
    local TargetIsEnemy = checkIsEnemy("target")
    local TargetShouldInterrupt = ShouldInterrupt("target")
    if DisruptIsCooldown and TargetIsEnemy and TargetIn10Yard and TargetShouldInterrupt then
        return Cast("瓦解目标")
    end

    local FocusIsEnemy = checkIsEnemy("focus")
    local DisruptInRangeFocus = checkSkillInRange(183752, "focus") -- 瓦解
    local FocusShouldInterrupt = ShouldInterrupt("focus")
    if DisruptIsCooldown and FocusIsEnemy and DisruptInRangeFocus and FocusShouldInterrupt then
        return Cast("瓦解焦点")
    end

    local CanUseTomeOfLightDevotion = checkTomeOfLightDevotion() -- [圣光虔敬魔典]
    if CanUseTomeOfLightDevotion then
        return Cast("圣光虔敬魔典")
    end

    -- 1. 使用地狱火
    -- 2. 使用恶魔变身

    -- 3. 始终将[破裂]作为[收割者战刃]的第一个增强技能施放
    -- Use  Fracture with  Rending Strike to debuff the target with  Reaver's Mark.
    local FractureCharges = checkSkillCharges(263642, 800) -- 破裂
    local PlayerHaveRendingStrikeBuff = checkPlayerAuraExists(442442) -- 撕裂猛击，强化[破裂]

    if (FractureCharges >= 1) and PlayerHaveRendingStrikeBuff then
        if TargetIn5Yard then
            return Cast("破裂")
        end
        if EnemyIn5Yard then
            return Cast("就近破裂")
        end
    end

    -- 4. 始终将[灵魂裂劈]作为[收割者战刃]的第二个增强技能施放
    -- Use  Soul Cleave with  Glaive Flurry to proc  Fury of the Aldrachi and trigger  Thrill of the Fight.
    local PlayerHaveGlaiveFlurryBuff = checkPlayerAuraExists(442435) -- 战刃乱舞，强化[灵魂裂劈]
    if (fury >= 30) and PlayerHaveGlaiveFlurryBuff then
        if TargetIn5Yard then
            return Cast("灵魂裂劈")
        end
        if EnemyIn5Yard then
            return Cast("就近灵魂裂劈")
        end
    end

    -- 5. 不要浪费破裂
    local FractureChargesNear = checkSkillCharges(263642, 1700) -- 破裂
    if FractureChargesNear >= 2 then
        if TargetIn5Yard then
            return Cast("破裂")
        end
        if EnemyIn5Yard then
            return Cast("就近破裂")
        end
    end

    -- 6. 冷却结束时施放[恶魔追击]以触发[战刃绝技]
    -- 手动释放

    -- 2. 冷却结束时施放[收割者战刃]，无论是被动触发还是通过[恶魔追击]施放

    -- 7. Use  Reaver's Glaive to activate the  Rending Strike and  Glaive Flurry buffs if you do not have  Thrill of the Fight active or have less than 4 seconds remaining on it.
    local ReaverGlaiveUsable = IsSpellKnownOrOverridesKnown(442294) -- 收割者战刃可用
    local ReaverGlaiveInRange = checkSkillInRange(442294, "target") -- 收割者战刃可用
    local PlayerThrillOfTheFightBuffRemaining = getPlayerAuraRemainingTime(1227062) --酣战热血，用掉上面2个buff后获得
    if ReaverGlaiveUsable
            and ReaverGlaiveInRange
            and (not PlayerHaveGlaiveFlurryBuff)
            and (not PlayerHaveRendingStrikeBuff)
            and (PlayerThrillOfTheFightBuffRemaining < 3)
            and (UnitHealth("target") > ReaverGlaiveTargetHp) then
        return Cast("收割者战刃")
    end

    -- [灵魂切削]
    local SoulCarverUsable = IsSpellKnownOrOverridesKnown(207407)
    if SoulCarverUsable then
        local SoulCarverIsCooldown = CoolDown(207407)
        if SoulCarverIsCooldown then
            return Cast("灵魂切削")
        end
    end




    -- 9. 冷却结束时施放[献祭光环]
    -- 8. Use Immolation Aura.
    local ImmolationAuraIsCooldown = CoolDown(258920) -- 献祭光环
    if ImmolationAuraIsCooldown then
        return Cast("献祭光环")
    end

    -- [黑眼之赐] 天赋，邪能毁灭提前
    if IsPlayerSpell(389708) and  (not ShionVars["NotUseFelDevastation"])  then
        if (not IsMoving) then
            if (fury >= 50) and FelDevastationIsCooldown then
                return Cast("邪能毁灭")
            end
        end
    end

    -- 5. 冷却结束时施放[烈火烙印]以触发[天赋:炽烈灭亡]的伤害
    -- 9. Use  Fiery Brand if the debuff is not currently active.
    if FieryBrandIsCooldown and TargetIn30Yard then
        if IsBurst() then
            return Cast("烈火烙印")
        end
    end

    -- 10. Use  Sigil of Flame if the debuff is not already active or you have 2 charges available.
    -- 8. 冷却结束时施放[烈焰咒符]
    local TargetSigilofFlameDebuffRemaining = getTargetDebuffRemainingTime("target", 204598, "HARMFUL|PLAYER") -- 目标身上[烈焰咒符]的剩余时间
    local SigilOfFlameCharges = checkSkillCharges(204596) -- 烈焰咒符
    if (TargetSigilofFlameDebuffRemaining == 0) and (SigilOfFlameCharges >= 1) and (furyDeficit > 30) and TargetIn5Yard then
        return Cast("烈焰咒符脚下")
    end

    if (SigilOfFlameCharges >= 2) and TargetIn5Yard then
        return Cast("烈焰咒符脚下")
    end

    -- 11. Use  Soul Carver.
    -- 12. 如果携带[怨念咒符]天赋则施放
    -- 12. Use  Sigil of Spite.
    local SigilOfSpiteIsCooldown = CoolDown(390163) -- 怨念州府
    if TargetIsBoss or IsBurst() or IsAOE then
        if (not IsMoving) then
            if SigilOfSpiteIsCooldown then
                return Cast("怨念咒符脚下")
            end
        end
    end

    -- 11. 冷却结束时施放[邪能毁灭]
    -- 13. Use  Fel Devastation if you have at least 50 Fury.
    if (not ShionVars["NotUseFelDevastation"]) and (TargetIsBoss or IsBurst() or IsAOE) then
        if (not IsMoving) then
            if (fury >= 50) and FelDevastationIsCooldown then
                return Cast("邪能毁灭")
            end
        end
    end



    -- 6. 如果[单目标]则：在灵魂碎片达到4-5时优先用于[幽魂炸弹]
    -- 7. 如果[多目标]则：在灵魂碎片达到4-5时全力施放[幽魂炸弹]
    -- 14. Use  Spirit Bomb with 4+ Souls.
    local SpiritBombUsable = IsSpellKnownOrOverridesKnown(247454) -- 幽魂炸弹
    if SpiritBombUsable and (soulNum >= 4) and (fury >= 50) then
        return Cast("幽魂炸弹")
    end

    -- 13. 尽可能多地施放[灵魂裂劈]
    -- 15. Spend Fury with  Soul Cleave.
    if not IsPlayerSpell(389708) then
        if (fury >= 30) and EnemyIn5Yard then
            if IsMoving or (not FelDevastationIsCooldown) or ShionVars["NotUseFelDevastation"] then
                if TargetIn5Yard then
                    return Cast("灵魂裂劈")
                end
                if EnemyIn5Yard then
                    return Cast("就近灵魂裂劈")
                end
            end
        end
    end



    --print((fury >= 50))
    --print(TargetIn5Yard)
    if (fury >= 50) then
        if TargetIn5Yard then
            return Cast("灵魂裂劈")
        end
        if EnemyIn5Yard then
            return Cast("就近灵魂裂劈")
        end
    end

    -- 不要浪费破裂
    -- 16. Use  Fracture.
    if FractureCharges >= 1 then
        if TargetIn5Yard then
            return Cast("破裂")
        end
        if EnemyIn5Yard then
            return Cast("就近破裂")
        end
    end

    -- 14. 如果不会怒气溢出，施放[邪能之刃]
    --  17. Fel blade if you won't cap Fury.
    local FelBladeIsCooldown = CoolDown(232893) -- 邪能之刃
    if (furyDeficit > 40) and FelBladeIsCooldown then
        if TargetIn5Yard then
            return Cast("邪能之刃")
        end
        if EnemyIn5Yard then
            return Cast("就近邪能之刃")
        end
    end


    --  18. Throw Glaive for filler or when kiting.
    -- 16. 无其他选择时使用[投掷利刃]填充
    local ThrowGlaiveCharges = checkSkillCharges(204157) -- 投掷利刃
    if (not ReaverGlaiveUsable) and (ThrowGlaiveCharges >= 1) and TargetIn30Yard then
        return Cast("投掷利刃")
    end

    return Idle("无事可做")
end


-- 这个监听
local rotationEventFrame = CreateFrame("Frame")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_CHANNEL_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_SUCCEEDED")
rotationEventFrame:RegisterEvent("PLAYER_LEAVE_COMBAT")
rotationEventFrame:RegisterEvent("PLAYER_ENTER_COMBAT")
rotationEventFrame:RegisterEvent("PLAYER_STARTED_MOVING")
rotationEventFrame:RegisterEvent("PLAYER_STOPPED_MOVING")
rotationEventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, event, ...)
end)
function rotationEventFrame:UNIT_SPELLCAST_START(event, unitTarget, castGUID, spellID)
    checkTargetIsTankOutburstDamage(event, spellID)
end

function rotationEventFrame:UNIT_SPELLCAST_CHANNEL_START(event, unitTarget, castGUID, spellID)
    checkTargetIsTankOutburstDamage(event, spellID)
end

function rotationEventFrame:UNIT_SPELLCAST_SUCCEEDED(event, unitTarget, castGUID, spellID)
    clearTargetIsTankOutburstDamage(event, spellID)
end

function rotationEventFrame:PLAYER_STARTED_MOVING()
    --moving_time = GetTime() + 360
    return
end

function rotationEventFrame:PLAYER_STOPPED_MOVING()
    --moving_time = GetTime()
    return
end
function rotationEventFrame:PLAYER_LEAVE_COMBAT()
    if ShionVars["AutoBurst"] then
        ClearBurst();
    end
end
function rotationEventFrame:PLAYER_ENTER_COMBAT()
    if ShionVars["AutoBurst"] then
        SetBurst(25);
        --print("自动爆发25秒")
    end
end