from string import Template

from app.common.utils import replace_keys

template_string = """

local Prop = PixelRotationLT.Prop
local Idle = PixelRotationLT.Idle
local CoolDown = PixelRotationLT.CoolDown
local Cast = PixelRotationLT.Cast

PixelRotationLT["performBattleLogic"] = function()
$code
end
"""
template = Template(template_string)


def battle_logic_generator(profile, props, macros):
    macro_mapping = {}
    for macro in macros:
        title = macro["title"]
        macro_name = macro["macro_name"]
        macro_mapping[title] = macro_name

    prop_mapping = {}
    for prop in props:
        title = prop["title"]
        func_name = prop["func_name"]
        prop_mapping[title] = func_name

    rotation_text = profile.get("rotation")
    # battle_logic = replace_property_in_text(text=rotation_text, key="Prop", mapping=prop_mapping)
    battle_logic = replace_keys(text=rotation_text, key="Prop", mapping=prop_mapping)
    # print(battle_logic)
    # print("===================")
    battle_logic = replace_keys(text=battle_logic, key="Cast", mapping=macro_mapping)
    # print(battle_logic)
    # print("===================")

    code = "\n".join([" " * 4 + line for line in battle_logic.splitlines()])

    result = template.substitute({
        "code": code,
    })

    return result
