#!/usr/bin/env python3
"""
投资组合管理脚本
简化版本，基于 udiedrichsen/stock-analysis 的核心概念
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import yfinance as yf

@dataclass
class Asset:
    """资产类，存储投资组合中的资产信息"""
    ticker: str
    asset_type: str  # "stock" or "crypto"
    quantity: float
    cost_basis: float  # 单位成本
    added_at: str
    current_price: float = 0.0
    current_value: float = 0.0
    gain_loss: float = 0.0
    gain_loss_pct: float = 0.0

@dataclass
class Portfolio:
    """投资组合类，存储投资组合信息"""
    name: str
    created_at: str
    updated_at: str
    assets: List[Asset]
    total_cost: float = 0.0
    total_value: float = 0.0
    total_gain_loss: float = 0.0
    total_gain_loss_pct: float = 0.0

class PortfolioStore:
    """投资组合存储管理类"""
    def __init__(self, path: Optional[Path] = None):
        """初始化存储路径"""
        self.path = path or Path.home() / ".clawdbot" / "skills" / "stock-analysis" / "portfolios.json"
        self._data: Optional[Dict] = None
    
    def _load(self) -> Dict:
        """从磁盘加载投资组合数据"""
        if self._data is not None:
            return self._data
        
        try:
            if self.path.exists():
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                return self._data
        except (json.JSONDecodeError, IOError):
            pass
        
        # 如果加载失败，初始化空数据
        self._data = {"version": 1, "portfolios": {}}
        return self._data
    
    def _save(self) -> None:
        """将投资组合数据保存到磁盘"""
        if self._data is None:
            return
        
        # 确保目录存在
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        # 原子写入：先写入临时文件，然后重命名
        tmp_path = self.path.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            tmp_path.replace(self.path)
        except Exception:
            if tmp_path.exists():
                tmp_path.unlink()
            raise
    
    def create_portfolio(self, name: str) -> Portfolio:
        """创建新投资组合"""
        data = self._load()
        key = name.lower().replace(" ", "-")
        
        if key in data["portfolios"]:
            raise ValueError(f"投资组合 '{name}' 已存在")
        
        now = datetime.now().isoformat()
        portfolio = {
            "name": name,
            "created_at": now,
            "updated_at": now,
            "assets": []
        }
        
        data["portfolios"][key] = portfolio
        self._save()
        
        return Portfolio(
            name=name,
            created_at=now,
            updated_at=now,
            assets=[]
        )
    
    def add_asset(self, portfolio_name: str, ticker: str, quantity: float, cost_basis: float) -> Asset:
        """向投资组合添加资产"""
        data = self._load()
        key = portfolio_name.lower().replace(" ", "-")
        
        # 查找投资组合
        if key not in data["portfolios"]:
            raise ValueError(f"投资组合 '{portfolio_name}' 不存在")
        
        portfolio = data["portfolios"][key]
        ticker = ticker.upper()
        
        # 检查资产是否已存在
        for asset in portfolio["assets"]:
            if asset["ticker"] == ticker:
                raise ValueError(f"资产 '{ticker}' 已在投资组合中")
        
        # 验证代码并获取当前价格
        asset_type = "crypto" if ticker.endswith("-USD") else "stock"
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            current_price = info.get('regularMarketPrice', info.get('currentPrice', 0))
            
            if current_price == 0:
                raise ValueError(f"无法获取 '{ticker}' 的当前价格")
        except Exception as e:
            raise ValueError(f"无法验证代码 '{ticker}': {e}")
        
        now = datetime.now().isoformat()
        current_value = quantity * current_price
        gain_loss = current_value - (quantity * cost_basis)
        gain_loss_pct = (gain_loss / (quantity * cost_basis)) * 100 if cost_basis > 0 else 0
        
        asset = Asset(
            ticker=ticker,
            asset_type=asset_type,
            quantity=quantity,
            cost_basis=cost_basis,
            added_at=now,
            current_price=current_price,
            current_value=current_value,
            gain_loss=gain_loss,
            gain_loss_pct=gain_loss_pct
        )
        
        portfolio["assets"].append(asdict(asset))
        portfolio["updated_at"] = now
        self._save()
        
        return asset
    
    def get_portfolio(self, name: str, update_prices: bool = True) -> Optional[Portfolio]:
        """获取投资组合并更新价格"""
        data = self._load()
        key = name.lower().replace(" ", "-")
        
        if key not in data["portfolios"]:
            return None
        
        portfolio_data = data["portfolios"][key]
        assets = []
        
        total_cost = 0.0
        total_value = 0.0
        
        for asset_data in portfolio_data["assets"]:
            asset = Asset(**asset_data)
            
            if update_prices:
                # 更新当前价格
                try:
                    stock = yf.Ticker(asset.ticker)
                    info = stock.info
                    asset.current_price = info.get('regularMarketPrice', info.get('currentPrice', 0))
                    asset.current_value = asset.quantity * asset.current_price
                    asset.gain_loss = asset.current_value - (asset.quantity * asset.cost_basis)
                    asset.gain_loss_pct = (asset.gain_loss / (asset.quantity * asset.cost_basis)) * 100 if asset.cost_basis > 0 else 0
                except:
                    pass  # 保持原有价格
            
            assets.append(asset)
            total_cost += asset.quantity * asset.cost_basis
            total_value += asset.current_value
        
        total_gain_loss = total_value - total_cost
        total_gain_loss_pct = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
        
        return Portfolio(
            name=portfolio_data["name"],
            created_at=portfolio_data["created_at"],
            updated_at=portfolio_data["updated_at"],
            assets=assets,
            total_cost=total_cost,
            total_value=total_value,
            total_gain_loss=total_gain_loss,
            total_gain_loss_pct=total_gain_loss_pct
        )
    
    def list_portfolios(self) -> List[str]:
        """列出所有投资组合名称"""
        data = self._load()
        return [portfolio["name"] for portfolio in data["portfolios"].values()]
    
    def remove_asset(self, portfolio_name: str, ticker: str) -> bool:
        """从投资组合移除资产"""
        data = self._load()
        key = portfolio_name.lower().replace(" ", "-")
        
        if key not in data["portfolios"]:
            return False
        
        portfolio = data["portfolios"][key]
        ticker = ticker.upper()
        
        # 查找并移除资产
        original_length = len(portfolio["assets"])
        portfolio["assets"] = [a for a in portfolio["assets"] if a["ticker"] != ticker]
        
        if len(portfolio["assets"]) < original_length:
            portfolio["updated_at"] = datetime.now().isoformat()
            self._save()
            return True
        
        return False

def format_portfolio_output(portfolio: Portfolio, output_format: str = "text"):
    """格式化投资组合输出"""
    if output_format == "json":
        return json.dumps(asdict(portfolio), indent=2, default=str)
    
    # 文本格式输出
    output = []
    output.append("=" * 60)
    output.append(f"投资组合: {portfolio.name}")
    output.append(f"创建时间: {portfolio.created_at}")
    output.append(f"更新时间: {portfolio.updated_at}")
    output.append("=" * 60)
    
    output.append(f"总成本: ${portfolio.total_cost:,.2f}")
    output.append(f"总价值: ${portfolio.total_value:,.2f}")
    
    if portfolio.total_gain_loss >= 0:
        output.append(f"总收益: +${portfolio.total_gain_loss:,.2f} (+{portfolio.total_gain_loss_pct:.1f}%)")
    else:
        output.append(f"总亏损: -${abs(portfolio.total_gain_loss):,.2f} ({portfolio.total_gain_loss_pct:.1f}%)")
    
    output.append("\n资产明细:")
    output.append("-" * 60)
    
    for i, asset in enumerate(portfolio.assets, 1):
        output.append(f"{i}. {asset.ticker} ({asset.asset_type})")
        output.append(f"   数量: {asset.quantity:,}")
        output.append(f"   成本: ${asset.cost_basis:.2f}/单位")
        output.append(f"   当前价: ${asset.current_price:.2f}")
        output.append(f"   当前值: ${asset.current_value:,.2f}")
        
        if asset.gain_loss >= 0:
            output.append(f"   收益: +${asset.gain_loss:,.2f} (+{asset.gain_loss_pct:.1f}%)")
        else:
            output.append(f"   亏损: -${abs(asset.gain_loss):,.2f} ({asset.gain_loss_pct:.1f}%)")
        
        output.append("")
    
    # 计算资产分布
    if portfolio.assets:
        output.append("资产分布:")
        for asset in portfolio.assets:
            percentage = (asset.current_value / portfolio.total_value) * 100
            output.append(f"  • {asset.ticker}: {percentage:.1f}%")
    
    output.append("=" * 60)
    output.append("注：价格数据来自 Yahoo Finance，可能有15分钟延迟")
    output.append("=" * 60)
    
    return "\n".join(output)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="投资组合管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新投资组合")
    create_parser.add_argument("name", help="投资组合名称")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="向投资组合添加资产")
    add_parser.add_argument("ticker", help="股票/加密货币代码（例如：AAPL, BTC-USD）")
    add_parser.add_argument("--quantity", "-q", type=float, required=True, help="数量")
    add_parser.add_argument("--cost", "-c", type=float, required=True, help="单位成本")
    add_parser.add_argument("--portfolio", "-p", default="default", help="投资组合名称（默认: default）")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示投资组合")
    show_parser.add_argument("--portfolio", "-p", help="投资组合名称（默认显示所有）")
    show_parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有投资组合")
    
    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="从投资组合移除资产")
    remove_parser.add_argument("ticker", help="股票/加密货币代码")
    remove_parser.add_argument("--portfolio", "-p", default="default", help="投资组合名称")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    store = PortfolioStore()
    
    try:
        if args.command == "create":
            portfolio = store.create_portfolio(args.name)
            print(f"✅ 创建投资组合: {portfolio.name}")
            
        elif args.command == "add":
            asset = store.add_asset(args.portfolio, args.ticker, args.quantity, args.cost)
            print(f"✅ 已向 '{args.portfolio}' 添加 {asset.ticker}:")
            print(f"   数量: {asset.quantity:,} 单位")
            print(f"   成本: ${asset.cost_basis:.2f}/单位")
            print(f"   当前价: ${asset.current_price:.2f}")
            print(f"   当前值: ${asset.current_value:,.2f}")
            
            if asset.gain_loss >= 0:
                print(f"   未实现收益: +${asset.gain_loss:,.2f} (+{asset.gain_loss_pct:.1f}%)")
            else:
                print(f"   未实现亏损: -${abs(asset.gain_loss):,.2f} ({asset.gain_loss_pct:.1f}%)")
        
        elif args.command == "show":
            if args.portfolio:
                portfolio = store.get_portfolio(args.portfolio, update_prices=True)
                if portfolio:
                    print(format_portfolio_output(portfolio, args.output))
                else:
                    print(f"❌ 投资组合 '{args.portfolio}' 不存在")
            else:
                portfolios = store.list_portfolios()
                if portfolios:
                    print("可用投资组合:")
                    for name in portfolios:
                        print(f"  • {name}")
                else:
                    print("暂无投资组合，使用 'create' 命令创建一个")
        
        elif args.command == "list":
            portfolios = store.list_portfolios()
            if portfolios:
                print("投资组合列表:")
                for name in portfolios:
                    print(f"  • {name}")
            else:
                print("暂无投资组合")
        
        elif args.command == "remove":
            success = store.remove_asset(args.portfolio, args.ticker)
            if success:
                print(f"✅ 已从 '{args.portfolio}' 移除 {args.ticker.upper()}")
            else:
                print(f"❌ 移除失败: 资产或投资组合不存在")
    
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()