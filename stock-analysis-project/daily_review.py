#!/usr/bin/env python3
"""
每日标准化复盘流程
严格遵循中短线稳健型交易策略的复盘要求
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import pandas as pd
import yfinance as yf

class DailyReview:
    """每日复盘系统"""
    
    def __init__(self):
        self.watchlist = []  # 观察股票列表
        self.positions = {}  # 持仓记录
        
    def load_watchlist(self, filepath: str = "watchlist.json"):
        """加载观察列表"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.watchlist = data.get('stocks', [])
                self.positions = data.get('positions', {})
        except FileNotFoundError:
            print(f"观察列表文件 {filepath} 不存在，创建新文件", file=sys.stderr)
            self.watchlist = []
            self.positions = {}
    
    def save_watchlist(self, filepath: str = "watchlist.json"):
        """保存观察列表"""
        data = {
            'stocks': self.watchlist,
            'positions': self.positions,
            'updated': datetime.now().isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def assess_market_environment(self) -> Dict:
        """大盘环境评估"""
        indices = {
            '上证指数': '000001.SS',
            '深证成指': '399001.SZ',
            '创业板指': '399006.SZ'
        }
        
        results = {}
        
        for name, symbol in indices.items():
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period='1mo')
                
                if hist.empty:
                    results[name] = {'status': '数据获取失败', 'above_20ma': False}
                    continue
                
                # 计算20日均线
                hist['MA20'] = hist['Close'].rolling(window=20).mean()
                latest = hist.iloc[-1]
                
                above_20ma = latest['Close'] > latest['MA20']
                ma20_trend = "上升" if latest['MA20'] > hist.iloc[-21]['MA20'] else "下降"
                
                results[name] = {
                    'current': latest['Close'],
                    'ma20': latest['MA20'],
                    'above_20ma': above_20ma,
                    'ma20_trend': ma20_trend,
                    'status': '健康' if above_20ma else '谨慎'
                }
                
            except Exception as e:
                results[name] = {'status': f'错误: {str(e)}', 'above_20ma': False}
        
        # 综合判断
        healthy_count = sum(1 for r in results.values() if r.get('above_20ma', False))
        total_count = len(results)
        
        if healthy_count == total_count:
            market_status = "强势市场"
        elif healthy_count >= total_count * 0.5:
            market_status = "震荡市场"
        else:
            market_status = "弱势市场"
        
        return {
            'indices': results,
            'market_status': market_status,
            'healthy_ratio': f"{healthy_count}/{total_count}",
            'recommendation': self.get_market_recommendation(market_status)
        }
    
    def get_market_recommendation(self, status: str) -> str:
        """根据市场状态给出建议"""
        recommendations = {
            "强势市场": "✅ 市场健康，可积极寻找机会",
            "震荡市场": "⚠️  市场震荡，控制仓位，精选个股",
            "弱势市场": "⛔ 市场弱势，减少操作，观望为主"
        }
        return recommendations.get(status, "未知市场状态")
    
    def analyze_sector_strength(self) -> Dict:
        """板块强弱分析"""
        # 常见板块ETF
        sectors = {
            '科技': 'XLK',  # Technology Select Sector SPDR
            '金融': 'XLF',  # Financial Select Sector SPDR
            '医疗': 'XLV',  # Health Care Select Sector SPDR
            '消费': 'XLY',  # Consumer Discretionary Select Sector SPDR
            '工业': 'XLI',  # Industrial Select Sector SPDR
            '能源': 'XLE',  # Energy Select Sector SPDR
            '材料': 'XLB',  # Materials Select Sector SPDR
            '公用事业': 'XLU',  # Utilities Select Sector SPDR
            '房地产': 'XLRE',  # Real Estate Select Sector SPDR
        }
        
        results = {}
        
        for name, symbol in sectors.items():
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period='5d')
                
                if hist.empty or len(hist) < 3:
                    results[name] = {'change_1d': 0, 'change_3d': 0, 'strength': '未知'}
                    continue
                
                # 计算涨跌幅
                change_1d = (hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100
                change_3d = (hist['Close'].iloc[-1] - hist['Close'].iloc[-4]) / hist['Close'].iloc[-4] * 100
                
                # 判断强度
                if change_1d > 1 and change_3d > 3:
                    strength = "强势"
                elif change_1d > 0 and change_3d > 0:
                    strength = "偏强"
                elif change_1d < -1 and change_3d < -3:
                    strength = "弱势"
                elif change_1d < 0 and change_3d < 0:
                    strength = "偏弱"
                else:
                    strength = "震荡"
                
                results[name] = {
                    'symbol': symbol,
                    'change_1d': change_1d,
                    'change_3d': change_3d,
                    'strength': strength
                }
                
            except Exception as e:
                results[name] = {'change_1d': 0, 'change_3d': 0, 'strength': f'错误: {str(e)}'}
        
        # 排序找出强势板块
        strong_sectors = [(name, data) for name, data in results.items() 
                         if data.get('strength') in ['强势', '偏强']]
        strong_sectors.sort(key=lambda x: x[1].get('change_3d', 0), reverse=True)
        
        weak_sectors = [(name, data) for name, data in results.items() 
                       if data.get('strength') in ['弱势', '偏弱']]
        weak_sectors.sort(key=lambda x: x[1].get('change_3d', 0))
        
        return {
            'sectors': results,
            'strong_sectors': strong_sectors[:3],  # 前3强
            'weak_sectors': weak_sectors[:3],      # 前3弱
            'top_sector': strong_sectors[0][0] if strong_sectors else "无"
        }
    
    def review_watchlist(self) -> Dict:
        """自选股管理"""
        if not self.watchlist:
            return {'total': 0, 'actions': [], 'summary': '观察列表为空'}
        
        actions = []
        to_remove = []
        to_reduce = []
        to_hold = []
        
        for ticker in self.watchlist:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period='1mo')
                
                if hist.empty:
                    actions.append(f"{ticker}: 数据获取失败")
                    continue
                
                # 计算均线
                hist['MA5'] = hist['Close'].rolling(window=5).mean()
                hist['MA10'] = hist['Close'].rolling(window=10).mean()
                hist['MA20'] = hist['Close'].rolling(window=20).mean()
                
                latest = hist.iloc[-1]
                prev = hist.iloc[-2] if len(hist) >= 2 else latest
                
                # 检查破位条件
                below_20ma = latest['Close'] < latest['MA20']
                ma20_declining = latest['MA20'] < prev['MA20']
                
                if below_20ma and ma20_declining:
                    actions.append(f"❌ {ticker}: 跌破20日均线且均线下行，建议删除")
                    to_remove.append(ticker)
                    continue
                
                # 检查走弱条件
                below_5ma = latest['Close'] < latest['MA5']
                below_10ma = latest['Close'] < latest['MA10']
                volume_declining = latest['Volume'] < hist['Volume'].tail(5).mean() * 0.7
                
                if (below_5ma or below_10ma) and volume_declining:
                    actions.append(f"⚠️  {ticker}: 跌破短期均线且缩量，建议减仓")
                    to_reduce.append(ticker)
                    continue
                
                # 检查强势条件
                above_all_ma = (latest['Close'] > latest['MA5'] > latest['MA10'] > latest['MA20'])
                volume_increasing = latest['Volume'] > hist['Volume'].tail(5).mean() * 1.2
                
                if above_all_ma and volume_increasing:
                    actions.append(f"✅ {ticker}: 均线多头排列且放量，建议持有")
                    to_hold.append(ticker)
                else:
                    actions.append(f"📊 {ticker}: 趋势正常，继续观察")
                    to_hold.append(ticker)
                    
            except Exception as e:
                actions.append(f"{ticker}: 分析错误 - {str(e)}")
        
        # 更新观察列表（移除破位股票）
        new_watchlist = [t for t in self.watchlist if t not in to_remove]
        
        # 确保数量在5-10只
        if len(new_watchlist) > 10:
            # 保留最近分析的强势股票
            new_watchlist = new_watchlist[:10]
            actions.append(f"📋 观察列表超过10只，自动裁剪至10只")
        elif len(new_watchlist) < 5:
            actions.append(f"📋 观察列表不足5只，建议添加新标的")
        
        self.watchlist = new_watchlist
        
        return {
            'total': len(self.watchlist),
            'actions': actions,
            'to_remove': to_remove,
            'to_reduce': to_reduce,
            'to_hold': to_hold,
            'summary': f"观察列表: {len(self.watchlist)}只，删除{len(to_remove)}只，减仓{len(to_reduce)}只"
        }
    
    def optimize_watchlist(self, new_candidates: List[str] = None) -> List[str]:
        """观察池优化"""
        if new_candidates:
            # 添加新候选，但不超过总数限制
            available_slots = 10 - len(self.watchlist)
            if available_slots > 0:
                add_count = min(available_slots, len(new_candidates))
                self.watchlist.extend(new_candidates[:add_count])
        
        # 确保唯一性
        self.watchlist = list(dict.fromkeys(self.watchlist))
        
        return self.watchlist
    
    def generate_daily_report(self) -> str:
        """生成每日复盘报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 执行各项分析
        market = self.assess_market_environment()
        sectors = self.analyze_sector_strength()
        watchlist_review = self.review_watchlist()
        
        # 生成报告
        report = []
        report.append("=" * 80)
        report.append(f"📊 每日标准化复盘报告 - {timestamp}")
        report.append("=" * 80)
        
        # 1. 大盘环境评估
        report.append("\n一、大盘环境评估:")
        report.append("-" * 40)
        for name, data in market['indices'].items():
            status = "✅" if data.get('above_20ma', False) else "❌"
            report.append(f"{status} {name}: ${data.get('current', 0):.2f} | "
                         f"20日线: ${data.get('ma20', 0):.2f} | "
                         f"状态: {data.get('status', '未知')}")
        
        report.append(f"\n📈 市场状态: {market['market_status']} ({market['healthy_ratio']}指数健康)")
        report.append(f"💡 操作建议: {market['recommendation']}")
        
        # 2. 板块强弱分析
        report.append("\n二、板块强弱分析:")
        report.append("-" * 40)
        
        if sectors['strong_sectors']:
            report.append("🔥 强势板块:")
            for name, data in sectors['strong_sectors']:
                report.append(f"  • {name}: 今日{data.get('change_1d', 0):+.1f}% | "
                            f"3日{data.get('change_3d', 0):+.1f}%")
        
        if sectors['weak_sectors']:
            report.append("\n💧 弱势板块:")
            for name, data in sectors['weak_sectors']:
                report.append(f"  • {name}: 今日{data.get('change_1d', 0):+.1f}% | "
                            f"3日{data.get('change_3d', 0):+.1f}%")
        
        report.append(f"\n🎯 重点关注: {sectors['top_sector']} 板块")
        
        # 3. 自选股管理
        report.append("\n三、自选股管理:")
        report.append("-" * 40)
        
        if watchlist_review['actions']:
            for action in watchlist_review['actions']:
                report.append(action)
        else:
            report.append("无自选股需要处理")
        
        report.append(f"\n📋 {watchlist_review['summary']}")
        
        # 4. 观察池优化建议
        report.append("\n四、观察池优化建议:")
        report.append("-" * 40)
        
        current_count = len(self.watchlist)
        if current_count < 5:
            report.append(f"⚠️  观察池仅{current_count}只，建议添加{5-current_count}只强势股")
        elif current_count > 10:
            report.append(f"⚠️  观察池{current_count}只过多，建议精简至10只以内")
        else:
            report.append(f"✅ 观察池{current_count}只，数量适中")
        
        if self.watchlist:
            report.append(f"\n当前观察池 ({len(self.watchlist)}只):")
            for i, ticker in enumerate(self.watchlist, 1):
                report.append(f"  {i}. {ticker}")
        
        # 5. 明日操作计划
        report.append("\n五、明日操作计划:")
        report.append("-" * 40)
        
        if market['market_status'] == "强势市场":
            report.append("1. ✅ 市场健康，可积极寻找买入机会")
            report.append("2. 🎯 重点关注强势板块中的个股")
            report.append("3. 📊 严格执行买入条件检查")
        elif market['market_status'] == "震荡市场":
            report.append("1. ⚠️  市场震荡，控制仓位在50%以下")
            report.append("2. 🎯 只做最强势的个股")
            report.append("3. 🛡️  严格执行止损纪律")
        else:
            report.append("1. ⛔ 市场弱势，减少操作，观望为主")
            report.append("2. 💰 如有持仓，严格执行止损")
            report.append("3. 📚 利用时间研究，等待机会")
        
        report.append("\n六、交易纪律提醒:")
        report.append("-" * 40)
        report.append("1. 🎯 趋势优先：只做上升趋势")
        report.append("2. 💰 仓位管理：单股≤20%，总仓≤80%")
        report.append("3. 🛡️  严格止损：下跌7%无条件止损")
        report.append("4. 📊 量价为证：上涨放量，回调缩量")
        report.append("5. 🧠 能力圈内：只做能理解的交易")
        
        report.append("\n" + "=" * 80)
        report.append("💡 复盘完成时间: 10分钟内")
        report.append("📅 下次复盘: 明日开盘前")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="每日标准化复盘系统")
    parser.add_argument("--watchlist", default="watchlist.json", help="观察列表文件路径")
    parser.add_argument("--add", nargs="+", help="添加股票到观察列表")
    parser.add_argument("--remove", nargs="+", help="从观察列表移除股票")
    parser.add_argument("--list", action="store_true", help="显示当前观察列表")
    parser.add_argument("--report", action="store_true", help="生成每日复盘报告")
    parser.add_argument("--save", action="store_true", help="保存观察列表")
    
    args = parser.parse_args()
    
    review = DailyReview()
    review.load_watchlist(args.watchlist)
    
    if args.add:
        review.watchlist.extend(args.add)
        review.watchlist = list(dict.fromkeys(review.watchlist))  # 去重
        print(f"✅ 已添加 {len(args.add)} 只股票到观察列表")
    
    if args.remove:
        removed = []
        for ticker in args.remove:
            if ticker in review.watchlist:
                review.watchlist.remove(ticker)
                removed.append(ticker)
        if removed:
            print(f"✅ 已移除 {len(removed)} 只股票: {', '.join(removed)}")
        else:
            print("⚠️  未找到要移除的股票")
    
    if args.list:
        if review.watchlist:
            print(f"\n📋 当前观察列表 ({len(review.watchlist)}只):")
            for i, ticker in enumerate(review.watchlist, 1):
                print(f"  {i}. {ticker}")
        else:
            print("观察列表为空")
    
    if args.report:
        print(review.generate_daily_report())
    
    if args.save or args.add or args.remove:
        review.save_watchlist(args.watchlist)
        print(f"💾 观察列表已保存到 {args.watchlist}")
    
    # 如果没有指定任何操作，显示帮助
    if not any([args.add, args.remove, args.list, args.report, args.save]):
        print("每日标准化复盘系统")
        print("=" * 50)
        print("使用方法:")
        print("  --add AAPL MSFT GOOGL     添加股票到观察列表")
        print("  --remove AAPL             从观察列表移除股票")
        print("  --list                    显示当前观察列表")
        print("  --report                  生成每日复盘报告")
        print("  --save                    保存观察列表")
        print("  --watchlist file.json     指定观察列表文件")
        print("\n示例:")
        print("  python daily_review.py --report")
        print("  python daily_review.py --add AAPL MSFT --save")

if __name__ == "__main__":
    main()