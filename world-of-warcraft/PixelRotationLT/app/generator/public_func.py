def interrupt_spell_list_generator(interrupt_spell_list):
    result = ""
    result += "PixelRotationLT.InterruptSpellList  = {\n"
    for spell_id in interrupt_spell_list:
        result += f"    [{spell_id}] = true,\n"
    result += "};\n"
    return result


def interrupt_black_list_generator(interrupt_black_list):
    result = ""
    result += "PixelRotationLT.InterruptBlacklist = {\n"
    for spell_id in interrupt_black_list:
        result += f"    [{spell_id}] = true,\n"
    result += "};\n"
    return result


def important_spell_list_generator(important_spell_list):
    print(important_spell_list)
    result = ""
    result += "PixelRotationLT.ImportantSpellList = {\n"
    for spell_id in important_spell_list:
        result += f"    [{spell_id}] = true,\n"
    result += "};\n"
    return result


# "": [],
# "interrupt_black_list": [],
# "important_spell_list": []


def public_func_generator(interrupt_spell_list, important_spell_list, interrupt_black_list):
    result = ""
    result += interrupt_spell_list_generator(interrupt_spell_list)
    result += important_spell_list_generator(important_spell_list)
    result += interrupt_black_list_generator(interrupt_black_list)
    return result
