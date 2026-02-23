import pathlib

rotation_path = pathlib.Path(__file__).parent.joinpath("rotation.lua")

rotation_content = open(rotation_path, "r", encoding="utf-8").read()

rotation_macros = {
    '心灵冰冻焦点': "/cast [@focus] 心灵冰冻",
    '心灵冰冻目标': "/cast 心灵冰冻",
    '巫妖之躯': "/cast 巫妖之躯",
    '冰封之韧': "/cast 冰封之韧",
    '心灵冰冻': "/cast 心灵冰冻",
    '凋零缠绕': "/cast 凋零缠绕",
    '憎恶附肢': "/cast 憎恶附肢",
    '复活盟友': "/cast 复活盟友",
    '灵界打击': "/cast 灵界打击",
    '亡者复生': "/cast 亡者复生",
    '扩散': "/cast 扩散",
    '邪恶突袭': "/cast 邪恶突袭",
    '亵渎': "/cast [@player] 亵渎",
    '爆发': "/cast 爆发",
    '黑暗突变': "/cast 黑暗突变",
    '天灾打击': "/cast 天灾打击",
    '吸血鬼打击': "/cast 天灾打击",
    '脓疮打击': "/cast 脓疮打击",
    '脓疮毒镰': "/cast 脓疮打击",
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