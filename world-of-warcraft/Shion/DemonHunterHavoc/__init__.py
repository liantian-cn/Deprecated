import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    '刃舞': "/cast 刃舞",
    '怨念咒符脚下': "/cast [@player] 怨念咒符",
    '恶魔变身原地': "/cast [@player] 恶魔变形",
    '投掷利刃': "/cast 投掷利刃",
    '排气臂铠护腕': "/use 9",
    '收割者战刃': "/cast 收割者战刃",
    '眼棱': "/cast 眼棱",
    '死亡横扫': "/cast 刃舞",
    '毁灭': "/cast 混乱打击",
    '混乱打击': "/cast 混乱打击",
    '烈焰咒符脚下': "/use [@player] 烈焰咒符",
    '献祭光环': "/cast 献祭光环",
    '瓦解焦点': "/cast [@focus] 瓦解",
    '瓦解目标': "/cast 瓦解",
    '邪能之刃': "/cast 邪能之刃",
    '精华破碎': "/cast 精华破碎",
    '恶魔追击': "/cast 恶魔追击",
    '13号饰品': "/use 13",
    '14号饰品': "/use 14",
}
spell_list = [
    {
        "title": "打断技能清单",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "MeleeDPSInterruptSpellList"
    },
    {
        "title": "打断技能黑名单",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "MeleeDPSInterruptBlacklist"
    },
]