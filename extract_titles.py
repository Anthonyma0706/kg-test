import os
from bs4 import BeautifulSoup
import argparse
import json
import re

def extract_titles(html_file_path, md_output_dir, json_output_dir):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取带层级的标题（修复：明确层级关系，确保知识点层级>=4）
    titles_with_level = []
    for anchor in soup.find_all(class_='tree-anchor'):
        li_parent = anchor.find_parent('li')
        if not li_parent:
            continue
        level = int(li_parent.get('data-level', 1))
        title = anchor.get('title')
        if title and '复习与测试' not in title:
            titles_with_level.append((level, title))

    # 生成 Markdown（保持不变）
    html_file_name = os.path.basename(html_file_path)
    md_file_name = os.path.splitext(html_file_name)[0] + '.md'
    md_file_path = os.path.join(md_output_dir, md_file_name)
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        for level, title in titles_with_level:
            indent = '    ' * (level - 1)
            md_file.write(f'{indent}- {title}\n')

    # 生成 JSON（关键修改：优化层级匹配逻辑）
    json_data = {"chapter": "", "sections": []}
    current_section = None       # 当前一级小节（level=2）
    current_subsection = None    # 当前二级子小节（level=3）

    for level, title in titles_with_level:
        if level == 1:  # 章节（如 "第二十五章 概率初步"）
            json_data["chapter"] = title
            current_section = None  # 章节变更时重置下级引用
        elif level == 2:  # 一级小节（如 "21.1 一元二次方程"）
            current_section = {
                "sectionTitle": title,
                "subsections": [],  # 子小节列表（level=3）
                "knowledgePoints": []  # 知识点列表（当没有子小节时使用）
            }
            json_data["sections"].append(current_section)
            current_subsection = None  # 一级小节变更时重置子小节引用
        elif level == 3:  # 二级子小节（如 "一元二次方程的定义"）
            current_subsection = {
                "subsectionTitle": title,
                "knowledgePoints": []  # 知识点列表（level>=4）
            }
            if current_section:
                current_section["subsections"].append(current_subsection)
        elif level >= 4:  # 知识点（如 "一元二次方程的定义" 下的具体知识点）
            if current_subsection:
                # 如果存在当前子小节，知识点添加到子小节中
                current_subsection["knowledgePoints"].append(title)
            elif current_section:
                # 如果不存在子小节但存在当前小节，知识点直接添加到小节中
                current_section["knowledgePoints"].append(title)

    # 写入 JSON（保持不变）
    json_file_name = os.path.splitext(html_file_name)[0] + '.json'
    json_file_path = os.path.join(json_output_dir, json_file_name)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='提取 HTML 层级标题并生成 Markdown/JSON')
    parser.add_argument('html_dir', help='HTML 文件目录')
    parser.add_argument('md_output_dir', help='Markdown 输出目录')
    parser.add_argument('json_output_dir', help='JSON 输出目录')
    args = parser.parse_args()
    
    os.makedirs(args.md_output_dir, exist_ok=True)
    os.makedirs(args.json_output_dir, exist_ok=True)
    
    for root, _, files in os.walk(args.html_dir):
        for file in files:
            if file.endswith('.html'):
                extract_titles(os.path.join(root, file), args.md_output_dir, args.json_output_dir)