import os
from bs4 import BeautifulSoup
import argparse

def extract_titles(html_file_path, md_output_dir):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取带层级的标题
    titles_with_level = []
    for anchor in soup.find_all(class_='tree-anchor'):
        li_parent = anchor.find_parent('li')
        if not li_parent:
            continue
        level = int(li_parent.get('data-level', 1))
        title = anchor.get('title')
        if title and '复习与测试' not in title:
            titles_with_level.append((level, title))

    # 生成 Markdown
    html_file_name = os.path.basename(html_file_path)
    md_file_name = os.path.splitext(html_file_name)[0] + '.md'
    md_file_path = os.path.join(md_output_dir, md_file_name)
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        for level, title in titles_with_level:
            indent = '    ' * (level - 1)
            md_file.write(f'{indent}- {title}\n')
    
    print(f'已转换: {html_file_path} -> {md_file_path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='提取 HTML 层级标题并生成 Markdown')
    parser.add_argument('html_dir', help='HTML 文件目录')
    parser.add_argument('md_output_dir', help='Markdown 输出目录')
    args = parser.parse_args()
    
    os.makedirs(args.md_output_dir, exist_ok=True)
    
    for root, _, files in os.walk(args.html_dir):
        for file in files:
            if file.endswith('.html'):
                extract_titles(os.path.join(root, file), args.md_output_dir)
    
    print('所有HTML文件转换完成！')