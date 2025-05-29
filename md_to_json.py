import os
import json
import argparse
import re

class TreeNode:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.children = []
        self.parent = None

def build_tree(lines):
    """构建层级树结构"""
    root = TreeNode("ROOT", -1)
    stack = [root]
    
    for line in lines:
        line = line.rstrip('\n')
        if not line.strip():
            continue
            
        # 计算缩进级别（每4个空格为一级）
        indent_level = (len(line) - len(line.lstrip())) // 4
        title = line.strip('- ').strip()
        
        # 创建新节点
        node = TreeNode(title, indent_level)
        
        # 找到正确的父节点
        while len(stack) > 1 and stack[-1].level >= indent_level:
            stack.pop()
        
        parent = stack[-1]
        node.parent = parent
        parent.children.append(node)
        stack.append(node)
    
    return root

def build_json_structure(root):
    """根据树结构构建JSON"""
    json_data = {"chapter": "", "sections": []}
    
    # 按层级组织数据结构
    chapter_data = {"sections": {}}
    
    def traverse_node(node):
        """遍历节点并按层级处理"""
        if node.level == 0:  # 章节
            # 设置章节标题
            json_data["chapter"] = node.title
        elif node.level == 1:  # 小节
            section_title = node.title
            if section_title not in chapter_data["sections"]:
                chapter_data["sections"][section_title] = {
                    "subsections": {},
                    "knowledgePoints": []
                }
        elif node.level == 2:  # 可能是子小节或知识点
            # 检查是否有Level 3的子节点
            has_level3_children = any(child.level == 3 for child in node.children)
            
            # 找到父节点（小节）
            section_parent = node.parent
            if section_parent and section_parent.level == 1:
                section_title = section_parent.title
                
                if section_title not in chapter_data["sections"]:
                    chapter_data["sections"][section_title] = {
                        "subsections": {},
                        "knowledgePoints": []
                    }
                
                if has_level3_children:
                    # 如果有Level 3子节点，则这是真正的子小节
                    subsection_title = node.title
                    if subsection_title not in chapter_data["sections"][section_title]["subsections"]:
                        chapter_data["sections"][section_title]["subsections"][subsection_title] = {
                            "knowledgePoints": []
                        }
                else:
                    # 如果没有Level 3子节点，则这是知识点
                    knowledge_point = node.title
                    chapter_data["sections"][section_title]["knowledgePoints"].append(knowledge_point)
                    
        elif node.level == 3:  # 知识点
            knowledge_point = node.title
            
            # 找到父节点（应该是子小节）
            parent = node.parent
            if parent and parent.level == 2:
                section_parent = parent.parent
                if section_parent and section_parent.level == 1:
                    section_title = section_parent.title
                    subsection_title = parent.title
                    chapter_data["sections"][section_title]["subsections"][subsection_title]["knowledgePoints"].append(knowledge_point)
        
        # 递归处理子节点
        for child in node.children:
            traverse_node(child)
    
    # 开始遍历
    for child in root.children:
        traverse_node(child)
    
    # 转换为最终的JSON格式
    for section_title, section_data in chapter_data["sections"].items():
        section = {
            "sectionTitle": section_title,
            "subsections": [],
            "knowledgePoints": section_data.get("knowledgePoints", [])
        }
        
        # 添加子小节
        for subsection_title, subsection_data in section_data["subsections"].items():
            subsection = {
                "subsectionTitle": subsection_title,
                "knowledgePoints": subsection_data["knowledgePoints"]
            }
            section["subsections"].append(subsection)
        
        json_data["sections"].append(section)
    
    return json_data

def parse_markdown_to_json(md_file_path, json_output_dir):
    """将单个markdown文件转换为JSON格式"""
    with open(md_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 构建树结构
    root = build_tree(lines)
    
    # 构建JSON
    json_data = build_json_structure(root)
    
    # 生成输出文件路径
    md_file_name = os.path.basename(md_file_path)
    json_file_name = os.path.splitext(md_file_name)[0] + '.json'
    json_file_path = os.path.join(json_output_dir, json_file_name)
    
    # 写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    
    print(f'已转换: {md_file_path} -> {json_file_path}')

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将Markdown文件转换为JSON知识图谱格式')
    parser.add_argument('md_input_dir', help='包含Markdown文件的输入目录')
    parser.add_argument('json_output_dir', help='JSON文件输出目录')
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.json_output_dir, exist_ok=True)
    
    # 处理输入目录中的所有markdown文件
    for root, _, files in os.walk(args.md_input_dir):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                parse_markdown_to_json(md_file_path, args.json_output_dir)
    
    print('所有Markdown文件转换完成！')

if __name__ == '__main__':
    main() 