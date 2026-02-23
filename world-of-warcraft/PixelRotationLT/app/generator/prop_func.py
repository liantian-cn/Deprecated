from string import Template

template_string = """
PixelRotationLT["$func_name"] = function($args)
    -- $title
    -- USE: /dump PixelRotationLT["$func_name"]()
    -- USE: /dump PixelRotationLT.$func_name()
    -- USE: /dump PixelRotationLT.Prop("$func_name")
    
$code
end
"""
template = Template(template_string)


def prop_func_generator(props):
    result = ""
    for prop in props:
        code = prop["code"]
        code = "\n".join([" " * 4 + line for line in code.splitlines()])
        title = prop["title"]
        func_name = prop["func_name"]
        func_args = ",".join(prop["func_args"])
        result += template.substitute({
            "title": title,
            "func_name": func_name,
            "code": code,
            "args": func_args
        })
    return result
