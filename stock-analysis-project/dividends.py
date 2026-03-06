#!/usr/bin/env python3
"""
股息分析脚本
简化版本，基于 udiedrichsen/stock-analysis 的核心概念
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional
import yfinance as yf

@dataclass
class DividendAnalysis:
    """股息分析结果"""
    ticker: str
    company_name: str
    current_price: float
    dividend_yield: float  # 股息收益率
    dividend_per_share: float  # 每股股息
    payout_ratio: float  # 派息率
    dividend_growth_5yr: Optional[float]  # 5年股息增长率
    consecutive_years: Optional[int]  # 连续增长年数
    safety_score: float  # 安全评分 0-100
    income_rating: str  # 收入评级
    
    # 计算字段
    annual_income_per_share: float = 0.0
    yield_on_cost: float = 0.0

def analyze_dividend(ticker: str) -> Optional[DividendAnalysis]:
    """分析股息数据"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 基本数据
        company_name = info.get('longName', info.get('shortName', ticker))
        current_price = info.get('regularMarketPrice', info.get('currentPrice', 0))
        
        if current_price == 0:
            return None
        
        # 股息数据
        dividend_yield = info.get('dividendYield', 0)
        if dividend_yield is None:
            dividend_yield = 0
        
        # 每股股息
        dividend_rate = info.get('dividendRate', 0)
        if dividend_rate is None:
            dividend_rate = 0
        
        # 派息率
        payout_ratio = info.get('payoutRatio', 0)
        if payout_ratio is None:
            payout_ratio = 0
        
        # 股息增长率（简化）
        dividend_growth_5yr = info.get('dividendGrowth', None)
        
        # 连续增长年数（简化）
        consecutive_years = None
        
        # 计算安全评分
        safety_score = calculate_safety_score(
            dividend_yield=dividend_yield,
            payout_ratio=payout_ratio,
            current_price=current_price
        )
        
        # 收入评级
        income_rating = get_income_rating(dividend_yield, safety_score)
        
        # 计算字段
        annual_income_per_share = dividend_rate
        yield_on_cost = dividend_yield * 100  # 转换为百分比
        
        return DividendAnalysis(
            ticker=ticker,
            company_name=company_name,
            current_price=current_price,
            dividend_yield=dividend_yield,
            dividend_per_share=dividend_rate,
            payout_ratio=payout_ratio,
            dividend_growth_5yr=dividend_growth_5yr,
            consecutive_years=consecutive_years,
            safety_score=safety_score,
            income_rating=income_rating,
            annual_income_per_share=annual_income_per_share,
            yield_on_cost=yield_on_cost
        )
    
    except Exception as e:
        print(f"分析 {ticker} 时出错: {e}", file=sys.stderr)
        return None

def calculate_safety_score(dividend_yield: float, payout_ratio: float, current_price: float) -> float:
    """计算股息安全评分"""
    score = 50.0  # 基础分
    
    # 股息收益率评分
    if dividend_yield > 0:
        if 0.02 <= dividend_yield <= 0.06:  # 2-6% 合理范围
            score += 20
        elif dividend_yield > 0.06:  # >6% 可能不可持续
            score += 10
        elif dividend_yield < 0.02:  # <2% 太低
            score += 5
    else:
        score -= 20  # 无股息
    
    # 派息率评分
    if payout_ratio > 0:
        if payout_ratio <= 0.6:  # ≤60% 安全
            score += 20
        elif payout_ratio <= 0.8:  # 60-80% 一般
            score += 10
        else:  # >80% 高风险
            score -= 10
    
    # 确保分数在0-100之间
    return max(0, min(100, score))

def get_income_rating(dividend_yield: float, safety_score: float) -> str:
    """获取收入评级"""
    if dividend_yield == 0:
        return "无股息"
    
    if safety_score >= 80:
        return "优秀"
    elif safety_score >= 60:
        return "良好"
    elif safety_score >= 40:
        return "中等"
    else:
        return "较差"

def format_dividend_output(analysis: DividendAnalysis, output_format: str = "text") -> str:
    """格式化股息分析输出"""
    if output_format == "json":
        return json.dumps(asdict(analysis), indent=2, default=str)
    
    # 文本格式输出
    output = []
    output.append("=" * 60)
    output.append(f"股息分析: {analysis.ticker} ({analysis.company_name})")
    output.append("=" * 60)
    
    output.append(f"当前价格: ${analysis.current_price:.2f}")
    output.append(f"股息收益率: {analysis.dividend_yield * 100:.2f}%")
    output.append(f"每股股息: ${analysis.dividend_per_share:.2f}")
    output.append(f"年化股息收入/股: ${analysis.annual_income_per_share:.2f}")
    
    if analysis.payout_ratio:
        output.append(f"派息率: {analysis.payout_ratio * 100:.1f}%")
    else:
        output.append("派息率: 数据不可用")
    
    if analysis.dividend_growth_5yr:
        output.append(f"5年股息增长率: {analysis.dividend_growth_5yr * 100:.1f}%")
    
    if analysis.consecutive_years:
        output.append(f"连续增长年数: {analysis.consecutive_years} 年")
    
    output.append(f"安全评分: {analysis.safety_score:.1f}/100")
    output.append(f"收入评级: {analysis.income_rating}")
    
    # 投资建议
    output.append("\n投资建议:")
    if analysis.safety_score >= 70 and analysis.dividend_yield >= 0.03:
        output.append("  ✅ 优质股息股：收益率合理，安全性高")
    elif analysis.safety_score >= 50:
        output.append("  ⚠️  一般股息股：可考虑，但需监控风险")
    else:
        output.append("  ❌ 高风险股息股：收益率可能不可持续")
    
    output.append("=" * 60)
    output.append("注：股息数据基于最近12个月，实际支付可能变化")
    output.append("=" * 60)
    
    return "\n".join(output)

def compare_dividends(analyses: List[DividendAnalysis], output_format: str = "text") -> str:
    """比较多个股息股票"""
    if output_format == "json":
        return json.dumps([asdict(a) for a in analyses], indent=2, default=str)
    
    # 文本格式比较表
    output = []
    output.append("=" * 90)
    output.append("股息股票比较")
    output.append("=" * 90)
    output.append(f"{'代码':<8} {'公司':<25} {'价格':>8} {'收益率':>8} {'每股股息':>10} {'安全评分':>10} {'评级':>8}")
    output.append("-" * 90)
    
    for analysis in analyses:
        output.append(
            f"{analysis.ticker:<8} "
            f"{analysis.company_name[:24]:<25} "
            f"${analysis.current_price:>7.2f} "
            f"{analysis.dividend_yield*100:>7.2f}% "
            f"${analysis.dividend_per_share:>9.2f} "
            f"{analysis.safety_score:>9.1f} "
            f"{analysis.income_rating:>8}"
        )
    
    output.append("=" * 90)
    
    # 排序建议
    sorted_by_safety = sorted(analyses, key=lambda x: x.safety_score, reverse=True)
    sorted_by_yield = sorted(analyses, key=lambda x: x.dividend_yield, reverse=True)
    
    output.append("\n推荐排序:")
    output.append("1. 按安全性排序:")
    for i, analysis in enumerate(sorted_by_safety[:3], 1):
        output.append(f"   {i}. {analysis.ticker} (安全分: {analysis.safety_score:.1f}, 收益率: {analysis.dividend_yield*100:.2f}%)")
    
    output.append("\n2. 按收益率排序:")
    for i, analysis in enumerate(sorted_by_yield[:3], 1):
        output.append(f"   {i}. {analysis.ticker} (收益率: {analysis.dividend_yield*100:.2f}%, 安全分: {analysis.safety_score:.1f})")
    
    output.append("=" * 90)
    
    return "\n".join(output)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="股息分析工具")
    parser.add_argument("tickers", nargs="+", help="股票代码")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--compare", action="store_true", help="比较模式")
    parser.add_argument("--min-yield", type=float, default=0, help="最小股息收益率（例如: 0.03 表示 3%）")
    parser.add_argument("--min-safety", type=float, default=0, help="最小安全评分（0-100）")
    
    args = parser.parse_args()
    
    analyses = []
    
    for ticker in args.tickers:
        analysis = analyze_dividend(ticker.upper())
        if analysis:
            # 应用过滤器
            if analysis.dividend_yield >= args.min_yield and analysis.safety_score >= args.min_safety:
                analyses.append(analysis)
            elif args.min_yield == 0 and args.min_safety == 0:
                analyses.append(analysis)
        else:
            print(f"警告：无法分析 {ticker}，跳过", file=sys.stderr)
    
    if not analyses:
        print("错误：没有可分析的股票", file=sys.stderr)
        sys.exit(1)
    
    if args.compare:
        print(compare_dividends(analyses, args.output))
    else:
        for analysis in analyses:
            print(format_dividend_output(analysis, args.output))
            print()  # 空行分隔

if __name__ == "__main__":
    main()