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
-- 秒驱散的魔法减益列表
local InstantDispelMagicDebuffList = {};
-- 手动驱散魔法减益列表
local ManualDispelMagicDebuffList = {};
-- 会爆炸的魔法减益列表
local ExplodeDispelMagicDebuffList = {};
-- 高伤害减益效果列表
local HighDamageDebuffList = {};
-- 高伤害减益健康分数偏移量
local HighDamageDebuffHealthScoreOffset = -0.2;
-- 中等伤害减益效果列表
local MidDamageDebuffList = {};
-- 中等伤害减益健康分数偏移量
local MidDamageDebuffHealthScoreOffset = -0.1;
-- 怪物打断玩家的技能列表
local EnemyInterruptsCastsList = {};
-- 需要预兆覆盖的技能列表
local requiredPremonitionTimer = GetTime()
local requiredPremonitionList = {};

-- 圣光涌动触发的快疗血线
local Flash_Heal_on_Surge_of_Light = 0.95
-- 爆炸debuff驱散血线
local Explode_Debuff_Remove_Hp_Score = 0.9
local TANKScoreOffset = 0.05;
local HEALERScoreOffset = -0.02;
local HUNTERScoreOffset = -0.01;
local DRUIDScoreOffset = -0.01;
local DEATHKNIGHTScoreOffset = 0.01;
local DEMONHUNTERScoreOffset = 0.01;


-- 配置

ShionVars["ShieldTank"] = false;
local function ToggleShieldTank()
    ShionVars["ShieldTank"] = not ShionVars["ShieldTank"];
    ShionCB["ShieldTank"]:SetChecked(ShionVars["ShieldTank"]);
end
CreateLine("给T套盾", "ShieldTank", ToggleShieldTank)

ShionVars["ActionInNoCombat"] = false;
local function ToggleActionInNoCombat()
    ShionVars["ActionInNoCombat"] = not ShionVars["ActionInNoCombat"];
    ShionCB["ActionInNoCombat"]:SetChecked(ShionVars["ActionInNoCombat"]);
end
CreateLine("非战斗治疗", "ActionInNoCombat", ToggleActionInNoCombat)

ShionVars["ClearDebuff"] = true;
local function ToggleClearDebuff()
    ShionVars["ClearDebuff"] = not ShionVars["ClearDebuff"];
    ShionCB["ClearDebuff"]:SetChecked(ShionVars["ClearDebuff"]);
end
CreateLine("驱散", "ClearDebuff", ToggleClearDebuff)

ShionVars["SavaMana"] = false;
local function ToggleSavaMana()
    ShionVars["SavaMana"] = not ShionVars["SavaMana"];
    ShionCB["SavaMana"]:SetChecked(ShionVars["SavaMana"]);
end
CreateLine("节约法力值", "SavaMana", ToggleSavaMana)


ShionVars["MoreFlash"] = false;
local function ToggleMoreFlash()
    ShionVars["MoreFlash"] = not ShionVars["MoreFlash"];
    ShionCB["MoreFlash"]:SetChecked(ShionVars["MoreFlash"]);
end
CreateLine("更多的快速治疗", "MoreFlash", ToggleMoreFlash)


--[[
AOE检测
]]

local function IsAOE()
    return requiredPremonitionTimer > GetTime()
end


--[[
    获取洞察预兆的可用层数
    返回：可用层数
    技能效果：你接下来施放的3个法术的冷却时间缩短7秒。
]]
local function PremonitionOfInsightCharges()
    if not IsSpellKnownOrOverridesKnown(428933) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428933)
    return chargeInfo.currentCharges
end


--[[
    检查玩家是否有洞察预兆buff
    返回：true/false
]]
local function HasPremonitionOfInsightBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(428933)
    if aura then
        return true
    end
end

--[[
    检查玩家是否有[分秒必争]buff
    返回：true/false
]]
local function HasWasteNoTimeBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(440683)
    if aura then
        return true
    end
end

--[[
    获取虔诚预兆的可用层数
    返回：可用层数
    技能效果：你造成的治疗效果提高20%，并将对玩家造成的过量治疗的70%重新分配给附近最多4个盟友，持续15秒。
]]
local function PremonitionOfPietyCharges()
    if not IsSpellKnownOrOverridesKnown(428930) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428930)
    return chargeInfo.currentCharges
end


--[[
    检查玩家是否有虔诚预兆buff
    返回：true/false
]]
local function HasPremonitionOfPietyBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(428930)
    if aura then
        return true
    end
end


--[[
    获取慰藉预兆的可用层数
    返回：可用层数
    技能效果：你的下一个单体治疗法术将为目标提供一个护盾，吸收0点伤害，并使其受到的伤害降低15%，持续15秒。
]]
local function PremonitionOfSolaceCharges()
    if not IsSpellKnownOrOverridesKnown(428934) then
        return 0
    end
    local chargeInfo = C_Spell.GetSpellCharges(428934)
    return chargeInfo.currentCharges
end

--[[
    检查玩家是否有慰藉预兆buff
    返回：true/false
]]
local function HasPremonitionOfSolaceBuff()
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(428934)
    if aura then
        return true
    end
end


--[[
    获取远见预兆的可用层数
    返回：可用层数
    技能效果：获得效果为100%的洞察预兆、虔诚预兆和慰藉预兆。
]]
local function PremonitionOfClairvoyanceCharges()
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
local function TotalPremonitionCharges()
    local totalCharges = PremonitionOfInsightCharges() + PremonitionOfPietyCharges() + PremonitionOfSolaceCharges() + PremonitionOfClairvoyanceCharges()
    return totalCharges
end


--[[
    自动选择敌人目标
    优先选择焦点目标，其次当前目标
    返回：目标单位标识或nil
]]
local function AutoEnemyTarget()
    if UnitExists("focus") and UnitCanAttack("player", "focus") and UnitAffectingCombat("focus") then
        return "focus"
    end
    if UnitExists("target") and UnitCanAttack("player", "target") and UnitAffectingCombat("target") then
        return "target"
    end
    return nil
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
    获取小队成员列表
    返回：包含小队成员单位标识的table
]]
local function getPartyMembers()
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
    return partyMembers
end

--[[
    获取无坦克小队成员列表
    返回：包含小队成员单位标识的table
]]
local function getNonTankPartyMembers()
    local numGroupMembers = GetNumGroupMembers()
    local partyMembers = {}
    local role
    table.insert(partyMembers, "player")
    if numGroupMembers > 0 then
        for i = 1, numGroupMembers do
            local unitName = "party" .. i
            role = UnitGroupRolesAssigned(unitName)
            if UnitExists(unitName) and not (UnitIsDeadOrGhost(unitName)) and C_Spell.IsSpellInRange(139, unitName) and (role ~= "TANK") then
                table.insert(partyMembers, unitName)
            end
        end
    end
    return partyMembers
end

--[[
    获取坦克名称
    参数：partyMembers - 小队成员列表
    返回：坦克单位标识或nil
]]
local function getTankName(partyMembers)
    local role
    for _, unitName in ipairs(partyMembers) do
        role = UnitGroupRolesAssigned(unitName)
        if role == "TANK" then
            return unitName
        end
    end
    return nil
end


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

    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unitName, i, "HARMFUL")
        if not debuffData then
            break
        end
        if HighDamageDebuffList[debuffData.spellId] or HighDamageDebuffList[debuffData.name] then
            healthScoreOffset = healthScoreOffset - 20
        elseif MidDamageDebuffList[debuffData.spellId] or MidDamageDebuffList[debuffData.name] then
            healthScoreOffset = healthScoreOffset - 10
        end
    end

    if ShionVars["SavaMana"] then
        healthScoreOffset = healthScoreOffset + 10
    end

    return healthScoreBase + healthScoreOffset

end


--[[
    计算小队健康分数并排序
    参数：partyMembers - 小队成员列表
    返回：按健康分数排序的小队成员数组
]]
local function calculatePartyHealthScore(partyMembers)
    local members = {}
    for _, unitName in ipairs(partyMembers) do
        members[unitName] = calculateUnitHealthScore(unitName)
    end
    -- 将table转换为可以排序的数组
    local sortedArray = {}
    for name, value in pairs(members) do
        table.insert(sortedArray, { name = name, value = value })
    end

    table.sort(sortedArray, function(a, b)
        return a.value < b.value
    end)

    return sortedArray
end


--[[
    获取单位盾剩余时间
    参数：unitName - 单位标识
    返回：剩余时间(秒)
]]
local function UnitShieldRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, ShieldSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
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
    获取单位救赎剩余时间
    参数：unitName - 单位标识
    返回：剩余时间(秒)
]]
local function UnitAtonementRemaining(unitName)
    local aura = C_UnitAuras.GetAuraDataBySpellName(unitName, AtonementSpellInfo.name, "PLAYER|HELPFUL")
    if aura then
        local remaining = aura.expirationTime - GetTime() - (SpellQueueWindow / 1000)
        return math.max(remaining, 0)
    end
    return 0
end


--[[
    默认盾逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：需要套盾的目标单位标识
    默认逻辑：
        1. 优先给玩家自己。
        2. 如果最低生命值的玩家，分数小于40，则盾他。
        2. 评分从低到高，如果没有盾则返回该单位，但是跳过tanke
        2. 如果都有盾，则返回player
]]
local function DefaultShieldLogic(partyHealthScore)
    if UnitShieldRemaining("player") == 0 then
        return "player"
    end
    for _, item in ipairs(partyHealthScore) do
        if item.value < 0.5 then
            return item.name
        elseif (item.value < 0.90) and (UnitAtonementRemaining(item.name) < 1) then
            return item.name
        elseif (item.value < 0.95) and (UnitShieldRemaining(item.name) < 1) then
            return item.name
        end
    end
    for _, item in ipairs(partyHealthScore) do
        return item.name
    end

    return "player"
end

--[[
    非战斗盾逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：需要套盾的目标单位标识
    默认逻辑：
        1. 优先给玩家自己。
        2. 给没盾的
]]
local function NoCombatShieldLogic(partyHealthScore)
    if UnitShieldRemaining("player") == 0 then
        return "player"
    end
    for _, item in ipairs(partyHealthScore) do
        if (UnitAtonementRemaining(item.name) < 1) then
            return item.name
        end
    end
    return "player"
end


--[[
    默认苦修逻辑
    参数：partyHealthScore - 排序后的小队健康分数
          enemyTarget - 敌人目标
    返回：苦修目标单位标识
    默认逻辑：
        1. 存在救赎的单位，且血量低于90%，则大于2个对敌人进行苦修
        2. 否则对血量最低的目标苦修。
        3. 如果没有低于90%的单位，则对敌人进行苦修。
]]
local function DefaultPenanceLogic(partyHealthScore, enemyTarget)
    local aoe_count = 0 -- 血量低于90%,且有救赎的玩家的数量
    local lowest_target = nil -- 血量最低的玩家
    local lowest_target_value = 0.9 -- 血量最低的玩家的血量分数

    for _, item in ipairs(partyHealthScore) do
        if (item.value < 0.90) and (UnitAtonementRemaining(item.name) > 1) then
            aoe_count = aoe_count + 1
        end
        if item.value < lowest_target_value then
            lowest_target = item.name
            lowest_target_value = item.value
        end
    end
    -- 当3个人缺血时候，苦修敌人
    if aoe_count >= 3 then
        return enemyTarget
    end
    -- 如果lowest_target存在，则返回lowest_target
    if lowest_target then
        return lowest_target
    end
    -- 如果没有lowest_target，则返回enemyTarget
    return enemyTarget
end

--[[
    脱战苦修逻辑
    优先未满血
    其次积分最低
]]
local function NoCombatPenanceLogic(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        if (UnitHealth(item.name) / UnitHealthMax(item.name)) < 0.99 then
            return item.name
        end
    end
    for _, item in ipairs(partyHealthScore) do
        return item.name
    end
    return nil
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
    默认耀逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：是否应该释放耀
    默认逻辑：
      AOE中
        有瞬发buff
        有一个人没有救赎就用
      非AOE中
        有2个人血量低于90且没救赎就用。
]]
local radiance_spell_time = GetTime()
local function DefaultRadianceLogic(partyHealthScore)
    -- 如果近期是放过，则不是放
    if radiance_spell_time > GetTime() then
        return false
    end
    if HasWasteNoTimeBuff() then
        return true
    end
    -- 如果血量低于90%，没有救赎的玩家有2个，则释放。
    local count = 0 -- 血量低于90%,且没有救赎的玩家的数量
    for _, item in ipairs(partyHealthScore) do
        if (item.value < 0.90) and (UnitAtonementRemaining(item.name) < 1) then
            count = count + 1
            if count >= 2 then
                return true
            end
        end
    end

    -- 如果即将到来
    -- 未全部有救赎
    if IsAOE() then
        for _, item in ipairs(partyHealthScore) do
            if (UnitAtonementRemaining(item.name) < 1) then
                return true
            end
        end
    end

    return false
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


--[[
    获取圣光涌动层数
    返回：层数
    技能效果：快速治疗瞬发
]]
local function getSurgeOfLightCharges()
    --local spellInfo = C_Spell.GetSpellInfo(spell_name)
    local aura = C_UnitAuras.GetPlayerAuraBySpellID(114255)
    if aura then
        return aura.applications
    end
    return 0
end


--[[
    默认圣光涌动触发快疗逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：需要快疗的目标单位标识或nil
    默认逻辑：
        1. 评分从低到高，血量低于Flash_Heal_on_Surge_of_Light的单位，切没有救赎的单位，进行快疗。
    快疗治疗量很低，更多是刷新救赎
]]
local function DefaultFlashHealLogic(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        if (UnitHealth(item.name) / UnitHealthMax(item.name)) < Flash_Heal_on_Surge_of_Light then
            if UnitAtonementRemaining(item.name) < 1 then
                return item.name
            end
        end
    end
    return nil
end


--[[
   给没有救赎的人用
]]
local function FlashHealLogic2(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        if (UnitAtonementRemaining(item.name) < 1) then
            return item.name
        end
    end
    return nil
end

--[[
   积分最低的，血不满的单位
]]
local function FlashHealLogic3(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        if (UnitHealth(item.name) / UnitHealthMax(item.name)) < 0.99 then
            return item.name
        end
    end
    return nil
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
    耐力buff逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：是否需要释放耐力buff
]]
local function FortitudeLogic(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        local aura = C_UnitAuras.GetAuraDataBySpellName(item.name, FortitudeSpellInfo.name, "PLAYER|HELPFUL")
        if not aura then
            return true
        end
    end
    return false
end


--[[
    检查单位是否有可驱散减益
    参数：unitName - 单位标识
    返回：
        3 - 需要秒驱的减益，对应字典 InstantDispelMagicDebuffList
        2 - 会爆炸的减益，对应字典 ExplodeDispelMagicDebuffList
        1 - 可驱散的减益
        -1 - 不能驱散的减益，对应字典 ManualDispelMagicDebuffList
        0 - 没有可驱散减益
]]
local function hasDebuff(unitName)
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


--[[
    驱散减益效果逻辑
    参数：
        partyHealthScore - 排序后的小队健康分数数组，包含单位名称和健康分数值(0-1之间)
    返回：
        unitName - 需要驱散的目标单位标识或nil(无需驱散时)
    逻辑说明：
        1. 遍历小队成员，检查是否存在需要处理的减益效果：
            - 优先级3(最高): InstantDispelMagicDebuffList中的减益(需秒驱)
            - 优先级2: ExplodeDispelMagicDebuffList中的减益(会爆炸的减益)，且全队血量安全时(>90%)
            - 优先级1: 普通可驱散减益，且全队血量安全时(>50%)
        2. 一旦找到符合条件的单位立即返回，确保高优先级减益优先处理
        3. 全队血量评估使用party_min_health_score判断整体安全状况
]]--
local function DebuffRemoveLogic(partyHealthScore)
    local debuff
    local party_min_health_score = 1
    for _, item in ipairs(partyHealthScore) do
        if item.value < party_min_health_score then
            party_min_health_score = item.value
        end
    end
    for _, item in ipairs(partyHealthScore) do
        debuff = hasDebuff(item.name)
        if debuff == 3 then
            return item.name
        elseif (debuff == 2) and (party_min_health_score > Explode_Debuff_Remove_Hp_Score) then
            return item.name
        elseif (debuff == 1) and (party_min_health_score > 0.50) then
            return item.name
        end
    end
    return nil
end


--[[
    默认恢复逻辑
    参数：partyHealthScore - 排序后的小队健康分数
    返回：是否应该释放耀
    默认逻辑：
        1. 不存在救赎，且分数低于90的队友，存在。
        2. 给他恢复
]]
local function DefaultRenewsLogic(partyHealthScore)
    for _, item in ipairs(partyHealthScore) do
        if (item.value < 0.90) and (UnitAtonementRemaining(item.name) < 1) then
            return item.name
        end
    end
    return nil
end


local function main_rotation()
    -- 基础参数初始化 --
    local defaultTarget = "player"
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()

    -- 职业和专精检查 --
    if not (classFilename == "PRIEST" and currentSpec == 1) then
        return Idle("专精不匹配")
    end

    -- 异常状态检查 --
    if IsMounted("player")
            or UnitInVehicle("player")
            or ChatFrame1EditBox:IsVisible()
            or UnitIsDeadOrGhost("player")
            or checkPlayerIsCasting() then
        return Idle("空白")
    end

    -- 战斗环境参数获取 --
    local enemyTarget = AutoEnemyTarget()               -- 自动选择敌人目标
    local partyMembers = getPartyMembers()              -- 获取有效小队成员列表
    local partyNonTankMembers = getNonTankPartyMembers() -- 获取无坦克小队成员列表
    local tankName = getTankName(partyMembers)          -- 确定当前坦克
    local partyHealthScore = calculatePartyHealthScore(partyMembers)  -- 计算小队健康评分
    local partyNonTankHealthScore = calculatePartyHealthScore(partyNonTankMembers)  -- 计算无坦克小队健康评分
    local isMoving = GetUnitSpeed("player") > 0         -- 移动状态检测

    local PenanceCooldown = CoolDown(47540, 700) --苦修CD检查
    local ShieldCooldown = CoolDown(17) --盾CD
    -- 非战斗逻辑处理 --
    if not UnitAffectingCombat("player") then
        -- 当坦克也不在战斗时处理耐力buff
        if (tankName and (not UnitAffectingCombat(tankName))) or (not tankName) then

            if FortitudeLogic(partyHealthScore) then
                return Cast("耐力")
            end

            if ShionVars["ActionInNoCombat"] then
                -- 血量最少的玩家
                if PenanceCooldown then
                    defaultTarget = NoCombatPenanceLogic(partyHealthScore)
                    return Cast(defaultTarget .. "苦修")
                end

                if ShieldCooldown then
                    defaultTarget = NoCombatShieldLogic(partyHealthScore)
                    return Cast(defaultTarget .. "盾")
                end


            end

            return Idle("不在战斗中")
        end
    end

    -- 保命技能处理 --
    local DesperatePrayerCooldown = CoolDown(19236)    -- 绝望祷言CD检查
    if DesperatePrayerCooldown then
        if calculateUnitHealthScore("player") < 0.50 then
            return Cast("绝望祷言")          -- 自保治疗
        end
    end

    -- 预兆
    -- 在AOE中，有两层就用
    -- 没两层手动来。

    -- 预兆系统处理 --
    if IsAOE() then
        -- 预兆触发窗口期
        if TotalPremonitionCharges() == 2 then
            -- 有2层预兆时优先使用
            return Cast("预兆")
        end
    end


    --    耀
    -- AOE中
    -- 有瞬发buff
    -- 有一个人没有救赎就用
    -- 非AOE中
    -- 有2个人血量低于90且没救赎就用。
    -- 耀技能处理 --
    local radianceCharges = getRadianceCharges()        -- 获取耀充能数
    if radianceCharges > 1 then
        if DefaultRadianceLogic(partyHealthScore) then
            -- 群体治疗需求判断
            return Cast("耀")                -- 群体救赎应用
        end
    end

    -- 驱散优先级处理 --
    if ShionVars["ClearDebuff"] then
        local PurifyCooldown = CoolDown(527)
        if PurifyCooldown then
            -- 自动驱散处理
            defaultTarget = DebuffRemoveLogic(partyHealthScore)
            if defaultTarget then
                return Cast(defaultTarget .. "纯净术")
            end

            --主标指向驱散处理

            if UnitExists("mouseover") and (not UnitIsDeadOrGhost("mouseover")) and UnitIsPlayer("mouseover") then
                if hasDebuff("mouseover") > 0 then
                    return Cast("mouseover纯净术")
                end
            end

        end
    end


    -- 自动套盾
    --有至少四层苦修buff后使用。
    --给没有盾的
    --优先给自己
    --给血量最低的非T玩家。
    local wealAndWoeStack = getWealAndWoeStack()

    if ShieldCooldown and (wealAndWoeStack >= 3) then
        if IsAOE() then
            return Cast("player盾")
        end
        if ShionVars["ShieldTank"] then
            defaultTarget = DefaultShieldLogic(partyHealthScore)
        else
            defaultTarget = DefaultShieldLogic(partyNonTankHealthScore)
        end

        if defaultTarget then
            if not HasPremonitionOfInsightBuff() then
                return Cast(defaultTarget .. "盾")
            end
        end
    end


    -- 苦修卡CD用

    if PenanceCooldown then
        --print("苦修CD")

        if HasPremonitionOfInsightBuff() then
            if enemyTarget then
                return Cast(enemyTarget .. "苦修")
            else
                return Cast("切换目标")
            end
        end
        defaultTarget = DefaultPenanceLogic(partyHealthScore, enemyTarget)
        if defaultTarget then
            return Cast(defaultTarget .. "苦修")
        else
            return Cast("切换目标")
        end
    end

    -- 当有圣光涌动buff时，使用快疗
    local surgeOfLightCharges = getSurgeOfLightCharges()
    if surgeOfLightCharges > 0 then
        defaultTarget = DefaultFlashHealLogic(partyNonTankHealthScore)
        if defaultTarget then
            return Cast(defaultTarget .. "快速治疗")
        end
    end

    -- 快速治疗
    --AOE中：给没有救赎的人用
    defaultTarget = FlashHealLogic2(partyNonTankHealthScore)
    if IsAOE() and defaultTarget then
        return Cast(defaultTarget .. "快速治疗")
    end

    -- 为没有救赎的坦克使用快速治疗

    if tankName and (UnitAtonementRemaining(tankName) < 1) then
        if isMoving then
            return Cast(tankName .. "恢复")
        end
        return Cast(tankName .. "快速治疗")
    end

    --
    if defaultTarget and (not ShionVars["SavaMana"]) then
        if isMoving and UnitRenewsRemaining(defaultTarget) < 1 then
            return Cast(defaultTarget .. "恢复")
        end
        if not isMoving then
            return Cast(defaultTarget .. "快速治疗")

        end
    end
    ---- 为坦克套恢复
    --if tankName and UnitRenewsRemaining(tankName) == 0 then
    --    return Cast(tankName .. "恢复")
    --end
    --
    ---- 恢复使用逻辑
    --defaultTarget = DefaultRenewsLogic(partyHealthScore)
    --if defaultTarget then
    --    return Cast(defaultTarget .. "恢复")
    --end

    if not enemyTarget then
        return Cast("切换目标")
    end

    if enemyTarget then

        if (UnitPainRemaining(enemyTarget) == 0) then
            return Cast(enemyTarget .. "痛")
        end

        -- 自动灌注
        local PowerInfusionCooldown = CoolDown(10060)
        if PowerInfusionCooldown then
            return Cast("player灌注")
        end


        -- 如果[暗影魔]/[摧心魔]可用，则对目标释放。

        if CoolDown(34433) then
            return Cast(enemyTarget .. "暗影魔")
        end

        -- 如果[心灵震爆]可用，则对目标释放。

        if CoolDown(8092) and (not isMoving) then
            return Cast(enemyTarget .. "心灵震爆")
        end

        -- 目标血量小于20，则灭

        if IsSpellKnownOrOverridesKnown(32379)
                and CoolDown(32379)
                and ((UnitHealth(enemyTarget) / UnitHealthMax(enemyTarget)) < 0.20) then
            return Cast(enemyTarget .. "灭")
        end

        -- 惩击
        --没有苦修buff时候
        --作为填充技能
        if not ShionVars["MoreFlash"] then
        if (wealAndWoeStack <= 1) then
            return Cast(enemyTarget .. "惩击")
        end
        end


    end

    --快速治疗3
    --当惩击无法使用时
    --给任何不满血的最低积分目标。
    defaultTarget = FlashHealLogic3(partyHealthScore)
    if defaultTarget and (not isMoving) and (not ShionVars["SavaMana"]) then
        return Cast(defaultTarget .. "快速治疗")
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
rotationEventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, event, ...)
end)
function rotationEventFrame:UNIT_SPELLCAST_START(event, unitTarget, castGUID, spellID)
    if requiredPremonitionList[spellID] then
        requiredPremonitionTimer = GetTime() + 3
    end
    --checkTargetIsTankOutburstDamage(event, spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_CHANNEL_START(event, unitTarget, castGUID, spellID)
    --checkTargetIsTankOutburstDamage(event, spellID)
    return
end

function rotationEventFrame:UNIT_SPELLCAST_SUCCEEDED(event, unitTarget, castGUID, spellID)
    if (spellID == 105509) and (unitTarget == "player") then
        radiance_spell_time = GetTime() + 10
    end
    --clearTargetIsTankOutburstDamage(event, spellID)
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





