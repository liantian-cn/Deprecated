import pathlib


lua_01_header = open(pathlib.Path(__file__).parent.joinpath("Header.lua"), "r", encoding="utf-8").read()
lua_04_footer = open(pathlib.Path(__file__).parent.joinpath("Footer.lua"), "r", encoding="utf-8").read()
toc_content = open(pathlib.Path(__file__).parent.joinpath("Shion.toc"), "r", encoding="utf-8").read()
