local RenewsSpellInfo = C_Spell.GetSpellInfo(139)       -- 恢复的spell信息
local PainSpellInfo = C_Spell.GetSpellInfo(589)         -- 暗言术：痛的spell信息
local FortitudeSpellInfo = C_Spell.GetSpellInfo(21562)  -- 真言术：韧的spell信息

-- 技能清单
-- Cast("player盾")
-- Cast("party1盾")
-- Cast("party2盾")
-- Cast("party3盾")
-- Cast("party4盾")
-- Cast("target苦修")
-- Cast("player苦修")
-- Cast("party1苦修")
-- Cast("party2苦修")
-- Cast("party3苦修")
-- Cast("party4苦修")
-- Cast("party1target苦修")
-- Cast("party2target苦修")
-- Cast("party3target苦修")
-- Cast("party4target苦修")
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
-- Cast("party1target灭")
-- Cast("party2target灭")
-- Cast("party3target灭")
-- Cast("party4target灭")
-- Cast("target心灵震爆")
-- Cast("party1target心灵震爆")
-- Cast("party2target心灵震爆")
-- Cast("party3target心灵震爆")
-- Cast("party4target心灵震爆")
-- Cast("target暗影魔")
-- Cast("party1target暗影魔")
-- Cast("party2target暗影魔")
-- Cast("party3target暗影魔")
-- Cast("party4target暗影魔")
-- Cast("target痛")
-- Cast("party1target痛")
-- Cast("party2target痛")
-- Cast("party3target痛")
-- Cast("party4target痛")
-- Cast("player纯净术")
-- Cast("party1纯净术")
-- Cast("party2纯净术")
-- Cast("party3纯净术")
-- Cast("party4纯净术")
-- Cast("mouseover纯净术")

-- 术语清单
-- 洞察预兆 = PremonitionOfInsight
-- 虔诚预兆 = PremonitionOfPiety
-- 慰藉预兆 = PremonitionOfSolace
-- 远见预兆 = PremonitionOfClairvoyance
-- 预兆 = Premonition
-- 圣光涌动 = SurgeOfLight
-- 伤害 = Damage
-- 减益效果 = Debuff
-- 增益效果 = Buff
-- 效果 = Aura
-- 职业：戒律牧 = Discipline
-- 技能：真言术：盾 = Shield
-- 技能：恢复 = Renews
-- 被动：救赎 = Atonement
-- 技能：苦修 = Penance
-- 技能：真言术：耀 = Radiance
-- 技能：暗言术：痛 = Pain
-- 技能：快速治疗 = FlashHeal
-- 技能：真言术：韧 = Fortitude
-- 技能：纯净术 = Purify
-- 技能：强力纯净术 = ImprovedPurify
-- 魔法效果 = Magic
-- 疾病效果 = Disease
-- 牧师  = Priest


-- 字典定义
local spell_dict = {}   -- 一个临时表
-- 秒驱散的魔法减益列表
local InstantDispelMagicDebuffList = {};  -- 秒驱
local ManualDispelMagicDebuffList = {};  -- 手动驱散 (不驱散)
local ExplodeDispelMagicDebuffList = {}; -- 会爆炸的魔法减益列表
-- 减益效果列表
local HighDamageDebuffList = {};
local MidDamageDebuffList = {};
-- 怪物打断玩家的技能列表
local EnemyInterruptsSpellList = {};
local EnemyInterruptsTime = GetTime();
-- 需要预兆覆盖的技能列表
local requiredPremonitionTimer = GetTime()
local requiredPremonitionList = {};
-- Boss的AOE技能列表
local BossAOESpellList = {};
local AOESpellList = {};
local AoeTimer = GetTime()
-- 耀事件
local radianceSpellTime = GetTime()

local TANKScoreOffset = 0.05;
local HEALERScoreOffset = -0.03;
local HUNTERScoreOffset = -0.01;
local DRUIDScoreOffset = -0.01;
local DEATHKNIGHTScoreOffset = 0.03;
local DEMONHUNTERScoreOffset = 0.03;

--[[
    计算单位健康分数
    参数：unitName - 单位标识
    返回：健康分数(0-1之间)
]]
local function calculateUnitHealthScore(unitName)
    local maxHealth = UnitHealthMax(unitName)
    local currentHealth = UnitHealth(unitName)
    local totalHealAbsorbs = UnitGetTotalHealAbsorbs(unitName) -- 治疗吸收盾
    local healthScoreBase = (currentHealth - totalHealAbsorbs) / maxHealth
    local healthScoreOffset = 0

    -- 根据职责微调分数
    local role = UnitGroupRolesAssigned(unitName)
    local className, classFilename, classId = UnitClass(unitName)
    if role == "TANK" then
        healthScoreOffset = healthScoreOffset + TANKScoreOffset
    end

    if role == "HEALER" then
        healthScoreOffset = healthScoreOffset + HEALERScoreOffset
    end

    if classFilename == "DEATHKNIGHT" then
        healthScoreOffset = healthScoreOffset + DEATHKNIGHTScoreOffset
    end

    if classFilename == "DEMONHUNTER" then
        healthScoreOffset = healthScoreOffset + DEMONHUNTERScoreOffset
    end

    if classFilename == "HUNTER" then
        healthScoreOffset = healthScoreOffset + HUNTERScoreOffset
    end
    if classFilename == "DRUID" then
        healthScoreOffset = healthScoreOffset + DRUIDScoreOffset
    end

    return healthScoreBase + healthScoreOffset, healthScoreBase
end


--[[
    获取单位盾剩余时间
    参数：unitName - 单位标识
    返回：剩余时间(秒)
]]
local ShieldSpellInfo = C_Spell.GetSpellInfo(17)        -- 真言术：盾的spell信息
local function UnitShieldRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, ShieldSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end


--[[
    获取单位救赎剩余时间
    参数：unitName - 单位标识
    返回：剩余时间(秒)
]]
local AtonementSpellInfo = C_Spell.GetSpellInfo(194384) -- 救赎的spell信息
local function UnitAtonementRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, AtonementSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end


--[[
    检查玩家是否正在施法
    返回：true/false
]]
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


--[[
    获取单位恢复剩余时间
    参数：unitName - 单位标识
    返回：剩余时间(秒)
]]
local function UnitRenewsRemaining(unitName)

    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, RenewsSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end

--[[
    检查玩家的buff
    返回：
     - 高危buff数量
     - 中危buff数量
     - 驱散状态
        3 - 需要秒驱的减益，对应字典 InstantDispelMagicDebuffList
        2 - 会爆炸的减益，对应字典 ExplodeDispelMagicDebuffList
        1 - 可驱散的减益
        0 - 没有可驱散减益
       -1 - 不能驱散的减益，对应字典 ManualDispelMagicDebuffList
]]
local function calculateUnitAuras(unitName)
    local numHighRiskAuras = 0
    local numMidRiskAuras = 0
    local dispelState = 0
    local ImprovedPurify = IsPlayerSpell(390632)
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unitName, i, "HARMFUL")
        if not debuffData then
            break
        end
        if HighDamageDebuffList[debuffData.spellId] or HighDamageDebuffList[debuffData.name] then
            numHighRiskAuras = numHighRiskAuras + 1
        elseif MidDamageDebuffList[debuffData.spellId] or MidDamageDebuffList[debuffData.name] then
            numMidRiskAuras = numMidRiskAuras + 1
        end
        if (debuffData.dispelName == "Magic") or (debuffData.dispelName == "Disease" and ImprovedPurify) then
            if InstantDispelMagicDebuffList[debuffData.spellId] or InstantDispelMagicDebuffList[debuffData.name] then
                dispelState = 3
            elseif ManualDispelMagicDebuffList[debuffData.spellId] or ManualDispelMagicDebuffList[debuffData.name] then
                dispelState = -1
            elseif ExplodeDispelMagicDebuffList[debuffData.spellId] or ExplodeDispelMagicDebuffList[debuffData.name] then
                dispelState = 2
            end
            dispelState = 1
        end
    end
    return numHighRiskAuras, numMidRiskAuras, dispelState
end


--[[
    获取耀的充能数
    返回：充能数
]]
local function getRadianceCharges()
    if not IsSpellKnownOrOverridesKnown(194509) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(194509)
    return chargeInfo.currentCharges
end


--[[
    检查玩家是否有[分秒必争]buff
    返回：true/false
]]
local function checkWasteNoTimeBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(440683)
    if aura then
        return true
    end
end


--[[
    检查玩家[祸福相倚]的层数
    返回：num
]]
local function getWealAndWoeStack()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(390787)
    if aura then
        return aura.applications
    end
    return 0
end


--[[
    获取洞察预兆的可用层数
    返回：可用层数
    技能效果：你接下来施放的3个法术的冷却时间缩短7秒。
]]
local function getPremonitionOfInsightCharges()
    if not IsSpellKnownOrOverridesKnown(428933) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428933)
    return chargeInfo.currentCharges
end


--[[
    获取虔诚预兆的可用层数
    返回：可用层数
    技能效果：你造成的治疗效果提高20%，并将对玩家造成的过量治疗的70%重新分配给附近最多4个盟友，持续15秒。
]]
local function getPremonitionOfPietyCharges()
    if not IsSpellKnownOrOverridesKnown(428930) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428930)
    return chargeInfo.currentCharges
end


--[[
    获取慰藉预兆的可用层数
    返回：可用层数
    技能效果：你的下一个单体治疗法术将为目标提供一个护盾，吸收0点伤害，并使其受到的伤害降低15%，持续15秒。
]]
local function getPremonitionOfSolaceCharges()
    if not IsSpellKnownOrOverridesKnown(428934) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428934)
    return chargeInfo.currentCharges
end


--[[
    获取远见预兆的可用层数
    返回：可用层数
    技能效果：获得效果为100%的洞察预兆、虔诚预兆和慰藉预兆。
]]
local function getPremonitionOfClairvoyanceCharges()
    if not IsSpellKnownOrOverridesKnown(440725) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(440725)
    return chargeInfo.currentCharges
end


--[[
    获取总预兆层数
    返回：总层数
    因为总有一个预兆可用。
]]
local function getPremonitionCharges()
    local totalCharges = getPremonitionOfInsightCharges() + getPremonitionOfPietyCharges() + getPremonitionOfSolaceCharges() + getPremonitionOfClairvoyanceCharges()
    return totalCharges
end


--[[
    检测盾的冷却
]]
local function getShieldCoolDown()
    local spellCooldownInfo = C_Spell.GetSpellCooldown(17)
    if spellCooldownInfo.duration == 0 then
        return 0
    else
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end

--[[
    检测苦修的冷却
]]
local function getPenanceCooldown()
    local spellCooldownInfo = C_Spell.GetSpellCooldown(47540)
    if spellCooldownInfo.duration == 0 then
        return 0
    else
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end


--[[
    自动选择敌人目标
    优先选择焦点目标，其次当前目标
    返回：目标单位标识或nil
]]
local function AutoEnemyTarget(tankUnit)
    if tankUnit ~= nil then
        if UnitExists(tankUnit .. "target") and UnitCanAttack("player", tankUnit .. "target") and UnitAffectingCombat(tankUnit .. "target") then
            return tankUnit .. "target"
        end
    end
    if UnitExists("target") and UnitCanAttack("player", "target") and UnitAffectingCombat("target") then
        return "target"
    end
    if UnitExists("party1target") and UnitCanAttack("player", "party1target") and UnitAffectingCombat("party1target") then
        return "party1target"
    end
    if UnitExists("party2target") and UnitCanAttack("player", "party2target") and UnitAffectingCombat("party2target") then
        return "party2target"
    end
    if UnitExists("party3target") and UnitCanAttack("player", "party3target") and UnitAffectingCombat("party3target") then
        return "party3target"
    end
    if UnitExists("party4target") and UnitCanAttack("player", "party4target") and UnitAffectingCombat("party4target") then
        return "party4target"
    end
    return nil
end

--[[
    获取公共冷却
]]
local function getGcdRemaining()
    local spellCooldownInfo = C_Spell.GetSpellCooldown(61304)
    if spellCooldownInfo.duration == 0 then
        return 0
    else
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end


--[[
    获取圣光涌动层数
    返回：层数
    技能效果：快速治疗瞬发
]]
local function getSurgeOfLightCharges()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(114255)
    if aura then
        return aura.applications
    end
    return 0
end


--[[
    获取单位痛剩余时间
    参数：unitToken - 单位标识
    返回：剩余时间(秒)
]]
local function UnitPainRemaining(unitToken)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitToken, PainSpellInfo.name, "PLAYER|HARMFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end

local function checkIsAoeComing()
    if requiredPremonitionTimer > GetTime() then
        return true
    end
    if AoeTimer > GetTime() then
        return true
    end
    return false
end

local function checkIsEnemyInterrupt()
    if EnemyInterruptsTime > GetTime() then
        return true
    end
end

local function main_rotation()
    -- 基础参数初始化 --

    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()

    -- 职业和专精检查 --
    if not (classFilename == "PRIEST" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    --
    local isPlayerMoving = GetUnitSpeed("player") > 0                 -- [玩家]是否移动中
    local isPlayerMounted = IsMounted("player")                       -- [玩家]是否坐骑中
    local isPlayerInVehicle = UnitInVehicle("player")                 -- [玩家]是否载具中
    local isPlayerUseChat = ChatFrame1EditBox:IsVisible()            -- [玩家]是否使用聊天框
    local isPlayerDead = UnitIsDeadOrGhost("player")                  -- [玩家]是否死亡
    local isPlayerCasting = checkPlayerIsCasting()                    -- [玩家]是否正在施法

    if isPlayerCasting then
        return Idle("正在施法")
    end

    if isPlayerMounted then
        return Idle("坐骑中")
    end

    if isPlayerInVehicle then
        return Idle("载具中")
    end

    if isPlayerUseChat then
        return Idle("使用聊天框")
    end

    if isPlayerDead then
        return Idle("死亡")
    end

    if not UnitAffectingCombat("player") then
        return Idle("not 战斗中")
    end

    local defaultTarget = "player"
    local tankUnit = nil                                              -- 坦克
    local numGroupMembers = GetNumGroupMembers()                      -- 获取小队的总人数
    local partyMembers = {}
    local lowestHealthUnit = defaultTarget                              -- 最低健康分数目标
    local lowestHealthScore = 120                                     -- 最低健康分数
    local lowestHealthBase = 100                                      -- 最低健康分数的基础值
    local nonAtonementLowestHealthUnit = nil                          -- [无救赎的]最低健康分数目标
    local nonAtonementLowestHealthScore = 120                         -- [无救赎的]最低健康分数
    local nonAtonementLowestHealthBase = 120                          -- [无救赎的]的健康分数基础
    local nonShieldLowestHealthUnit = nil                             -- [无盾的]最低健康分数目标
    local nonShieldLowestHealthScore = 120                            -- [无盾的]最低健康分数
    local tankHaveShield = false                                      -- 坦克是否有盾
    local tankHaveAtonement = false                                   -- 坦克是否有救赎
    local AtonementUnitsCount = 0                                     -- 救赎覆盖数
    local nonAtonementUnitsCount = 0                                  -- 无救赎覆数
    local HighDamageDebuffSum = 0                                     -- [高伤害减益]总数
    local MidDamageDebuffSum = 0                                      -- [中伤害减益]总数
    local HighDamageDebuffUnitSum = 0                                 -- [高伤害减益]目标数
    local MidDamageDebuffUnitsSum = 0                                 -- [中伤害减益]目标数
    local HighDamageDebuffLowestHealthUnit = nil                      -- [高伤害减益]最低健康分数目标
    local HighDamageDebuffLowestHealthScore = 120                     -- [高伤害减益]最低健康分数
    local MidDamageDebuffLowestHealthUnit = nil                       -- [中伤害减益]最低健康分数目标
    local MidDamageDebuffLowestHealthScore = 120                      -- [中伤害减益]最低健康分数
    local HaveDebuffAndWithoutRenewUnit = nil                         -- 有[减益]无[恢复]最低健康分数的目标
    local HaveDebuffAndWithoutRenewScore = 120                        -- 有[减益]无[恢复]最低健康分数

    table.insert(partyMembers, "player")
    if numGroupMembers > 0 then
        for i = 1, numGroupMembers do
            local unitName = "party" .. i
            if UnitExists(unitName)                                   -- 目标必须存在
                    and not (UnitIsDeadOrGhost(unitName))             -- 目标必须存活
                    and C_Spell.IsSpellInRange(139, unitName) then
                -- 目标必须在范围内
                table.insert(partyMembers, unitName)
            end
        end
    end

    local currentHealthScore = 0
    local currentHealthBase = 0
    local currentAtonementRemaining = 0
    local currentRenewsRemaining = 0
    local currentShieldRemaining = 0
    local currentHighDamageDebuffNum = 0
    local currentMidDamageDebuffNum = 0
    local currentDispelState = 0
    local currentIsTank = ""
    for _, currentUnit in ipairs(partyMembers) do
        currentHealthScore, currentHealthBase = calculateUnitHealthScore(currentUnit)
        currentAtonementRemaining = UnitAtonementRemaining(currentUnit)
        currentShieldRemaining = UnitShieldRemaining(currentUnit)
        currentRenewsRemaining = UnitRenewsRemaining(currentUnit)
        currentIsTank = UnitGroupRolesAssigned(unit) == "TANK"
        if currentIsTank then
            tankUnit = currentUnit
        end
        if currentHealthScore < lowestHealthScore then
            lowestHealthUnit = currentUnit
            lowestHealthScore = currentHealthScore
            lowestHealthBase = currentHealthBase
        end
        -- 救赎
        if (currentAtonementRemaining > 2) then
            AtonementUnitsCount = AtonementUnitsCount + 1
            if currentIsTank then
                tankHaveAtonement = true
            end
        else
            if (currentHealthScore < nonAtonementLowestHealthScore) and (currentHealthBase < 0.99) then
                nonAtonementLowestHealthUnit = currentUnit
                nonAtonementLowestHealthScore = currentHealthScore
                nonAtonementLowestHealthBase = currentHealthBase
                nonAtonementUnitsCount = nonAtonementUnitsCount + 1
            end
        end
        -- 盾
        if (currentShieldRemaining < 1) and (not currentIsTank) then
            if currentHealthScore < nonShieldLowestHealthScore then
                nonShieldLowestHealthUnit = currentUnit
                nonShieldLowestHealthScore = currentHealthScore
            end
        elseif (currentShieldRemaining > 2) and currentIsTank then
            tankHaveShield = true
        end
        -- 增益计算
        currentHighDamageDebuffNum, currentMidDamageDebuffNum, currentDispelState = calculateUnitAuras(currentUnit)
        HighDamageDebuffSum = HighDamageDebuffSum + currentHighDamageDebuffNum         -- [高伤害减益]总数
        MidDamageDebuffSum = MidDamageDebuffSum + currentMidDamageDebuffNum            -- [中伤害减益]总数
        -- 增益计算
        if currentHighDamageDebuffNum > 0 then
            HighDamageDebuffUnitSum = HighDamageDebuffUnitSum + 1                     -- [高伤害减益]目标数
            if currentHealthScore < HighDamageDebuffLowestHealthScore then
                HighDamageDebuffLowestHealthUnit = currentUnit
                HighDamageDebuffLowestHealthScore = currentHealthScore
            end
        end
        -- 增益计算
        if currentMidDamageDebuffNum > 0 then
            MidDamageDebuffUnitsSum = MidDamageDebuffUnitsSum + 1                     -- [中伤害减益]目标数
            if currentHealthScore < MidDamageDebuffLowestHealthScore then
                MidDamageDebuffLowestHealthUnit = currentUnit
                MidDamageDebuffLowestHealthScore = currentHealthScore
            end
        end

        -- 恢复和增益
        if ((currentHighDamageDebuffNum > 0) or (currentMidDamageDebuffNum > 0)) and (currentRenewsRemaining < 1) then
            if currentHealthScore < HaveDebuffAndWithoutRenewScore then
                HaveDebuffAndWithoutRenewUnit = currentUnit
                HaveDebuffAndWithoutRenewScore = currentHealthScore
            end
        end


    end

    local isAoeComing = checkIsAoeComing()                            -- 是否即将AOE
    local isEnemyInterrupt = checkIsEnemyInterrupt()                  -- 是否敌人打断
    local enemyTarget = AutoEnemyTarget(tankUnit)                      -- 自动选择敌人目标
    -- 技能状态追踪                                                     --
    local radianceCharges = getRadianceCharges()                      -- [真言术：耀]的充能
    local hasWasteNoTimeBuff = checkWasteNoTimeBuff()                 -- [分秒必争]的buff
    local premonitionCharges = getPremonitionCharges()                -- [预兆]充能
    local wealAndWoeStack = getWealAndWoeStack()                      -- [祸福相倚]层数
    local gcd = getGcdRemaining()                                     -- [GCD]剩余时间
    local shieldCooldown = getShieldCoolDown()                        -- [真言术：盾]冷却
    local isShieldAvailable = shieldCooldown <= gcd                   -- [真言术：盾]是否可用
    local penanceCooldown = getPenanceCooldown()                      -- [苦修]冷却
    local isPenanceAvailable = penanceCooldown <= gcd                 -- [苦修]是否可用
    local surgeOfLightCharges = getSurgeOfLightCharges()              -- [圣光涌动]层数
    -- 健康分数最低的玩家
    -- 最低的健康分数
    -- 救赎覆盖数

    -- 新版本逻辑

    -- 优先判断是否群疗



    -- 福音的逻辑
    --  if has救赎Count >= 4 and 福音Count >= 3 then
    --  elseif has救赎Count >= 2 and 福音Count >= 2 then



    -- 耀的释放逻辑
    --  - 耀可用
    --    - 如果存在[分秒必争],[最低健康分数<90]，释放耀。
    --    - 如果Aoe即将到到来，且未全铺救赎
    --      - 如果预兆有2层，则先释放预兆
    --      - 否则释放耀
    --    - 如果不在移动，且有2个人缺救赎。则释放耀
    if (radianceCharges > 0) and (radianceSpellTime < GetTime()) and (not isEnemyInterrupt)  then
        if hasWasteNoTimeBuff and (lowestHealthScore < 90) then
            return Cast("耀")
        end
        if isAoeComing and (AtonementUnitsCount < numGroupMembers) then
            if premonitionCharges > 1 then
                return Cast("预兆")
            end
            return Cast("耀")
        end
        if (not isPlayerMoving) and (nonAtonementUnitsCount >= 2) then
            return Cast("耀")
        end
    end

    -- isAoeComing
    --  - 如果盾可用 祸福相倚Stacks >= 4，盾自己
    if isAoeComing then
        if isShieldAvailable and (wealAndWoeStack >= 4) then
            return Cast("player盾")
        end
    end

    --if enemyTarget then
    --    if not UnitIsUnit("focus", enemyTarget) then
    --        return Cast(enemyTarget .. "焦点")
    --    end
    --end
    -- 苦修逻辑
    -- 大前提是可用
    -- 如果祸福相倚Stacks < 4，苦修
    if isPenanceAvailable and (wealAndWoeStack < 4) and (not isEnemyInterrupt) then
        if enemyTarget then
            return Cast(enemyTarget .. "苦修")
        end
        return Cast(lowestHealthUnit .. "苦修")
    end

    -- 盾逻辑
    -- 如果 祸福相倚Stacks >= 4
    --   - 如果最低生命值的玩家，分数小于40，则盾他。
    --   - 如果有debuff的玩家,则盾他。
    --   - 如果有生命值低于90%的玩家，没救赎，盾他。
    --   - 如果生命值低于95，且没盾，则盾他。
    --   - 盾没盾的非坦克玩家
    if isShieldAvailable and (wealAndWoeStack >= 4) then
        if (lowestHealthScore < 40) then
            return Cast(lowestHealthUnit .. "盾")
        end
        if (HighDamageDebuffSum > 0) then
            return Cast(HighDamageDebuffLowestHealthUnit .. "盾")
        end
        if (MidDamageDebuffSum > 0) then
            return Cast(MidDamageDebuffLowestHealthUnit .. "盾")
        end
        if (nonAtonementLowestHealthScore < 90) then
            return Cast(nonAtonementLowestHealthUnit .. "盾")
        end
        if (lowestHealthScore < 95) then
            return Cast(lowestHealthUnit .. "盾")
        end
        return Cast(nonShieldLowestHealthUnit .. "盾")
    end


    -- 快疗逻辑
    -- 如果has圣光涌动
    --   - 如果有debuff的玩家，快疗给他
    --   - 如果有没救赎的最低生命值的玩家，快疗给他
    --   - 给生命值低于90%的玩家

    if (surgeOfLightCharges > 0) then
        if (HighDamageDebuffSum > 0) then
            return Cast(HighDamageDebuffLowestHealthUnit .. "快速治疗")
        end
        if (MidDamageDebuffSum > 0) then
            return Cast(MidDamageDebuffLowestHealthUnit .. "快速治疗")
        end
        if nonAtonementLowestHealthUnit then
            return Cast(nonAtonementLowestHealthUnit .. "快速治疗")
        end
        if (lowestHealthScore < 90) then
            return Cast(lowestHealthUnit .. "快速治疗")
        end
    end

    -- 恢复逻辑
    --   - 如果没救赎，给恢复
    --   - 如果玩家存在debuff，给恢复
    if nonAtonementLowestHealthUnit then
        --print(nonAtonementLowestHealthUnit .. "恢复")
        --print(nonAtonementLowestHealthBase)
        return Cast(nonAtonementLowestHealthUnit .. "恢复")
    end

    if HaveDebuffAndWithoutRenewUnit then
        return Cast(HaveDebuffAndWithoutRenewUnit .. "恢复")
    end


    -- 开始战斗逻辑

    if enemyTarget and (UnitPainRemaining("focus") == 0) then
        return Cast(enemyTarget .. "痛")
    end

    if enemyTarget and CoolDown(34433) then
        return Cast(enemyTarget .. "暗影魔")
    end

    if enemyTarget and CoolDown(8092) and (not isPlayerMoving) then
        return Cast(enemyTarget .. "心灵震爆")
    end

    if enemyTarget
            and IsSpellKnownOrOverridesKnown(32379)
            and CoolDown(32379)
            and ((UnitHealth(enemyTarget) / UnitHealthMax(enemyTarget)) < 0.20) then
        return Cast(enemyTarget .. "灭")
    end

    return Idle("无事可做")
end

local function handelEventSpellID(spellId)
    if requiredPremonitionList[spellId] then
        requiredPremonitionTimer = GetTime() + 4
        return
    elseif BossAOESpellList[spellId] then
        AoeTimer = GetTime() + 4
        return
    elseif AOESpellList[spellId] then
        AoeTimer = GetTime() + 4
        return
    elseif EnemyInterruptsSpellList[spellId] then
        EnemyInterruptsTime = GetTime() + 3
        return
    end

    if ShionVars["GlobalDEBUG"] then
        local spellInfo = C_Spell.GetSpellInfo(spellId)
        local name = spellInfo.name
        if requiredPremonitionList[name] then
            requiredPremonitionTimer = GetTime() + 4
            spell_dict[spellId] = name;
            return
        elseif BossAOESpellList[name] then
            AoeTimer = GetTime() + 4
            spell_dict[spellId] = name;
            return
        elseif AOESpellList[name] then
            AoeTimer = GetTime() + 4
            spell_dict[spellId] = name;
            return
        elseif EnemyInterruptsSpellList[name] then
            EnemyInterruptsTime = GetTime() + 3
            spell_dict[spellId] = name;
            return
        end
    end
end



-- 这个监听
local rotationEventFrame = CreateFrame("Frame")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_CHANNEL_START")
rotationEventFrame:RegisterEvent("UNIT_SPELLCAST_SUCCEEDED")
rotationEventFrame:RegisterEvent("PLAYER_LEAVE_COMBAT")
rotationEventFrame:RegisterEvent("PLAYER_ENTER_COMBAT")
rotationEventFrame:RegisterEvent("ADDON_LOADED"); -- Fired when saved variables are loaded
rotationEventFrame:RegisterEvent("PLAYER_LOGOUT"); -- Fired when about to log out
rotationEventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, event, ...)
end)

function rotationEventFrame:ADDON_LOADED(event, addOnName, containsBindings)
    if addOnName == "Shion" then
        if ShionSave == nil then
            ShionSave = {};
        end
    end
    return
end
function rotationEventFrame:PLAYER_LOGOUT(event)
    ShionSave["spell_dict"] = spell_dict;
end

function rotationEventFrame:UNIT_SPELLCAST_START(event, unitTarget, castGUID, spellID)
    handelEventSpellID(spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_CHANNEL_START(event, unitTarget, castGUID, spellID)
    handelEventSpellID(spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_SUCCEEDED(event, unitTarget, castGUID, spellID)
    if (spellID == 105509) and (unitTarget == "player") then
        radianceSpellTime = GetTime() + 10
        print(radianceSpellTime)
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


BossAOESpellList["震地"] = true;          --车间
BossAOESpellList["静电脉冲"] = true;       --妈妈矿区
BossAOESpellList["地震回荡"] = true;       --妈妈矿区
BossAOESpellList["强力碾压"] = true;       --剧场
BossAOESpellList["狂野闪电"] = true;       --鸟巢
BossAOESpellList["粉碎现实"] = true;       --鸟巢
BossAOESpellList["喷涌佳酿"] = true;       --酒庄
BossAOESpellList["振翼之风"] = true;       --酒庄
BossAOESpellList["遮天蔽日！"] = true;       --酒庄
BossAOESpellList["献祭葬火"] = true;       --修道院
BossAOESpellList["盲目之光"] = true;       --修道院
BossAOESpellList["吹灭之息"] = true;       --裂口
BossAOESpellList["永恒黑暗"] = true;       --裂口
BossAOESpellList["快速启动"] = true;       --水闸
BossAOESpellList["泥石流"] = true;         --水闸
BossAOESpellList["涡轮增压"] = true;       --水闸


AOESpellList["超级电钻"] = true;    --车间
AOESpellList["短路"] = true;    --车间
AOESpellList["迅速萃取"] = true;    --老妈矿区
AOESpellList["充能射击"] = true;    --老妈矿区
AOESpellList["碾地猛击"] = true;    --剧场
AOESpellList["灵魂风暴"] = true;    --剧场
AOESpellList["局部风暴"] = true;    --鸟巢
AOESpellList["诱集暗影"] = true;    --鸟巢
AOESpellList["饕餮虚空"] = true;    --鸟巢
AOESpellList["蜂拥惊喜"] = true;    --酒庄
AOESpellList["雷霆一击"] = true;    --修道院
AOESpellList["热浪"] = true;    --修道院
AOESpellList["圣光烁辉"] = true;    --修道院
AOESpellList["神圣鸣罪"] = true;    --修道院
AOESpellList["压制咆哮"] = true;    --暗焰裂口
AOESpellList["镇火冲击"] = true;    --暗焰裂口
AOESpellList["扭曲精华"] = true;    --水闸
AOESpellList["逆流"] = true;    --水闸

EnemyInterruptsSpellList["瓦解怒吼"] = true;
EnemyInterruptsSpellList["打断怒吼"] = true;
EnemyInterruptsSpellList["雷音贯耳"] = true;

ManualDispelMagicDebuffList["动能胶质炸药"] = true;
ManualDispelMagicDebuffList["不稳定的腐蚀"] = true;
ManualDispelMagicDebuffList["震地回响"] = true;
ManualDispelMagicDebuffList["烈焰撕咬"] = true;
ManualDispelMagicDebuffList["饕餮虚空"] = true;
ManualDispelMagicDebuffList["虚弱灵魂"] = true;
ManualDispelMagicDebuffList["虚弱光环"] = true;
ManualDispelMagicDebuffList["最后一击"] = true;
ManualDispelMagicDebuffList["灵魂枯萎"] = true;
ManualDispelMagicDebuffList["巨口蛙毒"] = true;
ManualDispelMagicDebuffList["培植毒药"] = true;