# 项目修改日志

## 2024年修改记录

### 修复md_to_json.py层级处理逻辑
**日期**: 当前
**问题**: 发现算法把所有叶子节点都当作知识点，但实际上8个空格缩进的应该是subsectionTitle，12个空格缩进的才是knowledgePoints

**修复方案**:
1. 删除了基于叶子节点的检测算法
2. 改为按固定层级规则处理：
   - Level 0 (0个空格): 章节 → chapter
   - Level 1 (4个空格): 小节 → sectionTitle
   - Level 2 (8个空格): 子小节 → subsectionTitle
   - Level 3 (12个空格): 知识点 → knowledgePoints

**核心改进**:
- 使用traverse_node函数递归遍历所有节点
- 根据node.level直接判断数据归属
- 正确处理父子关系和数据结构嵌套
- 支持知识点归属到subsection或section

**验证结果**: 
- ✅ 子小节正确识别为subsectionTitle
- ✅ 知识点正确归类到knowledgePoints数组
- ✅ 空知识点子小节正确处理为空数组
- ✅ JSON结构完全符合规范

### 创建md_to_json.py脚本
**日期**: 当前
**背景**: 发现extract_titles.py生成的JSON文件知识点为空，但md_files中的markdown文件格式正确

**创建内容**:
1. 新建md_to_json.py脚本，用于从markdown文件生成JSON知识图谱
2. 采用树结构算法：
   - 构建层级树结构
   - 识别叶子节点作为知识点
   - 根据父节点层级进行归类

**发现的markdown结构**:
- 0个空格缩进：章节 (level 0)
- 4个空格缩进：小节 (level 1) 
- 8个空格缩进：子小节 (level 2)
- 12个空格缩进：知识点 (level 3)

**技术要点**:
- 使用TreeNode类构建层级关系
- find_leaf_nodes函数识别最后一级分支
- 知识点的上级可以是subsection/section/chapter中的任意一个

**状态**: 脚本已创建并成功运行，发现markdown结构比预期更深

### 修复JSON生成逻辑错误
**日期**: 当前
**问题**: extract_titles.py中的JSON生成逻辑存在缺陷，当没有三级子小节时，四级及以上的知识点无法正确归属到二级小节中，导致knowledgePoints为空。

**修改内容**:
1. 在level=2时为section添加knowledgePoints字段
2. 在level>=4时增加判断逻辑：
   - 如果存在current_subsection，知识点添加到子小节中
   - 如果不存在子小节但存在current_section，知识点直接添加到小节中
3. 更新了data-formats.mdc中的JSON结构示例

**影响范围**: 
- 修改了extract_titles.py的核心JSON生成逻辑
- 确保了JSON输出的正确性和完整性
- 更新了相关文档

### 生成Cursor规则 - 项目初始化
**日期**: 当前
**修改内容**: 
1. 创建了`.cursor/rules/`目录结构
2. 生成了4个核心Cursor规则文件：
   - `project-overview.mdc` - 项目概览和核心文件说明
   - `code-patterns.mdc` - 代码模式和架构规则
   - `development-workflow.mdc` - 开发工作流和最佳实践
   - `data-formats.mdc` - 数据格式规范

**目的**: 为项目建立完整的Cursor规则体系，帮助AI更好地理解项目结构、代码模式和开发规范，提高后续开发效率。

**影响范围**: 
- 新增Cursor规则目录和文件
- 建立了项目的标准化文档体系
- 为后续AI辅助开发提供了上下文基础 

### 简化extract_titles.py - 专注HTML到MD转换
**日期**: 当前
**背景**: 现在有了专门的md_to_json.py处理MD到JSON转换，extract_titles.py应该专注于HTML到MD的转换

**修改内容**:
1. 移除所有JSON相关代码：
   - 删除json和re导入
   - 删除json_output_dir参数
   - 删除JSON生成逻辑（约40行代码）
   - 删除JSON文件写入代码

2. 简化函数签名：
   - `extract_titles(html_file_path, md_output_dir, json_output_dir)` → `extract_titles(html_file_path, md_output_dir)`
   - 命令行参数从3个减少到2个

3. 保留核心功能：
   - HTML解析和标题提取
   - Markdown文件生成
   - 层级缩进处理

**工作流程优化**:
- HTML → MD: 使用 `extract_titles.py`
- MD → JSON: 使用 `md_to_json.py`
- 职责分离，代码更清晰

**测试验证**: ✅ 生成的Markdown文件格式完全正确，层级结构保持一致

### 最终修复：动态判断Level 2内容类型
**日期**: 当前
**核心问题**: Level 2内容需要动态判断：
- 如果有Level 3子节点 → 应该是子小节(subsectionTitle)
- 如果没有Level 3子节点 → 应该是知识点(knowledgePoints)

**实现方案**:
```python
has_level3_children = any(child.level == 3 for child in node.children)
if has_level3_children:
    # Level 2 是子小节
else:
    # Level 2 是知识点
```

**测试验证**:
- ✅ `16.1 二次根式` → subsections: [], knowledgePoints: ["求二次根式的值", ...]
- ✅ `18.1 平行四边形` → subsections: [{"subsectionTitle": "18.1.1 平行四边形的性质", ...}]

**最终状态**: md_to_json.py脚本现在能够完美处理所有markdown层级结构，正确生成符合规范的JSON知识图谱！

### 修复md_to_json.py层级处理逻辑 

### 更新README.md文档
**日期**: 当前
**背景**: 根据近期的脚本重构和功能分离，需要更新项目文档

**主要更新内容**:
1. **架构说明**: 添加两步转换流程图和脚本功能分离说明
2. **双脚本介绍**: 
   - `extract_titles.py`: HTML→MD转换专用
   - `md_to_json.py`: MD→JSON转换专用
3. **完整使用流程**: 提供分步骤和一键执行的使用示例
4. **智能层级识别**: 详细说明动态判断Level 2内容的算法
5. **技术特点**: 添加优势和技术实现说明

**文档结构优化**:
- 增加工具架构章节
- 完善MD到JSON转换说明
- 更新JSON示例为实际数据
- 添加Markdown层级结构映射
- 补充技术特点和实现细节

**用户体验改进**:
- 提供清晰的分步骤执行指南
- 添加完整的参数说明表格
- 包含实际的输出示例
- 突出智能识别功能的优势

### 简化extract_titles.py - 专注HTML到MD转换 