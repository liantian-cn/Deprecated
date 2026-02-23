D:\PythonENV\PixelBot_311\Scripts\python.exe E:\Documents\GitHub\Shion\Test1.py 
Decoded and decompressed result:
===========================================================================================
=======================         Hekili        ===========================================
=======================         PropC82F        ===========================================
None
===========================================================================================
=======================         Party        ===========================================
=======================         PropCfaa        ===========================================
-- 本脚本为Wa1Key编写，并免费分享。
-- 1：戒律可以输出； 2：允许Hekili推荐惩击； 3：中断施法
-- 251：戒律不组队输出； 253：暗影输出； 255：什么也不做
local Mounted = IsMounted("player")-- 坐骑
local InVehicle = UnitInVehicle("player")-- 载具
local ChatFrame = ChatFrame1EditBox:IsVisible()-- 聊天框
local Dead = UnitIsDeadOrGhost("player")-- 死亡
local Channel = UnitChannelInfo("player")-- 引导法术
local inRaid = UnitPlayerOrPetInRaid("player")-- 在团队中
local inParty = UnitPlayerOrPetInParty("player")-- 在队伍中
local ismoving = GetUnitSpeed("player") > 0 -- 检查玩家是否移动
local combat = UnitAffectingCombat("player")-- 检查战斗状态
local TargetCanAttack = UnitCanAttack("player", "target")-- 目标可以攻击
local Specialization = GetSpecialization()-- 当前专精
local inRange = C_Spell.IsSpellInRange(585, "target")-- 敌对目标范围内

if Mounted or InVehicle or ChatFrame or Dead then
    return 什么也不做
end
if Specialization == 1 and (not inParty or inRaid) then
    if inRange then
        if Channel then
            return 什么也不做
        else
            return 戒律不组队输出
        end
    else
        return 什么也不做
    end
end

if Specialization == 2 then
    return 252
end

if Specialization == 3 then
    if inRange then
        if Channel then
            return 什么也不做
        else
            return 暗影输出
        end
    else
        return 什么也不做
    end
end

local debuffs = {
    "燧火创伤", --酒庄
    "灼热之陨", --剧场
    "鱼叉", --水闸
    "饕餮虚空", "混沌腐蚀", "混沌脆弱" --鸟巢
}
--Boss技能
local BossSpell = {
    "震地", --车间
    "静电脉冲", "地震回荡", --妈妈矿区
    "强力碾压", --剧场
    "狂野闪电", "粉碎现实", --鸟巢
    "喷涌佳酿", "振翼之风", "遮天蔽日！", --酒庄
    "献祭葬火", "盲目之光", --修道院
    "吹灭之息", "永恒黑暗", --裂口
    "快速启动", "泥石流", "涡轮增压", --水闸
}

--小怪技能无控制
local Nameplate = {
    "超级电钻", "短路", --车间
    "迅速萃取", "充能射击", --老妈矿区
    "碾地猛击", "灵魂风暴", --剧场
    "局部风暴", "诱集暗影", "饕餮虚空", "", --鸟巢
    "蜂拥惊喜", --酒庄
    "雷霆一击", "热浪", "圣光烁辉", "神圣鸣罪", --修道院
    "压制咆哮", "镇火冲击", --暗焰裂口
    "扭曲精华", "逆流", --水闸
}
--打断技能，需要主动中断当前施法以免被沉默
local Nameplateinterrupt = {"瓦解怒吼", "打断怒吼", "雷音贯耳", --修道院，剧场
    }

--有效目标
local function isValidUnit(unit)
    return UnitExists(unit) and
        not UnitIsDeadOrGhost(unit) and
        UnitCanAssist("player", unit) and
        UnitInRange(unit)
end
--检差单位生命值百分比，损失生命值
local function UnitHealthPct(unit)
    local healthPct = 0
    local lossHealth = 0
    if isValidUnit(unit) then
        local maxHealth = UnitHealthMax(unit)
        local currentHealth = UnitHealth(unit)
        local healAbsorbs = UnitGetTotalHealAbsorbs(unit) or 0
        healthPct = (currentHealth - healAbsorbs) / maxHealth * 100
        lossHealth = maxHealth - currentHealth - healAbsorbs
        return healthPct, lossHealth
    end
    return healthPct, lossHealth
end
-- 检查单位施法的函数，返回剩余时间（毫秒）
local function checkCasting(unitType, spellList)
    for i = 1, 40 do
        local unit = unitType .. i
        if UnitExists(unit) then
            local spellName, _, _, startTime, endTime = UnitCastingInfo(unit)
            if spellName then
                for _, spell in ipairs(spellList) do
                    if spellName == spell then
                        local timeLeftMs = endTime - (GetTime() * 1000)-- 转换为毫秒
                        return timeLeftMs
                    end
                end
            end
        end
    end
    return nil
end
-- 检查单位是否正在施放特定法术的函数
local function isUnitCastingSpell(unitOrType, spellInput, isMultiUnit)
    local spellName
    if type(spellInput) == "number" then
        local spellInfo = C_Spell.GetSpellInfo(spellInput)
        spellName = spellInfo and spellInfo.name or nil
    else
        spellName = spellInput
    end
    
    if not spellName then return false end
    
    local units = {}
    if isMultiUnit then
        for i = 1, 40 do
            table.insert(units, unitOrType .. i)
        end
    else
        units = {unitOrType}
    end
    
    for _, unit in ipairs(units) do
        local castingSpellName = UnitCastingInfo(unit)
        local channelingSpellName = UnitChannelInfo(unit)
        if castingSpellName == spellName or channelingSpellName == spellName then
            return true
        end
    end
    return false
end
-- 获取技能冷却时间的函数
local function getCooldown(spellID)
    local cooldown = C_Spell.GetSpellCooldown(spellID)
    return (cooldown.startTime > 0) and (cooldown.startTime + cooldown.duration - GetTime()) or 0
end
--获取技能充能层数的函数
local function getCharges(spellID)
    local charges = C_Spell.GetSpellCharges(spellID)
    return charges and charges.currentCharges or 0
end
-- 获取单位光环的函数，返回是否有光环及光环层数
local function hasAura(unit, auraName, onlyPlayerCast)
    for j = 1, 40 do
        local auraData = C_UnitAuras.GetAuraDataByIndex(unit, j, "HELPFUL")
        if not auraData then break end
        if auraData.name == auraName then
            if onlyPlayerCast then
                if auraData.sourceUnit == "player" then
                    return true, auraData.applications or 1 -- 返回 true 和层数
                end
            else
                return true, auraData.applications or 1 -- 返回 true 和层数
            end
        end
    end
    return false, 0 -- 没有找到光环，返回 false 和 0 层
end
-- 获取单位有害光环的函数，返回是否有debuff和debuff数量
local function hasDebuff(unit)
    local debuffCount = 0
    
    for _, debuff in ipairs(debuffs) do
        for i = 1, 40 do
            local debuffData = C_UnitAuras.GetAuraDataByIndex(unit, i, "HARMFUL")
            if not debuffData then break end
            if debuffData.name == debuff then
                debuffCount = debuffCount + 1
                break -- 找到后跳出内层循环，避免重复计数同一debuff
            end
        end
    end
    
    return debuffCount > 0, debuffCount
end

-- 改成

local function hasDebuff(unit)
    local debuffCount = 0
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unit, i, "HARMFUL")
        if not debuffData then break end
        if debuffs[debuffData.name] then
            debuffCount = debuffCount + 1
        end
    end

    return debuffCount > 0, debuffCount
end


--学会了某个法术
local function knownSpell(spellID)
    return IsPlayerSpell(spellID)
end

if isUnitCastingSpell("boss1", "黑暗降临", false) then
    return 什么也不做
end
--检测boss、姓名版的施法
local BossAoeRemainingMs = checkCasting("boss", BossSpell)
local AoeRemainingMs = checkCasting("nameplate", Nameplate)
local NameplateinterruptRemainingMs = checkCasting("nameplate", Nameplateinterrupt)
local AoeIsComeing = false
if BossAoeRemainingMs and BossAoeRemainingMs > 0 and BossAoeRemainingMs <= 1100 then
    AoeIsComeing = true
end
if AoeRemainingMs and AoeRemainingMs > 0 and AoeRemainingMs <= 1100 then
    AoeIsComeing = true
end

--定义光环名称
local 圣光涌动 = "圣光涌动"
local 救赎 = "救赎"
local 分秒必争 = "分秒必争"
local 祸福相倚 = "祸福相倚"
local 盾Aura = "真言术：盾"

local known福音 = knownSpell(472433)-- 学会了福音
local known预兆 = knownSpell(428924)-- 学会了预兆


local playerHealthPct, playerLossHealth = UnitHealthPct("player")-- 玩家生命值百分比，缺失生命值
local isCast耀 = isUnitCastingSpell("player", 194509, false)-- 正在施放真言术：耀
local isSmite = isUnitCastingSpell("player", 585, false)-- 正在施放惩击

-- 检查技能冷却
local GCD = getCooldown(61304)-- 公共冷却
local 盾 = getCooldown(17) <= GCD -- 真言术：盾
local 苦修 = getCooldown(47540) <= GCD -- 苦修
local 福音 = getCooldown(472433) <= GCD and known福音 -- 福音
local Can盾time = getCooldown(47540) - getCooldown(17) < 3 -- 苦修和盾的相差时间小于3秒
local 耀remainingMs = getCooldown(194509)-- 真言术：耀
-- 检测技能充能
local 耀Charges = getCharges(194509)-- 真言术：耀
local 预兆Charges = getCharges(428924)-- 预兆
local 痛苦压制Charges = getCharges(33206)-- 痛苦压制
--检查玩家自身光环
local has圣光涌动 = hasAura("player", 圣光涌动, true)-- 圣光涌动
local playerHas救赎 = hasAura("player", 救赎, true)-- 救赎
local playerHas分秒必争 = hasAura("player", 分秒必争, true)-- 分秒必争(瞬发耀)
local playerHas祸福相倚, 祸福相倚Stacks = hasAura("player", 祸福相倚, true)-- 祸福相倚
local playerHas盾 = hasAura("player", 盾Aura, true)-- 真言术：盾
local playerhasdebuff, playerDebuffCount = hasDebuff("player")
--检测队伍信息
local has救赎Count = 0 -- 统计有“救赎”光环的单位数量

local No救赎Count = 0 -- 统计没有“救赎”光环且血量低于阈值的单位数量
local No救赎Lowest = 0 -- 存储血量最低且无“救赎”光环的单位索引，默认值为 0
local No救赎LowestHealth = 100 -- 存储血量最低且无“救赎”光环的单位血量百分比，默认值为 100%
local No救赎Tank = 0 -- 存储无“救赎”坦克的单位索引，默认值为 0

local No盾 = 0 -- 记录最后一个无盾的单位
local No盾Lowest = 0 -- 存储血量最低且无“盾”光环的单位索引，默认值为 0
local No盾HealthLowest = 100 -- 存储血量最低且无“盾”光环的单位血量百分比，默认值为 100%
local No盾Tank = 0 -- 存储无“盾”坦克的单位索引，默认值为 0

local LowestUnit = 0 -- 存储血量最低的单位索引（不检测光环），默认值为 0
local LowestHealth = 100 -- 存储血量最低单位的血量百分比（不检测光环），默认值为 100%

local 福音Count = 0 -- 满足“福音”治疗量的单位
local memberWithDebuff = 0 -- 有指定debuff的成员id
local memberWithDebuffCount = 0 -- 有指定debuff的成员数量
local VeryDangerUnit = 0

if playerHas救赎 then
    has救赎Count = has救赎Count + 1
else
    if playerHealthPct < 99 then
        No救赎Count = No救赎Count + 1
    end
    if playerHealthPct < No救赎LowestHealth then
        No救赎LowestHealth = playerHealthPct
        No救赎Lowest = 1
    end
end

if playerHealthPct < LowestHealth then
    LowestHealth = playerHealthPct
    LowestUnit = 1
end

if playerhasdebuff and not playerHas救赎 then
    memberWithDebuffCount = memberWithDebuffCount + 1
    memberWithDebuff = 1
end
if playerDebuffCount >= 2 then
    VeryDangerUnit = 1
end
-- 小队成员
for i = 1, 4 do
    local unit = "party" .. i
    if isValidUnit(unit) then
        local partyHealthPct, lossHealth = UnitHealthPct(unit)
        local has救赎 = hasAura(unit, 救赎, true)
        local has盾 = hasAura(unit, 盾Aura, true)
        local istank = UnitGroupRolesAssigned(unit) == "TANK"
        local hasdebuff, DebuffCount = hasDebuff(unit)
        
        if hasdebuff and not has救赎 then
            memberWithDebuffCount = memberWithDebuffCount + 1
            memberWithDebuff = i + 1
        end
        if DebuffCount >= 2 then
            VeryDangerUnit = i + 1
        end
        if not has盾 then
            No盾 = i + 1
            if partyHealthPct < No盾HealthLowest then
                No盾HealthLowest = partyHealthPct
                No盾Lowest = i + 1
            end
            if istank then
                No盾Tank = i + 1
            end
        end
        if has救赎 then
            has救赎Count = has救赎Count + 1
        else
            if partyHealthPct < 90 then
                No救赎Count = No救赎Count + 1
            end
            if partyHealthPct < No救赎LowestHealth then
                No救赎LowestHealth = partyHealthPct
                No救赎Lowest = i + 1
            end
        end
        if istank and not has救赎 then
            No救赎Tank = i + 1
        end
        if istank and not has盾 then
            No盾Tank = i + 1
        end
        if partyHealthPct < LowestHealth then
            LowestHealth = partyHealthPct
            LowestUnit = i + 1
        end
    end
end

if not playerHas盾 then
    No盾 = 1
    if playerHealthPct < No盾HealthLowest then
        No盾HealthLowest = playerHealthPct
        No盾Lowest = 1
    end
end

if 福音 then
    local _, intellect = UnitStat("player", 4)-- 获取智力值
    local versatilityBonus = GetCombatRatingBonus(29) / 100 + 1 -- 获取全能百分比
    local 福音Value = intellect * versatilityBonus * 54 -- 福音的总体治疗量(打九折)
    --福音的平均治疗量
    local Average福音 = has救赎Count > 0 and (福音Value / has救赎Count) or 0
    if playerHas救赎 and playerLossHealth > Average福音 then
        福音Count = 福音Count + 1
    end
    
    for i = 1, 4 do
        local unit = "party" .. i
        if isValidUnit(unit) then
            local partyHealthPct, lossHealth = UnitHealthPct(unit)
            if lossHealth > Average福音 then
                福音Count = 福音Count + 1
            end
        end
    end
end

-- 10：预兆；       11：耀；        12：福音；        13：苦修
if combat then
    if NameplateinterruptRemainingMs and NameplateinterruptRemainingMs < 500 then
        return 3 --中断施法
    end
    if Channel then --在引导
        return 什么也不做
    end
    
    if 福音 then
        if has救赎Count >= 4 and 福音Count >= 3 then
            return 福音
        elseif has救赎Count >= 2 and 福音Count >= 2 then
            return 福音
        elseif has救赎Count == 1 and 福音Count == 1 then
            return 福音
        end
    end
    if 痛苦压制Charges > 0 and VeryDangerUnit > 0 then
        return VeryDangerUnit + 80
    end
    --群疗
    if isCast耀 then
        return 0
    else
        if 耀Charges > 0 or 耀remainingMs <= GCD then
            if playerHas分秒必争 then
                if LowestHealth <= 90 then
                    return 耀
                end
            else
                if has救赎Count <= 4 and AoeIsComeing then
                    if known预兆 and 预兆Charges >= 2 then
                        return 预兆
                    else
                        return 耀
                    end
                end
            end
            if not ismoving and No救赎Count >= 2 then
                return 耀
            end
        else
            if 盾 and known预兆 and 祸福相倚Stacks >= 4 and AoeIsComeing then
                return 盾自己
            end
        end
    end
    
    if known预兆 then --单体治疗
        if 苦修 and 祸福相倚Stacks < 4 then
            if TargetCanAttack and inRange then
                return 苦修
            else
                return LowestUnit + 75 -- 75-80苦修
            end
        end
        if 盾 and 祸福相倚Stacks >= 4 then -- 61-65 盾
            if No盾HealthLowest < 40 then
                return No盾Lowest + 60
            end
            if memberWithDebuffCount == 1 then
                return memberWithDebuff + 60
            end
            if No救赎LowestHealth < 90 then
                return No救赎Lowest + 60
            end
            if No盾HealthLowest < 95 then
                return No盾Lowest + 60
            end
            if No盾Tank > 1 then
                return No盾Tank + 60
            elseif No盾 > 0 then
                return No盾 + 60
            end
        end
        if has圣光涌动 then -- 66-70快速治疗
            if memberWithDebuffCount == 1 then
                return memberWithDebuff + 65
            end
            if No救赎Count >= 1 then
                return No救赎Lowest + 65
            elseif LowestHealth <= 90 then
                return LowestUnit + 65
            end
        end
        if No救赎Count >= 1 then -- 70-75 恢复
            return No救赎Lowest + 70
        end
        if memberWithDebuffCount == 1 then -- 70-75 恢复
            return memberWithDebuff + 70
        end
        if Can盾time and 祸福相倚Stacks >= 4 and inRange then --允许Hekili推荐惩击
            return 2
        end
    else --以下非白戒律
        if memberWithDebuffCount == 1 then
            --61-65盾，66-70快速治疗，71-75恢复
            local indexMapping = {
                [1] = {61, 66, 71},
                [2] = {62, 67, 72},
                [3] = {63, 68, 73},
                [4] = {64, 69, 74},
                [5] = {65, 70, 75},
            }
            
            local indexGroup
            if 盾 then
                indexGroup = 1
            elseif has圣光涌动 then
                indexGroup = 2
            else
                indexGroup = 3
            end
            if indexGroup then
                return indexMapping[memberWithDebuff] and indexMapping[memberWithDebuff][indexGroup]
            end
        end
        if No救赎Count == 1 or 耀Charges == 0 or ismoving then
            local indexMapping = {
                [1] = {61, 66, 71},
                [2] = {62, 67, 72},
                [3] = {63, 68, 73},
                [4] = {64, 69, 74},
                [5] = {65, 70, 75},
            }
            local indexGroup
            if has圣光涌动 then
                indexGroup = 2
            elseif 盾 then
                indexGroup = 1
            else
                indexGroup = 3
            end
            if indexGroup then
                return indexMapping[No救赎Lowest] and indexMapping[No救赎Lowest][indexGroup]
            end
        end
        if 盾 and No救赎Tank > 1 then
            return No救赎Tank + 60
        end
    end
    
    if No救赎Count == 0 and inRange then
        return 1
    end
else
    if known预兆 then
        if 苦修 and 祸福相倚Stacks < 4 and LowestHealth < 80 then
            return LowestUnit + 75 --75-80苦修
        end
        if 祸福相倚Stacks >= 4 then
            if No盾HealthLowest < 100 and No盾Lowest > 0 then
                return No盾Lowest + 60
            elseif No盾Tank > 1 then
                return No盾Tank + 60
            elseif No盾 > 0 then
                return No盾 + 60
            end
        end
    else
        if No救赎Tank > 1 and 盾 then
            return No救赎Tank + 60
        end
    end
    if LowestHealth < 70 then
        if ismoving then
            if has圣光涌动 then
                return LowestUnit + 65 --66-70快速治疗
            end
            if 苦修 then
                return LowestUnit + 75 --75-80苦修
            end
        else
            if 苦修 then
                return LowestUnit + 75 --75-80苦修
            end
            return LowestUnit + 65 --66-70快速治疗
        end
    end
end

return 0
===========================================================================================
=======================         Red        ===========================================
=======================         PropC81F        ===========================================
Red
===========================================================================================
=======================         Trinkets        ===========================================
=======================         PropCfaa        ===========================================
local abilityID = Hekili_GetRecommendedAbility("Primary", 1)

if abilityID then
    if abilityID < 0 then
        return 1
    else
        return 0
    end
end
===========================================================================================
=======================         纯净        ===========================================
=======================         PropC74D        ===========================================
527
===========================================================================================
=======================         驱散        ===========================================
=======================         PropCfaa        ===========================================
-- 排除特定的Debuff名称
local excludedDebuffs = {
    ["动能胶质炸药"] = true,
    ["不稳定的腐蚀"] = true,
    ["震地回响"] = true,
    ["烈焰撕咬"] = true,
    ["饕餮虚空"] = true,
    ["虚弱灵魂"] = true,
    ["虚弱光环"] = true,
    ["最后一击"] = true,
    ["灵魂枯萎"] = true,
    ["巨口蛙毒"] = true,
    ["培植毒药"] = true
}

-- 特殊优先处理的Debuff（按需扩展）
local priorityDebuffs = {
    [4400303] = true -- 特殊ID
}

-- 检查玩家是否学习了某法术
local function hasLearnedSpell(spellID)
    return spellID and IsPlayerSpell(spellID) or false
end

-- 检查玩家是否学习了多个法术中的任意一个
local function hasLearnedAnySpell(spellIDs)
    for _, spellID in ipairs(spellIDs) do
        if hasLearnedSpell(spellID) then
            return true
        end
    end
    return false
end

-- 各法术的驱散能力映射
local dispelAbilities = {
    Magic = {527, 360823, 4987, 115450, 88423}, -- 魔法驱散
    Disease = {390632, 213634, 393024, 213644, 388874, 218164}, -- 疾病驱散
    Curse = {383016, 51886, 392378, 2782, 475}, -- 诅咒驱散
    Poison = {392378, 2782, 393024, 213644, 388874, 218164, 365585}-- 中毒驱散
}

-- 动态生成驱散能力
local dispelCapabilities = {}
for debuffType, spellIDs in pairs(dispelAbilities) do
    dispelCapabilities[debuffType] = hasLearnedAnySpell(spellIDs)
end

-- 检查是否可以驱散指定类型的debuff
local function canDispelType(debuffType)
    return dispelCapabilities[debuffType] or false
end

-- 检查单位是否有可驱散的Debuff
local function hasDispellableDebuff(unit)
    for j = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unit, j, "HARMFUL")
        if not debuffData then break end
        
        local name = debuffData.name
        local debuffType = debuffData.dispelName
        local spellId = debuffData.spellId
        
        -- 排除无需驱散的Debuff
        if excludedDebuffs[name] then
            -- 直接跳过当前循环
            elseif debuffType and canDispelType(debuffType) then
            return true
            elseif priorityDebuffs[spellId] then
                return true
            end
    end
    return false
end

-- 优先检查自己
if hasDispellableDebuff("player") then
    return 1
end
-- 检查小队成员
for i = 1, 4 do
    local unit = "party" .. i
    if UnitExists(unit) and not UnitIsDeadOrGhost(unit) and UnitInRange(unit) and UnitCanAssist("player", unit) then
        if hasDispellableDebuff(unit) then
            return i + 1
        end
    end
end
return 0
===========================================================================================
=======================         目标驱散        ===========================================
=======================         PropCfaa        ===========================================
local ImprovedPurify = IsPlayerSpell(390632)

local function hasMagicDebuff(unit)
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unit, i, "HARMFUL")
        if not debuffData then break end
        if debuffData.dispelName == "Magic" then
            return true
        end
    end
    return false
end

local function hasDiseaseDebuff(unit)
    for i = 1, 40 do
        local debuffData = C_UnitAuras.GetAuraDataByIndex(unit, i, "HARMFUL")
        if not debuffData then break end
        if debuffData.dispelName == "Disease" then
            return true
        end
    end
    return false
end

local unit = "target"
if UnitExists(unit) and UnitInRange(unit) and UnitCanAssist("player", unit) then
    if hasMagicDebuff(unit) or (ImprovedPurify and hasDiseaseDebuff(unit)) then
        return 1
    end
end

return 0
===========================================================================================
=======================         Raid        ===========================================
=======================         PropCfaa        ===========================================
--本脚本为Wa1Key编写，并免费分享。
--选择敌人：46, 耀：50, 盾：51, 福音：52, 快速治疗：53, 恢复：54, 耐力：55
local time = GetTime()

local frame = CreateFrame("Frame")
frame:RegisterEvent("ADDON_LOADED")
frame:SetScript("OnEvent", function(self, event, arg1, arg2)
    if event == "ADDON_LOADED" then
        _G["LastTime"] = time
    end
end)

local Mounted = IsMounted("player")-- 坐骑
local InVehicle = UnitInVehicle("player")-- 载具
local ChatFrame = ChatFrame1EditBox:IsVisible()-- 聊天框
local Dead = UnitIsDeadOrGhost("player")-- 死亡
local Channel = UnitChannelInfo("player")-- 引导法术
local inRaid = UnitPlayerOrPetInRaid("player")-- 在团队中
local ismoving = GetUnitSpeed("player") > 0 -- 检查玩家是否移动
local combat = UnitAffectingCombat("player")-- 检查战斗状态
local Specialization = GetSpecialization()-- 当前专精

local UnitHealth = UnitHealth
local UnitHealthMax = UnitHealthMax
local UnitGetTotalHealAbsorbs = UnitGetTotalHealAbsorbs
local UnitExists = UnitExists
local UnitInRange = UnitInRange
local UnitIsDeadOrGhost = UnitIsDeadOrGhost
local UnitCanAssist = UnitCanAssist
local GetNumGroupMembers = GetNumGroupMembers
local C_Spell = C_Spell
local C_UnitAuras = C_UnitAuras

-- 将这些常量声明为局部变量
local SPELL_ID_耀 = 194509
local SPELL_ID_盾 = 17
local SPELL_ID_GCD = 61304

if not inRaid or Mounted or InVehicle or ChatFrame or Dead or Channel or Specialization ~= 1 then
    return 什么也不做
end
if not _G["LastTime"] or _G["LastTime"] < GetTime() - 0.3 then
    --检测单位生命值百分比和失去的生命值
    local function UnitHealthPct(unit)
        local maxHealth = UnitHealthMax(unit)
        if maxHealth == 0 then return 0, 0 end
        local currentHealth = UnitHealth(unit)
        local healAbsorbs = UnitGetTotalHealAbsorbs(unit) or 0
        local effectiveHealth = currentHealth - healAbsorbs
        return (effectiveHealth / maxHealth * 100), (maxHealth - effectiveHealth)
    end
    
    -- 检查玩家是否正在施放特定法术的函数
    local function isCastingSpell(spellID)
        local spellName = C_Spell.GetSpellInfo(spellID)
        local castingSpellName = UnitCastingInfo("player")
        local channelingSpellName = UnitChannelInfo("player")
        return castingSpellName == spellName or channelingSpellName == spellName
    end
    
    -- 获取技能冷却时间的函数
    local function getCooldown(spellID)
        local cooldown = C_Spell.GetSpellCooldown(spellID)
        return (cooldown.startTime > 0) and (cooldown.startTime + cooldown.duration - time) or 0
    end
    
    --获取技能充能层数的函数
    local function getCharges(spellID)
        local charges = C_Spell.GetSpellCharges(spellID)
        return charges and charges.currentCharges or 0
    end
    
    --获取单位光环的函数
    local function hasAura(unit, auraName, onlyPlayerCast)
        local auraData = AuraUtil.FindAuraByName(auraName, unit, "HELPFUL")
        if auraData then
            if onlyPlayerCast then
                return auraData.sourceUnit == "player"
            end
            return true
        end
        return false
    end
    
    local function targetcanattack(unit)
        if UnitCanAttack("player", unit) and not UnitIsDeadOrGhost(unit) then
            return 1
        else
            return 46
        end
    end
    
    local aura圣光涌动 = "圣光涌动"
    local auraName1 = "救赎"
    local auraRenew = "恢复"
    local auraAngel = "救赎之魂"
    
    local isCast耀 = isCastingSpell(194509)--正在施放真言术：耀
    -- 检查技能冷却
    local GCD = getCooldown(61304)-- 公共冷却
    local 盾 = getCooldown(17) <= GCD -- 真言术：盾
    
    -- 检测技能充能
    local 耀Charges = getCharges(194509)--真言术：耀
    --检查玩家自身光环
    local has圣光涌动 = hasAura("player", aura圣光涌动, true)--圣光涌动
    
    local NumMembers = GetNumGroupMembers()
    local unitsMissing救赎 = 0
    local LowestNo救赎 = 0
    local LowestNo救赎Health = 100
    local RenewCount = 0
    
    for i = 1, NumMembers do
        local unit = "raid" .. i
        
        -- 合并两个循环的检查
        if UnitExists(unit) then
            
            if hasAura(unit, auraRenew, false) then
                RenewCount = RenewCount + 1
            end
            
            -- 检查救赎
            if UnitInRange(unit) and not UnitIsDeadOrGhost(unit) and UnitCanAssist("player", unit)
                and not hasAura(unit, auraAngel, false) and not hasAura(unit, auraName1, true) then
                local healthPct = UnitHealthPct(unit)
                if healthPct <= 90 then
                    unitsMissing救赎 = unitsMissing救赎 + 1
                    if healthPct < LowestNo救赎Health then
                        LowestNo救赎Health = healthPct
                        LowestNo救赎 = i
                    end
                end
                
                -- 提前退出条件
                if (耀Charges > 0 and unitsMissing救赎 >= 3) or
                    (耀Charges == 0 and unitsMissing救赎 >= 1) then
                    break
                end
            end
        end
    end
    
    local UnitIsLowest = UnitIsUnit("target", "raid" .. LowestNo救赎)
    
    local function Solo()
        if has圣光涌动 then
            if UnitIsLowest then
                return 53
            else
                return LowestNo救赎 + 5
            end
        elseif 盾 then
            if UnitIsLowest then
                return 51
            else
                return LowestNo救赎 + 5
            end
        elseif RenewCount < 2 then
            if UnitIsLowest then
                return 54
            else
                return LowestNo救赎 + 5
            end
        else
            return targetcanattack("target")
        end
    end
    
    if combat then
        if unitsMissing救赎 == 0 then
            return targetcanattack("target")
        else
            if unitsMissing救赎 > 2 and not ismoving then
                if 耀Charges == 0 then
                    return Solo()
                else
                    if not isCast耀 then
                        if UnitIsLowest then
                            return 50
                        else
                            return LowestNo救赎 + 5
                        end
                    end
                end
            else
                return Solo()
            end
        end
        return 1
    end
    _G["LastTime"] = GetTime()
    return 0
end
===========================================================================================
=======================         Buffs        ===========================================
=======================         PropC81F        ===========================================
Buffs
===========================================================================================
=======================         PriestSpells        ===========================================
=======================         PropC81F        ===========================================
PriestSpells
===========================================================================================
=======================         DesperatePrayer        ===========================================
=======================         PropC81F        ===========================================
DesperatePrayer
===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================                 ===========================================
=======================         PropCfcd        ===========================================

===========================================================================================
=======================         i1        ===========================================
=======================         n61        ===========================================
/cast [@player]真言术：盾
===========================================================================================
=======================         i2        ===========================================
=======================         n62        ===========================================
/cast [@party1]真言术：盾
===========================================================================================
=======================         i3        ===========================================
=======================         n63        ===========================================
/cast [@party2]真言术：盾
===========================================================================================
=======================         i4        ===========================================
=======================         n64        ===========================================
/cast [@party3]真言术：盾
===========================================================================================
=======================         i5        ===========================================
=======================         n65        ===========================================
/cast [@party4]真言术：盾
===========================================================================================
=======================         i6        ===========================================
=======================         n66        ===========================================
/cast [@player]快速治疗
===========================================================================================
=======================         i7        ===========================================
=======================         n67        ===========================================
/cast [@party1]快速治疗
===========================================================================================
=======================         i8        ===========================================
=======================         n68        ===========================================
/cast [@party2]快速治疗
===========================================================================================
=======================         i9        ===========================================
=======================         n69        ===========================================
/cast [@party3]快速治疗
===========================================================================================
=======================         i10        ===========================================
=======================         n70        ===========================================
/cast [@party4]快速治疗
===========================================================================================
=======================         i11        ===========================================
=======================         n71        ===========================================
/cast [@player]恢复
===========================================================================================
=======================         i12        ===========================================
=======================         n72        ===========================================
/cast [@party1]恢复
===========================================================================================
=======================         i13        ===========================================
=======================         n73        ===========================================
/cast [@party2]恢复
===========================================================================================
=======================         i14        ===========================================
=======================         n74        ===========================================
/cast [@party3]恢复
===========================================================================================
=======================         i15        ===========================================
=======================         n75        ===========================================
/cast [@party4]恢复
===========================================================================================
=======================         i16        ===========================================
=======================         n76        ===========================================
/cast [@player]苦修
===========================================================================================
=======================         i17        ===========================================
=======================         n77        ===========================================
/cast [@party1]苦修
===========================================================================================
=======================         i18        ===========================================
=======================         n78        ===========================================
/cast [@party2]苦修
===========================================================================================
=======================         i19        ===========================================
=======================         n79        ===========================================
/cast [@party3]苦修
===========================================================================================
=======================         i20        ===========================================
=======================         n80        ===========================================
/cast [@party4]苦修
===========================================================================================
=======================         i21        ===========================================
=======================         n81        ===========================================
/cast [@player]压制
===========================================================================================
=======================         i22        ===========================================
=======================         n82        ===========================================
/cast [@party1]压制
===========================================================================================
=======================         i23        ===========================================
=======================         n83        ===========================================
/cast [@party2]压制
===========================================================================================
=======================         i24        ===========================================
=======================         n84        ===========================================
/cast [@party3]压制
===========================================================================================
=======================         i25        ===========================================
=======================         n85        ===========================================
/cast [@party4]压制
===========================================================================================
=======================         i26        ===========================================
=======================         n86        ===========================================
/cast [@party1]能量灌注
===========================================================================================
=======================         i27        ===========================================
=======================         n87        ===========================================
/cast [@party2]能量灌注
===========================================================================================
=======================         i28        ===========================================
=======================         n88        ===========================================
/cast [@party3]能量灌注
===========================================================================================
=======================         i29        ===========================================
=======================         n89        ===========================================
/cast [@party4]能量灌注
===========================================================================================
=======================         i30        ===========================================
=======================         n528        ===========================================
/cast 驱散魔法
===========================================================================================
=======================         i31        ===========================================
=======================         n585        ===========================================
/cast 惩击
===========================================================================================
=======================         i32        ===========================================
=======================         n589        ===========================================
/cast 暗言术：痛
===========================================================================================
=======================         i33        ===========================================
=======================         n8092        ===========================================
/cast 心灵震爆
===========================================================================================
=======================         i34        ===========================================
=======================         n占位1        ===========================================
占位1
===========================================================================================
=======================         i35        ===========================================
=======================         n10060        ===========================================
/cast [target=focus,exists]能量灌注;能量灌注
===========================================================================================
=======================         i36        ===========================================
=======================         n15407        ===========================================
/cast 精神鞭笞
===========================================================================================
=======================         i37        ===========================================
=======================         n15487        ===========================================
/cast 沉默
===========================================================================================
=======================         i38        ===========================================
=======================         n19236        ===========================================
/cast 绝望祷言
===========================================================================================
=======================         i39        ===========================================
=======================         n21562        ===========================================
/cast [@player]真言术：韧
===========================================================================================
=======================         i40        ===========================================
=======================         n32375        ===========================================
/cast [@cursor]群体驱散
===========================================================================================
=======================         i41        ===========================================
=======================         n32379        ===========================================
/cast 暗言术：灭
===========================================================================================
=======================         i42        ===========================================
=======================         n33206        ===========================================
/cast 痛苦压制
===========================================================================================
=======================         i43        ===========================================
=======================         n34433        ===========================================
/cast 暗影魔
===========================================================================================
=======================         i44        ===========================================
=======================         n34914        ===========================================
/cast 吸血鬼之触
===========================================================================================
=======================         i45        ===========================================
=======================         n47540        ===========================================
/cast 苦修
===========================================================================================
=======================         i46        ===========================================
=======================         n占位2        ===========================================
占位2
===========================================================================================
=======================         i47        ===========================================
=======================         n62618        ===========================================
/cast [@cursor]真言术：障
===========================================================================================
=======================         i48        ===========================================
=======================         n73510        ===========================================
/cast 心灵尖刺
===========================================================================================
=======================         i49        ===========================================
=======================         n120517        ===========================================
/cast 光晕
===========================================================================================
=======================         i50        ===========================================
=======================         n120644        ===========================================
/cast 光晕
===========================================================================================
=======================         i51        ===========================================
=======================         n123040        ===========================================
/cast 暗影魔
===========================================================================================
=======================         i52        ===========================================
=======================         n132157        ===========================================
/cast 神圣新星
===========================================================================================
=======================         i53        ===========================================
=======================         n204197        ===========================================
/cast 净化邪恶
===========================================================================================
=======================         i54        ===========================================
=======================         n205385        ===========================================
/cast 暗影冲撞
===========================================================================================
=======================         i55        ===========================================
=======================         n205448        ===========================================
/cast 虚空箭
===========================================================================================
=======================         i56        ===========================================
=======================         n228260        ===========================================
/cast 虚空爆发
===========================================================================================
=======================         i57        ===========================================
=======================         n232698        ===========================================
/cast 暗影形态
===========================================================================================
=======================         i58        ===========================================
=======================         n占位3        ===========================================
占位3
===========================================================================================
=======================         i59        ===========================================
=======================         n263165        ===========================================
/cast 虚空洪流
===========================================================================================
=======================         i60        ===========================================
=======================         n271466        ===========================================
/cast 微光屏障
===========================================================================================
=======================         i61        ===========================================
=======================         n335467        ===========================================
/cast 噬灵疫病
===========================================================================================
=======================         i62        ===========================================
=======================         n391109        ===========================================
/cast 黑暗升华
===========================================================================================
=======================         i63        ===========================================
=======================         n391403        ===========================================
/cast 精神鞭笞：狂
===========================================================================================
=======================         i64        ===========================================
=======================         n400169        ===========================================
/cast 黑暗训斥
===========================================================================================
=======================         i65        ===========================================
=======================         n407466        ===========================================
/cast 心灵尖刺
===========================================================================================
=======================         i66        ===========================================
=======================         n421453        ===========================================
/cast 终极苦修
===========================================================================================
=======================         i67        ===========================================
=======================         n450215        ===========================================
/cast 虚空冲击
===========================================================================================
=======================         i68        ===========================================
=======================         n450983        ===========================================
/cast 心灵震爆
===========================================================================================
=======================         i69        ===========================================
=======================         n451235        ===========================================
/cast 虚空幽灵
===========================================================================================
=======================         i70        ===========================================
=======================         n457042        ===========================================
/cast 暗影冲撞
===========================================================================================
=======================         i71        ===========================================
=======================         n大红        ===========================================
/use 阿加治疗药水
===========================================================================================
=======================         i72        ===========================================
=======================         n盾        ===========================================
/cast 真言术：盾
===========================================================================================
=======================         i73        ===========================================
=======================         n福        ===========================================
/cast 福音
===========================================================================================
=======================         i74        ===========================================
=======================         n恢        ===========================================
/cast 恢复
===========================================================================================
=======================         i75        ===========================================
=======================         n快        ===========================================
/cast 快速治疗
===========================================================================================
=======================         i76        ===========================================
=======================         n切换目标        ===========================================
/targetenemy
===========================================================================================
=======================         i77        ===========================================
=======================         n驱        ===========================================
/cast 纯净术
===========================================================================================
=======================         i78        ===========================================
=======================         n驱1        ===========================================
/cast [@player]纯净术
===========================================================================================
=======================         i79        ===========================================
=======================         n驱2        ===========================================
/cast [@party1]纯净术
===========================================================================================
=======================         i80        ===========================================
=======================         n驱3        ===========================================
/cast [@party2]纯净术
===========================================================================================
=======================         i81        ===========================================
=======================         n驱4        ===========================================
/cast [@party3]纯净术
===========================================================================================
=======================         i82        ===========================================
=======================         n驱5        ===========================================
/cast [@party4]纯净术
===========================================================================================
=======================         i83        ===========================================
=======================         n驱M        ===========================================
/cast [@mouseover,help]纯净术
===========================================================================================
=======================         i84        ===========================================
=======================         n上个敌人        ===========================================
/targetlastenemy
===========================================================================================
=======================         i85        ===========================================
=======================         n饰品        ===========================================
/use 13\n/use 14
===========================================================================================
=======================         i86        ===========================================
=======================         n选择敌人        ===========================================
/cleartarget\n/targetenemy
===========================================================================================
=======================         i87        ===========================================
=======================         n耀        ===========================================
/cast 真言术：耀
===========================================================================================
=======================         i88        ===========================================
=======================         n预兆        ===========================================
/cast 预兆
===========================================================================================
=======================         i89        ===========================================
=======================         n治疗石        ===========================================
/use 治疗石
===========================================================================================
=======================         i90        ===========================================
=======================         n中断施法        ===========================================
/stopcasting
===========================================================================================
=======================         i91        ===========================================
=======================         n8122        ===========================================
/cast 心灵尖啸
===========================================================================================
=======================         i92        ===========================================
=======================         n护腕        ===========================================
/use 9
===========================================================================================
=======================         i93        ===========================================
=======================         n恶魔石        ===========================================
/use 恶魔石
===========================================================================================
=======================         main        ===========================================
local Raid = Prop("Raid")
local party = Prop("Party")
local Hekili = Prop("Hekili")
local Trinkets = Prop("Trinkets") == 1
local PriestSpell1s = Prop("PriestSpells")
local Red = Prop("Red")

if Red == 1 then
    Cast("大红")
end
if Red == 2 then
    Cast("护腕")
end
if Red == 3 then
    Cast("恶魔石")
end

if Prop("DesperatePrayer") == 1 then
    Cast("19236")
end
if PriestSpell1s == 10 then -- 终极苦修
    Cast("421453")
end
if PriestSpell1s == 20 then -- 群体驱散，鼠标位置
    Cast("32375")
end
if PriestSpell1s == 30 then -- 福音
    Cast("福")
end
if PriestSpell1s == 40 then -- 真言术：障，鼠标位置
    Cast("62618")
end
if PriestSpell1s == 50 then -- 微光屏障
    Cast("271466")
end
if PriestSpell1s == 60 then -- 心灵尖啸
    Cast("8122")
end

if Prop("纯净") == 1 then
    if Prop("目标驱散") == 1 then
        Cast("驱")
    end
    for i = 1, 5 do
        if Prop("驱散") == i then
            Cast("驱" .. i)
            break
        end
    end
end

--队伍
if party == 3 then
    Cast("中断施法")
else
    if party > 60 and party <= 85 then
        Cast(tostring(party))
    end
    if party == 10 then
        Cast("预兆")
    end
    if party == 11 then
        Cast("耀")
    end
    if party == 12 then
        Cast("福")
    end
    if party == 13 then
        Cast("47540")
    end
    
    if party == 1 then
        if Trinkets then
            Cast("饰品")
        else
            if Hekili >= 1 then
                Cast(tostring(Hekili))
            end
        end
    end
    if party == 2 and Hekili ~= 585 then
        if Trinkets then
            Cast("饰品")
        else
            if Hekili >= 1 then
                Cast(tostring(Hekili))
            end
        end
    end

end


--耐力
if Prop("Buffs") == 1 then
    Cast("21562")
end
if party == 251 or party == 253 then
    if Prop("Trinkets") == 1 then
        Cast("饰品")
    else
        if Hekili >= 1 then
            Cast(tostring(Hekili))
        end
    end
end
Sleep(100)
===========================================================================================
=======================         raidtest        ===========================================
local Raid = Prop("Raid")
local Hekili = Prop("Hekili")
--团队
if Raid >= 6 and Raid <= 45 then
    Select(Raid)
end
if Raid == 46 then
    Cast("上个敌人")
end
if Raid == 50 then
    Cast("耀")
end
if Raid == 51 then
    Cast("盾")
end
if Raid == 52 then
    Cast("福")
end
if Raid == 53 then
    Cast("快")
end
if Raid == 54 then
    Cast("恢")
end
--耐力
if Prop("Buffs") == 1 then
    Cast("21562")
end
if Raid == 1 then
    if Prop("Trinkets") == 1 then
        Cast("饰品")
    else
        if Hekili >= 1 then
            Cast(tostring(Hekili))
        end
    end
end

进程已结束，退出代码为 0
