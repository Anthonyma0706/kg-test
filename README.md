# 知识图谱提取工具

## 概述
这是一个专门用于从HTML教材文件中提取章节结构并转换为知识图谱的工具集。工具采用两步转换流程：首先将HTML转换为Markdown，然后将Markdown转换为JSON格式的知识图谱。

## 工具架构

### 📁 两步转换流程
```
HTML文件 → extract_titles.py → Markdown文件 → md_to_json.py → JSON知识图谱
```

### 🔧 脚本功能分离
- **`extract_titles.py`**: 专注HTML到Markdown的转换
- **`md_to_json.py`**: 专注Markdown到JSON的转换
- **职责分离**: 每个脚本功能单一，便于维护和测试

## `extract_titles.py` 功能详解

### 主要功能
1. **HTML标题提取**：从HTML文件中精准提取带层级的标题结构
2. **Markdown生成**：根据提取的标题结构，生成带缩进的Markdown列表
3. **内容过滤**：自动过滤掉如"复习与测试"等非知识点内容
4. **层级保持**：准确保持原始HTML中的层级结构

### 使用方式
```bash
python extract_titles.py html_files md_files
```

### 参数说明
| 参数名          | 描述                          | 示例值                          |
|-----------------|-------------------------------|---------------------------------|
| `html_dir`      | 包含HTML文件的目录            | `html_files`                    |
| `md_output_dir` | 输出Markdown文件的目录        | `md_files`                      |

### 处理逻辑
1. **HTML解析**：解析HTML文件中 `tree-anchor` 类的元素
2. **层级确定**：根据元素的 `data-level` 属性确定标题的层级关系
3. **内容过滤**：自动过滤掉包含"复习与测试"的标题
4. **Markdown输出**：生成规范的层级缩进Markdown文件

## `md_to_json.py` 功能详解

### 主要功能
1. **Markdown解析**：解析层级结构的Markdown文件
2. **智能识别**：动态判断Level 2内容是子小节还是知识点
3. **JSON生成**：转换为符合规范的JSON知识图谱结构
4. **批量处理**：支持批量转换整个目录的Markdown文件

### 使用方式
```bash
python md_to_json.py md_files json_files
```

### 参数说明
| 参数名           | 描述                          | 示例值                          |
|------------------|-------------------------------|---------------------------------|
| `md_input_dir`   | 包含Markdown文件的目录        | `md_files`                      |
| `json_output_dir`| 输出JSON文件的目录            | `json_files`                    |

### 智能层级识别
```python
# 动态判断Level 2内容类型：
if has_level3_children:
    # Level 2 是子小节 (subsectionTitle)
else:
    # Level 2 是知识点 (knowledgePoints)
```

### Markdown层级结构
- **0个空格缩进**: 章节 (level 0) → `chapter`
- **4个空格缩进**: 小节 (level 1) → `sectionTitle` 
- **8个空格缩进**: 子小节 (level 2) → `subsectionTitle` 或知识点
- **12个空格缩进**: 知识点 (level 3) → `knowledgePoints`

## 完整使用流程

### 步骤1：HTML到Markdown
```bash
python extract_titles.py html_files md_files
```

### 步骤2：Markdown到JSON
```bash
python md_to_json.py md_files json_files
```

### 一键执行示例
```bash
# 完整转换流程
python extract_titles.py html_files md_files
python md_to_json.py md_files json_files
```

## JSON格式输出规范

### 基本结构
```json
{
    "chapter": "章节标题",
    "sections": [
        {
            "sectionTitle": "小节标题",
            "subsections": [],
            "knowledgePoints": ["知识点1", "知识点2"]
        }
    ]
}
```

### 字段说明

#### 1. 章节 (`chapter`)
- **类型**：字符串
- **描述**：教材的章节标题
- **示例**：`"第十六章 二次根式"`

#### 2. 小节 (`sections`)
- **类型**：数组
- **描述**：包含该章节下所有小节的数组

**小节对象属性**：
- `sectionTitle`：小节标题（字符串）
- `subsections`：子小节数组（数组）
- `knowledgePoints`：知识点数组（数组）

#### 3. 子小节 (`subsections`)
- **类型**：数组
- **描述**：当小节下有带编号的子小节时使用
- **结构**：
```json
{
    "subsectionTitle": "子小节标题",
    "knowledgePoints": ["知识点1", "知识点2"]
}
```

#### 4. 知识点 (`knowledgePoints`)
- **类型**：数组
- **描述**：包含该小节/子小节下的所有知识点
- **智能归属规则**：
  - 当Level 2内容没有Level 3子节点时，Level 2直接作为知识点
  - 当Level 2内容有Level 3子节点时，Level 2作为子小节，Level 3作为知识点

## 输出示例

### 情况1：小节直接包含知识点
```json
{
    "sectionTitle": "16.1 二次根式",
    "subsections": [],
    "knowledgePoints": [
        "求二次根式的值",
        "求二次根式中的参数",
        "二次根式有意义的条件"
    ]
}
```

### 情况2：小节包含子小节
```json
{
    "sectionTitle": "18.1 平行四边形",
    "subsections": [
        {
            "subsectionTitle": "18.1.1 平行四边形的性质",
            "knowledgePoints": [
                "利用平行四边形的性质求解",
                "利用平行四边形的性质证明"
            ]
        }
    ],
    "knowledgePoints": []
}
```

## 技术特点

### ✅ 优势
- **职责分离**：两个脚本各司其职，代码简洁
- **智能识别**：动态判断内容层级，无需人工干预
- **批量处理**：支持整个目录的批量转换
- **格式规范**：输出符合知识图谱标准的JSON格式
- **易于维护**：功能模块化，便于调试和扩展

### 🔧 技术实现
- **HTML解析**：使用BeautifulSoup解析HTML结构
- **树结构算法**：构建层级树来处理复杂嵌套
- **动态判断**：基于子节点存在性判断内容类型
- **编码支持**：全面支持中文字符编码
```
        