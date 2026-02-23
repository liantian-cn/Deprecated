import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    "target痛": "/cast [@target] 暗言术：痛",
    "target灭": "/cast [@target] 暗言术：灭",
    "target心灵震爆": "/cast [@target] 心灵震爆",
    "target暗影魔": "/cast [@target] 暗影魔",
    "target惩击": "/cast [@target] 惩击",
    "focus痛": "/cast [@focus] 暗言术：痛",
    "focus灭": "/cast [@focus] 暗言术：灭",
    "focus心灵震爆": "/cast [@focus] 心灵震爆",
    "focus暗影魔": "/cast [@focus] 暗影魔",
    "focus惩击": "/cast [@focus] 惩击",
    'player盾': "/cast [@player] 真言术：盾",
    'party1盾': "/cast [@party1] 真言术：盾",
    'party2盾': "/cast [@party2] 真言术：盾",
    'party3盾': "/cast [@party3] 真言术：盾",
    'party4盾': "/cast [@party4] 真言术：盾",
    "target苦修": "/cast [@target] 苦修",
    "focus苦修": "/cast [@focus] 苦修",
    'player苦修': "/cast [@player] 苦修",
    'party1苦修': "/cast [@party1] 苦修",
    'party2苦修': "/cast [@party2] 苦修",
    'party3苦修': "/cast [@party3] 苦修",
    'party4苦修': "/cast [@party4] 苦修",
    'player恢复': "/cast [@player] 恢复",
    'party1恢复': "/cast [@party1] 恢复",
    'party2恢复': "/cast [@party2] 恢复",
    'party3恢复': "/cast [@party3] 恢复",
    'party4恢复': "/cast [@party4] 恢复",
    'player纯净术': "/cast [@player] 纯净术",
    'party1纯净术': "/cast [@party1] 纯净术",
    'party2纯净术': "/cast [@party2] 纯净术",
    'party3纯净术': "/cast [@party3] 纯净术",
    'party4纯净术': "/cast [@party4] 纯净术",
    'mouseover纯净术': "/cast [@mouseover] 纯净术",
    'player快速治疗': "/cast [@player] 快速治疗",
    'party1快速治疗': "/cast [@party1] 快速治疗",
    'party2快速治疗': "/cast [@party2] 快速治疗",
    'party3快速治疗': "/cast [@party3] 快速治疗",
    'party4快速治疗': "/cast [@party4] 快速治疗",
    '切换目标': "/cleartarget\n/targetenemy",
    '虔诚预兆': "/cast 虔诚预兆",
    '慰藉预兆': "/cast 慰藉预兆",
    '洞察预兆': "/cast 洞察预兆",
    '远见预兆': "/cast 远见预兆",
    '耀': "/cast [@player] 真言术：耀",
    '绝望祷言': "/cast [@player] 绝望祷言",
    '耐力': "/cast [@player] 真言术：韧",
    '预兆': "/cast 预兆",
}

spell_list = [
    {
        "title": "需要预兆覆盖的技能列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "requiredPremonitionList"
    },
    {
        "title": "会爆炸的魔法减益列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "ExplodeDispelMagicDebuffList"
    },
    {
        "title": "秒驱散的魔法减益列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "InstantDispelMagicDebuffList"
    },
    {
        "title": "手动驱散魔法减益列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "ManualDispelMagicDebuffList"
    },
    {
        "title": "高伤害减益效果列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "HighDamageDebuffList"
    },
    {
        "title": "中等伤害减益效果列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "MidDamageDebuffList"
    },
    {
        "title": "怪物打断玩家的技能列表",
        "placeholder": "请输入技能ID，用逗号分隔",
        "code": "EnemyInterruptsCastsList"
    }

]