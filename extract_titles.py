import os
from bs4 import BeautifulSoup
import argparse
import json


def extract_titles(html_file_path, md_output_dir, json_output_dir):
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有class为tree-anchor的元素，并提取层级和标题
    titles_with_level = []
    for anchor in soup.find_all(class_='tree-anchor'):
        # 找到父级<li>元素获取data-level属性（假设结构为<li><div><a class="tree-anchor">）
        li_parent = anchor.find_parent('li')
        if not li_parent:
            continue  # 无层级信息则跳过
        level = int(li_parent.get('data-level', 1))  # 默认层级1
        title = anchor.get('title')
        if title and '复习与测试' not in title:
            titles_with_level.append((level, title))

    # 生成Markdown文件名
    html_file_name = os.path.basename(html_file_path)
    md_file_name = os.path.splitext(html_file_name)[0] + '.md'
    md_file_path = os.path.join(md_output_dir, md_file_name)

    # 写入带层级的Markdown列表（每层缩进4个空格）
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        for level, title in titles_with_level:
            indent = '    ' * (level - 1)  # 层级1无缩进，层级2缩进4空格，以此类推
            md_file.write(f'{indent}- {title}\n')

    # 生成JSON结构
    json_structure = {}  # 初始化JSON结构
    current_levels = [json_structure]
    for level, title in titles_with_level:
        if level == 1:
            # 一级标题，直接添加到根节点
            if '1' not in json_structure:
                json_structure['1'] = []
            json_structure['1'].append({title: {}})
            current_levels = [json_structure, json_structure['1'][-1][title]]
        elif level > len(current_levels):
            # 进入更深层级
            last_dict = current_levels[-1]
            if '知识点' not in last_dict:
                last_dict['知识点'] = []
            last_dict['知识点'].append({title: {}})
            current_levels.append(last_dict['知识点'][-1][title])
        else:
            # 返回上层级
            current_levels = current_levels[:level]
            last_dict = current_levels[-1]
            if str(level) not in last_dict:
                last_dict[str(level)] = []
            last_dict[str(level)].append({title: {}})
            current_levels.append(last_dict[str(level)][-1][title])

    # 生成JSON文件名
    json_file_name = os.path.splitext(html_file_name)[0] + '.json'
    json_file_path = os.path.join(json_output_dir, json_file_name)

    # 写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_structure, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract hierarchical titles from HTML files and save to Markdown and JSON.')
    parser.add_argument('html_dir', type=str, help='Directory containing HTML files.')
    parser.add_argument('md_output_dir', type=str, help='Directory to save Markdown files.')
    parser.add_argument('json_output_dir', type=str, help='Directory to save JSON files.')
    args = parser.parse_args()

    # 确保输出目录存在
    os.makedirs(args.md_output_dir, exist_ok=True)
    os.makedirs(args.json_output_dir, exist_ok=True)

    # 遍历目录下所有HTML文件
    for root, dirs, files in os.walk(args.html_dir):
        for file in files:
            if file.endswith('.html'):
                html_file_path = os.path.join(root, file)
                extract_titles(html_file_path, args.md_output_dir, args.json_output_dir)