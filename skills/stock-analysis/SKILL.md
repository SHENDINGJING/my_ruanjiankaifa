---
name: stock-analysis
description: 使用Yahoo Finance数据分析股票和加密货币，支持投资组合管理、带警报的观察列表、股息分析、8维度股票评分、热门趋势检测（Hot Scanner）和谣言/早期信号检测（Rumor Scanner）。可用于股票分析、投资组合跟踪、收益反应分析、加密货币监控、热门股票发现，或在主流新闻之前找到市场谣言。
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": ["python", "uv"],
          "python": "3.10+",
          "packages": [
            "yfinance>=0.2.40",
            "pandas>=2.0.0", 
            "fear-and-greed>=0.4",
            "edgartools>=2.0.0",
            "feedparser>=6.0.0"
          ]
        },
        "install": [
          {
            "id": "python-deps",
            "kind": "python",
            "command": "uv pip install yfinance pandas fear-and-greed edgartools feedparser"
          }
        ],
      },
  }
---

# Stock Analysis Skill

基于 udiedrichsen/stock-analysis v6.2.0 的股票与加密货币分析技能。

## 功能概述

这是一个全面的股票和加密货币分析工具，支持：

### 核心功能
1. **8维度股票分析** - 全面的股票评估
2. **加密货币分析** - 数字货币市场分析
3. **投资组合管理** - 多投资组合跟踪
4. **观察列表与警报** - 价格目标、止损、信号变化警报
5. **股息分析** - 股息收益率、安全评分等
6. **热门扫描** - 实时热门股票和加密货币发现
7. **谣言扫描** - 早期信号、并购谣言、内幕交易检测

### 数据源整合
- Yahoo Finance - 主要股票和加密货币数据
- CoinGecko - 加密货币市场数据
- CNN Fear & Greed Index - 市场情绪指数
- SEC EDGAR - 公司财务文件
- Google News - 财经新闻
- Twitter/X & Reddit - 社交媒体情绪（可选）

## 安装要求

### 系统要求
- Python 3.10+
- uv 包管理器（推荐）或 pip

### Python依赖包
```bash
# 使用 uv 安装
uv pip install yfinance pandas fear-and-greed edgartools feedparser

# 或使用 pip
pip install yfinance>=0.2.40 pandas>=2.0.0 fear-and-greed>=0.4 edgartools>=2.0.0 feedparser>=6.0.0
```

## 命令参考

### 股票分析
```bash
# 基本分析
uv run scripts/analyze_stock.py AAPL

# 快速模式（跳过内幕交易和突发新闻）
uv run scripts/analyze_stock.py AAPL --fast

# 比较多个股票
uv run scripts/analyze_stock.py AAPL MSFT GOOGL

# 加密货币分析
uv run scripts/analyze_stock.py BTC-USD ETH-USD
```

### 股息分析
```bash
# 分析股息
uv run scripts/dividends.py JNJ

# 比较股息股票
uv run scripts/dividends.py JNJ PG KO MCD --output json
```

### 观察列表与警报
```bash
# 添加到观察列表
uv run scripts/watchlist.py add AAPL

# 带价格目标警报
uv run scripts/watchlist.py add AAPL --target 200

# 带止损警报
uv run scripts/watchlist.py add AAPL --stop 150

# 信号变化警报
uv run scripts/watchlist.py add AAPL --alert-on signal

# 查看观察列表
uv run scripts/watchlist.py list

# 检查触发的警报
uv run scripts/watchlist.py check

# 移除观察列表
uv run scripts/watchlist.py remove AAPL
```

### 投资组合管理
```bash
# 创建投资组合
uv run scripts/portfolio.py create "Tech Portfolio"

# 添加资产
uv run scripts/portfolio.py add AAPL --quantity 100 --cost 150
uv run scripts/portfolio.py add BTC-USD --quantity 0.5 --cost 40000

# 查看投资组合
uv run scripts/portfolio.py show

# 分析投资组合
uv run scripts/analyze_stock.py --portfolio "Tech Portfolio" --period weekly
```

### 热门扫描
```bash
# 完整扫描
python3 scripts/hot_scanner.py

# 快速扫描（跳过社交媒体）
python3 scripts/hot_scanner.py --no-social

# JSON输出
python3 scripts/hot_scanner.py --json
```

### 谣言扫描
```bash
# 查找早期信号、并购谣言、内幕交易活动
python3 scripts/rumor_scanner.py
```

## 分析维度

### 股票分析（8维度）
| 维度 | 权重 | 描述 |
|------|------|------|
| 收益惊喜 | 30% | EPS超出/低于预期的情况 |
| 基本面 | 20% | 市盈率、利润率、增长率、债务等 |
| 分析师情绪 | 20% | 分析师评级和目标价格 |
| 历史模式 | 10% | 过去的收益反应模式 |
| 市场环境 | 10% | VIX指数、SPY/QQQ趋势 |
| 行业表现 | 15% | 相对行业强度 |
| 动量 | 15% | RSI、52周区间、成交量 |
| 情绪 | 10% | 恐惧/贪婪指数、空头头寸、内幕交易、看跌/看涨比率 |

### 加密货币分析（3维度）
1. **市值与分类** - 加密货币的市值排名和分类
2. **BTC相关性** - 30天内与比特币的相关性
3. **动量** - RSI和价格区间

## 风险检测

技能会检测以下风险：
- **收益前风险**：距离收益发布少于14天，预期高波动性
- **收益后飙升**：5天内涨幅超过15%，收益可能已被定价
- **超买**：RSI>70且接近52周高点，高风险入场
- **风险规避模式**：GLD/TLT/UUP同时上涨，资金流向避险资产
- **地缘政治风险**：检测台湾、中国、俄罗斯、中东等地缘政治关键词
- **突发新闻风险**：过去24小时内的危机关键词

## 输出示例

### 股票分析输出
```
=============================================================================
股票分析: AAPL (Apple Inc.)
生成时间: 2024-03-06 11:48:00
=============================================================================
建议: BUY (置信度: 78.5%)

支持点:
• 收益惊喜: 超出预期 12.3% - EPS $2.18 对比预期 $1.94
• 基本面强劲: 市盈率合理，现金流健康
• 分析师情绪积极: 85%买入评级，平均目标价 $205
• 行业表现优异: 相对科技板块表现+15%

风险提示:
• 超买警告: RSI 72，接近52周高点
• 市场环境: VIX指数上升，市场波动性增加
=============================================================================
免责声明：不构成财务建议。
=============================================================================
```

### 投资组合摘要
```
投资组合: Tech Portfolio
创建时间: 2024-03-01
总价值: $125,430.50
总成本: $98,750.00
总收益: $26,680.50 (+27.0%)

资产分布:
• AAPL: 40.2% ($50,400.00) | 收益: +$12,600.00 (+33.3%)
• MSFT: 35.8% ($44,880.50) | 收益: +$8,980.50 (+25.0%)
• BTC-USD: 24.0% ($30,150.00) | 收益: +$5,100.00 (+20.4%)
```

## 配置文件

### 数据存储位置
- 投资组合数据: `~/.clawdbot/skills/stock-analysis/portfolios.json`
- 观察列表数据: `~/.clawdbot/skills/stock-analysis/watchlist.json`
- 缓存数据: `~/.clawdbot/skills/stock-analysis/cache/`

### 环境变量（可选）
```bash
# Twitter/X API（用于社交媒体情绪分析）
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"

# Reddit API（用于Reddit情绪分析）
export REDDIT_CLIENT_ID="your_id"
export REDDIT_CLIENT_SECRET="your_secret"
export REDDIT_USER_AGENT="your_user_agent"
```

## 使用场景

### 1. 快速股票评估
```bash
# 快速查看股票状态
uv run scripts/analyze_stock.py TSLA --fast
```

### 2. 投资组合定期检查
```bash
# 每周检查投资组合
uv run scripts/analyze_stock.py --portfolio "My Portfolio" --period weekly
```

### 3. 股息投资研究
```bash
# 寻找优质股息股票
uv run scripts/dividends.py --min-yield 3 --min-safety 70
```

### 4. 市场机会发现
```bash
# 发现热门机会
python3 scripts/hot_scanner.py --json | jq '.top_gainers[0:5]'
```

### 5. 风险监控
```bash
# 检查谣言和早期信号
python3 scripts/rumor_scanner.py --risk-only
```

## 安全注意事项

### 数据隐私
- 所有数据本地处理，不上传云端
- API密钥本地存储，加密保护
- 敏感数据不记录日志

### 使用限制
- 仅供个人研究和教育使用
- 不构成财务建议
- 遵守Yahoo Finance等数据源的使用条款
- 避免高频请求，防止IP被封

## 故障排除

### 常见问题
1. **数据获取失败**：检查网络连接，尝试使用VPN
2. **依赖包错误**：确保Python版本≥3.10，使用uv重新安装
3. **API限制**：Yahoo Finance有速率限制，等待后重试
4. **缓存问题**：清除缓存目录 `~/.clawdbot/skills/stock-analysis/cache/`

### 错误处理
- **无效股票代码**：验证代码格式（美股: AAPL, 加密货币: BTC-USD）
- **数据不完整**：某些股票可能缺少部分数据
- **网络超时**：增加超时时间或重试

## 性能优化

### 缓存策略
- 价格数据缓存1小时
- 基本面数据缓存24小时
- 新闻数据缓存30分钟

### 批量处理
- 多股票分析使用批量API调用
- 并行处理独立的数据源
- 增量更新避免重复获取

### 内存管理
- 大数据集使用分页处理
- 及时释放不再使用的数据
- 使用生成器处理流数据

## 扩展开发

### 添加新数据源
1. 在 `data_sources/` 目录创建新模块
2. 实现标准数据接口
3. 添加到分析管道配置

### 自定义分析维度
1. 修改 `analysis/dimensions.py`
2. 添加新的维度类
3. 更新权重配置

### 集成其他工具
- 导出到Excel: `--output excel`
- 发送到Telegram: `--telegram-bot`
- 生成报告PDF: `--report-pdf`

## 免责声明

**重要**：本工具仅供教育和研究目的使用，不构成财务建议。股票和加密货币投资存在风险，可能导致资金损失。用户应自行进行独立研究，并在必要时咨询专业财务顾问。

基于 udiedrichsen/stock-analysis v6.2.0 的功能文档创建。