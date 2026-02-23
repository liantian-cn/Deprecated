import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    '幽魂炸弹': "/cast 幽魂炸弹\n/cast 恶魔尖刺",
    '怨念咒符脚下': "/cast [@player] 怨念咒符",
    '恶魔尖刺': "/cast 恶魔尖刺",
    '投掷利刃': "/cast 投掷利刃",
    '排气臂铠护腕': "/use 9",
    '收割者战刃': "/cast 收割者战刃\n/cast 恶魔尖刺",
    '灵魂裂劈': "/cast 灵魂裂劈\n/cast 恶魔尖刺",
    '就近灵魂裂劈': "/cleartarget\n/targetenemy\n/cast 灵魂裂劈\n/targetlasttarget\n/cast 恶魔尖刺",
    '烈火烙印': "/cast 烈火烙印",
    '烈焰咒符脚下': "/use [@player] 烈焰咒符",
    '献祭光环': "/cast 献祭光环\n/cast 恶魔尖刺",
    '瓦解焦点': "/cast [@focus] 瓦解",
    '瓦解目标': "/cast 瓦解",
    '破裂': "/cast 破裂\n/cast 恶魔尖刺",
    '就近破裂': "/cleartarget\n/targetenemy\n/cast 破裂\n/targetlasttarget\n/cast 恶魔尖刺",
    '邪能之刃': "/cast 邪能之刃",
    '就近邪能之刃': "/cleartarget\n/targetenemy\n/cast 邪能之刃\n/targetlasttarget\n/cast 恶魔尖刺",
    '邪能毁灭': "/cast 邪能毁灭",
    '圣光虔敬魔典': "/use 13",
    '13号饰品': "/use 13",
    '14号饰品': "/use 14",
    '恶魔变形': "/cast 恶魔变形",
    '灵魂切削': "/cast 灵魂切削",
}

spell_list = [
    {
        "title": "打断技能清单",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "VDHInterruptSpellList"
    },
    {
        "title": "打断技能黑名单",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "VDHInterruptBlacklist"
    },
    {
        "title": "坦克尖刺伤害",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "VDHTankOutburstDamage"
    },
    {
        "title": "坦克减伤技能或增益",
        "placeholder": "请输入技能ID，用逗号分隔。释放or获得后则认为尖刺伤害规避",
        "code": "VDHTankSustainedDamage"
    }

]
