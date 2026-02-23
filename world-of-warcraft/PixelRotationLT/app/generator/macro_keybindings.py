from string import Template

template_string = """
local $macroBtn = CreateFrame("Button", "$button_name", UIParent, "SecureActionButtonTemplate");
$macroBtn:SetAttribute("type", "macro");
$macroBtn:SetAttribute("macrotext", "$macro_text");
$macroBtn:RegisterForClicks("AnyDown", "AnyUp");
SetOverrideBindingClick($macroBtn, true, "$key_binding", "$button_name");
"""
template = Template(template_string)


def macro_keybindings_generator(macros):
    result = ""
    for macro in macros:
        result += template.substitute({
            "macroBtn": macro["frame_name"],
            "button_name": macro["btn_name"],
            "macro_text": "\\n".join(macro["code"].split("\n")),
            "key_binding": macro["key"]
        })
    return result
