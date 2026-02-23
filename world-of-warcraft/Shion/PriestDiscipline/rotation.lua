local ShieldSpellInfo = C_Spell.GetSpellInfo(17)        -- 真言术：盾的spell信息
local RenewsSpellInfo = C_Spell.GetSpellInfo(139)       -- 恢复的spell信息
local AtonementSpellInfo = C_Spell.GetSpellInfo(194384) -- 救赎的spell信息
local PainSpellInfo = C_Spell.GetSpellInfo(589)         -- 暗言术：痛的spell信息
local FortitudeSpellInfo = C_Spell.GetSpellInfo(21562)  -- 真言术：韧的spell信息

-- 技能清单
-- Cast("player盾")
-- Cast("party1盾")
-- Cast("party2盾")
-- Cast("party3盾")
-- Cast("party4盾")
-- Cast("target苦修")
-- Cast("focus苦修")
-- Cast("player苦修")
-- Cast("party1苦修")
-- Cast("party2苦修")
-- Cast("party3苦修")
-- Cast("party4苦修")
-- Cast("player恢复")
-- Cast("party1恢复")
-- Cast("party2恢复")
-- Cast("party3恢复")
-- Cast("party4恢复")
-- Cast("player快速治疗")
-- Cast("party1快速治疗")
-- Cast("party2快速治疗")
-- Cast("party3快速治疗")
-- Cast("party4快速治疗")
-- Cast("虔诚预兆")
-- Cast("慰藉预兆")
-- Cast("洞察预兆")
-- Cast("远见预兆")
-- Cast("target灭")
-- Cast("focus灭")
-- Cast("target惩击")
-- Cast("focus惩击")
-- Cast("target心灵震爆")
-- Cast("focus心灵震爆")
-- Cast("target暗影魔")
-- Cast("focus暗影魔")
-- Cast("target痛")
-- Cast("focus痛")
-- Cast("player纯净术")
-- Cast("party1纯净术")
-- Cast("party2纯净术")
-- Cast("party3纯净术")
-- Cast("party4纯净术")
-- Cast("mouseover纯净术")
-- Cast("player灌注")
-- Cast("party1灌注")
-- Cast("party2灌注")
-- Cast("party3灌注")
-- Cast("party4灌注")

-- 自我救助标准
local SelfHealScore = 0.45
-- 渐隐术血线标准
local FadeHealScore = 0.85
-- 防御苦修阈值
local DefensivePenanceScore = 0.75
-- 坦克苦修阈值
local TankPenanceScore = 0.50
-- 快疗队友阈值
local FlashHealScore = 0.7
-- 治疗自己阈值
local HealSelfScore = 0.8
-- 圣光涌动阈值
local LightningScore = -0.1
-- 福音治疗量
local evangelismValue = 5660000
-- 耀的治疗量
local radianceValue = 550000

-- 字典定义
-- 秒驱散的魔法减益列表
local InstantDispelMagicDebuffList = {};
-- 手动驱散魔法减益列表
local ManualDispelMagicDebuffList = {};
-- 会爆炸的魔法减益列表
local ExplodeDispelMagicDebuffList = {};
-- 高伤害减益效果列表
local HighDamageDebuffList = {};
-- 中等伤害减益效果列表
local MidDamageDebuffList = {};
-- 怪物打断玩家的技能列表
local EnemyInterruptsCastsList = {};
-- 需要预兆覆盖的技能列表
local AoeSpellList = {};

-- 快疗治疗量系数
local FlashHealScale = 1.0
-- 爆炸debuff驱散血线
local Explode_Debuff_Remove_Hp_Score = 0.80

local healthScoreWeightByClass = {
    [1] = 0.0, -- WARRIOR
    [2] = 0.0, -- PALADIN
    [3] = -0.01, -- HUNTER
    [4] = 0.0, -- ROGUE
    [5] = 0.0, -- PRIEST
    [6] = 0.05, -- DEATHKNIGHT
    [7] = 0.0, -- SHAMAN
    [8] = -0.01, -- MAGE
    [9] = 0.0, -- WARLOCK
    [10] = 0.0, -- MONK
    [11] = -0.01, -- DRUID
    [12] = 0.01, -- DEMONHUNTER
    [13] = 0.0, -- EVOKER
}
local healthScoreWeightByRole = {
    ["TANK"] = 0.2,
    ["HEALER"] = -0.02,
    ["DAMAGER"] = 0.0,
    ["NONE"] = 0.0,
}

ShionVars["ActionInNoCombat"] = false;
local function ToggleActionInNoCombat()
    ShionVars["ActionInNoCombat"] = not ShionVars["ActionInNoCombat"];
    ShionCB["ActionInNoCombat"]:SetChecked(ShionVars["ActionInNoCombat"]);
end
CreateLine("非战斗治疗", "ActionInNoCombat", ToggleActionInNoCombat)


ShionVars["UseFlash"] = false;
local function ToggleUseFlash()
    ShionVars["UseFlash"] = not ShionVars["UseFlash"];
    ShionCB["UseFlash"]:SetChecked(ShionVars["UseFlash"]);
end
CreateLine("使用快速治疗", "UseFlash", ToggleUseFlash)

ShionVars["UseFade"] = true;
local function ToggleUseFade()
    ShionVars["UseFade"] = not ShionVars["UseFade"];
    ShionCB["UseFade"]:SetChecked(ShionVars["UseFade"]);
end
CreateLine("使用渐隐", "UseFade", ToggleUseFade)



-- AOE 即将来临时
local AoeStartTime = GetTime()
local AoeEndTime = GetTime()
local function AOEComing()
    return GetTime() < AoeStartTime
end
local function InAOE()
    return (GetTime() < AoeEndTime) and (GetTime() > AoeStartTime)
end

-- 自动选择敌人目标
local function AutoEnemyTarget()
    if UnitExists("focus") and UnitCanAttack("player", "focus") and UnitAffectingCombat("focus") then
        return "focus"
    end
    if UnitExists("target") and UnitCanAttack("player", "target") and UnitAffectingCombat("target") then
        return "target"
    end
    return nil
end

-- 单位剩余时间计算：护盾的
local function UnitShieldRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, ShieldSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end
-- 单位剩余时间计算：救赎的
local function UnitAtonementRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, AtonementSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end
-- 单位剩余时间计算：恢复的
local function UnitRenewsRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, RenewsSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end
-- 单位剩余时间计算：韧的
local function UnitFortitudeRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, FortitudeSpellInfo.name, "HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end
-- 获取洞察预兆的可用层数，你接下来施放的3个法术的冷却时间缩短7秒。
local function PremonitionOfInsightCharges()
    if not IsSpellKnownOrOverridesKnown(428933) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428933)
    return chargeInfo.currentCharges
end
-- 获取虔诚预兆的可用层数，你造成的治疗效果提高20%，并将对玩家造成的过量治疗的70%重新分配给附近最多4个盟友，持续15秒。
local function PremonitionOfPietyCharges()
    if not IsSpellKnownOrOverridesKnown(428930) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428930)
    return chargeInfo.currentCharges
end
-- 获取慰藉预兆的可用层数，你的下一个单体治疗法术将为目标提供一个护盾，吸收0点伤害，并使其受到的伤害降低15%，持续15秒。
local function PremonitionOfSolaceCharges()
    if not IsSpellKnownOrOverridesKnown(428934) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428934)
    return chargeInfo.currentCharges
end
-- 获取远见预兆的可用层数，获得效果为100%的洞察预兆、虔诚预兆和慰藉预兆。
local function PremonitionOfClairvoyanceCharges()
    if not IsSpellKnownOrOverridesKnown(440725) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(440725)
    return chargeInfo.currentCharges
end
-- 获取总预兆层数
local function TotalPremonitionCharges()
    local totalCharges = PremonitionOfInsightCharges() + PremonitionOfPietyCharges() + PremonitionOfSolaceCharges() + PremonitionOfClairvoyanceCharges()
    return totalCharges
end
-- 检查玩家是否有[分秒必争]buff
local function HasWasteNoTimeBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(440683)
    if aura then
        return true
    end
end
-- 检查玩家是否有洞察预兆buff，，你接下来施放的3个法术的冷却时间缩短7秒。
local function HasPremonitionOfInsightBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(428933)
    if aura then
        return true
    end
end
-- 获取圣光涌动层数；快速治疗瞬发
local function getSurgeOfLightCharges()
    --local spellInfo = C_Spell.GetSpellInfo(spell_name)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(114255)
    if aura then
        return aura.applications
    end
    return 0
end
-- 耀可用
local radiance_spell_time = GetTime()
local function getRadianceCharges()
    -- 先开会不会
    if not IsSpellKnownOrOverridesKnown(194509) then
        return 0
    end
    -- 配合时间坚挺，10秒只放一次耀
    if radiance_spell_time > GetTime() then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(194509)
    local charges = chargeInfo.currentCharges
    if charges > 0 then
        --有瞬发
        if HasWasteNoTimeBuff() then
            return charges
        end
        if GetUnitSpeed("player") == 0 then
            return charges
        end
        -- 不在移动
    end
    return 0
end
-- 检查玩家[祸福相倚]的层数
local function getWealAndWoeStack()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(390787)
    if aura then
        return aura.applications
    end
    return 0
end
-- 获取单位痛剩余时间
local function UnitPainRemaining(unitToken)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitToken, PainSpellInfo.name, "PLAYER|HARMFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end
-- 单个单位健康分数计算
local function calculateUnitHealthScore(unitName, role, classID)
    local maxHealth = UnitHealthMax(unitName)
    local currentHealth = UnitHealth(unitName)
    local currentUnitIncomingHeal = UnitGetIncomingHeals(unitName, "player") or 0
    local totalHealAbsorbs = UnitGetTotalHealAbsorbs(unitName) -- 治疗吸收盾
    local healthScoreBase = (currentHealth - totalHealAbsorbs + currentUnitIncomingHeal) / maxHealth
    local healingDeficit = maxHealth - currentHealth + totalHealAbsorbs
    local healthScoreOffset = 0
    local unitHighDamageDebuffCount = 0
    local unitMidDamageDebuffCount = 0

    -- 根据职责微调分数
    healthScoreOffset = healthScoreOffset + healthScoreWeightByRole[role]
    -- 根据职业微调分数
    healthScoreOffset = healthScoreOffset + healthScoreWeightByClass[classID]
    -- 计算单位的高伤害减益数量
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unitName, i, "HARMFUL")
        if not debuffData then
            break
        end
        if HighDamageDebuffList[debuffData.spellId] or HighDamageDebuffList[debuffData.name] then
            healthScoreOffset = healthScoreOffset - 20
            unitHighDamageDebuffCount = unitHighDamageDebuffCount + 1
        elseif MidDamageDebuffList[debuffData.spellId] or MidDamageDebuffList[debuffData.name] then
            healthScoreOffset = healthScoreOffset - 10
            unitMidDamageDebuffCount = unitMidDamageDebuffCount + 1
        end
    end

    return healthScoreBase, healthScoreBase + healthScoreOffset, healingDeficit, unitHighDamageDebuffCount, unitMidDamageDebuffCount

end


--[[
    单位Debuff状态计算：
    返回值：
    高危Debuff数量。
    中危Debuff数量。
]]
local function UnitDispelDebuffCalculate(unitName)
    -- 强化纯净，可驱散疾病
    local ImprovedPurify = IsPlayerSpell(390632)
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unitName, i, "HARMFUL")
        if not debuffData then
            break
        end
        if (debuffData.dispelName == "Magic") or (debuffData.dispelName == "Disease" and ImprovedPurify) then
            if InstantDispelMagicDebuffList[debuffData.spellId] then
                return 3
            elseif ManualDispelMagicDebuffList[debuffData.spellId] then
                return -1
            elseif ExplodeDispelMagicDebuffList[debuffData.spellId] then
                return 2
            end
            return 1
        end
    end
    return 0
end

-- 计算小队健康分数并排序
-- /dump calculatePartyHealthScore()
local function calculatePartyHealthScore()

    -- 先获得小队可视范围的成员，保存到partyMembers
    local numGroupMembers = GetNumGroupMembers()
    local partyMembers = {}
    table.insert(partyMembers, "player")
    if numGroupMembers > 0 then
        for i = 1, numGroupMembers do
            local unitName = "party" .. i
            if UnitExists(unitName) and not (UnitIsDeadOrGhost(unitName)) and C_Spell.IsSpellInRange(139, unitName) then
                table.insert(partyMembers, unitName)
            end
        end
    end

    -- 遍历小队成员，计算健康分数，血量，最大血量。
    local sortedArray = {}
    local currentUnitHealthPercent, currentUnitHealthScore, currentUnitHealingDeficit, currentUnitHighDamageDebuffCount, currentUnitMidDamageDebuffCount
    local currentUnitRole
    local currentUnitClassName, currentUnitClassId
    local currentUnitTable = {}
    for _, unitName in pairs(partyMembers) do
        currentUnitClassName, _, currentUnitClassId = UnitClass(unitName)
        currentUnitRole = UnitGroupRolesAssigned(unitName)
        currentUnitHealthPercent, currentUnitHealthScore, currentUnitHealingDeficit, currentUnitHighDamageDebuffCount, currentUnitMidDamageDebuffCount = calculateUnitHealthScore(unitName, currentUnitRole, currentUnitClassId)
        currentUnitTable = {
            unit = unitName,
            name = UnitName(unitName),
            healthPercent = currentUnitHealthPercent,
            healthScore = currentUnitHealthScore,
            healthMax = UnitHealthMax(unitName),
            shieldRemaining = UnitShieldRemaining(unitName),
            atonementRemaining = UnitAtonementRemaining(unitName),
            renewsRemaining = UnitRenewsRemaining(unitName),
            fortitudeRemaining = UnitFortitudeRemaining(unitName),
            dispelDebuffCode = UnitDispelDebuffCalculate(unitName),
            role = currentUnitRole,
            class = currentUnitClassName,
            classId = currentUnitClassId,
            inCombat = UnitAffectingCombat(unitName),
            highDamageDebuffCount = currentUnitHighDamageDebuffCount,
            midDamageDebuffCount = currentUnitMidDamageDebuffCount,
            HealingDeficit = currentUnitHealingDeficit
        }
        table.insert(sortedArray, currentUnitTable)
    end

    -- 排序
    table.sort(sortedArray, function(a, b)
        if a.healthScore == b.healthScore then
            -- 当健康分数相同时，使用最大生命值作为次要排序条件（由低到高）
            return a.healthMax < b.healthMax
        end
        -- 主要根据健康分数排序（由低到高）
        return a.healthScore < b.healthScore
    end)

    return sortedArray
end

-- 拷贝table
local function copyTable(partyHealthScore)
    local newTable = {}
    for _, unitTable in ipairs(partyHealthScore) do
        table.insert(newTable, unitTable)
    end
    return newTable
end

-- 摘取出玩家状态
local function getPlayerUnit(partyHealthScore)
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.unit == "player" then
            return unitTable
        end
    end
    return nil
end
-- 摘取出坦克状态
local function getTankTable(partyHealthScore)
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.role == "TANK" then
            return unitTable
        end
    end
    return nil
end

-- 无救赎玩家统计
local function NonAtonementStatus(partyHealthScore, required_time)
    if not required_time then
        required_time = 5
    end
    local NonAtonementList = {}  --无救赎角色列表
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.atonementRemaining <= required_time then
            table.insert(NonAtonementList, unitTable)
        end
    end
    -- 并且按救赎剩余时间从小到大排序
    table.sort(NonAtonementList, function(a, b)
        if a.atonementRemaining == b.atonementRemaining then
            return a.healthScore < b.healthScore
        end
        -- 主要根据健康分数排序（由低到高）
        return a.atonementRemaining < b.atonementRemaining
    end)
    return NonAtonementList
end

-- 检查玩家是否正在施法
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
-- 小队有人在战斗中
local function checkSomeOneInCombat(partyHealthScore)
    for _, unit in pairs(partyHealthScore) do
        if unit.inCombat then
            return true
        end
    end
    return false
end

-- 战斗前补耐力的逻辑：如果队伍有任一人耐力小于5分钟，则补
local function FortitudePreCombatLogic(partyHealthScore)
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.fortitudeRemaining < 300 then
            return true
        end
    end
    return false
end

-- 驱散逻辑
local function getDebuffNeedRemoveUnit(partyHealthScore)
    local party_min_health_score = 1   -- 队伍非T最低血量
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.role ~= "TANK" then
            party_min_health_score = math.min(party_min_health_score, unitTable.healthPercent)
        end
    end
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.dispelDebuffCode == 3 then
            -- 有立即驱散的，则驱散
            return unitTable
        elseif (unitTable.dispelDebuffCode == 2) and (party_min_health_score > Explode_Debuff_Remove_Hp_Score) then
            -- 有爆炸驱散的，并且队伍非T最低血量大于Explode_Debuff_Remove_Hp_Score，则驱散
            return unitTable
        elseif (unitTable.dispelDebuffCode == 1) and (party_min_health_score > 0.3) then
            -- 有普通驱散的，并且队伍非T最低血量大于0.7，则驱散
            return unitTable
        end
    end
    return nil
end

-- 最低健康分的单位-非T
local function getLowestHealthScoreUnit(partyHealthScore)
    local lowestHealthScore = 2
    local lowestHealthScoreUnitTable = nil
    for _, unitTable in ipairs(partyHealthScore) do
        if (unitTable.role ~= "TANK") and (unitTable.healthScore < lowestHealthScore) then
            lowestHealthScore = unitTable.healthScore
            lowestHealthScoreUnitTable = unitTable
        end
    end
    return lowestHealthScoreUnitTable
end
-- 最低健康分的单位-含T
local function getLowestHealthScoreUnitWithTank(partyHealthScore)
    local lowestHealthScore = 2
    local lowestHealthScoreUnitTable = nil
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.healthScore < lowestHealthScore then
            lowestHealthScore = unitTable.healthScore
            lowestHealthScoreUnitTable = unitTable
        end
    end
    return lowestHealthScoreUnitTable
end

-- 最低血量单位-非T。当满血是不存在这个目标。
local function getLowestHealthPercentUnit(partyHealthScore)
    local lowestHealthPercent = 0.99
    local lowestHealthPercentUnitTable = nil
    for _, unitTable in ipairs(partyHealthScore) do
        if (unitTable.role ~= "TANK") and (unitTable.healthPercent < lowestHealthPercent) then
            lowestHealthPercent = unitTable.healthPercent
            lowestHealthPercentUnitTable = unitTable
        end
    end
    return lowestHealthPercentUnitTable
end

-- 最低血量单位-含T。当满血是不存在这个目标。
local function getLowestHealthPercentUnitWithTank(partyHealthScore)
    local lowestHealthPercent = 0.99
    local lowestHealthPercentUnitTable = nil
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.healthPercent < lowestHealthPercent then
            lowestHealthPercent = unitTable.healthPercent
            lowestHealthPercentUnitTable = unitTable
        end
    end
    return lowestHealthPercentUnitTable
end

-- 盾剩余时间最少的单位-非T
-- 因为默认partyHealthScore存在排序。所以都没有盾的时候，是健康分数的排序。
local function getShieldRemainingMinUnit(partyHealthScore)
    local shieldRemainingMin = 18
    local shieldRemainingMinUnitTable = nil
    for _, unitTable in ipairs(partyHealthScore) do
        if (unitTable.role ~= "TANK") and (unitTable.shieldRemaining < shieldRemainingMin) then
            shieldRemainingMin = unitTable.shieldRemaining
            shieldRemainingMinUnitTable = unitTable
        end
    end
    return shieldRemainingMinUnitTable
end

-- 血量缺口大于指定值的单位数量-非T
local function getHealingDeficitGreaterThanUnit(partyHealthScore, healingDeficit)
    local count = 0
    for _, unitTable in ipairs(partyHealthScore) do
        if (unitTable.role ~= "TANK") and (unitTable.HealingDeficit > healingDeficit) then
             count = count + 1
        end
    end
    return count
end

-- 福音逻辑
local function EvangelismLogic(partyHealthScore)
    if not IsSpellKnownOrOverridesKnown(472433) then
        return false
    end
    if not CoolDown(472433, 700) then
        return false
    end

    local atonementCount = 0                -- 救赎玩家总数
    for _, unitTable in ipairs(partyHealthScore) do
        if unitTable.atonementRemaining > 2 then
            atonementCount = atonementCount + 1
        end
    end
    if atonementCount == 0 then
        return false
    end
    local evangelismPerUnit = evangelismValue / atonementCount
    local NotOverUnit = 0
    for _, unitTable in ipairs(partyHealthScore) do
        if (unitTable.atonementRemaining > 2) and (unitTable.HealingDeficit < evangelismPerUnit) then
            NotOverUnit = NotOverUnit + 1
        end
    end
    if NotOverUnit >= 3 then
        return true
    end

    return false
end


-- 灌注逻辑：从detail获取最高伤害玩家，给灌注
local function PowerInfusionLogic(partyHealthScore)
    local currentUnit = "player"
    local currentMaxDamage = 0
    local unitDamage
    for _, unitTable in ipairs(partyHealthScore) do
        unitDamage = Details.UnitDamage(unitTable.unit)
        if unitDamage > currentMaxDamage then
            currentMaxDamage = unitDamage
            currentUnit = unitTable.unit
        end
    end
    return currentUnit
end
-- 治疗逻辑
local function main_rotation()
    -- 基础参数初始化 --

    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()

    -- 职业和专精检查 --
    if not (classFilename == "PRIEST" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    -- 异常状态检查 --
    if IsMounted("player") then
        return Idle("坐骑")
    end
    if UnitInVehicle("player") then
        return Idle("载具")
    end
    if ChatFrame1EditBox:IsVisible() then
        return Idle("聊天框")
    end
    if UnitIsDeadOrGhost("player") then
        return Idle("死亡")
    end
    if checkPlayerIsCasting() then
        return Idle("在施法")
    end

    if C_UnitAuras.GetAuraDataBySpellName("player", "进食饮水", "HELPFUL|PLAYER") then
        return Idle("进食饮水")
    end

    if C_UnitAuras.GetAuraDataBySpellName("player", "食物和饮料", "HELPFUL|PLAYER") then
        return Idle("食物和饮料")
    end

    -- 战斗环境参数获取 --
    local enemyTarget = AutoEnemyTarget()               -- 自动选择敌人目标
    local partyHealthScore = calculatePartyHealthScore() -- 计算小队健康评分
    local playerUnit = getPlayerUnit(partyHealthScore)                                          -- 摘取出当前玩家的状态
    local tankUnit = getTankTable(partyHealthScore)                                              -- 坦克恢复逻辑
    local lowestHealthScoreUnit = getLowestHealthScoreUnit(partyHealthScore)                      -- 非坦克最低分单位
    --local lowestHealthScoreUnitWithTank = getLowestHealthScoreUnitWithTank(partyHealthScore)      -- 最低分单位
    local lowestHealthPercentUnit = getLowestHealthPercentUnit(partyHealthScore)                  -- 非坦克最低血量单位
    --local lowestHealthPercentUnitWithTank = getLowestHealthPercentUnitWithTank(partyHealthScore)  -- 最低血量单位
    local debuffNeedRemoveUnit = getDebuffNeedRemoveUnit(partyHealthScore)                        -- 驱散逻辑
    local shieldRemainingMinUnit = getShieldRemainingMinUnit(partyHealthScore)                    -- 盾剩余时间最少的单位
    local isMoving = GetUnitSpeed("player") > 0         -- 移动状态检测
    local someOneInCombat = checkSomeOneInCombat(partyHealthScore)
    local nonAtonementList = nil                      -- 无救赎角色列表
    --local defaultTarget = "player"
    --local defaultTargetTable = playerUnit

    local PenanceCooldown = CoolDown(47540, 700)            --[苦修]
    local ShieldCooldown = CoolDown(17)                     --[真言术：盾]
    local DesperatePrayerCooldown = CoolDown(19236)         -- [绝望祷言]
    local FadeCooldown = CoolDown(586)                      -- [渐隐术]
    local PurifyCooldown = CoolDown(527)                    -- [纯净术]
    local surgeOfLightCharges = getSurgeOfLightCharges()    -- 圣光涌动层数
    local radianceCharges = getRadianceCharges()            -- [真言术：耀]
    local wealAndWoeStack = getWealAndWoeStack()            -- [祸福相倚]层数

    -- AOE
    local aoeComing = AOEComing()
    local inAoe = InAOE()
    -- 不同AOE环境下，救赎判定不一样。
    if aoeComing then
        nonAtonementList = NonAtonementStatus(partyHealthScore, 5)
    elseif inAoe then
        nonAtonementList = NonAtonementStatus(partyHealthScore, 3)
    else
        nonAtonementList = NonAtonementStatus(partyHealthScore, 1)
    end


    -- 非战斗逻辑处理 --
    if (not someOneInCombat) then
        if FortitudePreCombatLogic(partyHealthScore) then
            return Cast("耐力")
        end
        if ShionVars["ActionInNoCombat"] then
            -- 非战斗，苦修给健康分最低的
            if PenanceCooldown and lowestHealthScoreUnit then
                return Cast(lowestHealthScoreUnit.unit .. "苦修")
            end

            if ShieldCooldown and shieldRemainingMinUnit then
                return Cast(shieldRemainingMinUnit.unit .. "盾")
            end
        end

    end

    if not UnitAffectingCombat("player") then
        return Idle("不在战斗中")
    end

    -- 保命技能处理:生命值小于50%使用绝望祷言
    if playerUnit.healthScore < SelfHealScore then
        if DesperatePrayerCooldown then
            return Cast("绝望祷言")          -- 自保治疗
        end
    end

    -- 保命技能处理:生命值小于90%使用渐隐术
    if FadeCooldown and ShionVars["UseFade"] then
        if playerUnit.healthScore < FadeHealScore then
            return Cast("渐隐术")            -- 自保治疗
        end
    end

    if EvangelismLogic(partyHealthScore) then
        return Cast("福音")
    end

    -- AOE 预兆逻辑
    if inAoe then
        -- 预兆触发窗口期
        if TotalPremonitionCharges() == 2 then
            -- 有2层预兆时优先使用
            return Cast("预兆")
        end
    end

    -- AOE自我套盾逻辑
    if aoeComing or inAoe then
        if playerUnit.shieldRemaining == 0 then
            return Cast("player盾")
        end
    end

    -- AOE补救赎逻辑
    if aoeComing or inAoe then
        --如果有两个人没有救赎，则用耀
        if (#nonAtonementList >= 2) and (radianceCharges >= 1) then
            return Cast("耀")
        end
        if #nonAtonementList >= 1 then
            return Cast(nonAtonementList[1].unit .. "恢复")
        end
    end


    if PurifyCooldown and debuffNeedRemoveUnit then
        return Cast(debuffNeedRemoveUnit.unit .. "纯净术")
    end


    -- 耀有2层充能时，优先不浪费
    if radianceCharges > 1 then
        -- 没救赎的人大于等于2时
        if #nonAtonementList >= 2 then
            -- 群体治疗需求判断
            return Cast("耀")                -- 群体救赎应用
        end
        -- 或者有效治疗3个人时
        if getHealingDeficitGreaterThanUnit(partyHealthScore, radianceValue) >= 3 then
            return Cast("耀")
        end
    end



    -- 盾逻辑，[祸福相倚]层数大于3，且没有减CD预兆时候，用盾
    if ShieldCooldown and (wealAndWoeStack >= 3) and (not HasPremonitionOfInsightBuff()) then
        return Cast(shieldRemainingMinUnit.unit .. "盾")
    end

    if not enemyTarget then
        return Cast("切换目标")
    end

    -- 苦修卡CD用
    if PenanceCooldown then
        -- 如果血量最低的非T玩家，血量低于御苦修阈值，给他苦修
        if lowestHealthPercentUnit and (lowestHealthPercentUnit.healthPercent < DefensivePenanceScore) then
            return Cast(lowestHealthPercentUnit.unit .. "苦修")
        end

        -- 如果坦克玩家的血量，低于坦克苦修阈值，则给坦克苦修。
        if tankUnit and (tankUnit.healthPercent < TankPenanceScore) then
            return Cast(tankUnit.unit .. "苦修")
        end

        -- 至少也要释放进攻苦修
        if enemyTarget then
            return Cast(enemyTarget .. "苦修")
        end

    end

    --  圣光涌动给需要治疗的人
    if surgeOfLightCharges > 0 then

        if playerUnit.healthScore < (HealSelfScore + LightningScore) then
            return Cast("player快速治疗")
        end
        if lowestHealthPercentUnit and (lowestHealthPercentUnit.healthScore < (FlashHealScore + LightningScore)) then
            return Cast(lowestHealthPercentUnit.unit .. "快速治疗")
        end

    end

    if (playerUnit.healthScore < HealSelfScore)  and (not isMoving) then
        return Cast("player快速治疗")
    end

    -- 使用恢复保持坦克的救赎
    if tankUnit and (tankUnit.renewsRemaining < 1) then
        return Cast(tankUnit.unit .. "恢复")
    end


    -- 补救赎逻辑，如果有治疗缺口，用恢复
    if #nonAtonementList >= 1 then
        return Cast(nonAtonementList[1].unit .. "恢复")
    end

    if enemyTarget and (UnitPainRemaining(enemyTarget) == 0) then
        return Cast(enemyTarget .. "痛")
    end

    -- 自动灌注
    local PowerInfusionCooldown = CoolDown(10060)
    if PowerInfusionCooldown and (not HasPremonitionOfInsightBuff()) then
        return Cast(PowerInfusionLogic(partyHealthScore) .. "灌注")
    end

    if enemyTarget and CoolDown(34433)
            and (inAoe or aoeComing or IsSpellKnownOrOverridesKnown(123040))
            and (not HasPremonitionOfInsightBuff()) then
        return Cast(enemyTarget .. "暗影魔")
    end

    -- 如果[心灵震爆]可用，则对目标释放。
    if enemyTarget
            and (not isMoving)
            and CoolDown(8092)
            and (not HasPremonitionOfInsightBuff()) then
        return Cast(enemyTarget .. "心灵震爆")
    end

    -- 目标血量小于20，则灭
    if enemyTarget
            and IsSpellKnownOrOverridesKnown(32379)
            and CoolDown(32379)
            and (not HasPremonitionOfInsightBuff())
            and ((UnitHealth(enemyTarget) / UnitHealthMax(enemyTarget)) < 0.20) then
        return Cast(enemyTarget .. "灭")
    end


    -- 只用快疗填充那些需要治疗的
    if ShionVars["UseFlash"] or inAoe then
        if lowestHealthPercentUnit and (lowestHealthPercentUnit.healthPercent < FlashHealScore) then
            return Cast(lowestHealthPercentUnit.unit .. "快速治疗")
        end
    end

    -- 惩击填充

    if (wealAndWoeStack <= 2) and (not isMoving) then
        return Cast(enemyTarget .. "惩击")
    end

    if ShionVars["UseFlash"] and lowestHealthPercentUnit and (lowestHealthPercentUnit.healthPercent < FlashHealScore) then
        return Cast(lowestHealthPercentUnit.unit .. "快速治疗")
    end
    return Idle("无事可做")
end

local function SetAoeTimer(spellId)
    local aoe_info = AoeSpellList[spellId]
    if aoe_info then
        AoeStartTime = GetTime() + aoe_info.start
        AoeEndTime = GetTime() + aoe_info.start + aoe_info.duration
    end
end

-- 这个监听
local rotationEventFrame = CreateFrame("Frame")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_CHANNEL_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_SUCCEEDED")
rotationEventFrame:RegisterEvent("PLAYER_LEAVE_COMBAT")
rotationEventFrame:RegisterEvent("PLAYER_ENTER_COMBAT")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_SENT")
rotationEventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, event, ...)
end)
function rotationEventFrame:UNIT_SPELLCAST_START(event, unitTarget, castGUID, spellID)
    SetAoeTimer(spellID)
    ----checkTargetIsTankOutburstDamage(event, spellID)
    if (spellID == 105509) and (unitTarget == "player") then
        radiance_spell_time = GetTime() + 2
    end
    if (spellID == 194509) and (unitTarget == "player") then
        radiance_spell_time = GetTime() + 2
    end
    return
end

function rotationEventFrame:UNIT_SPELLCAST_CHANNEL_START(event, unitTarget, castGUID, spellID)
    SetAoeTimer(spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_SUCCEEDED(event, unitTarget, castGUID, spellID)
    if (spellID == 105509) and (unitTarget == "player") then
        radiance_spell_time = GetTime() + 10
    end
    if (spellID == 194509) and (unitTarget == "player") then
        radiance_spell_time = GetTime() + 10
    end
    --clearTargetIsTankOutburstDamage(event, spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_SENT(event, unit, target, castGUID, spellID)
    if (spellID == 10060) and (unit == "player") then
        SendChatMessage("已对[" .. target .. "]释放" .. C_Spell.GetSpellLink(10060) .. "，", "PARTY");
    end

    return
end

function rotationEventFrame:PLAYER_STARTED_MOVING()
    return
end

function rotationEventFrame:PLAYER_STOPPED_MOVING()
    return
end
function rotationEventFrame:PLAYER_LEAVE_COMBAT()
    return
end
function rotationEventFrame:PLAYER_ENTER_COMBAT()
    return
end

HighDamageDebuffList["燧火创伤"] = true;  --酒庄
HighDamageDebuffList["灼热之陨"] = true;  --剧场
HighDamageDebuffList["鱼叉"] = true;     --水闸
HighDamageDebuffList["饕餮虚空"] = true;  --鸟巢
HighDamageDebuffList["混沌腐蚀"] = true;  --鸟巢
HighDamageDebuffList["混沌脆弱"] = true;  --鸟巢


AoeSpellList[258622] = { start = 5, duration = 6 };           -- 暴富矿区   地震回荡    5秒 施法时间    艾泽洛克与力量产生共鸣并引发一次地震，对所有玩家造成1768543点自然伤害，并使他们的移动速度降低30%，持续6秒。同时使地怒者获得地震回荡。
AoeSpellList[262347] = { start = 2.5, duration = 8 };         -- 暴富矿区   静电脉冲    2.5秒 施法时间  释放一次电子脉冲，造成2652815点初始自然伤害和每2秒442136点额外自然伤害，持续8秒，并将敌人击退。
AoeSpellList[263628] = { start = 2, duration = 8 };           -- 暴富矿区   充能护盾    2秒 施法时间    用电化盾牌打击主要目标，电流会轰击目标，造成5895145点自然伤害，并使他们的移动速度降低60%，持续8秒。后续攻击会产生闪电链，对最多5个目标造成1473786点自然伤害。
AoeSpellList[269429] = { start = 2, duration = 3 };           -- 暴富矿区   充能射击    2秒 施法时间    向施法者的当前威胁目标发射艾泽里特能量冲击，造成736893点奥术伤害。

AoeSpellList[297128] = { start = 2, duration = 3 };           -- 麦卡贡行动  短路       2秒 施法时间    每0.5秒对所有的玩家造成552670点自然伤害，持续3秒。
AoeSpellList[1215409] = { start = 2.5, duration = 5 };        -- 麦卡贡行动  超级电钻    2.5秒 施法时间   在5秒内钻取地面，每1秒对所有玩家造成4点自然伤害。

AoeSpellList[330716] = { start = 2.5, duration = 8 };         -- 伤逝剧场   灵魂风暴    2.5秒 施法时间   每2秒对所有玩家造成1326408点暗影伤害，持续8秒。
AoeSpellList[1215741] = { start = 4, duration = 3 };         -- 伤逝剧场   强力碾压     4秒 施法时间     能量达到100点时，德茜雅释放一次强力粉碎，对所有玩家造成2358058点自然伤害并降低其移动速度30%，持续10秒。
AoeSpellList[1215850] = { start = 1, duration = 3 };         -- 伤逝剧场   碾地猛击     1秒 施法时间     对所有玩家造成15点物理伤害，并使周围的地面喷发，对冲击点周围4码内的玩家造成30点自然伤害。

AoeSpellList[424431] = { start = 2, duration = 8 };           -- 圣焰隐修院  圣光烁辉    2秒 施法时间     艾蕾娜·安博兰兹引导圣光之怒，每1秒对所有玩家造成589514点神圣伤害，持续8秒。
AoeSpellList[428169] = { start = 4, duration = 1 };           -- 圣焰隐修院   盲目之光   4秒 施法时间     穆普雷释放出耀眼的光芒，对所有玩家造成1473786点神圣伤害。面向穆普雷的玩家额外受到147379点神圣伤害，并被盲目之光迷惑，持续4秒。
--AoeSpellList[446368] = { start = 5, duration = 1 };         -- 圣焰隐修院  献祭葬火    5秒 施法时间     布朗派克摆出一个燃烧的葬火柴堆，具有3层效果并持续30秒。每当玩家接触葬火柴堆，都会消耗一层效果，使玩家受到牺牲烈焰影响，并使葬火堆爆发出神圣能量，对所有玩家造成736893点伤害。
AoeSpellList[448492] = { start = 1, duration = 3 };          -- 圣焰隐修院  雷霆一击    1秒 施法时间     对50码范围内的敌人造成2063301点自然伤害并使其移动速度降低50%，持续6秒。
AoeSpellList[448791] = { start = 2.5, duration = 1 };         -- 圣焰隐修院  神圣鸣罪    2.5秒 施法时间	对50码内的所有玩家造成2063301点神圣伤害。

AoeSpellList[424958] = { start = 2, duration = 3 };           -- 驭雷栖巢   粉碎现实    2秒 施法时间     雷卫戈伦为战锤注入虚空能量，随后跃向一名玩家的位置，对所有玩家造成2210679点暗影伤害。
AoeSpellList[427404] = { start = 2, duration = 5 };           -- 驭雷栖巢   局部风暴    2秒 施法时间     引导风暴，每1秒对周围50码范围内的玩家造成663204点自然伤害，持续5秒。
AoeSpellList[430812] = { start = 1.5, duration = 6 };         -- 驭雷栖巢   诱集暗影    1.5秒 施法时间   施法者将所有玩家拉近，每1秒造成442136点暗影伤害，持续6秒，并在施法结束时对7码范围内的玩家造成4421358点暗影伤害。
AoeSpellList[427404] = { start = 2, duration = 5 };           -- 驭雷栖巢   局部风暴    2秒 施法时间     引导风暴，每1秒对周围50码范围内的玩家造成663204点自然伤害，持续5秒。

AoeSpellList[425394] = { start = 3, duration = 3 };           -- 暗焰裂口   吹灭之息    3秒 施法时间     布雷炙孔召唤强风，对所有玩家造成2947572点自然伤害，并熄灭所有蜡烛。
AoeSpellList[428066] = { start = 3, duration = 3 };           -- 暗焰裂口   压制咆哮    3秒 施法时间     施法者发出霸气的咆哮，对50码内能直接听清的所有玩家造成1768543点伤害，并使50码内能直接听清的所有盟友的伤害和急速提高10。
AoeSpellList[428266] = { start = 3, duration = 4 };           -- 暗焰裂口   永恒黑暗    3秒 施法时间     黑暗之主每1秒释放一股纯粹的暗影波，持续4秒。每股暗影波对所有玩家造成1179029点暗影伤害，并降低烛光的热量。
AoeSpellList[430171] = { start = 2.7, duration = 1 };         -- 暗焰裂口   镇火冲击    2.7秒 施法时间   施法者释放出凶猛的烛焰，对60码内的敌人造成1768543点火焰伤害。

AoeSpellList[435622] = { start = 4.5, duration = 5 };         -- 燧酿酒庄   遮天蔽日！   4.5秒 施法时间   能量达到100点时，戈尔迪·底爵向空中胡乱射击，引爆剩余的所有燧酿炸弹，并且每1秒对所有玩家造成589514点火焰伤害，持续5秒。
AoeSpellList[439365] = { start = 2, duration = 8 };           -- 燧酿酒庄   喷涌佳酿    2秒 施法时间     艾帕喷涌出蜜酒，每2秒对所有玩家造成1179029点火焰伤害，持续8秒。蜜酒液滴向外飞溅，对3码内的敌人造成4421359点火焰伤害。
AoeSpellList[439524] = { start = 1.5, duration = 2 };         -- 燧酿酒庄   振翼之风    1.5秒 施法时间   本克·鸣蜂命令辛迪凶猛地拍动翅膀，在周围召唤一股强风将玩家推离，并且每0.5秒对所有玩家造成589514点自然伤害，持续2秒。
AoeSpellList[442995] = { start = 3, duration = 1 };           -- 燧酿酒庄   蜂拥惊喜    3秒 施法时间     对周围的敌人造成1768543点物理伤害，受影响玩家受到蜂拥惊喜的伤害提高10%，持续30秒。

AoeSpellList[460156] = { start = 1.5, duration = 12 };        -- 水闸行动   快速启动    1.5秒 施法时间   所有暗索无人机都被击败后，老大娘会尝试快速补充枯竭的电池。该程序使其受到的伤害提高200%，并且每1.5秒释放能量脉冲，持续12秒。每一股能量都会对所有玩家造成1061126点自然伤害。
AoeSpellList[465463] = { start = 4, duration = 10 };          -- 水闸行动   涡轮增压    4秒 施法时间     吉泽尔将发电机的能量吸收到电池组中，每1秒获得10点电能，并对所有玩家造成663204点自然伤害，持续10秒。
AoeSpellList[465827] = { start = 2.5, duration = 6 };         -- 水闸行动   扭曲精华    2.5秒 施法时间   施法者扭曲60码内所有玩家的精华，每1秒造成442136点暗影伤害并吸收受到的442136点治疗量，持续6秒。
AoeSpellList[469721] = { start = 3, duration = 6 };           -- 水闸行动   逆流       3秒 施法时间     泡泡向玩家喷射海量唾沫，造成4点冰霜伤害，并且每1秒额外造成2点冰霜伤害，持续6秒。


ExplodeDispelMagicDebuffList[294929] = true;                    -- 烈焰撕咬，麦卡贡行动
ManualDispelMagicDebuffList[429493] = true;                     -- 不稳定的腐蚀，驭雷栖巢尾王驱散
--ManualDispelMagicDebuffList[473690] = true;                     -- 动能胶质炸药， 水闸行动
--ManualDispelMagicDebuffList[473713] = true;                     -- 动能胶质炸药， 水闸行动
HighDamageDebuffList[322795] = true;        -- 伤逝剧场，肉钩
HighDamageDebuffList[424737] = true;        -- 驭雷栖巢，混沌腐蚀
HighDamageDebuffList[446403] = true;        -- 圣焰隐修院，牺牲烈焰
HighDamageDebuffList[447270] = true;        -- 圣焰隐修院，掷矛
HighDamageDebuffList[447272] = true;        -- 圣焰隐修院，掷矛
HighDamageDebuffList[448787] = true;        -- 圣焰隐修院，纯净
HighDamageDebuffList[468631] = true;        -- 水闸行动，鱼叉
HighDamageDebuffList[1214523] = true;       -- 驭雷栖巢，饕餮虚空

MidDamageDebuffList[320069] = true;         -- 致死打击，T only
MidDamageDebuffList[330532] = true;         -- 锯齿箭
MidDamageDebuffList[424414] = true;         -- 贯穿护甲，T only
MidDamageDebuffList[424797] = true;         -- 驭雷栖巢，混沌脆弱，受到混沌腐蚀的伤害提高300%，持续10秒。此效果可叠加。
MidDamageDebuffList[429493] = true;         -- 驭雷栖巢，不稳定的腐蚀
MidDamageDebuffList[473690] = true;         -- 动能胶质炸药
MidDamageDebuffList[1217821] = true;        -- 麦卡贡，灼热巨颚
MidDamageDebuffList[1223803] = true;        -- 剧场，黑暗之井
MidDamageDebuffList[1223804] = true;        -- 剧场，黑暗之井