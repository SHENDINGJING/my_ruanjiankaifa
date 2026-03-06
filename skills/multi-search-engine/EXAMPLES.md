# Multi Search Engine - 使用示例

## 基本搜索

### 简单搜索
```bash
# 英文搜索（默认使用 Google）
node search-tool.js search "openclaw documentation"

# 中文搜索（自动使用百度）
node search-tool.js search "人工智能发展"

# 直接搜索（无需输入 search 命令）
node search-tool.js "machine learning tutorial"
```

### 指定搜索引擎
```bash
# 使用 Google
node search-tool.js search "python programming" --engine google

# 使用百度
node search-tool.js search "Python 编程" --engine baidu

# 使用 DuckDuckGo（隐私保护）
node search-tool.js search "privacy tools" --engine duckduckgo

# 使用 WolframAlpha（计算和知识）
node search-tool.js search "integrate x^2" --engine wolfram
```

## 高级搜索功能

### 搜索运算符
```bash
# 在特定网站内搜索
node search-tool.js search "site:github.com openclaw"

# 搜索特定文件类型
node search-tool.js search "filetype:pdf deep learning"

# 搜索标题中包含特定词
node search-tool.js search "intitle:OpenClaw documentation"

# 精确短语搜索
node search-tool.js search '"artificial intelligence" history'

# 排除特定词
node search-tool.js search "python -django tutorial"

# 布尔 OR 搜索
node search-tool.js search "python OR java tutorial"

# 数字范围搜索
node search-tool.js search "python 2020..2023"
```

### 时间过滤
```bash
# 过去一小时
node search-tool.js search "latest news" --time past-hour

# 过去24小时
node search-tool.js search "breaking news" --time past-day

# 过去一周
node search-tool.js search "recent developments" --time past-week

# 过去一个月
node search-tool.js search "monthly updates" --time past-month

# 过去一年
node search-tool.js search "annual report 2024" --time past-year
```

### 搜索类型
```bash
# 图片搜索
node search-tool.js search "mountain landscape" --type images

# 新闻搜索
node search-tool.js search "technology news" --type news

# 视频搜索
node search-tool.js search "programming tutorial" --type videos

# 学术搜索
node search-tool.js search "machine learning papers" --type academic

# 购物搜索
node search-tool.js search "laptop reviews" --type shopping
```

## 引擎组搜索

### 中文引擎组
```bash
# 使用所有中文引擎
node search-tool.js search "中国人工智能政策" --chinese

# 结果会显示：
# - Baidu (百度)
# - Bing CN (必应中国)
# - Sogou (搜狗)
# - Zhihu (知乎)
```

### 全球引擎组
```bash
# 使用所有全球引擎
node search-tool.js search "global warming research" --global

# 结果会显示：
# - Google
# - Bing
# - DuckDuckGo
# - Startpage
```

### 隐私引擎组
```bash
# 使用隐私保护引擎
node search-tool.js search "online privacy tips" --privacy

# 结果会显示：
# - DuckDuckGo
# - Startpage
```

### 多引擎同时搜索
```bash
# 使用多个引擎
node search-tool.js search "compare search engines" --multiple

# 结果会显示所有可用引擎
```

## 交互式搜索

### 启动交互模式
```bash
# 不提供参数启动交互模式
node search-tool.js

# 交互模式步骤：
# 1. 输入搜索查询
# 2. 选择引擎选项（1-6）
# 3. 选择搜索类型
# 4. 选择时间过滤
# 5. 显示搜索结果
```

### 交互模式示例
```
🎯 Interactive Multi-Search
=========================

Enter your search query: 机器学习实践

Available options:
1. Default (auto-select engine)
2. Chinese engines
3. Global engines
4. Privacy-focused engines
5. Multiple engines
6. Specific engine

Choose option (1-6): 2

Search types: web, images, news, videos, academic, shopping
Search type (press Enter for web): academic

Time filters: past-hour, past-day, past-week, past-month, past-year
Time filter (press Enter for none): past-year

🔍 Searching for: "机器学习实践"
📁 Search type: academic (Academic papers)
⏰ Time filter: past-year (Past year)
🚀 Using 4 engine(s): Baidu (百度), Bing CN (必应中国), Sogou (搜狗), Zhihu (知乎)
```

## 实用工具命令

### 查看可用引擎
```bash
# 列出所有搜索引擎
node search-tool.js engines

# 输出：
# Chinese Engines:
#   baidu        - Baidu (百度) (Chinese web search)
#   bing-cn      - Bing CN (必应中国) (Microsoft search in China)
#   sogou        - Sogou (搜狗) (Chinese search engine)
#   zhihu        - Zhihu (知乎) (Chinese Q&A platform)
# 
# Global Engines:
#   google       - Google (Global web search)
#   bing         - Bing (Microsoft global search)
#   duckduckgo   - DuckDuckGo (Privacy-focused search)
#   startpage    - Startpage (Privacy search with Google results)
# 
# Knowledge Engine:
#   wolfram      - WolframAlpha (Computational knowledge engine)
```

### 查看搜索运算符
```bash
# 显示高级搜索运算符
node search-tool.js operators

# 输出：
# Advanced Search Operators
#   site:         - Search within specific site
#   filetype:     - Search for file type (pdf, doc, etc.)
#   intitle:      - Search in page titles
#   inurl:        - Search in URLs
#   "phrase"      - Exact phrase match
#   -exclude      - Exclude term
#   OR            - Boolean OR operator
#   ..            - Number range (2020..2023)
# 
# Time Filters:
#   past-hour     - Past hour
#   past-day      - Past 24 hours
#   past-week     - Past week
#   past-month    - Past month
#   past-year     - Past year
# 
# Search Types:
#   web           - General web search
#   images        - Image search
#   news          - News search
#   videos        - Video search
#   academic      - Academic papers
#   shopping      - Product search
```

### 查看帮助
```bash
# 显示帮助信息
node search-tool.js help
```

## 实际应用场景

### 学术研究
```bash
# 搜索最新学术论文
node search-tool.js search "transformer architecture" --type academic --time past-year

# 多引擎比较搜索结果
node search-tool.js search "large language models survey" --multiple --type academic
```

### 技术问题解决
```bash
# 搜索编程错误信息
node search-tool.js search "TypeError: Cannot read property" --engine google

# 搜索中文技术问题
node search-tool.js search "Python 连接数据库错误" --chinese
```

### 市场调研
```bash
# 搜索产品评测
node search-tool.js search "iPhone 15 review" --type shopping --multiple

# 搜索行业新闻
node search-tool.js search "AI industry trends 2024" --type news --time past-month
```

### 学习资源
```bash
# 搜索教程
node search-tool.js search "React tutorial for beginners" --type videos

# 搜索文档
node search-tool.js search "site:docs.openclaw.ai" --engine google
```

## 与 OpenClaw 集成

### 在 OpenClaw 会话中使用
```javascript
// 在 OpenClaw 技能中调用搜索
const { performSearch } = require('./search-tool.js');

// 执行搜索
performSearch("openclaw skills", { engine: "google" });

// 获取引擎列表
const { ENGINES } = require('./search-tool.js');
console.log('Available engines:', Object.keys(ENGINES));
```

### 搜索历史记录
所有搜索都会自动保存到：
```
memory/search-history/searches.md
```

文件格式：
```markdown
# Search History

## 2024-03-06T08:54:00.000Z
- **Query**: machine learning tutorial
- **Engines**: Google
- **Options**: {"type":"videos"}
- **Chinese content**: No
```

## 提示和技巧

### 1. 自动引擎选择
- 包含中文字符的查询会自动使用百度
- 英文查询默认使用 Google
- 包含计算或知识类查询会建议使用 WolframAlpha

### 2. 隐私保护
- 使用 `--privacy` 选项保护搜索隐私
- 搜索历史本地存储，不上传
- 可随时清除搜索历史

### 3. 效率优化
- 使用时间过滤减少无关结果
- 使用搜索运算符精确匹配
- 使用多引擎比较获取全面信息

### 4. 结果分析
- 比较不同引擎的结果差异
- 注意结果的时间戳
- 验证信息的权威性

## 故障排除

### 常见问题
1. **引擎无响应**：尝试其他引擎
2. **速率限制**：等待片刻或切换引擎
3. **无结果**：调整关键词或使用更通用的术语
4. **编码问题**：确保查询字符串正确编码

### 错误信息
- `Unknown engine`：检查引擎名称是否正确
- `No query provided`：提供搜索查询
- `Invalid time filter`：使用有效的时间过滤器

基于 gpyAngyoujun/multi-search-engine v2.0.1 的功能实现。