# Yume 文档生成器

一个简单易用的Markdown文档生成器，可以将多个Markdown文件合并为一个美观的HTML文档。

## 项目依赖

- **Python 3.12+**：项目使用Python 3.12及以上版本的语法特性
- **第三方库**：
  - `jinja2>=3.1.6,<4`：HTML模板引擎，用于渲染最终的HTML文档
  - `markdown>=3.10,<4`：将Markdown文本转换为HTML格式
  - `pillow>=12.1.0,<13`：图像处理库，用于缩放和处理文档中的图片

## 安装方法

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/Yume.git
   cd Yume
   ```

2. **安装依赖**
   项目使用`uv`作为包管理工具，执行以下命令安装依赖：
   ```bash
   uv install
   ```

## 使用方法

### 基本使用

将Markdown文件放入`content`目录，然后执行以下命令：

```bash
uv run python main.py
```

生成的HTML文件将保存在`output`目录中。

### 设置日志级别

支持通过命令行参数设置日志级别：

```bash
# 输出INFO级别的日志
uv run python main.py --log-level INFO

# 输出DEBUG级别的详细日志
uv run python main.py --log-level DEBUG
```

日志级别选项：`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## 项目结构

```
Yume/
├── content/              # Markdown源文件目录
│   ├── media/            # 图片资源目录
│   ├── 01_introduction.md   # 示例Markdown文件
│   ├── 02_usage.md          # 示例Markdown文件
│   └── 03_project_structure.md  # 示例Markdown文件
├── output/               # 生成的HTML输出目录
│   ├── media/            # 处理后的图片目录
│   └── index.html        # 生成的HTML文档
├── main.py               # 主程序文件
├── templates.html        # HTML模板文件
├── pyproject.toml        # 项目依赖配置
├── uv.lock               # uv包管理器锁定文件
└── README.md             # 项目说明文档
```

## 主要函数逻辑

### 1. `process_image(img_path: Path, output_dir: Path) -> str`

**功能**：处理Markdown中的图片，缩放宽度为720px并保存到输出目录。

**参数**：
- `img_path`：原始图片的路径
- `output_dir`：输出目录路径

**返回值**：处理后的图片相对路径

**工作流程**：
1. 确保输出媒体目录存在
2. 打开原始图片
3. 计算缩放后的尺寸（保持宽高比）
4. 缩放图片（使用LANCZOS插值算法）
5. 保存处理后的图片
6. 返回相对路径

### 2. `read_template(template_file: Path) -> Template`

**功能**：读取HTML模板文件并返回Jinja2模板对象。

**参数**：
- `template_file`：模板文件路径

**返回值**：Jinja2 Template对象

### 3. `process_markdown_file(md_file: Path, content_dir: Path, output_dir: Path) -> dict`

**功能**：处理单个Markdown文件，转换为HTML并提取章节信息。

**参数**：
- `md_file`：Markdown文件路径
- `content_dir`：内容目录路径
- `output_dir`：输出目录路径

**返回值**：包含章节信息的字典（id、标题、HTML内容）

**工作流程**：
1. 读取Markdown文件内容
2. 处理文件中的图片链接
3. 使用markdown库将Markdown转换为HTML
4. 从Markdown内容或文件名提取章节标题和ID
5. 返回章节信息

### 4. `render_and_save_html(template: Template, title: str, sections: list, output_dir: Path) -> Path`

**功能**：使用Jinja2模板渲染HTML并保存到文件。

**参数**：
- `template`：Jinja2 Template对象
- `title`：文档标题
- `sections`：章节信息列表
- `output_dir`：输出目录路径

**返回值**：生成的HTML文件路径

### 5. `main()`

**功能**：主程序入口，协调整个文档生成流程。

**工作流程**：
1. 配置参数和日志
2. 确保输出目录存在
3. 读取HTML模板
4. 获取并排序所有Markdown文件
5. 处理每个Markdown文件
6. 渲染HTML文档
7. 保存生成的HTML文件

## 工作原理

1. **输入处理**：程序从`content`目录读取所有Markdown文件，并按文件名排序。

2. **内容转换**：
   - 处理Markdown中的图片链接，将本地图片缩放并复制到输出目录
   - 使用`markdown`库将Markdown文本转换为HTML格式
   - 提取每个Markdown文件的标题作为章节标题

3. **模板渲染**：
   - 使用Jinja2模板引擎，将转换后的HTML内容填充到`templates.html`模板中
   - 生成包含导航和所有章节内容的完整HTML文档

4. **输出保存**：将生成的HTML文件保存到`output`目录，同时将处理后的图片保存到`output/media`目录

## 配置说明

### Markdown文件命名

建议使用数字前缀命名Markdown文件，以便程序按顺序处理：
```
01_introduction.md
02_usage.md
03_project_structure.md
```

### 图片处理

在Markdown中使用相对路径引用图片：
```markdown
![示例图片](./media/example.png)
```

程序会自动：
- 查找`content/media`目录中的图片
- 缩放图片宽度为720px（保持宽高比）
- 保存到`output/media`目录
- 更新HTML中的图片路径

### HTML模板

可以修改`templates.html`文件来自定义生成的HTML文档样式和结构。模板使用Jinja2语法，支持以下变量：
- `title`：文档标题
- `sections`：章节列表，每个章节包含`id`、`title`和`content`字段

## 日志功能

程序使用Python标准库的`logging`模块记录运行信息：

- **DEBUG级别**：详细的调试信息，包括文件大小、图片尺寸等
- **INFO级别**：关键处理步骤，如文件处理、图片转换等
- **WARNING级别**：警告信息（默认级别）
- **ERROR级别**：错误信息
- **CRITICAL级别**：严重错误信息

## 扩展建议

1. **添加目录生成**：自动生成文档目录导航
2. **支持主题切换**：提供多种HTML模板选择
3. **添加搜索功能**：在生成的HTML中添加内容搜索功能
4. **支持更多格式**：如PDF、EPUB等输出格式
5. **添加语法高亮**：对代码块进行语法高亮处理

## 许可证

MIT License
