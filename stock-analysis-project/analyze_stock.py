#!/usr/bin/env python3
"""
股票分析主脚本，使用Yahoo Finance数据进行8维度股票分析和加密货币分析
基于 udiedrichsen/stock-analysis v6.2.0 的核心功能
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Literal, Optional, Tuple, List, Dict
import pandas as pd

try:
    import yfinance as yf
    from fear_and_greed import FearAndGreed
    HAS_DEPS = True
except ImportError as e:
    print(f"错误：缺少依赖包: {e}")
    print("请安装: pip install yfinance pandas fear-and-greed")
    HAS_DEPS = False
    sys.exit(1)

@dataclass
class StockData:
    """股票数据类，存储从Yahoo Finance获取的所有数据"""
    ticker: str
    asset_type: Literal["stock", "crypto"]
    info: Dict
    earnings_history: Optional[pd.DataFrame]
    analyst_info: Optional[Dict]
    price_history: Optional[pd.DataFrame]
    company_name: str = ""
    current_price: float = 0.0
    market_cap: float = 0.0

@dataclass
class AnalysisDimension:
    """分析维度结果"""
    name: str
    score: float  # 0-100分
    weight: float  # 权重百分比
    explanation: str
    details: Dict

@dataclass
class StockAnalysisResult:
    """股票分析结果"""
    ticker: str
    company_name: str
    timestamp: str
    recommendation: Literal["BUY", "HOLD", "SELL"]
    confidence: float  # 0-1
    current_price: float
    target_price: Optional[float]
    supporting_points: List[str]
    caveats: List[str]
    dimensions: List[AnalysisDimension]
    total_score: float

def fetch_stock_data(ticker: str, verbose: bool = False) -> Optional[StockData]:
    """
    从Yahoo Finance获取股票数据，带重试逻辑
    Args:
        ticker: 股票代码
        verbose: 是否打印调试信息
    Returns:
        StockData对象或None
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if verbose:
                print(f"正在获取 {ticker} 的数据...", file=sys.stderr)
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 检测资产类型
            asset_type = "crypto" if ticker.endswith("-USD") else "stock"
            
            # 获取公司名称
            company_name = info.get('longName', info.get('shortName', ticker))
            
            # 获取当前价格
            current_price = info.get('regularMarketPrice', info.get('currentPrice', 0))
            
            # 获取市值
            market_cap = info.get('marketCap', 0)
            
            # 获取收益历史
            try:
                earnings_history = stock.earnings
                if earnings_history is not None and earnings_history.empty:
                    earnings_history = None
            except:
                earnings_history = None
            
            # 获取分析师信息
            try:
                analyst_info = {
                    'recommendations': stock.recommendations,
                    'upgrades_downgrades': stock.upgrades_downgrades,
                    'earnings_dates': stock.earnings_dates
                }
            except:
                analyst_info = None
            
            # 获取价格历史
            try:
                price_history = stock.history(period="1y")
                if price_history.empty:
                    price_history = None
            except:
                price_history = None
            
            return StockData(
                ticker=ticker,
                asset_type=asset_type,
                info=info,
                earnings_history=earnings_history,
                analyst_info=analyst_info,
                price_history=price_history,
                company_name=company_name,
                current_price=current_price,
                market_cap=market_cap
            )
            
        except Exception as e:
            if verbose:
                print(f"获取 {ticker} 数据失败 (尝试 {attempt+1}/{max_retries}): {e}", file=sys.stderr)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                time.sleep(wait_time)
    
    return None

def analyze_earnings_surprise(data: StockData) -> AnalysisDimension:
    """分析收益惊喜情况（权重30%）"""
    score = 50.0  # 默认分数
    explanation = "无收益数据可用"
    details = {}
    
    if data.earnings_history is not None and not data.earnings_history.empty:
        try:
            # 获取最近的收益数据
            latest_earnings = data.earnings_history.iloc[-1]
            actual_eps = latest_earnings.get("Reported EPS")
            expected_eps = latest_earnings.get("EPS Estimate")
            
            if actual_eps is not None and expected_eps is not None:
                # 计算惊喜百分比
                surprise_pct = ((actual_eps - expected_eps) / abs(expected_eps)) * 100
                
                # 计算分数：惊喜越大分数越高
                if surprise_pct > 0:
                    score = min(100, 50 + surprise_pct * 2)  # 超出预期加分
                    explanation = f"超出预期 {surprise_pct:.1f}%"
                else:
                    score = max(0, 50 + surprise_pct * 2)    # 低于预期减分
                    explanation = f"低于预期 {abs(surprise_pct):.1f}%"
                
                details = {
                    "actual_eps": actual_eps,
                    "expected_eps": expected_eps,
                    "surprise_pct": surprise_pct
                }
        except:
            pass
    
    return AnalysisDimension(
        name="收益惊喜",
        score=score,
        weight=30.0,
        explanation=explanation,
        details=details
    )

def analyze_fundamentals(data: StockData) -> AnalysisDimension:
    """分析基本面（权重20%）"""
    score = 50.0
    explanation = "基本面数据有限"
    details = {}
    
    info = data.info
    
    # 检查关键基本面指标
    metrics = []
    
    # 市盈率
    pe_ratio = info.get('trailingPE')
    if pe_ratio:
        if pe_ratio < 15:
            metrics.append(f"市盈率较低({pe_ratio:.1f})")
            score += 10
        elif pe_ratio > 30:
            metrics.append(f"市盈率较高({pe_ratio:.1f})")
            score -= 10
        details['pe_ratio'] = pe_ratio
    
    # 市净率
    pb_ratio = info.get('priceToBook')
    if pb_ratio:
        details['pb_ratio'] = pb_ratio
    
    # 债务权益比
    debt_to_equity = info.get('debtToEquity')
    if debt_to_equity:
        if debt_to_equity < 0.5:
            metrics.append(f"债务水平健康({debt_to_equity:.2f})")
            score += 5
        elif debt_to_equity > 1.0:
            metrics.append(f"债务较高({debt_to_equity:.2f})")
            score -= 5
        details['debt_to_equity'] = debt_to_equity
    
    # 利润率
    profit_margins = info.get('profitMargins')
    if profit_margins:
        if profit_margins > 0.15:
            metrics.append(f"利润率良好({profit_margins:.1%})")
            score += 10
        details['profit_margins'] = profit_margins
    
    # 收入增长率
    revenue_growth = info.get('revenueGrowth')
    if revenue_growth:
        if revenue_growth > 0.1:
            metrics.append(f"收入增长强劲({revenue_growth:.1%})")
            score += 10
        elif revenue_growth < 0:
            metrics.append(f"收入下降({revenue_growth:.1%})")
            score -= 10
        details['revenue_growth'] = revenue_growth
    
    # 确保分数在0-100之间
    score = max(0, min(100, score))
    
    if metrics:
        explanation = ", ".join(metrics)
    
    return AnalysisDimension(
        name="基本面",
        score=score,
        weight=20.0,
        explanation=explanation,
        details=details
    )

def analyze_analyst_sentiment(data: StockData) -> AnalysisDimension:
    """分析师情绪分析（权重20%）"""
    score = 50.0
    explanation = "无分析师数据"
    details = {}
    
    if data.analyst_info and 'recommendations' in data.analyst_info:
        try:
            recommendations = data.analyst_info['recommendations']
            if recommendations is not None and not recommendations.empty:
                # 获取最新评级
                latest = recommendations.iloc[-1]
                
                # 简化评分：买入=100，持有=50，卖出=0
                rating_map = {
                    'Buy': 100,
                    'Strong Buy': 100,
                    'Outperform': 80,
                    'Market Perform': 50,
                    'Hold': 50,
                    'Underperform': 20,
                    'Sell': 0,
                    'Strong Sell': 0
                }
                
                firm = latest.get('Firm', '')
                to_grade = latest.get('To Grade', '')
                
                if to_grade in rating_map:
                    score = rating_map[to_grade]
                    explanation = f"{firm}: {to_grade}"
                else:
                    explanation = f"{firm}评级: {to_grade}"
                
                details = {
                    "firm": firm,
                    "rating": to_grade,
                    "date": latest.name.strftime('%Y-%m-%d') if hasattr(latest.name, 'strftime') else str(latest.name)
                }
        except:
            pass
    
    return AnalysisDimension(
        name="分析师情绪",
        score=score,
        weight=20.0,
        explanation=explanation,
        details=details
    )

def analyze_momentum(data: StockData) -> AnalysisDimension:
    """动量分析（权重15%）"""
    score = 50.0
    explanation = "动量数据不足"
    details = {}
    
    if data.price_history is not None and not data.price_history.empty:
        try:
            prices = data.price_history['Close']
            
            # 计算简单动量指标
            current_price = prices.iloc[-1]
            price_20d_ago = prices.iloc[-20] if len(prices) >= 20 else prices.iloc[0]
            price_50d_ago = prices.iloc[-50] if len(prices) >= 50 else prices.iloc[0]
            
            momentum_20d = (current_price - price_20d_ago) / price_20d_ago * 100
            momentum_50d = (current_price - price_50d_ago) / price_50d_ago * 100
            
            # 基于动量评分
            if momentum_20d > 5 and momentum_50d > 10:
                score = 80
                explanation = f"强劲上涨趋势(20日:{momentum_20d:.1f}%, 50日:{momentum_50d:.1f}%)"
            elif momentum_20d < -5 and momentum_50d < -10:
                score = 20
                explanation = f"下跌趋势(20日:{momentum_20d:.1f}%, 50日:{momentum_50d:.1f}%)"
            else:
                score = 50
                explanation = f"横盘整理(20日:{momentum_20d:.1f}%, 50日:{momentum_50d:.1f}%)"
            
            details = {
                "momentum_20d": momentum_20d,
                "momentum_50d": momentum_50d,
                "current_price": current_price
            }
            
        except:
            pass
    
    return AnalysisDimension(
        name="动量",
        score=score,
        weight=15.0,
        explanation=explanation,
        details=details
    )

def get_market_sentiment() -> Dict:
    """获取市场情绪数据"""
    try:
        fgi = FearAndGreed()
        return {
            "fear_greed_index": fgi.value,
            "classification": fgi.classification,
            "last_update": fgi.last_update.strftime('%Y-%m-%d') if fgi.last_update else None
        }
    except:
        return {
            "fear_greed_index": 50,
            "classification": "Neutral",
            "last_update": None
        }

def synthesize_signal(dimensions: List[AnalysisDimension], data: StockData) -> StockAnalysisResult:
    """合成最终信号"""
    # 计算加权总分
    total_score = sum(d.score * d.weight for d in dimensions) / sum(d.weight for d in dimensions)
    
    # 生成建议
    if total_score >= 70:
        recommendation = "BUY"
        confidence = (total_score - 70) / 30  # 70-100映射到0-1
    elif total_score >= 40:
        recommendation = "HOLD"
        confidence = (total_score - 40) / 30  # 40-70映射到0-1
    else:
        recommendation = "SELL"
        confidence = (40 - total_score) / 40  # 0-40映射到1-0
    
    # 确保置信度在0-1之间
    confidence = max(0.0, min(1.0, confidence))
    
    # 生成支持点
    supporting_points = []
    for dim in dimensions:
        if dim.score >= 70:
            supporting_points.append(f"{dim.name}: {dim.explanation}")
    
    # 生成风险提示
    caveats = []
    for dim in dimensions:
        if dim.score <= 30:
            caveats.append(f"{dim.name}: {dim.explanation}")
    
    # 计算目标价格（简化版）
    target_price = None
    if data.current_price > 0:
        if recommendation == "BUY":
            target_price = data.current_price * 1.15  # 15%上涨目标
        elif recommendation == "SELL":
            target_price = data.current_price * 0.85  # 15%下跌目标
    
    return StockAnalysisResult(
        ticker=data.ticker,
        company_name=data.company_name,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        recommendation=recommendation,
        confidence=confidence,
        current_price=data.current_price,
        target_price=target_price,
        supporting_points=supporting_points,
        caveats=caveats,
        dimensions=dimensions,
        total_score=total_score
    )

def format_output(result: StockAnalysisResult, output_format: str = "text"):
    """格式化输出"""
    if output_format == "json":
        return json.dumps(asdict(result), indent=2, default=str)
    
    # 文本格式输出
    output = []
    output.append("=" * 77)
    output.append(f"股票分析: {result.ticker} ({result.company_name})")
    output.append(f"生成时间: {result.timestamp}")
    output.append("=" * 77)
    output.append(f"建议: {result.recommendation} (置信度: {result.confidence:.1%}, 综合评分: {result.total_score:.1f}/100)")
    output.append(f"当前价格: ${result.current_price:.2f}")
    if result.target_price:
        output.append(f"目标价格: ${result.target_price:.2f}")
    
    output.append("\n分析维度:")
    for dim in result.dimensions:
        output.append(f"  • {dim.name}: {dim.score:.1f}/100 ({dim.weight:.0f}%权重) - {dim.explanation}")
    
    if result.supporting_points:
        output.append("\n支持点:")
        for point in result.supporting_points:
            output.append(f"  • {point}")
    
    if result.caveats:
        output.append("\n风险提示:")
        for caveat in result.caveats:
            output.append(f"  • {caveat}")
    
    # 添加市场情绪
    market_sentiment = get_market_sentiment()
    output.append(f"\n市场情绪: {market_sentiment['classification']} (指数: {market_sentiment['fear_greed_index']})")
    
    output.append("=" * 77)
    output.append("免责声明：本分析基于公开数据，不构成财务建议。投资有风险，决策需谨慎。")
    output.append("=" * 77)
    
    return "\n".join(output)

def main():
    """主函数"""
    if not HAS_DEPS:
        print("错误：缺少必要的Python依赖包")
        print("请运行: pip install yfinance pandas fear-and-greed")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="股票和加密货币分析工具")
    parser.add_argument("tickers", nargs="+", help="股票或加密货币代码（例如：AAPL, BTC-USD）")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--fast", action="store_true", help="快速模式，跳过详细分析")
    args = parser.parse_args()
    
    results = []
    
    for ticker in args.tickers:
        if args.verbose:
            print(f"\n分析 {ticker}...", file=sys.stderr)
        
        # 获取数据
        data = fetch_stock_data(ticker.upper(), verbose=args.verbose)
        if not data:
            print(f"错误：无法获取 {ticker} 的数据", file=sys.stderr)
            continue
        
        # 分析各个维度
        dimensions = [
            analyze_earnings_surprise(data),
            analyze_fundamentals(data),
            analyze_analyst_sentiment(data),
            analyze_momentum(data)
        ]
        
        # 如果是快速模式，跳过其他维度
        if not args.fast:
            # 这里可以添加更多维度分析
            pass
        
        # 合成信号
        result = synthesize_signal(dimensions, data)
        results.append(result)
    
    # 输出结果
    if args.output == "json":
        print(json.dumps([asdict(r) for r in results], indent=2, default=str))
    else:
        for result in results:
            print(format_output(result))
            print()  # 空行分隔

if __name__ == "__main__":
    main()
