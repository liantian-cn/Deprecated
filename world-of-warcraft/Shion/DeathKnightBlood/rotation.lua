-- 打断部分
local MeleeDPSInterruptSpellList = {}; -- 打断技能清单
local MeleeDPSInterruptBlacklist = {}; -- 打断技能黑名单


ShionVars["InterruptAnything"] = false;
local function ToggleInterruptAnything()
    ShionVars["InterruptAnything"] = not ShionVars["InterruptAnything"];
    ShionCB["InterruptAnything"]:SetChecked(ShionVars["InterruptAnything"]);
end
CreateLine("任意打断", "InterruptAnything", ToggleInterruptAnything)


-- 危机设置

local crisisEndTime = GetTime()
local function checkCrisis()
    return GetTime() < crisisEndTime
end

function setCrisis(duration)
    crisisEndTime = GetTime() + duration
end

-- 有敌人在近战
-- 如果目标在近战范围，返回1
-- 如果目标不在近战范围，但是近战范围有敌人，返回2.
-- 如果目标不在近战范围，并且近战范围没有敌人，返回0.
local function checkEnemyInMelee()
    local targetInRange = C_Spell.IsSpellInRange(49998, "target") or false
    if UnitCanAttack("player", "target") and targetInRange and (not UnitIsDeadOrGhost("target")) then
        return 1
    end
    local unitID, unitInRange = nil, false
    for _, plate in pairs(C_NamePlate.GetNamePlates()) do
        unitID = plate.namePlateUnitToken
        unitInRange = C_Spell.IsSpellInRange(49998, unitID) or false
        if UnitCanAttack("player", unitID) and unitInRange and (not UnitIsDeadOrGhost(unitID)) then
            return 2
        end
    end
    return 0
end


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

-- 排气臂铠可用
local function checkRacesReady()
    local itemId = GetInventoryItemID("player", 9)
    if itemId ~= 221808 then
        return false
    end
    local _, duration, enable = C_Container.GetItemCooldown(221808)
    return (enable == 1) and (duration == 0)

end

local function checkSkillInRange(spell_id, targetUnit)
    if not UnitExists(targetUnit) then
        return false
    end
    return C_Spell.IsSpellInRange(spell_id, targetUnit) or false
end

local function getPlayerAuraRemainingTime(buff_id)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(buff_id)
    if aura then
        local remaining = aura.expirationTime - GetTime()
        return math.max(remaining, 0)
    end
    return 0
end

local function getPlayerAuraCount(buff_id)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(buff_id)
    if aura then
        return aura.applications
    else
        return 0
    end
end

local function checkPlayerAuraExists(buff_id)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(buff_id)

    if aura then
        return true
    end
    return false
end

local function getRuneCount()
    local spellCooldownInfo = C_Spell.GetSpellCooldown(61304)
    local gcd_remaining
    if spellCooldownInfo.duration == 0 then
        gcd_remaining = 0
    else
        gcd_remaining = spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end

    local amount = 0
    for i = 1, 6 do
        local start, duration, runeReady = GetRuneCooldown(i)
        if runeReady then
            amount = amount + 1
        else
            if (start + duration - GetTime()) < gcd_remaining then
                amount = amount + 1
            end
        end
    end
    return amount
end

local function getSkillCharges(spell_id, cooldownLimit)
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

local function NumberOfEnemyInRange(mob_range, mob_health)
    local inRange, unitID = 0
    for _, plate in pairs(C_NamePlate.GetNamePlates()) do
        unitID = plate.namePlateUnitToken
        if UnitCanAttack("player", unitID) and (not UnitIsDeadOrGhost(unitID)) then
            if isUnitInRange(unitID, mob_range) and UnitAffectingCombat(unitID) and (UnitHealth(unitID) > mob_health) then
                inRange = inRange + 1
            end
        end
    end
    return inRange
end

local function getSpellCoolDown(spell_id)
    local spellCooldownInfo = C_Spell.GetSpellCooldown(spell_id)

    if spellCooldownInfo.duration == 0 then
        return 0
    else
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end

local function getAuraInfo(targetUnit, buff_id, filter)
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

local function getMobDebuffCount(mob_range, buff_id)
    local inRange, unitID = 0
    for _, plate in pairs(C_NamePlate.GetNamePlates()) do
        unitID = plate.namePlateUnitToken

        if UnitCanAttack("player", unitID)
                and (not UnitIsDeadOrGhost(unitID))
                and isUnitInRange(unitID, mob_range) then

            local auraInfo = getAuraInfo(unitID, buff_id, "HARMFUL|PLAYER")
            if auraInfo then
                inRange = inRange + 1
            end

        end
    end
    return inRange
end

local function main_rotation()
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()
    if not (classFilename == "DEATHKNIGHT" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    local playerMaxHealth = UnitHealthMax("player")
    local playerCurrentHealth = UnitHealth("player")
    local playerHealAbsorbs = UnitGetTotalHealAbsorbs("player") -- 治疗吸收盾
    local playerAbsorbs = UnitGetTotalAbsorbs("player")  -- 身上的盾
    local playerHP = (playerCurrentHealth - playerHealAbsorbs) / playerMaxHealth * 100 -- 玩家的血量百分比

    local runicPower = UnitPower("player", Enum.PowerType.RunicPower)
    local runeCount = getRuneCount()
    local IsMoving = GetUnitSpeed("player") > 0
    local InBossCombat = UnitExists("target") and ((UnitLevel("target") == -1) or (UnitLevel("target") >= 82))
    local enemyInMelee = checkEnemyInMelee()

    if not UnitAffectingCombat("player") then
        return Idle("玩家不在战斗中")
    end

    if IsMounted() then
        return Idle("玩家在坐骑上")
    end

    if UnitIsPlayer("target") then
        return Idle("目标是玩家")
    end

    if UnitInVehicle("player") then
        return Idle("玩家在载具中")
    end

    if ChatFrame1EditBox:IsVisible() then
        return Idle("聊天框")
    end

    if UnitIsDeadOrGhost("player") then
        return Idle("玩家已死亡")
    end
    if checkPlayerIsCasting() then
        return Idle("在施法")
    end

    if (playerHP < 30) and checkRacesReady() then
        return Cast("工程护腕")
    end

    if checkCrisis() then
        if (playerHP < 80) and (runicPower > 40) then
            if enemyInMelee == 2 then
                return Cast("就近灵界打击")
            elseif enemyInMelee == 1 then
                return Cast("灵界打击")
            end
        end
    end

    if (playerHP < 50) and (runicPower > 40) then
        if enemyInMelee == 2 then
            return Cast("就近灵界打击")
        elseif enemyInMelee == 1 then
            return Cast("灵界打击")
        end
    end

    if CoolDown(47528) then

        if UnitCanAttack("player", "focus")
                and checkSkillInRange(47528, "focus")
                and ((ShionVars["InterruptAnything"] and CanInterrupt("focus")) or ShouldInterrupt("focus")) then

            return Cast("心灵冰冻焦点")

        end

        if UnitCanAttack("player", "target")
                and checkSkillInRange(47528, "target")
                and ((ShionVars["InterruptAnything"] and CanInterrupt("target")) or ShouldInterrupt("target")) then
            return Cast("心灵冰冻目标")
        end

    end

    -- 白骨之盾
    local buffBoneShieldCount = getPlayerAuraCount(195181)
    local buffBoneShieldRemainingTime = getPlayerAuraRemainingTime(195181)

    -- 破灭，死神印记炸了后的buff
    local buffExterminateRemainingTime = getPlayerAuraRemainingTime(441416)
    local buffExterminateExists = checkPlayerAuraExists(441416)

    -- 死神印记
    local spellReaperMarkUsable = IsSpellKnownOrOverridesKnown(439843) and CoolDown(439843) and checkSkillInRange(439843, "target")

    -- 死神的抚摩
    local spellDeathCaressUsable = CoolDown(195292) and checkSkillInRange(195292, "target")
    -- 精髓分裂
    local spellMarrowrendUsable = checkSkillInRange(195182, "target")

    --if ShionVars["GlobalDEBUG"] then
    --    print("buffBoneShieldCount" .. buffBoneShieldCount)
    --    print("buffBoneShieldRemainingTime" .. buffBoneShieldRemainingTime)
    --end
    if (buffBoneShieldCount < 5) or (buffBoneShieldRemainingTime < 6) then
        if spellReaperMarkUsable and not buffExterminateExists then
            return Cast("死神印记")
        end

        if spellDeathCaressUsable then
            return Cast("死神的抚摩")
        end

        if enemyInMelee == 2 then
            return Cast("就近精髓分裂")
        elseif enemyInMelee == 1 then
            return Cast("精髓分裂")
        end

    end

    if CoolDown(46585) then
        return Cast("亡者复生")
    end

    local buffDecayExists = checkPlayerAuraExists(188290) -- 死亡凋零存在
    local spellDecayCharges = getSkillCharges(43265) -- 死亡凋零充能
    --if ShionVars["GlobalDEBUG"] then
    --    print("spellDecayCharges".. spellDecayCharges)
    --end

    if (not IsMoving) and (not buffDecayExists) and (spellDecayCharges > 0) then
        return Cast("死亡凋零")
    end

    if spellReaperMarkUsable and not buffExterminateExists then
        return Cast("死神印记")
    end
    --
    ---- Cast Soul Reaper if the Target is below 35% HP.
    ---- 在以下情况施放灵魂收割（Soul Reaper）：目标生命值低于35%
    ---- Or you have the buff Reaper of Souls from your Reaper's Mark application.
    ---- 或你拥有收割者印记触发的收割之魂（Reaper of Souls）增益时。
    --
    --if Prop("技能可用", "灵魂收割") then
    --    if CoolDown("灵魂收割", 300) then
    --        if (Prop("目标血量") < 35) then
    --            return Cast("灵魂收割")
    --        end
    --    end
    --end
    --
    --
    --

    -- 符文刃舞的CD
    local spellDancingRuneWeaponCoolDown = getSpellCoolDown(49028)

    if IsSpellKnownOrOverridesKnown(219809)
            and CoolDown(219809)
            and buffDecayExists
            and (buffBoneShieldCount >= 5)
            and (spellDancingRuneWeaponCoolDown >= 25)
            and (runicPower < 90) then
        return Cast("墓石")
    end

    if IsSpellKnownOrOverridesKnown(194844)
            and CoolDown(194844)
            and buffDecayExists
            and (buffBoneShieldCount >= 5)
            and (spellDancingRuneWeaponCoolDown >= 25) then
        return Cast("白骨风暴")
    end

    if runicPower > 90 then
        if enemyInMelee == 2 then
            return Cast("就近灵界打击")
        elseif enemyInMelee == 1 then
            return Cast("灵界打击")
        end
    end

    local buffLuckOfDrawExists = checkPlayerAuraExists(1218601) -- 四件套存在
    if (runicPower > 40) and buffLuckOfDrawExists then
        if enemyInMelee == 2 then
            return Cast("就近灵界打击")
        elseif enemyInMelee == 1 then
            return Cast("灵界打击")
        end
    end

    --
    -- 吸血鬼之血
    local spellVampiricBloodCoolDown = getSpellCoolDown(55233)
    local buffVampiricBloodExists = checkPlayerAuraExists(55233)
    local debuffBloodPlagueCount = getMobDebuffCount(10, 55078)
    --if ShionVars["GlobalDEBUG"] then
    --    print("debuffBloodPlagueCount".. debuffBloodPlagueCount)
    --end

    if IsSpellKnownOrOverridesKnown(274156)
            and CoolDown(274156)
            and ((spellVampiricBloodCoolDown > 30) or (buffVampiricBloodExists))
            and ((debuffBloodPlagueCount >= 3) or (InBossCombat)) then
        return Cast("吞噬")
    end

    local spellBloodBoilCharges = getSkillCharges(50842)  --血液沸腾
    if (spellBloodBoilCharges > 0) and (NumberOfEnemyInRange(10, 200000) >= 5) then
        return Cast("血液沸腾")
    end

    if (spellBloodBoilCharges > 1) and (NumberOfEnemyInRange(10, 200000) > 0) then
        return Cast("血液沸腾")
    end

    if (buffBoneShieldCount < 9) then
        if spellDeathCaressUsable then
            return Cast("死神的抚摩")
        end

        if enemyInMelee == 2 then
            return Cast("就近精髓分裂")
        elseif enemyInMelee == 1 then
            return Cast("精髓分裂")
        end
    end

    if (runeCount >= 1) then
        if buffExterminateExists and (UnitHealth("target") > 10000000) then

            if enemyInMelee == 2 then
                return Cast("就近精髓分裂")
            elseif enemyInMelee == 1 then
                return Cast("精髓分裂")
            end
        end
        if enemyInMelee == 2 then
            return Cast("就近心脏打击")
        elseif enemyInMelee == 1 then
            return Cast("心脏打击")
        end
        return Cast("心脏打击")
    end

    return Idle("无事可做")
end

MeleeDPSInterruptSpellList[263202] = true;
MeleeDPSInterruptSpellList[263215] = true;
MeleeDPSInterruptSpellList[268702] = true;
MeleeDPSInterruptSpellList[268797] = true;
MeleeDPSInterruptSpellList[269302] = true;
MeleeDPSInterruptSpellList[271579] = true;
MeleeDPSInterruptSpellList[280604] = true;
MeleeDPSInterruptSpellList[293827] = true;
MeleeDPSInterruptSpellList[301088] = true;
MeleeDPSInterruptSpellList[330868] = true;
MeleeDPSInterruptSpellList[341902] = true;
MeleeDPSInterruptSpellList[341969] = true;
MeleeDPSInterruptSpellList[341977] = true;
MeleeDPSInterruptSpellList[422541] = true;
MeleeDPSInterruptSpellList[423051] = true;
MeleeDPSInterruptSpellList[424419] = true;
MeleeDPSInterruptSpellList[424420] = true;
MeleeDPSInterruptSpellList[425536] = true;
MeleeDPSInterruptSpellList[426145] = true;
MeleeDPSInterruptSpellList[426295] = true;
MeleeDPSInterruptSpellList[427260] = true;
MeleeDPSInterruptSpellList[427356] = true;
MeleeDPSInterruptSpellList[430238] = true;
MeleeDPSInterruptSpellList[437721] = true;
MeleeDPSInterruptSpellList[440687] = true;
MeleeDPSInterruptSpellList[441351] = true;
MeleeDPSInterruptSpellList[441627] = true;
MeleeDPSInterruptSpellList[446657] = true;
MeleeDPSInterruptSpellList[462771] = true;
MeleeDPSInterruptSpellList[465595] = true;
MeleeDPSInterruptSpellList[465871] = true;
MeleeDPSInterruptSpellList[468631] = true;
MeleeDPSInterruptSpellList[472378] = true;
MeleeDPSInterruptSpellList[473376] = true;
MeleeDPSInterruptSpellList[473993] = true;
MeleeDPSInterruptSpellList[474001] = true;
MeleeDPSInterruptSpellList[1214468] = true;
MeleeDPSInterruptSpellList[1214504] = true;
MeleeDPSInterruptSpellList[1214780] = true;
MeleeDPSInterruptSpellList[1216475] = true;
MeleeDPSInterruptSpellList[1217138] = true;