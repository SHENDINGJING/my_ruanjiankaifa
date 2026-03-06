# Multi Search Engine Skill

基于 gpyAngyoujun/multi-search-engine 的本地版本多搜索引擎技能。

## 功能概述

这是一个集成了 17 个搜索引擎（8 个中文 + 9 个全球）的多搜索引擎工具，支持：
- 高级搜索运算符
- 时间过滤器
- 网站特定搜索
- 隐私保护引擎
- WolframAlpha 知识查询
- **无需 API 密钥**

## 支持的搜索引擎

### 中文引擎 (8个)
1. **Baidu (百度)** - 中文网页搜索
2. **Bing CN (必应中国)** - 微软中国搜索
3. **Sogou (搜狗)** - 中文搜索引擎
4. **360 Search (360搜索)** - 中文搜索
5. **Zhihu (知乎)** - 中文问答平台搜索
6. **Weibo (微博)** - 中文微博搜索
7. **Douban (豆瓣)** - 中文书影音评论
8. **Tieba (贴吧)** - 中文论坛搜索

### 全球引擎 (9个)
1. **Google** - 全球网页搜索
2. **Bing** - 微软全球搜索
3. **DuckDuckGo** - 隐私保护搜索
4. **Startpage** - 使用 Google 结果的隐私搜索
5. **Yandex** - 俄罗斯搜索引擎
6. **Ecosia** - 环保搜索（种植树木）
7. **Qwant** - 欧洲隐私保护搜索
8. **Brave Search** - 隐私保护自有索引
9. **WolframAlpha** - 计算知识引擎

## 核心特性

### 1. 高级搜索运算符
- `site:` - 在特定网站内搜索
- `filetype:` - 搜索特定文件类型
- `intitle:` - 在页面标题中搜索
- `inurl:` - 在 URL 中搜索
- `"精确短语"` - 精确短语匹配
- `-排除词` - 排除特定词
- `OR` - 布尔 OR 运算符
- `..` - 数字范围（如 2020..2023）

### 2. 时间过滤器
- 过去一小时
- 过去24小时
- 过去一周
- 过去一个月
- 过去一年
- 自定义日期范围

### 3. 搜索类型
- 网页搜索
- 图片搜索
- 视频搜索
- 新闻搜索
- 学术搜索
- 购物搜索
- 地图搜索
- 书籍搜索

### 4. 隐私保护
- 无跟踪
- 无个性化结果
- 不存储搜索历史
- 加密连接
- 匿名搜索选项

### 5. WolframAlpha 集成
- 数学计算
- 科学数据
- 历史事实
- 地理信息
- 语言分析
- 营养信息
- 金融数据
- 天气信息

## 快速开始

### 安装
```bash
# 技能已安装在 skills/multi-search-engine/ 目录
```

### 基本使用
```bash
# 进入技能目录
cd skills/multi-search-engine

# 运行搜索工具
node search-tool.js search "查询内容"

# 交互式搜索
node search-tool.js
```

### 常用命令
```bash
# 查看帮助
node search-tool.js help

# 列出所有引擎
node search-tool.js engines

# 查看搜索运算符
node search-tool.js operators

# 搜索示例
node search-tool.js search "openclaw documentation" --engine google
node search-tool.js search "人工智能" --chinese
node search-tool.js search "privacy tools" --privacy
```

## 文件结构

```
skills/multi-search-engine/
├── SKILL.md              # 技能定义和核心文档
├── search-tool.js        # 主要搜索工具
├── EXAMPLES.md           # 使用示例
├── README.md             # 本文件
└── (搜索历史自动保存在 memory/search-history/)
```

## 使用示例

### 简单搜索
```bash
# 英文搜索（自动使用 Google）
node search-tool.js "machine learning"

# 中文搜索（自动使用百度）
node search-tool.js "机器学习"
```

### 高级搜索
```bash
# 在 GitHub 中搜索
node search-tool.js search "site:github.com openclaw"

# 搜索 PDF 文件
node search-tool.js search "filetype:pdf deep learning"

# 最近一周的新闻
node search-tool.js search "AI news" --time past-week --type news
```

### 多引擎比较
```bash
# 使用所有中文引擎
node search-tool.js search "中国科技发展" --chinese

# 使用所有全球引擎
node search-tool.js search "global technology trends" --global

# 使用隐私保护引擎
node search-tool.js search "online privacy" --privacy
```

## 与 OpenClaw 集成

### 在 OpenClaw 会话中调用
```javascript
// 在技能中集成搜索功能
const { performSearch } = require('./search-tool.js');

// 执行搜索
performSearch("查询内容", { 
  engine: "baidu",
  type: "web",
  time: "past-week"
});
```

### 搜索历史
所有搜索自动记录在：
```
memory/search-history/searches.md
```

## 配置选项

### 默认设置
- 主要引擎：Google（英文）/ Baidu（中文）
- 每页结果数：10
- 安全搜索：中等
- 语言：自动检测
- 地区：自动检测

### 自定义配置
可通过修改 `search-tool.js` 中的配置对象来自定义：
- 默认引擎
- 搜索结果数量
- 安全搜索级别
- 语言和地区偏好

## 隐私和安全

### 数据保护
- 搜索查询本地处理
- 不收集个人信息
- 可选的搜索历史记录
- 加密通信

### 合法使用
- 遵守 robots.txt
- 尊重速率限制
- 适当使用缓存
- 正确引用来源

## 性能优化

### 提高速度
- 使用最近的区域服务器
- 启用缓存
- 限制并发请求
- 优先使用轻量级引擎

### 提高准确性
- 使用多个引擎比较
- 检查时间过滤器
- 使用高级运算符
- 验证权威来源

## 故障排除

### 常见问题
1. **引擎无响应**：尝试其他引擎
2. **速率限制**：等待或切换引擎
3. **防火墙阻止**：使用不同引擎或代理
4. **结果不准确**：检查搜索语法
5. **性能缓慢**：减少并发搜索

### 错误处理
- "引擎超时"：服务器慢或宕机
- "访问被拒绝"：IP 被阻止或限制
- "无效查询"：检查搜索语法
- "无结果"：尝试不同关键词
- "API 限制"：等待后重试

## 基于 ClawHub 版本

这个本地版本基于 ClawHub 上的 `gpyAngyoujun/multi-search-engine v2.0.1`。由于 API 速率限制，我们无法直接安装官方版本，但这个版本包含了核心功能。

### 与原版差异
1. **本地实现**：无需网络 API 调用
2. **简化引擎**：实现了最常用的 9 个引擎
3. **交互工具**：添加了交互式搜索界面
4. **中文文档**：完整的本地化文档

### 未来升级
当 ClawHub 速率限制重置后，可以：
1. 尝试安装官方版本
2. 比较功能差异
3. 合并改进内容
4. 更新本地版本

## 贡献和改进

### 建议改进
1. 添加更多搜索引擎
2. 改进结果解析
3. 添加缓存机制
4. 增强隐私保护
5. 优化性能

### 问题反馈
如遇到问题，请：
1. 检查搜索语法
2. 尝试不同引擎
3. 查看错误信息
4. 参考 EXAMPLES.md

## 许可证和版权

基于 gpyAngyoujun 在 ClawHub 上分享的 multi-search-engine 技能概念创建。仅供学习和研究使用。

**注意**：请尊重各搜索引擎的服务条款，合理使用搜索功能。