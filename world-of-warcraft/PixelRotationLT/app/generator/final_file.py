# coding:utf-8
from datetime import datetime
now = datetime.now()


base_code = r"""
SetCVar("scriptErrors", 1);
SetCVar("doNotFlashLowHealthWarning", 1);
SetCVar("cameraIndirectVisibility", 1);
SetCVar("cameraIndirectOffset", 10);


PixelRotationLT = {}
PixelRotationLT.macro_dict = {}

PixelRotationLT.InfoBox = CreateFrame("Frame", nil, UIParent)
PixelRotationLT.InfoBox:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)
PixelRotationLT.InfoBox:SetSize(16, 16)

PixelRotationLT.InfoBox.tex = PixelRotationLT.InfoBox:CreateTexture()
PixelRotationLT.InfoBox.tex:SetAllPoints()

-- 创建文本框并设置位置
PixelRotationLT.InfoBox.textBox = CreateFrame("Frame", nil, UIParent)
PixelRotationLT.InfoBox.textBox:SetPoint("LEFT", PixelRotationLT.InfoBox, "RIGHT", 0, 0)
PixelRotationLT.InfoBox.textBox:SetSize(512, 16)

-- 创建文本
PixelRotationLT.InfoText = PixelRotationLT.InfoBox.textBox:CreateFontString(nil, "OVERLAY", "GameFontNormal")
PixelRotationLT.InfoText:SetPoint("LEFT", PixelRotationLT.InfoBox.textBox, "LEFT", 0, 0)
PixelRotationLT.InfoText:SetFont("Fonts\\FRIZQT__.TTF", 14, nil)

"""

base_code2 = """
PixelRotationLT.MODE = "TANK"

-- 定义一个名为 Cast 的函数，该函数接受一个参数 colorName
PixelRotationLT.Cast = function(colorName)
    -- 从 macro_dict 表中获取颜色信息
    local color = PixelRotationLT.macro_dict[colorName]
    -- 如果颜色信息存在
    if color then
        -- 获取颜色的红、绿、蓝和名称
        local r, g, b, name = color[1], color[2], color[3], color[4]
        -- 设置 InfoBox 的纹理颜色
        PixelRotationLT.InfoBox.tex:SetColorTexture(r / 255, g / 255, b / 255, 1)
        -- 设置 InfoText 的文本内容
        PixelRotationLT.InfoText:SetText(name)
        -- 如果颜色信息不存在
    else
        -- 打印错误信息
        print("颜色名不存在" .. colorName)
    end
end

-- 定义一个名为 Idle 的函数，该函数接受一个参数 title
PixelRotationLT.Idle = function(title)
    -- 设置 InfoBox 的纹理颜色为白色
    PixelRotationLT.InfoBox.tex:SetColorTexture(1, 1, 1, 1)
    -- 设置 InfoText 的文本内容
    PixelRotationLT.InfoText:SetText(title)
end

-- 定义一个名为 GcdRemaining 的函数
PixelRotationLT.GcdRemaining = function()
    -- 获取技能 61304 的冷却信息
    local spellCooldownInfo = C_Spell.GetSpellCooldown(61304)
    -- 如果技能没有冷却时间
    if spellCooldownInfo.duration == 0 then
        -- 返回 0
        return 0
        -- 如果技能有冷却时间
    else
        -- 返回技能剩余冷却时间
        return spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
    end
end


-- 检查技能冷却时间是否小于指定的冷却限制
PixelRotationLT.CoolDown = function(spellName, cooldownLimit)
    -- 获取技能信息
    local spellInfo = C_Spell.GetSpellInfo(spellName)  -- 使用 spellName 而不是 ability_id

    -- 判断技能信息是否存在
    if not spellInfo then
        -- 如果技能信息不存在，打印错误信息并返回
        return print("技能名称 >" .. spellName .. "< 不存在")
    end

    -- 如果没有指定冷却限制，则使用全局冷却时间作为默认值
    if cooldownLimit == nil then
        cooldownLimit = PixelRotationLT.GcdRemaining()
    else
        cooldownLimit = cooldownLimit/1000
    end

    -- 获取技能的冷却信息
    local spellCooldownInfo = C_Spell.GetSpellCooldown(spellInfo.spellID)

    -- 如果技能没有冷却时间，返回 true
    if spellCooldownInfo.duration == 0 then
        return true
    else
        -- 计算技能剩余冷却时间
        local remaining = spellCooldownInfo.startTime + spellCooldownInfo.duration - GetTime()
        -- 返回剩余冷却时间是否小于指定的冷却限制
        return remaining < cooldownLimit
    end
end

PixelRotationLT.Prop = function(key, ...)
    local func = PixelRotationLT[key]
    if func then
        return func(...)
    else
        return print("Prop对象 >" .. key .. "< 不存在") "Function not found!"
    end
end

-- 定义爆发时间为当前时间
PixelRotationLT.burst_time = GetTime();

-- 判断是否处于爆发状态的函数
-- 返回当前时间是否小于等于爆发时间
PixelRotationLT.IsBurst = function()
    -- 返回当前时间是否小于等于爆发时间
    return GetTime() <= PixelRotationLT.burst_time
end

-- 设置爆发时间的函数
-- 将爆发时间设置为当前时间加上传入的时间参数
PixelRotationLT.SetBurst = function(time)
    -- 将爆发时间设置为当前时间加上传入的时间参数
    PixelRotationLT.burst_time = GetTime() + time
end

-- 清除爆发状态的函数
-- 将爆发时间设置为当前时间减去30秒
PixelRotationLT.ClearBurst = function()
    -- 将爆发时间设置为当前时间减去30秒
    PixelRotationLT.burst_time = GetTime() - 30
end

-- 进入战斗时的处理函数
-- 设置爆发时间为25秒
PixelRotationLT.handleEnterCombat = function()
    -- 设置爆发时间为25秒
    PixelRotationLT.SetBurst(25);
end

-- 离开战斗时的处理函数
-- 清除爆发状态
PixelRotationLT.handleLeaveCombat = function()
    -- 清除爆发状态
    PixelRotationLT.ClearBurst();
end

PixelRotationLT.tick = 0

PixelRotationLT.Delay = function(delay)
    PixelRotationLT.tick = GetTime() + delay
    -- 设置 InfoBox 的纹理颜色为白色
    PixelRotationLT.InfoBox.tex:SetColorTexture(1, 1, 1, 1)
    -- 设置 InfoText 的文本内容
    PixelRotationLT.InfoText:SetText("Delay:" .. delay)
end


PixelRotationLT.CanInterruptCast = function(target)
    if not UnitExists(target) then
        return false
    end
    local name, _, _, _, _, _, _, notInterruptible, spellId = UnitCastingInfo(target)
    if name == nil then
        return false
    end
    if PixelRotationLT.InterruptBlacklist[spellId] then
        return false
    end
    if notInterruptible then
        return false
    end
    return true
end


PixelRotationLT.CanInterruptChannel = function(target)
    if not UnitExists(target) then
        return false
    end
    local name, _, _, _, _, _, notInterruptible, spellId, _, _ = UnitChannelInfo(target)
    if name == nil then
        return false
    end
    if PixelRotationLT.InterruptBlacklist[spellId] then
        return false
    end
    if notInterruptible then
        return false
    end
    return true
end

PixelRotationLT.CanInterrupt = function(target)
    return PixelRotationLT.CanInterruptCast(target) or PixelRotationLT.CanInterruptChannel(target)
end


PixelRotationLT.ShouldInterruptCast = function(target)
    if not PixelRotationLT.CanInterruptCast(target) then
        return false
    end
    local _, _, _, _, _, _, _, _, spellId = UnitCastingInfo(target)

    return PixelRotationLT.InterruptSpellList[spellId] or false
end

PixelRotationLT.ShouldInterruptChannel = function(target)
    if not PixelRotationLT.CanInterruptChannel(target) then
        return false
    end
    local _, _, _, _, _, _, _, spellID, _, _ = UnitChannelInfo(target)

    return PixelRotationLT.InterruptSpellList[spellID] or false
end

PixelRotationLT.ShouldInterrupt = function(target)
    return PixelRotationLT.ShouldInterruptCast(target) or PixelRotationLT.ShouldInterruptChannel(target)
end


PixelRotationLT.EnemiesIsImportantSpell = function()
    -- 获取所有可见的名称板
    local nameplates = C_NamePlate.GetNamePlates()
    for _, nameplate in ipairs(nameplates) do
        local unit = nameplate.namePlateUnitToken
        if unit and UnitCanAttack("player", unit) then  -- 检查是否是敌人
            local name, _, _, _, _, _, _, _, spellId = UnitCastingInfo(unit)
            if not name then
                _, _, _, _, _, _, _, spellId, _, _ = UnitChannelInfo(unit)
            end
                       
            -- 如果检测到敌人在释放列表中的技能
            if spellId and PixelRotationLT.ImportantSpellList[spellId] then
                return true
                -- 你可以在这里添加更多的处理逻辑，比如打断或提醒
            end
        end
    end
end


-- 检查全局环境中是否已经存在名为 Delay 的函数
if _G["Delay"] == nil then
    -- 如果不存在，将 PixelRotationLT 模块中的 Delay 函数赋值给全局变量 Delay
    Delay = PixelRotationLT.Delay   -- luacheck: ignore
else
    -- 如果已经存在，打印错误信息，提示用户 Delay 全局函数已被占用，无法使用
    print("Delay全局函数被占用，无法使用/script Delay(x) 设定延迟时间，请使用/script PixelRotationLT.Delay(x)")
end

-- 检查全局环境中是否已经存在名为 SetBurst 的函数
if _G["SetBurst"] == nil then
    -- 如果不存在，将 PixelRotationLT 模块中的 SetBurst 函数赋值给全局变量 SetBurst
    SetBurst = PixelRotationLT.SetBurst   -- luacheck: ignore
else
    -- 如果已经存在，打印错误信息，提示用户 SetBurst 全局函数已被占用，无法使用
    print("SetBurst全局函数被占用，无法使用/script SetBurst(x) 设定爆发时间，请使用/script PixelRotationLT.SetBurst(x)")
end

-- 检查全局环境中是否已经存在名为 ClearBurst 的函数
if _G["ClearBurst"] == nil then
    -- 如果不存在，将 PixelRotationLT 模块中的 ClearBurst 函数赋值给全局变量 ClearBurst
    ClearBurst = PixelRotationLT.ClearBurst     -- luacheck: ignore
else
    -- 如果已经存在，打印错误信息，提示用户 ClearBurst 全局函数已被占用，无法使用
    print("ClearBurst全局函数被占用，无法使用/script ClearBurst() 设定清空爆发，请使用/script PixelRotationLT.ClearBurst()")
end

-- 检查全局环境中是否已经存在名为 CanInterrupt 的函数
if _G["CanInterrupt"] == nil then
    -- 如果不存在，将 PixelRotationLT 模块中的 CanInterrupt 函数赋值给全局变量 CanInterrupt
    CanInterrupt = PixelRotationLT.CanInterrupt     -- luacheck: ignore
else
    -- 如果已经存在，打印错误信息，提示用户 ClearBurst 全局函数已被占用，无法使用
    print("CanInterrupt全局函数被占用，无法使用/script CanInterrupt() 检测能否打断，请使用/script PixelRotationLT.CanInterrupt()")
end

if _G["ShouldInterrupt"] == nil then
    -- 如果不存在，将 PixelRotationLT 模块中的 ShouldInterrupt 函数赋值给全局变量 ShouldInterrupt
    ShouldInterrupt = PixelRotationLT.ShouldInterrupt     -- luacheck: ignore
else
    -- 如果已经存在，打印错误信息，提示用户 ShouldInterrupt 全局函数已被占用，无法使用
    print("ShouldInterrupt全局函数被占用，无法使用/script ShouldInterrupt() 检测能否打断，请使用/script PixelRotationLT.ShouldInterrupt()")
end


"""

trigger_code = r"""
PixelRotationLT.Frame = CreateFrame("Frame", nil, UIParent)
PixelRotationLT.Frame:RegisterEvent("PLAYER_LEAVE_COMBAT")
PixelRotationLT.Frame:RegisterEvent("PLAYER_ENTER_COMBAT")
PixelRotationLT.Frame:RegisterEvent("PLAYER_STARTED_MOVING")
PixelRotationLT.Frame:RegisterEvent("PLAYER_STOPPED_MOVING")
PixelRotationLT.Frame:RegisterEvent("PLAYER_TOTEM_UPDATE")
PixelRotationLT.Frame:RegisterEvent("PLAYER_TARGET_CHANGED")
PixelRotationLT.Frame:RegisterEvent("PLAYER_FOCUS_CHANGED")
PixelRotationLT.Frame:RegisterEvent("PLAYER_DAMAGE_DONE_MODS")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_COMBAT", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_AURA", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_HEALTH", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_START", "player")
PixelRotationLT.Frame:RegisterEvent("UNIT_SPELLCAST_SENT")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_STOP", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_STOP", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_START", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_UPDATE", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_START", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_STOP", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_UPDATE", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTED", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_POWER_UPDATE", "player")
PixelRotationLT.Frame:RegisterUnitEvent("UNIT_POWER_FREQUENT", "player")


-- 定义一个名为 in_combat 的变量，初始值为 false
local in_combat = false

-- 定义一个名为 PixelRotationLT.Main 的函数
PixelRotationLT.Main = function()
    -- 如果当前时间减去 tick 小于 0.01 秒，则返回 false
    if GetTime() - PixelRotationLT.tick < 0.01 then
        return false
    end
    -- 更新 tick 为当前时间
    PixelRotationLT.tick = GetTime()

    -- 如果玩家是否处于战斗状态与 in_combat 不一致
    if UnitAffectingCombat("player") ~= in_combat then
        -- 如果玩家处于战斗状态
        if UnitAffectingCombat("player") then
            -- 调用 PixelRotationLT.handleEnterCombat 函数
            PixelRotationLT.handleEnterCombat()
        -- 如果玩家不处于战斗状态
        else
            -- 调用 PixelRotationLT.handleLeaveCombat 函数
            PixelRotationLT.handleLeaveCombat()
        end
        -- 更新 in_combat 为玩家当前的战斗状态
        in_combat = UnitAffectingCombat("player")
    end

    -- 调用 PixelRotationLT.performBattleLogic 函数
    PixelRotationLT.performBattleLogic()
end -- PixelRotationXLMain

-- 定义一个名为 OnEvent 的本地函数，接受 self、event 和可变参数
local function OnEvent(self, event, ...)
    -- 调用 PixelRotationLT.Main 函数
    PixelRotationLT.Main()
end

-- 为 PixelRotationLT.Frame 设置 OnEvent 脚本，调用 OnEvent 函数
PixelRotationLT.Frame:SetScript("OnEvent", OnEvent)


"""

toc_code = rf"""
## Interface: 110005, 110007, 110100
## Title:  |cffff5900Pixel|cffffb300Rotation|cfff0ff00L|cff96ff00T
## Notes: 神秘插件.
## Version: {now.strftime("%Y.%m.%d")}
## Author: liantian-cn
## IconAtlas: questlog-questtypeicon-weekly
## SavedVariables: PixelRotationLTSettings


PixelRotationLT.lua
"""


def final_file_generator(key_bind, public_func_lua, macro_dict, prop_func, battle_logic):
    lua_code = base_code + key_bind + public_func_lua + base_code2 + macro_dict + prop_func + battle_logic + trigger_code

    return lua_code, toc_code
