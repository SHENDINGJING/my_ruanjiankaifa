#!/usr/bin/env python3
"""
中短线稳健型股票交易策略分析系统
严格遵循用户提供的策略框架
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np
import yfinance as yf

@dataclass
class StockData:
    """股票数据容器"""
    ticker: str
    company_name: str
    current_price: float
    data: pd.DataFrame  # 包含OHLCV和均线数据
    fundamentals: Dict
    industry: str

@dataclass
class TrendAnalysis:
    """趋势分析结果"""
    is_uptrend: bool
    ma_alignment: str  # "多头排列", "空头排列", "混乱"
    above_20ma: bool
    above_60ma: bool
    ma_20_direction: str  # "上升", "下降", "走平"
    ma_60_direction: str
    details: Dict

@dataclass
class VolumePriceAnalysis:
    """量价分析结果"""
    volume_increasing: bool  # 成交量温和放大
    volume_amplification: float  # 成交量增幅百分比
    yang_volume_greater: bool  # 阳量大于阴量
    abnormal_volume: bool  # 异常巨量
    continuous_decline: bool  # 连续缩量下跌
    details: Dict

@dataclass
class FundamentalAnalysis:
    """基本面分析结果"""
    profit_positive: bool  # 净利润为正
    profit_decline: float  # 净利润同比下降百分比
    has_negative_events: bool  # 有重大负面事件
    industry_supported: bool  # 行业受政策支持
    details: Dict

@dataclass
class BuySignal:
    """买入信号"""
    ticker: str
    company_name: str
    current_price: float
    trend_qualified: bool
    volume_price_qualified: bool
    fundamental_qualified: bool
    all_conditions_met: bool
    buy_reasons: List[str]
    warnings: List[str]
    suggested_position: float  # 建议仓位比例
    stop_loss_price: float  # 止损价
    target_price: float  # 目标价

@dataclass
class PortfolioPosition:
    """持仓管理"""
    ticker: str
    entry_price: float
    current_price: float
    position_size: float  # 仓位比例
    stop_loss: float
    profit_loss_pct: float
    status: str  # "持有", "止损", "止盈"

class TradingStrategyAnalyzer:
    """交易策略分析器"""
    
    def __init__(self):
        self.positions = {}
    
    def fetch_stock_data(self, ticker: str, period: str = "3mo") -> Optional[StockData]:
        """获取股票数据"""
        try:
            stock = yf.Ticker(ticker)
            
            # 获取历史数据
            hist = stock.history(period=period)
            if hist.empty:
                return None
            
            # 计算均线
            hist['MA5'] = hist['Close'].rolling(window=5).mean()
            hist['MA10'] = hist['Close'].rolling(window=10).mean()
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA60'] = hist['Close'].rolling(window=60).mean()
            
            # 计算成交量均线
            hist['Volume_MA5'] = hist['Volume'].rolling(window=5).mean()
            hist['Volume_MA10'] = hist['Volume'].rolling(window=10).mean()
            
            # 获取基本信息
            info = stock.info
            company_name = info.get('longName', info.get('shortName', ticker))
            current_price = info.get('regularMarketPrice', info.get('currentPrice', hist['Close'].iloc[-1]))
            industry = info.get('industry', '未知')
            
            # 基本面数据
            fundamentals = {
                'profitMargins': info.get('profitMargins'),
                'returnOnEquity': info.get('returnOnEquity'),
                'debtToEquity': info.get('debtToEquity'),
                'revenueGrowth': info.get('revenueGrowth'),
                'earningsGrowth': info.get('earningsGrowth')
            }
            
            return StockData(
                ticker=ticker,
                company_name=company_name,
                current_price=current_price,
                data=hist,
                fundamentals=fundamentals,
                industry=industry
            )
            
        except Exception as e:
            print(f"获取 {ticker} 数据失败: {e}", file=sys.stderr)
            return None
    
    def analyze_trend(self, data: StockData) -> TrendAnalysis:
        """趋势分析 - 第一步筛选"""
        df = data.data
        
        if len(df) < 60:
            return TrendAnalysis(
                is_uptrend=False,
                ma_alignment="数据不足",
                above_20ma=False,
                above_60ma=False,
                ma_20_direction="未知",
                ma_60_direction="未知",
                details={"error": "数据不足60天"}
            )
        
        # 获取最新数据
        latest = df.iloc[-1]
        prev_20 = df.iloc[-21] if len(df) >= 21 else df.iloc[0]
        prev_60 = df.iloc[-61] if len(df) >= 61 else df.iloc[0]
        
        # 检查是否在均线上方
        above_20ma = latest['Close'] > latest['MA20']
        above_60ma = latest['Close'] > latest['MA60']
        
        # 检查均线方向
        ma20_dir = "上升" if latest['MA20'] > prev_20['MA20'] else "下降" if latest['MA20'] < prev_20['MA20'] else "走平"
        ma60_dir = "上升" if latest['MA60'] > prev_60['MA60'] else "下降" if latest['MA60'] < prev_60['MA60'] else "走平"
        
        # 检查均线排列
        ma5 = latest['MA5']
        ma10 = latest['MA10']
        ma20 = latest['MA20']
        ma60 = latest['MA60']
        
        if ma5 > ma10 > ma20 > ma60:
            ma_alignment = "多头排列"
            is_uptrend = True
        elif ma5 < ma10 < ma20 < ma60:
            ma_alignment = "空头排列"
            is_uptrend = False
        else:
            ma_alignment = "混乱"
            is_uptrend = False
        
        # 严格排除条件
        if ma_alignment == "空头排列":
            is_uptrend = False
        if ma20_dir == "向下" or ma60_dir == "向下":
            is_uptrend = False
        
        details = {
            "price": latest['Close'],
            "ma5": ma5,
            "ma10": ma10,
            "ma20": ma20,
            "ma60": ma60,
            "ma_alignment": ma_alignment,
            "above_20ma": above_20ma,
            "above_60ma": above_60ma,
            "ma20_direction": ma20_dir,
            "ma60_direction": ma60_dir
        }
        
        return TrendAnalysis(
            is_uptrend=is_uptrend,
            ma_alignment=ma_alignment,
            above_20ma=above_20ma,
            above_60ma=above_60ma,
            ma_20_direction=ma20_dir,
            ma_60_direction=ma60_dir,
            details=details
        )
    
    def analyze_volume_price(self, data: StockData) -> VolumePriceAnalysis:
        """量价分析 - 第二步筛选"""
        df = data.data
        
        if len(df) < 20:
            return VolumePriceAnalysis(
                volume_increasing=False,
                volume_amplification=0,
                yang_volume_greater=False,
                abnormal_volume=False,
                continuous_decline=False,
                details={"error": "数据不足"}
            )
        
        # 获取最近10个交易日数据
        recent = df.tail(10)
        
        # 计算成交量变化
        volume_5_avg = recent['Volume'].tail(5).mean()
        volume_10_avg = recent['Volume'].mean()
        prev_volume_avg = df['Volume'].iloc[-20:-10].mean() if len(df) >= 30 else volume_10_avg
        
        # 成交量增幅
        if prev_volume_avg > 0:
            volume_amplification = (volume_10_avg - prev_volume_avg) / prev_volume_avg * 100
            volume_increasing = volume_amplification >= 30  # 增幅不低于30%
        else:
            volume_amplification = 0
            volume_increasing = False
        
        # 检查阳量阴量
        yang_days = recent[recent['Close'] > recent['Open']]
        yin_days = recent[recent['Close'] < recent['Open']]
        
        yang_volume_avg = yang_days['Volume'].mean() if not yang_days.empty else 0
        yin_volume_avg = yin_days['Volume'].mean() if not yin_days.empty else 0
        
        yang_volume_greater = yang_volume_avg > yin_volume_avg * 1.1  # 阳量大于阴量10%以上
        
        # 检查异常巨量
        avg_volume = recent['Volume'].mean()
        abnormal_volume = False
        for i in range(len(recent)):
            if recent['Volume'].iloc[i] > avg_volume * 3 and recent['Close'].iloc[i] < recent['Open'].iloc[i]:
                abnormal_volume = True
                break
        
        # 检查连续缩量下跌
        continuous_decline = False
        if len(recent) >= 3:
            decline_count = 0
            for i in range(1, len(recent)):
                if recent['Close'].iloc[i] < recent['Close'].iloc[i-1] and recent['Volume'].iloc[i] < recent['Volume'].iloc[i-1]:
                    decline_count += 1
                else:
                    decline_count = 0
                
                if decline_count >= 3:
                    continuous_decline = True
                    break
        
        details = {
            "volume_5_avg": volume_5_avg,
            "volume_10_avg": volume_10_avg,
            "prev_volume_avg": prev_volume_avg,
            "volume_amplification_pct": volume_amplification,
            "yang_volume_avg": yang_volume_avg,
            "yin_volume_avg": yin_volume_avg,
            "abnormal_volume_detected": abnormal_volume,
            "continuous_decline_detected": continuous_decline
        }
        
        return VolumePriceAnalysis(
            volume_increasing=volume_increasing,
            volume_amplification=volume_amplification,
            yang_volume_greater=yang_volume_greater,
            abnormal_volume=abnormal_volume,
            continuous_decline=continuous_decline,
            details=details
        )
    
    def analyze_fundamentals(self, data: StockData) -> FundamentalAnalysis:
        """基本面分析 - 第三步筛选"""
        # 简化版基本面分析
        # 在实际应用中，需要获取完整的财务报表数据
        
        fundamentals = data.fundamentals
        industry = data.industry.lower()
        
        # 检查净利润（简化）
        profit_margins = fundamentals.get('profitMargins')
        profit_positive = profit_margins is not None and profit_margins > 0
        
        # 假设净利润下降（简化）
        profit_decline = 0
        
        # 检查负面事件（简化）
        has_negative_events = False
        
        # 检查行业支持（简化）
        supported_industries = [
            'technology', '半导体', '芯片', '新能源', '光伏', '风电',
            '电动汽车', '电池', '人工智能', '大数据', '云计算',
            '生物医药', '医疗器械', '高端制造', '智能制造'
        ]
        
        industry_supported = any(keyword in industry for keyword in supported_industries)
        
        details = {
            "profit_margins": profit_margins,
            "industry": industry,
            "industry_supported": industry_supported,
            "profit_positive": profit_positive
        }
        
        return FundamentalAnalysis(
            profit_positive=profit_positive,
            profit_decline=profit_decline,
            has_negative_events=has_negative_events,
            industry_supported=industry_supported,
            details=details
        )
    
    def check_buy_conditions(self, data: StockData) -> BuySignal:
        """检查买入条件"""
        trend = self.analyze_trend(data)
        volume_price = self.analyze_volume_price(data)
        fundamentals = self.analyze_fundamentals(data)
        
        buy_reasons = []
        warnings = []
        
        # 检查趋势条件
        if trend.is_uptrend:
            buy_reasons.append("趋势向上，均线多头排列")
        else:
            warnings.append(f"趋势不符合：{trend.ma_alignment}")
        
        if trend.above_20ma and trend.above_60ma:
            buy_reasons.append("股价在20日和60日均线上方")
        else:
            warnings.append("股价未在关键均线上方")
        
        # 检查量价条件
        if volume_price.volume_increasing:
            buy_reasons.append(f"成交量温和放大{volume_price.volume_amplification:.1f}%")
        else:
            warnings.append("成交量未明显放大")
        
        if volume_price.yang_volume_greater:
            buy_reasons.append("阳量大于阴量，资金流入")
        else:
            warnings.append("量价配合不理想")
        
        if volume_price.abnormal_volume:
            warnings.append("检测到异常巨量，需谨慎")
        
        if volume_price.continuous_decline:
            warnings.append("连续缩量下跌，趋势可能转弱")
        
        # 检查基本面条件
        if fundamentals.profit_positive:
            buy_reasons.append("基本面健康，净利润为正")
        else:
            warnings.append("净利润为负或数据缺失")
        
        if fundamentals.industry_supported:
            buy_reasons.append(f"行业受政策支持：{data.industry}")
        else:
            warnings.append(f"行业可能不受政策支持：{data.industry}")
        
        if fundamentals.has_negative_events:
            warnings.append("存在重大负面事件")
        
        # 综合判断
        trend_qualified = trend.is_uptrend and trend.above_20ma and trend.above_60ma
        volume_price_qualified = (volume_price.volume_increasing and 
                                 volume_price.yang_volume_greater and 
                                 not volume_price.abnormal_volume and 
                                 not volume_price.continuous_decline)
        fundamental_qualified = (fundamentals.profit_positive and 
                                not fundamentals.has_negative_events and 
                                fundamentals.industry_supported)
        
        all_conditions_met = trend_qualified and volume_price_qualified and fundamental_qualified
        
        # 计算建议仓位和止损
        suggested_position = 0.10 if all_conditions_met else 0  # 初始仓位10%
        stop_loss_price = data.current_price * 0.93  # 7%止损
        target_price = data.current_price * 1.15  # 15%目标
        
        return BuySignal(
            ticker=data.ticker,
            company_name=data.company_name,
            current_price=data.current_price,
            trend_qualified=trend_qualified,
            volume_price_qualified=volume_price_qualified,
            fundamental_qualified=fundamental_qualified,
            all_conditions_met=all_conditions_met,
            buy_reasons=buy_reasons,
            warnings=warnings,
            suggested_position=suggested_position,
            stop_loss_price=stop_loss_price,
            target_price=target_price
        )
    
    def analyze_stocks(self, tickers: List[str]) -> List[BuySignal]:
        """分析多个股票"""
        signals = []
        
        for ticker in tickers:
            print(f"分析 {ticker}...", file=sys.stderr)
            
            data = self.fetch_stock_data(ticker)
            if not data:
                print(f"  无法获取 {ticker} 数据", file=sys.stderr)
                continue
            
            signal = self.check_buy_conditions(data)
            signals.append(signal)
        
        return signals
    
    def format_signal_output(self, signal: BuySignal, output_format: str = "text") -> str:
        """格式化信号输出"""
        if output_format == "json":
            return json.dumps(asdict(signal), indent=2, ensure_ascii=False)
        
        # 文本格式输出
        output = []
        output.append("=" * 80)
        output.append(f"股票代码: {signal.ticker} - {signal.company_name}")
        output.append(f"当前价格: ${signal.current_price:.2f}")
        output.append("=" * 80)
        
        # 条件检查结果
        output.append("📊 策略条件检查:")
        output.append(f"  趋势条件: {'✅ 符合' if signal.trend_qualified else '❌ 不符合'}")
        output.append(f"  量价条件: {'✅ 符合' if signal.volume_price_qualified else '❌ 不符合'}")
        output.append(f"  基本面条件: {'✅ 符合' if signal.fundamental_qualified else '❌ 不符合'}")
        
        output.append(f"\n🎯 综合判断: {'🚀 符合买入条件' if signal.all_conditions_met else '⛔ 不符合买入条件'}")
        
        if signal.all_conditions_met:
            output.append(f"\n💡 交易建议:")
            output.append(f"  建议仓位: {signal.suggested_position * 100:.1f}% (初始建仓)")
            output.append(f"  止损价格: ${signal.stop_loss_price:.2f} (-7.0%)")
            output.append(f"  目标价格: ${signal.target_price:.2f} (+{((signal.target_price/signal.current_price)-1)*100:.1f}%)")
            output.append(f"  风险收益比: 1:{((signal.target_price-signal.current_price)/(signal.current_price-signal.stop_loss_price)):.1f}")
        
        if signal.buy_reasons:
            output.append(f"\n✅ 支持理由:")
            for reason in signal.buy_reasons:
                output.append(f"  • {reason}")
        
        if signal.warnings:
            output.append(f"\n⚠️  风险提示:")
            for warning in signal.warnings:
                output.append(f"  • {warning}")
        
        output.append("\n" + "=" * 80)
        output.append("📋 策略执行要点:")
        output.append("1. 趋势优先：只做上升趋势，不做抄底预测")
        output.append("2. 仓位管理：单股不超过20%，初始建仓10%")
        output.append("3. 严格止损：下跌7%无条件止损")
        output.append("4. 量价为证：上涨放量，回调缩量")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def format_comparison_output(self, signals: List[BuySignal], output_format: str = "text") -> str:
        """格式化比较输出"""
        if output_format == "json":
            return json.dumps([asdict(s) for s in signals], indent=2, ensure_ascii=False)
        
        # 筛选符合条件的信号
        qualified_signals = [s for s in signals if s.all_conditions_met]
        unqualified_signals = [s for s in signals if not s.all_conditions_met]
        
        output = []
        output.append("=" * 100)
        output.append("中短线稳健型股票交易策略 - 批量分析结果")
        output.append("=" * 100)
        
        if qualified_signals:
            output.append(f"\n🚀 符合买入条件的股票 ({len(qualified_signals)}只):")
            output.append("-" * 100)
            output.append(f"{'代码':<8} {'名称':<20} {'价格':>8} {'仓位':>8} {'止损':>10} {'目标':>10} {'风报比':>8}")
            output.append("-" * 100)
            
            for signal in qualified_signals:
                risk_reward = ((signal.target_price-signal.current_price)/(signal.current_price-signal.stop_loss_price))
                output.append(
                    f"{signal.ticker:<8} "
                    f"{signal.company_name[:19]:<20} "
                    f"${signal.current_price:>7.2f} "
                    f"{signal.suggested_position*100:>7.1f}% "
                    f"${signal.stop_loss_price:>9.2f} "
                    f"${signal.target_price:>9.2f} "
                    f"1:{risk_reward:>6.1f}"
                )
        
        if unqualified_signals:
            output.append(f"\n⛔ 不符合买入条件的股票 ({len(unqualified_signals)}只):")
            output.append("-" * 100)
            output.append(f"{'代码':<8} {'名称':<20} {'价格':>8} {'趋势':>8} {'量价':>8} {'基本面':>8} {'主要问题':<30}")
            output.append("-" * 100)
            
            for signal in unqualified_signals:
                # 找出主要问题
                main_issue = "未知"
                if not signal.trend_qualified:
                    main_issue = "趋势不符合"
                elif not signal.volume_price_qualified:
                    main_issue = "量价不符合"
                elif not signal.fundamental_qualified:
                    main_issue = "基本面不符合"
                
                output.append(
                    f"{signal.ticker:<8} "
                    f"{signal.company_name[:19]:<20} "
                    f"${signal.current_price:>7.2f} "
                    f"{'❌':>8} "
                    f"{'❌' if not signal.volume_price_qualified else '✅':>8} "
                    f"{'❌' if not signal.fundamental_qualified else '✅':>8} "
                    f"{main_issue:<30}"
                )
        
        # 策略统计
        total = len(signals)
        qualified = len(qualified_signals)
        qualification_rate = (qualified / total * 100) if total > 0 else 0
        
        output.append("\n" + "=" * 100)
        output.append(f"📈 策略统计: 分析{total}只股票，符合条件{qualified}只，合格率{qualification_rate:.1f}%")
        
        if qualified_signals:
            output.append("\n🎯 推荐排序（按风险收益比）:")
            sorted_signals = sorted(qualified_signals, 
                                  key=lambda x: ((x.target_price-x.current_price)/(x.current_price-x.stop_loss_price)), 
                                  reverse=True)
            
            for i, signal in enumerate(sorted_signals[:5], 1):
                risk_reward = ((signal.target_price-signal.current_price)/(signal.current_price-signal.stop_loss_price))
                output.append(f"{i}. {signal.ticker}: 价格${signal.current_price:.2f}, 风报比1:{risk_reward:.1f}, 仓位{signal.suggested_position*100:.1f}%")
        
        output.append("\n" + "=" * 100)
        output.append("💡 操作建议:")
        output.append("1. 优先选择风险收益比高的标的")
        output.append("2. 严格执行仓位管理（单股≤20%）")
        output.append("3. 设置好止损后入场")
        output.append("4. 每日复盘，及时调整")
        output.append("=" * 100)
        
        return "\n".join(output)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="中短线稳健型股票交易策略分析")
    parser.add_argument("tickers", nargs="+", help="股票代码列表")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--compare", action="store_true", help="比较模式")
    parser.add_argument("--detail", action="store_true", help="详细分析模式")
    
    args = parser.parse_args()
    
    analyzer = TradingStrategyAnalyzer()
    
    if args.detail:
        # 详细分析单个股票
        for ticker in args.tickers:
            data = analyzer.fetch_stock_data(ticker)
            if data:
                signal = analyzer.check_buy_conditions(data)
                print(analyzer.format_signal_output(signal, args.output))
                print("\n" + "=" * 80 + "\n")
    else:
        # 批量分析
        signals = analyzer.analyze_stocks(args.tickers)
        
        if args.compare:
            print(analyzer.format_comparison_output(signals, args.output))
        else:
            for signal in signals:
                print(analyzer.format_signal_output(signal, args.output))
                print()

if __name__ == "__main__":
    main()