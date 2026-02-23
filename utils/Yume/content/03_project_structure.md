# 项目结构

## 目录说明

- **content/**: 存放Markdown源文件，文件名按顺序排列
- **output/**: 存放生成的HTML文件
- **templates.html**: Jinja2模板文件，定义HTML页面结构
- **main.py**: 主脚本，负责读取Markdown文件并生成HTML
- **pyproject.toml**: 项目配置文件，包含依赖信息

## 文件命名规则

Markdown文件建议按照以下规则命名：

```
XX_filename.md
```

其中XX为数字，用于控制文件的合并顺序。

## 模板定制

可以修改templates.html文件来自定义HTML页面的样式和结构：

- 修改title标签自定义页面标题
- 修改CSS样式自定义主题
- 修改section结构自定义内容布局