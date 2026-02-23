import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    '就近灵界打击': "/cleartarget\n/targetenemy\n/cast 灵界打击\n/targetlasttarget",
    '灵界打击': "/cast 灵界打击",
    '就近精髓分裂': "/cleartarget\n/targetenemy\n/cast 精髓分裂\n/targetlasttarget",
    '精髓分裂': "/cast 精髓分裂",
    '死亡凋零': "/cast [@player] 枯萎凋零",
    '死神印记': "/cast 死神印记",
    '死神的抚摩': "/cast 死神的抚摩",
    '吞噬': "/cast 吞噬",
    '工程护腕': "/use 9",
    '心灵冰冻焦点': "/cast [target=focus] 心灵冰冻",
    '心灵冰冻目标': "/cast 心灵冰冻",
    '亡者复生': "/cast 亡者复生",
    '灵魂收割': "/cast 灵魂收割",
    '墓石': "/cast 墓石",
    '白骨风暴': "/cast 白骨风暴",
    '血液沸腾': "/cast 血液沸腾",
    '心脏打击': "/cast 心脏打击",
    '就近心脏打击': "/cleartarget\n/targetenemy\n/cast 心脏打击\n/targetlasttarget",
}
spell_list = [
    # {
    #     "title": "打断技能清单",
    #     "placeholder": "请输入技能ID，用逗号分隔",
    #     "code": "MeleeDPSInterruptSpellList"
    # }
]