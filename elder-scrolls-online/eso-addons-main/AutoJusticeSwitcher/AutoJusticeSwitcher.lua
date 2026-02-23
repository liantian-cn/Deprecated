
AutoJusticeSwitcher = {}
 
AutoJusticeSwitcher.name = "AutoJusticeSwitcher"

AutoJusticeSwitcher.previous_zoneid = 1

function AutoJusticeSwitcher.PlayerLoaded(eventCode, initial)
    local crimeZones = {769, 765, 766}
	zoneId,worldX,worldY,worldZ = GetUnitWorldPosition("player")
    local function isInCrimeZone(id)
        for _, v in ipairs(crimeZones) do
            if v == id then return true end
        end
        return false
    end

    if isInCrimeZone(zoneId)  then
        SetSetting(SETTING_TYPE_COMBAT, COMBAT_SETTING_PREVENT_ATTACKING_INNOCENTS, "0")
		zo_callLater(function() d("避免攻击无辜者已|cFF5733关闭|r") end, 300)
    else
        SetSetting(SETTING_TYPE_COMBAT, COMBAT_SETTING_PREVENT_ATTACKING_INNOCENTS, "1")
		zo_callLater(function() d("避免攻击无辜者已|c68F400开启|r") end, 300)
    end

    AutoJusticeSwitcher.previous_zoneid = zoneId
end

function AutoJusticeSwitcher.Initialize()
	
	
	EVENT_MANAGER:RegisterForEvent(AutoJusticeSwitcher.name, EVENT_PLAYER_ACTIVATED, AutoJusticeSwitcher.PlayerLoaded)
end

function AutoJusticeSwitcher.OnAddOnLoaded(event, addonName)
  if addonName == AutoJusticeSwitcher.name then
    AutoJusticeSwitcher.Initialize()

    EVENT_MANAGER:UnregisterForEvent(AutoJusticeSwitcher.name, EVENT_ADD_ON_LOADED) 
  end
end
 
EVENT_MANAGER:RegisterForEvent(AutoJusticeSwitcher.name, EVENT_ADD_ON_LOADED, AutoJusticeSwitcher.OnAddOnLoaded)
