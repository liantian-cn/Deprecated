import logging
import argparse
import os
import re
from pathlib import Path
from markdown import markdown
from jinja2 import Template
from PIL import Image

# 配置logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def process_image(img_path: Path, output_dir: Path) -> str:
    """处理图片：缩放宽度为720px，保存到output/media目录"""
    logging.debug(f"开始处理图片: {img_path}")
    
    # 确保输出媒体目录存在
    output_media_dir = output_dir / "media"
    output_media_dir.mkdir(exist_ok=True)
    logging.debug(f"输出媒体目录: {output_media_dir}")
    
    # 打开图片
    with Image.open(img_path) as img:
        # 计算缩放后的尺寸
        width, height = img.size
        new_width = 720
        new_height = int(height * (new_width / width))
        logging.debug(f"图片原始尺寸: {width}x{height}, 缩放后尺寸: {new_width}x{new_height}")
        
        # 缩放图片
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 如果图片模式是RGBA（带透明度通道）且保存格式是JPG，转换为RGB模式
        if resized_img.mode == 'RGBA' and img_path.suffix.lower() in ['.jpg', '.jpeg']:
            logging.debug(f"将图片从RGBA模式转换为RGB模式")
            resized_img = resized_img.convert('RGB')
        
        # 保存图片到output/media目录
        output_img_path = output_media_dir / img_path.name
        resized_img.save(output_img_path)
        logging.debug(f"图片已保存: {output_img_path}")
    
    # 返回相对路径
    relative_path = f"./media/{img_path.name}"
    logging.info(f"图片处理完成: {img_path} -> {relative_path}")
    return relative_path

def process_all_media_images(content_dir: Path, output_dir: Path) -> None:
    """处理content/media目录中的所有图片"""
    # 检查content/media目录是否存在
    media_dir = content_dir / "media"
    if not media_dir.exists():
        logging.info(f"媒体目录不存在，跳过图片处理: {media_dir}")
        return
    
    logging.info(f"开始处理媒体目录中的图片: {media_dir}")
    
    # 获取目录中的所有图片文件
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    image_files = [f for f in media_dir.iterdir() 
                  if f.is_file() and f.suffix.lower() in image_extensions]
    
    logging.info(f"找到 {len(image_files)} 个图片文件")
    for img_file in image_files:
        logging.debug(f"  - {img_file}")
        process_image(img_file, output_dir)
    
    logging.info(f"媒体目录图片处理完成: {media_dir}")


def read_template(template_file: Path) -> Template:
    """读取模板文件"""
    logging.info(f"读取模板文件: {template_file}")
    with open(template_file, "r", encoding="utf-8") as f:
        content = f.read()
    logging.debug(f"模板文件大小: {len(content)} 字节")
    return Template(content)


def process_markdown_file(md_file: Path, content_dir: Path, output_dir: Path) -> dict:
    """处理单个markdown文件，返回section数据"""
    logging.info(f"开始处理markdown文件: {md_file}")
    
    # 读取markdown文件内容
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    logging.debug(f"markdown文件大小: {len(md_content)} 字节")
    
    # 转换为HTML，启用扩展支持表格和代码块
    html_content = markdown(md_content, extensions=['extra', 'nl2br', 'toc', 'meta', 'codehilite'])
    logging.debug(f"转换后HTML大小: {len(html_content)} 字节")
    
    # 提取标题作为section的标题和id
    first_line = md_content.strip().split("\n")[0]
    if first_line.startswith("# "):
        section_title = first_line[2:]
        section_id = section_title.lower().replace(" ", "-")
        logging.debug(f"从内容提取标题: {section_title}")
    else:
        section_title = md_file.stem
        section_id = md_file.stem
        logging.debug(f"从文件名提取标题: {section_title}")
    
    section = {
        "id": section_id,
        "title": section_title,
        "content": html_content
    }
    logging.info(f"markdown文件处理完成: {md_file} -> 标题: {section_title}")
    return section


def render_and_save_html(template: Template, title: str, sections: list, output_dir: Path) -> Path:
    """渲染HTML并保存到文件"""
    logging.info(f"开始渲染HTML，标题: {title}, 章节数: {len(sections)}")
    
    # 渲染HTML
    html = template.render(title=title, sections=sections)
    logging.debug(f"渲染后HTML大小: {len(html)} 字节")
    
    # 保存到output目录
    output_file = output_dir / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    logging.info(f"HTML已保存到: {output_file}")
    return output_file


def main():
    logging.info("启动Yume文档生成器")
    
    # 配置参数
    content_dir = Path("content")
    output_dir = Path("output")
    template_file = Path("templates.html")
    title = "Yume 文档"
    
    logging.debug(f"配置参数 - 内容目录: {content_dir}, 输出目录: {output_dir}, 模板文件: {template_file}, 标题: {title}")
    
    # 确保输出目录存在
    output_dir.mkdir(exist_ok=True)
    logging.info(f"输出目录: {output_dir}")
    
    # 处理所有媒体图片
    process_all_media_images(content_dir, output_dir)
    
    # 读取模板文件
    template = read_template(template_file)
    
    # 获取所有markdown文件，按文件名排序
    md_files = sorted(content_dir.glob("*.md"))
    logging.info(f"找到 {len(md_files)} 个markdown文件")
    for md_file in md_files:
        logging.debug(f"  - {md_file}")
    
    sections = []
    for md_file in md_files:
        section = process_markdown_file(md_file, content_dir, output_dir)
        sections.append(section)
    
    # 渲染并保存HTML
    output_file = render_and_save_html(template, title, sections, output_dir)
    
    logging.info(f"HTML文件已生成：{output_file}")
    logging.info(f"图片已处理并保存到：{output_dir / 'media'}")
    logging.info("Yume文档生成完成")


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将markdown文件转换为HTML文档')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='WARNING', help='设置日志级别')
    args = parser.parse_args()
    
    # 设置日志级别
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    main()
