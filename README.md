# 知识图谱提取工具

## 概述
`extract_titles.py` 是一个强大的Python脚本，专门用于从HTML教材文件中提取章节结构，并将其转换为Markdown和JSON格式。该脚本能够自动处理复杂的嵌套结构，输出符合规范的知识图谱数据。

## `extract_titles.py` 功能详解
### 主要功能
1. **HTML标题提取**：从HTML文件中精准提取带层级的标题结构。
2. **Markdown生成**：根据提取的标题结构，生成带缩进的Markdown列表。
3. **JSON转换**：将提取的信息转换为符合规范的JSON知识结构。
4. **嵌套结构处理**：自动处理多级嵌套结构，包括章节、小节、子小节和知识点。
5. **内容过滤**：自动过滤掉如“复习与测试”等非知识点内容。

### 使用方式
运行脚本时，需要通过命令行传递必要的参数。以下是一个示例：
```bash
python extract_titles.py --html_dir /path/to/html/files --md_output_dir /path/to/md/output --json_output_dir /path/to/json/output
```

```bash
python extract_titles.py html_files md_files json_files
```

### 参数说明
| 参数名          | 描述                          | 示例值                          |
|-----------------|-------------------------------|---------------------------------|
| `html_dir`      | 包含HTML文件的目录            | `/Users/mma0706/html_files`     |
| `md_output_dir` | 输出Markdown文件的目录        | `/Users/mma0706/md_output`      |
| `json_output_dir` | 输出JSON文件的目录          | `/Users/mma0706/json_output`    |

### 处理逻辑
1. **HTML解析**：解析HTML文件中 `tree-anchor` 类的元素。
2. **层级确定**：根据元素的 `data-level` 属性确定标题的层级关系。
3. **内容过滤**：自动过滤掉包含“复习与测试”的标题。
4. **子小节识别**：使用正则表达式识别并处理“x.x.x”格式的子小节标题。
5. **数据生成**：根据处理结果生成符合规范的Markdown和JSON文件。

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
- **示例**：`"第十一单元 化学与社会"`

#### 2. 小节 (`sections`)
- **类型**：数组
- **描述**：包含该章节下所有小节的数组

**小节对象属性**：
- `sectionTitle`：小节标题（字符串）
- `subsections`：子小节数组（数组）
- `knowledgePoints`：知识点数组（数组）

### 3. 子小节 (`subsections`)
- **类型**：数组
- **描述**：当小节下有带编号的子小节时使用
- **结构**：
```json
{
    "subsectionTitle": "子小节标题",
    "knowledgePoints": ["知识点1", "知识点2"]
}
```

### 4. 知识点 (`knowledgePoints`)
- **类型**：数组
- **描述**：包含该小节/子小节下的所有知识点
- **规则**：
  - 当小节下没有子小节时，知识点直接放在小节的 `knowledgePoints` 中。
  - 当小节下有子小节时，知识点放在对应子小节的 `knowledgePoints` 中。

## 示例
### 情况1：只有小节和知识点
```json
{
    "sectionTitle": "1.1 正数和负数",
    "subsections": [],
    "knowledgePoints": [
        "正负数的定义",
        "相反意义的量"
    ]
}
```

### 情况2：有小节和子小节
```json
{
    "sectionTitle": "1.2 有理数",
    "subsections": [
        {
            "subsectionTitle": "1.2.1 有理数",
            "knowledgePoints": [
                "有理数的定义",
                "0的意义"
            ]
        }
    ]
}
```
```
        