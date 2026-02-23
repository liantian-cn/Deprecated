# 使用指南

## 安装依赖

使用uv安装所需依赖：

```bash
uv add markdown jinja2
```

## 运行脚本

```bash
uv run python main.py
```

## 配置选项

脚本支持以下配置：

- content_dir: Markdown文件目录
- output_dir: HTML输出目录
- template_file: 模板文件路径
- title: 页面标题