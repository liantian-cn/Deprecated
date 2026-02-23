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

--玩家在施法读条
local function checkPlayerIsCasting()
    local name, _, _, _, endTimeMs, _, _, _, _, _ = UnitChannelInfo("player")
    if name then
        return (GetTime() * 1000 + SpellQueueWindow) < endTimeMs
    end

    name, _, _, _, endTimeMs, _, _, _, _ = UnitCastingInfo("player")
    if name then
        return (GetTime() * 1000 + SpellQueueWindow) < endTimeMs
    end
    return false

end

--与玩家敌对
local function checkIsEnemy(targetUnit)
    return UnitCanAttack("player", targetUnit)
end




-- ------------------------------
-- 爆发控制
-- 爆发控制
local burst_mode = false;
local entry_combat_timer = GetTime();
local function SetBurst()
    burst_mode = true;
    if Hekili.DB.profile.toggles.cooldowns.value == false then
        Hekili:FireToggle("cooldowns")
    end
    if Hekili.DB.profile.toggles.essences.value == false then
        Hekili:FireToggle("essences")
    end

end

local function ClearBurst()
    burst_mode = false;
    if Hekili.DB.profile.toggles.cooldowns.value == true then
        Hekili:FireToggle("cooldowns")
    end
    if Hekili.DB.profile.toggles.essences.value == true then
        Hekili:FireToggle("essences")
    end
end

ShionVars["AutoBurst"] = true;
local function ToggleAutoBurst()
    ShionVars["AutoBurst"] = not ShionVars["AutoBurst"];
    ShionCB["AutoBurst"]:SetChecked(ShionVars["AutoBurst"]);
end
CreateLine("自动爆发", "AutoBurst", ToggleAutoBurst)

ShionVars["AutoMode"] = false;
local function ToggleAutoMode()
    ShionVars["AutoMode"] = not ShionVars["AutoMode"];
    ShionCB["AutoMode"]:SetChecked(ShionVars["AutoMode"]);
    if ShionCB["AutoMode"] then
        Hekili.DB.profile.toggles.mode.value = "automatic"
        Hekili:UpdateDisplayVisibility()
        Hekili:ForceUpdate("HEKILI_TOGGLE", true)
        if ShionVars["SingleMode"] then
            ShionVars["SingleMode"] = false;
            ShionCB["SingleMode"]:SetChecked(false);
        end
        if ShionVars["AoeMode"] then
            ShionVars["AoeMode"] = false;
            ShionCB["AoeMode"]:SetChecked(false);
        end
    end
end
CreateLine("自动模式", "AutoMode", ToggleAutoMode)

ShionVars["SingleMode"] = false;
local function ToggleSingleMode()
    ShionVars["SingleMode"] = not ShionVars["SingleMode"];
    ShionCB["SingleMode"]:SetChecked(ShionVars["SingleMode"]);
    if ShionCB["SingleMode"] then
        Hekili.DB.profile.toggles.mode.value = "single"
        Hekili:UpdateDisplayVisibility()
        Hekili:ForceUpdate("HEKILI_TOGGLE", true)
        if ShionVars["AoeMode"] then
            ShionVars["AoeMode"] = false;
            ShionCB["AoeMode"]:SetChecked(false);
        end
        if ShionVars["AutoMode"] then
            ShionVars["AutoMode"] = false;
            ShionCB["AutoMode"]:SetChecked(false);
        end
    end
end
CreateLine("单体模式", "SingleMode", ToggleSingleMode)

ShionVars["AoeMode"] = false;
local function ToggleAoeMode()
    ShionVars["AoeMode"] = not ShionVars["AoeMode"];
    ShionCB["AoeMode"]:SetChecked(ShionVars["AoeMode"]);
    if ShionCB["AoeMode"] then
        Hekili.DB.profile.toggles.mode.value = "aoe"
        Hekili:UpdateDisplayVisibility()
        Hekili:ForceUpdate("HEKILI_TOGGLE", true)
        if ShionVars["SingleMode"] then
            ShionVars["SingleMode"] = false;
            ShionCB["SingleMode"]:SetChecked(false);
        end
        if ShionVars["AutoMode"] then
            ShionVars["AutoMode"] = false;
            ShionCB["AutoMode"]:SetChecked(false);
        end
    end
end
CreateLine("AOE模式", "AoeMode", ToggleAoeMode)

-- local function checkIsAOE()


local VDH_eventFrame = CreateFrame("Frame")
VDH_eventFrame:RegisterEvent("PLAYER_LEAVE_COMBAT")
VDH_eventFrame:RegisterEvent("PLAYER_ENTER_COMBAT")
VDH_eventFrame:SetScript("OnEvent", function(self, event, ...)
    self[event](self, ...)
end)

function VDH_eventFrame:PLAYER_LEAVE_COMBAT()
    entry_combat_timer = GetTime() - 1200;
    if ShionVars["AutoBurst"] then
        ClearBurst();
    end
end

function VDH_eventFrame:PLAYER_ENTER_COMBAT()
    entry_combat_timer = GetTime();
    if ShionVars["AutoBurst"] then
        SetBurst();
    end
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
    local className, classFilename, classId = UnitClass("player")
    local currentSpec = GetSpecialization()
    if not (classFilename == "PRIEST" and currentSpec == 3) then
        return Idle("专精不匹配")
    end


    -- 不在战斗，则不做任何事
    local isPlayerInCombat = checkInCombat("player")
    if not isPlayerInCombat then
        return Idle("玩家不在战斗")
    end

    --local mapInfo = C_Map.GetMapInfo(C_Map.GetBestMapForUnit("player"))
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

    if Hekili.DB.profile.enabled == false then
        Hekili:Toggle()
    end

    if ShionVars["AutoBurst"] then
        if (GetTime() - entry_combat_timer > 25) and (burst_mode == true) then
            ClearBurst();
        end
    end

    local ability_id1, err1, info1 = Hekili_GetRecommendedAbility("Primary", 1)

    local ability_id = ability_id1
    if ability_id == nil then
        return Idle("没有推荐技能")
    end

    --if info1.indicator then
    --    return Cast("切换目标")
    --end

    if PlayerIsCasting then
        return Idle("玩家在施法读条")
    end

    if ability_id == 34914 then
        return Cast("[吸血鬼之触]")
    elseif ability_id == 232698 then
        return Cast("[暗影形态]")
    elseif ability_id == 15407 then
        return Cast("[精神鞭笞]")
        --elseif (ability_id < 0) and Ticket13Usable() then
        --    return Cast("13号饰品")
        --elseif (ability_id < 0) and Ticket14Usable() then
        --    return Cast("14号饰品")
    elseif ability_id == 335467 then
        return Cast("[噬灵疫病]")
    elseif ability_id == 15487 then
        return Cast("[沉默]")
    elseif ability_id == 263165 then
        return Cast("[虚空洪流]")
    elseif ability_id == 457042 then
        return Cast("[暗影冲撞]")
    elseif ability_id == 391109 then
        return Cast("[黑暗升华]")
    elseif ability_id == 47585 then

        return Cast("[消散]")
    elseif ability_id == 228260 then
        return Cast("[虚空爆发]")
    elseif ability_id == 8092 then
        return Cast("[心灵震爆]")
    elseif ability_id == 450983 then
        return Cast("[虚空冲击]")
    elseif ability_id == 73510 then
        return Cast("[心灵尖刺]")
    elseif ability_id == 407466 then
        return Cast("[心灵尖刺：狂]")
    elseif ability_id == 21562 then
        return Cast("[真言术：韧]")
    elseif ability_id == 120644 then
        return Cast("[光晕]")
    elseif ability_id == 2061 then
        return Cast("[快速治疗]")
    elseif ability_id == 132157 then
        return Cast("[神圣新星]")
    elseif ability_id == 15286 then
        return Cast("[吸血鬼的拥抱]")
    elseif ability_id == 34433 then
        return Cast("[暗影魔]")
    elseif ability_id == 19236 then
        return Cast("[绝望祷言]")
    elseif ability_id == 32379 then
        return Cast("[暗言术：灭]")
    elseif ability_id == 589 then
        return Cast("[暗言术：痛]")
    elseif ability_id == 10060 then
        return Cast("[能量灌注]")
    elseif ability_id == 586 then
        return Cast("[渐隐术]")
    elseif ability_id == 205448 then
        return Cast("[虚空箭]")
    elseif ability_id == 205385 then
        return Cast("[暗影冲撞]")
    elseif ability_id == 17 then
        return Cast("[真言术：盾]")
    elseif ability_id == 528 then
        return Cast("[驱散魔法]")
    elseif ability_id == 391403 then
        return Cast("[精神鞭笞：狂]")
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

ToggleAutoMode()