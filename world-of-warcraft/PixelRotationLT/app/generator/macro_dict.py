def macro_dict_generator(macros):
    result = ""
    for macro in macros:
        r, g, b = macro["color"].split(",")
        title = macro["title"]
        macro_name = macro["macro_name"]
        result += f"-- USE: /dump PixelRotationLT.Cast(\"{macro_name}\")\n"
        result += f"PixelRotationLT.macro_dict[\"{macro_name}\"] = {{ {r}, {g}, {b} , \"{title}\" }}\n"
    return result
