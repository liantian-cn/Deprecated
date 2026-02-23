SetCVar("scriptErrors", 1);
SetCVar("doNotFlashLowHealthWarning", 1);
SetCVar("cameraIndirectVisibility", 1);
SetCVar("cameraIndirectOffset", 10);
SetCVar("SpellQueueWindow", 400);
SetCVar("targetNearestDistance", 5)
SetCVar("cameraDistanceMaxZoomFactor", 2.6)
SetCVar("CameraReduceUnexpectedMovement", 1)
SetCVar("synchronizeSettings", 0)
SetCVar("synchronizeConfig", 0)
SetCVar("synchronizeBindings", 0)
SetCVar("synchronizeMacros", 0)
C_AddOns.DisableAddOn("PixelRotationXT", UnitName("player"))
C_AddOns.DisableAddOn("PixelRotationLT", UnitName("player"))
C_AddOns.DisableAddOn("PixelRotation", UnitName("player"))
C_AddOns.DisableAddOn("NewBeeBox", UnitName("player"))

local SpellQueueWindow = tonumber(GetCVar("SpellQueueWindow"));

local configFrame = CreateFrame("Frame", nil, UIParent, "BackdropTemplate")
configFrame:SetPoint("LEFT", UIParent, "LEFT", 0, 200)

-- 背景配置保持不变...
local backdropSettings = {
    bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
    edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
    tile = true,
    tileSize = 32,
    edgeSize = 16,
    insets = { left = 2, right = 2, top = 2, bottom = 2 }
}

configFrame:SetBackdrop(backdropSettings)
configFrame:SetBackdropColor(0, 0, 0, 0.7)
configFrame:SetBackdropBorderColor(0.5, 0.5, 0.5)

local container = CreateFrame("Frame", nil, configFrame)
container:SetWidth(160)
container:SetPoint("TOP", configFrame, "TOP", 0, -5) -- 顶部边距设置为5
container.lines = {}

-- 全局变量
ShionVars = {}
-- 所有checkBox
ShionCB = {}



-- 技能配置
ShionSpellMacro = {};
ShionSpellMacro["重载"] = { 0, 0, 0, "/reload", "ALT-F12" };
-- /script ShionCast("重载")

-- 自动计算尺寸的核心函数
local function UpdateFrameSize()
    local totalHeight = 5
    for _, line in ipairs(container.lines) do
        totalHeight = totalHeight + line:GetHeight() + 5
    end
    container:SetHeight(totalHeight)
    configFrame:SetSize(180, totalHeight + 10)
end

-- 创建行的函数
local function CreateLine(text, envKey, funcKey)
    local lastLine = #container.lines > 0 and container.lines[#container.lines] or nil

    local line = CreateFrame("Frame", nil, container)
    line:SetSize(160, 30)
    line:SetPoint("TOP", lastLine or container, lastLine and "BOTTOM" or "TOP", 0, lastLine and -5 or 0)

    local title = line:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    title:SetText(text)
    title:SetPoint("LEFT", 5, 0)

    ShionCB[envKey] = CreateFrame("CheckButton", nil, line, "UICheckButtonTemplate")
    local checkbox = ShionCB[envKey]
    checkbox:SetPoint("RIGHT", -5, 0)
    checkbox:SetChecked(ShionVars[envKey])

    checkbox:SetScript("OnClick", function(self)
        funcKey()
        print(string.format("选项 [%s] 状态已更新为：%s", text, tostring(ShionVars[envKey])));
    end)

    container.lines = container.lines or {}
    table.insert(container.lines, line) -- 注：这里不再需要 utable.lines 的判断
    UpdateFrameSize()
end



-- 左上角的方框和文字
local pixelFrame = CreateFrame("Frame", nil, UIParent)
pixelFrame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)
pixelFrame:SetSize(16, 16)
pixelFrame.tex = pixelFrame:CreateTexture()
pixelFrame.tex:SetAllPoints()
pixelFrame.textBox = CreateFrame("Frame", nil, UIParent)
pixelFrame.textBox:SetPoint("LEFT", pixelFrame, "RIGHT", 0, 0)
pixelFrame.textBox:SetSize(512, 16)

local infoFrame = pixelFrame.textBox:CreateFontString(nil, "OVERLAY", "GameFontNormal")
infoFrame:SetPoint("LEFT", pixelFrame.textBox, "LEFT", 0, 0)
infoFrame:SetFont("Fonts\\FRIZQT__.TTF", 14, nil)





-- 第一个参数：全局启动
ShionVars["GlobalStart"] = true;
local function ToggleGlobalStart()
    ShionVars["GlobalStart"] = not ShionVars["GlobalStart"];
    ShionCB["GlobalStart"]:SetChecked(ShionVars["GlobalStart"]);
    if ShionVars["GlobalStart"] then
        pixelFrame.tex:SetColorTexture(0 / 255, 0 / 255, 0 / 255, 1)
        infoFrame:SetText("Shion Enable")
    end
    if not ShionVars["GlobalStart"] then
        pixelFrame.tex:SetColorTexture(255 / 255, 255 / 255, 255 / 255, 1)
        infoFrame:SetText("Shion Disable")
    end
end
CreateLine("启动Shion", "GlobalStart", ToggleGlobalStart)

ShionVars["GlobalDEBUG"] = false;
local function ToggleGlobalDEBUG()
    ShionVars["GlobalDEBUG"] = not ShionVars["GlobalDEBUG"];
    ShionCB["GlobalDEBUG"]:SetChecked(ShionVars["GlobalDEBUG"]);
end
CreateLine("全局DEBUG", "GlobalDEBUG", ToggleGlobalDEBUG)

local function RegisterMacro()
    for key, value in pairs(ShionSpellMacro) do
        local r, g, b, macro, keybind = unpack(value)
        local buttonName = string.format("button_%s", key)
        local frame = CreateFrame("Button", buttonName, UIParent, "SecureActionButtonTemplate");
        frame:SetAttribute("type", "macro");
        frame:SetAttribute("macrotext", macro);
        frame:RegisterForClicks("AnyDown", "AnyUp");
        SetOverrideBindingClick(frame, true, keybind, buttonName);
    end
end

function ShionCast(macroName)
    -- 从 macro_dict 表中获取颜色信息
    local color = ShionSpellMacro[macroName]
    -- 如果颜色信息存在
    if color then
        -- 获取颜色的红、绿、蓝和名称
        local r, g, b, macro, keybind = unpack(color)
        pixelFrame.tex:SetColorTexture(r / 255, g / 255, b / 255, 1)
        infoFrame:SetText(macroName)
    else
        -- 打印错误信息
        print("红不存在" .. macroName)
    end
end

function ShionIdle(title)
    pixelFrame.tex:SetColorTexture(1, 1, 1, 1)
    infoFrame:SetText(title)
end

if _G["Cast"] == nil then
    Cast = ShionCast
else
    print("Cast全局函数被占用")
    local Cast = ShionCast
end

if _G["Idle"] == nil then
    Idle = ShionIdle
else
    print("Idle全局函数被占用")
    local Idle = ShionIdle
end

local function GcdRemaining()
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

local function CoolDown(spell_id, cooldownLimit)

    if ShionVars["GlobalDEBUG"] then
        if not IsSpellKnownOrOverridesKnown(spell_id) then
            print("不在技能列表的技能id: " .. tostring(spell_id))
        end
    end
    -- 如果没有指定冷却限制，则使用全局冷却时间作为默认值
    if cooldownLimit == nil then
        cooldownLimit = SpellQueueWindow / 1000
    else
        cooldownLimit = cooldownLimit / 1000
    end

    local spellCooldownInfo = C_Spell.GetSpellCooldown(spell_id)

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

-- 延迟控制
local tick = 0
function ShionDelay(delay)
    tick = GetTime() + delay
    pixelFrame.tex:SetColorTexture(1, 1, 1, 1)
    infoFrame:SetText("Delay:" .. delay)
end
if _G["Delay"] == nil then
    Delay = ShionDelay
else
    print("Delay全局函数被占用")
    local Delay = ShionDelay
end


