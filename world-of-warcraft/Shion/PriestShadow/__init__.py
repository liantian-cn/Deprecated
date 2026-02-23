import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    '13号饰品': "/use 13",
    '14号饰品': "/use 14",
    '[光晕]': "/cast 光晕",
    '[吸血鬼之触]': "/cast [@target] 吸血鬼之触",
    '[吸血鬼的拥抱]': "/cast 吸血鬼的拥抱",
    '[噬灵疫病]': "/cast [@target] 噬灵疫病",
    '[心灵震爆]': "/cast [@target] 心灵震爆",
    '[虚空冲击]': "/cast [@target] 心灵震爆",
    '[心灵尖刺]': "/cast [@target] 精神鞭笞",
    '[心灵尖刺：狂]': "/cast [@target] 精神鞭笞",
    '[快速治疗]': "/cast [@player ]快速治疗",
    '[暗影冲撞]': "/cast [@target] 暗影冲撞",
    '[暗影形态]': "/cast  暗影形态",
    '[暗影魔]': "/cast [@target] 暗影魔",
    '[暗言术：灭]': "/cast [@target] 暗言术：灭",
    '[暗言术：痛]': "/cast [@target] 暗言术：痛",
    '[沉默]': "/cast [@target] 沉默",
    '[消散]': "/cast 消散",
    '[渐隐术]': "/cast 渐隐术",
    '[真言术：盾]': "/cast [@player] 真言术：盾",
    '[真言术：韧]': "/cast [@player] 真言术：韧",
    '[神圣新星]': "/cast 神圣新星",
    '[精神鞭笞]': "/cast [@target] 精神鞭笞",
    '[绝望祷言]': "/cast [@player] 绝望祷言",
    '[能量灌注]': "/cast [@player] 能量灌注",
    '[虚空洪流]': "/cast [@target] 虚空洪流",
    '[虚空爆发]': "/cast [@target] 虚空爆发",
    '[驱散魔法]': "/cast [@target] 驱散魔法",
    '[虚空箭]': "/cast [@target] 虚空箭",
    '[黑暗升华]': "/cast [@target] 黑暗升华",
    '[精神鞭笞：狂]': "/cast [@target] 精神鞭笞：狂",
    '切换目标': "/targetenemy",

}
spell_list = [
]
