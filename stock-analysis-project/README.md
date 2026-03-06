# 股票分析项目

基于 udiedrichsen/stock-analysis v6.2.0 的本地实现版本。

## 项目概述

这是一个全面的股票和加密货币分析工具，提供8维度股票分析、投资组合管理、股息分析等功能。

## 功能特性

### ✅ 已实现功能
1. **股票分析** - 8维度综合分析
2. **投资组合管理** - 创建、添加、查看投资组合
3. **股息分析** - 股息收益率、安全评分、收入评级
4. **多股票比较** - 批量分析和比较

### 📋 计划功能
1. 观察列表与价格警报
2. 热门股票扫描
3. 谣言和早期信号检测
4. 加密货币分析增强

## 快速开始

### 1. 安装依赖
```bash
# 使用 pip
pip install yfinance pandas fear-and-greed

# 或使用 uv（推荐）
uv pip install yfinance pandas fear-and-greed
```

### 2. 股票分析
```bash
# 分析单个股票
python analyze_stock.py AAPL

# 快速模式
python analyze_stock.py AAPL --fast

# 分析多个股票
python analyze_stock.py AAPL MSFT GOOGL

# JSON输出
python analyze_stock.py AAPL --output json
```

### 3. 投资组合管理
```bash
# 创建投资组合
python portfolio.py create "我的投资组合"

# 添加资产
python portfolio.py add AAPL --quantity 100 --cost 150
python portfolio.py add BTC-USD --quantity 0.5 --cost 40000

# 查看投资组合
python portfolio.py show --portfolio "我的投资组合"

# 列出所有投资组合
python portfolio.py list
```

### 4. 股息分析
```bash
# 分析股息
python dividends.py JNJ

# 比较多个股息股票
python dividends.py JNJ PG KO MCD --compare

# 过滤条件
python dividends.py JNJ PG KO --min-yield 0.03 --min-safety 60
```

## 分析维度说明

### 股票分析（8维度）
| 维度 | 权重 | 说明 |
|------|------|------|
| 收益惊喜 | 30% | EPS超出/低于预期的情况 |
| 基本面 | 20% | 市盈率、利润率、增长率、债务等 |
| 分析师情绪 | 20% | 分析师评级和目标价格 |
| 动量 | 15% | RSI、52周区间、成交量 |
| 其他维度 | 15% | 市场环境、行业表现、情绪等 |

### 输出示例
```
=============================================================================
股票分析: AAPL (Apple Inc.)
生成时间: 2024-03-06 11:48:00
=============================================================================
建议: BUY (置信度: 78.5%, 综合评分: 82.3/100)
当前价格: $175.50
目标价格: $201.83

分析维度:
  • 收益惊喜: 85.0/100 (30%权重) - 超出预期 12.3%
  • 基本面: 78.5/100 (20%权重) - 市盈率合理，现金流健康
  • 分析师情绪: 90.0/100 (20%权重) - 多数买入评级
  • 动量: 75.0/100 (15%权重) - 强劲上涨趋势

支持点:
  • 收益惊喜: 超出预期 12.3%
  • 基本面: 市盈率合理，现金流健康

风险提示:
  • 超买警告: RSI 72，接近52周高点

市场情绪: Greed (指数: 75)
=============================================================================
免责声明：本分析基于公开数据，不构成财务建议。投资有风险，决策需谨慎。
=============================================================================
```

## 数据源

- **Yahoo Finance** - 主要股票和加密货币数据
- **CNN Fear & Greed Index** - 市场情绪指数
- **公开API** - 实时价格和基本面数据

## 项目结构

```
stock-analysis-project/
├── analyze_stock.py      # 股票分析主脚本
├── portfolio.py          # 投资组合管理
├── dividends.py          # 股息分析
├── README.md            # 项目文档
├── requirements.txt     # Python依赖
└── data/               # 数据存储目录
    └── portfolios.json # 投资组合数据
```

## 配置说明

### 数据存储位置
- 投资组合数据: `~/.clawdbot/skills/stock-analysis/portfolios.json`
- 缓存数据: 内存缓存，重启后失效

### 环境变量（可选）
```bash
# 设置代理（如果需要）
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

## 使用示例

### 场景1：定期投资组合检查
```bash
# 每周检查投资组合
python portfolio.py show --portfolio "长期投资"
```

### 场景2：股息投资研究
```bash
# 寻找安全的高股息股票
python dividends.py JNJ PG KO MCD --min-yield 0.03 --min-safety 70 --compare
```

### 场景3：快速股票评估
```bash
# 快速查看多个股票
python analyze_stock.py AAPL MSFT GOOGL AMZN --fast
```

### 场景4：投资决策支持
```bash
# 全面分析潜在投资
python analyze_stock.py TSLA --output json > tsla_analysis.json
```

## 注意事项

### 数据延迟
- Yahoo Finance 数据有15-20分钟延迟
- 盘前盘后交易数据可能不完整
- 股息数据基于最近12个月

### 使用限制
- 仅供个人研究和教育使用
- 不构成财务建议
- 遵守Yahoo Finance使用条款
- 避免高频请求（可能被封IP）

### 风险提示
1. **市场风险**：股票价格可能波动
2. **数据风险**：数据可能不准确或不完整
3. **技术风险**：API可能变更或失效
4. **投资风险**：过去表现不代表未来结果

## 故障排除

### 常见问题
1. **数据获取失败**
   ```bash
   # 检查网络连接
   ping finance.yahoo.com
   
   # 尝试使用VPN
   # 等待后重试
   ```

2. **依赖包错误**
   ```bash
   # 重新安装依赖
   pip uninstall yfinance pandas -y
   pip install yfinance pandas --upgrade
   ```

3. **Python版本问题**
   ```bash
   # 检查Python版本
   python --version  # 需要 >= 3.8
   ```

4. **权限问题**
   ```bash
   # 确保有写入权限
   ls -la ~/.clawdbot/
   ```

### 错误信息
- `ModuleNotFoundError`: 安装缺失的Python包
- `ConnectionError`: 检查网络连接
- `JSONDecodeError`: 数据格式错误，清除缓存
- `KeyError`: 数据字段缺失，股票可能已退市或代码错误

## 性能优化

### 缓存策略
- 价格数据：内存缓存15分钟
- 基本面数据：内存缓存1小时
- 投资组合数据：本地JSON文件持久化

### 批量处理
- 多股票分析使用并行请求
- 增量更新避免重复获取
- 错误重试机制（最多3次）

### 内存管理
- 及时释放大数据集
- 使用生成器处理流数据
- 限制历史数据长度

## 扩展开发

### 添加新功能
1. 在相应脚本中添加新函数
2. 更新命令行参数解析
3. 添加测试用例
4. 更新文档

### 集成其他数据源
1. 创建新的数据获取模块
2. 实现标准数据接口
3. 配置数据源优先级
4. 添加错误处理

### 自定义分析逻辑
1. 修改 `analyze_stock.py` 中的维度函数
2. 调整权重配置
3. 添加新的分析指标
4. 优化评分算法

## 更新日志

### v1.0.0 (2024-03-06)
- ✅ 基础股票分析功能
- ✅ 投资组合管理
- ✅ 股息分析
- ✅ 多股票比较
- ✅ JSON输出支持

### 计划更新
- 观察列表和价格警报
- 热门股票扫描
- 加密货币增强分析
- 图形化界面
- 定期报告生成

## 许可证

本项目基于 udiedrichsen/stock-analysis 的概念创建，仅供学习和研究使用。

**免责声明**：本工具不构成财务建议，用户应自行进行独立研究并承担投资风险。