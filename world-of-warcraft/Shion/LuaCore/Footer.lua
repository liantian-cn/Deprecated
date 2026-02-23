
RegisterMacro()

local main_frame = CreateFrame("Frame", nil, UIParent)
--main_frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
main_frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
main_frame:RegisterEvent("PLAYER_LEAVE_COMBAT")
main_frame:RegisterEvent("PLAYER_ENTER_COMBAT")
main_frame:RegisterEvent("PLAYER_STARTED_MOVING")
main_frame:RegisterEvent("PLAYER_STOPPED_MOVING")
main_frame:RegisterEvent("PLAYER_TOTEM_UPDATE")
main_frame:RegisterEvent("PLAYER_TARGET_CHANGED")
main_frame:RegisterEvent("PLAYER_FOCUS_CHANGED")
main_frame:RegisterEvent("PLAYER_DAMAGE_DONE_MODS")
main_frame:RegisterUnitEvent("UNIT_COMBAT", "player")
main_frame:RegisterUnitEvent("UNIT_AURA", "player")
main_frame:RegisterUnitEvent("UNIT_HEALTH", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_START", "player")
main_frame:RegisterEvent("UNIT_SPELLCAST_SENT")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_SUCCEEDED", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_FAILED", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_STOP", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_STOP", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_START", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_CHANNEL_UPDATE", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_START", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_STOP", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_EMPOWER_UPDATE", "player")
main_frame:RegisterUnitEvent("UNIT_SPELLCAST_INTERRUPTED", "player")
main_frame:RegisterUnitEvent("UNIT_POWER_UPDATE", "player")
main_frame:RegisterUnitEvent("UNIT_POWER_FREQUENT", "player")

local tick = GetTime()

main_frame:SetScript("OnEvent", function(self, event, ...)
    if tick < GetTime() then
        tick = GetTime() + 0.05
    else
        return
    end
    --if ShionVars["DEBUG"] then
    --    print(tick)
    --end
    if ShionVars["GlobalStart"] then
        main_rotation()
    else
        Idle("Shion未启动")
    end
end)
