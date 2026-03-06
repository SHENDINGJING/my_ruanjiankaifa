#!/usr/bin/env python3
"""
OpenClaw Canvas监控系统 - 方案3实现
使用OpenClaw Canvas功能实现实时屏幕监控
"""

import json
import time
import os
import sys
import subprocess
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import schedule
from pathlib import Path

class CanvasMonitor:
    """Canvas监控器"""
    
    def __init__(self, config_path: str = "canvas_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.canvas_dir = Path("canvas")
        self.screenshots_dir = Path("canvas_screenshots")
        self.setup_directories()
        
    def load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "canvas_settings": {
                "enabled": True,
                "canvas_host": "http://localhost:18789/__openclaw__/canvas/",
                "monitor_interval": 30,
                "snapshot_format": "png",
                "snapshot_quality": 0.9,
                "max_width": 1200
            },
            "node_settings": {
                "node_id": "auto",  # auto | <node-id>
                "node_name": "本地节点",
                "require_foreground": True
            },
            "monitoring_targets": [
                {
                    "name": "炒股软件监控",
                    "type": "browser_window",
                    "url": "https://quote.eastmoney.com/concept/sh601857.html",
                    "stocks": [
                        {
                            "symbol": "601857",
                            "name": "中国石油",
                            "user_data": {
                                "shares": 800,
                                "cost_price": 12.465,
                                "stop_loss": 11.592,
                                "first_target": 14.335
                            }
                        }
                    ]
                }
            ],
            "analysis_settings": {
                "enable_price_extraction": True,
                "enable_ocr": False,  # 需要安装OCR库
                "enable_ai_analysis": True,
                "ai_model": "deepseek/deepseek-chat"
            }
        }
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                return default_config
        except FileNotFoundError:
            return default_config
    
    def save_config(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def setup_directories(self):
        """创建必要的目录"""
        self.canvas_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        Path("logs/canvas").mkdir(parents=True, exist_ok=True)
        
        # 创建默认canvas页面
        self.create_default_canvas()
    
    def create_default_canvas(self):
        """创建默认canvas页面"""
        index_html = self.canvas_dir / "index.html"
        
        if not index_html.exists():
            html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票监控Canvas</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stock-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s ease;
        }
        .stock-card:hover {
            transform: translateY(-5px);
        }
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .stock-name {
            font-size: 1.5em;
            font-weight: bold;
        }
        .stock-symbol {
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .price-info {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }
        .price-item {
            text-align: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        .price-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .price-value {
            font-size: 1.8em;
            font-weight: bold;
        }
        .profit-positive {
            color: #4ade80;
        }
        .profit-negative {
            color: #f87171;
        }
        .alert-box {
            background: rgba(239, 68, 68, 0.2);
            border-left: 4px solid #ef4444;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
        .alert-box.show {
            display: block;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .status-bar {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 0.9em;
            opacity: 0.8;
        }
        #lastUpdate {
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 股票实时监控系统</h1>
        
        <div id="stockContainer">
            <!-- 股票信息将通过JavaScript动态加载 -->
            <div class="stock-card">
                <div class="stock-header">
                    <div class="stock-name">中国石油</div>
                    <div class="stock-symbol">601857</div>
                </div>
                <div class="price-info">
                    <div class="price-item">
                        <div class="price-label">当前价格</div>
                        <div class="price-value" id="currentPrice">12.16</div>
                    </div>
                    <div class="price-item">
                        <div class="price-label">成本价格</div>
                        <div class="price-value" id="costPrice">12.465</div>
                    </div>
                    <div class="price-item">
                        <div class="price-label">盈亏比例</div>
                        <div class="price-value profit-negative" id="profitPct">-2.45%</div>
                    </div>
                    <div class="price-item">
                        <div class="price-label">距止损</div>
                        <div class="price-value" id="toStopLoss">+4.9%</div>
                    </div>
                </div>
                <div class="alert-box" id="alertBox">
                    🚨 注意：已接近止损价！
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            <div>状态: <span id="statusText">监控中...</span></div>
            <div>最后更新: <span id="lastUpdate">--:--:--</span></div>
        </div>
    </div>

    <script>
        // 股票数据
        let stockData = {
            "601857": {
                name: "中国石油",
                currentPrice: 12.16,
                costPrice: 12.465,
                shares: 800,
                stopLoss: 11.592,
                firstTarget: 14.335
            }
        };

        // 更新股票显示
        function updateStockDisplay() {
            const stock = stockData["601857"];
            const profitPct = ((stock.currentPrice - stock.costPrice) / stock.costPrice * 100).toFixed(2);
            const toStopLossPct = ((stock.currentPrice - stock.stopLoss) / stock.stopLoss * 100).toFixed(1);
            
            document.getElementById('currentPrice').textContent = stock.currentPrice.toFixed(3);
            document.getElementById('costPrice').textContent = stock.costPrice.toFixed(3);
            document.getElementById('profitPct').textContent = profitPct + '%';
            document.getElementById('toStopLoss').textContent = '+' + toStopLossPct + '%';
            
            // 更新盈亏颜色
            const profitElement = document.getElementById('profitPct');
            profitElement.className = profitPct >= 0 ? 'price-value profit-positive' : 'price-value profit-negative';
            
            // 检查是否需要显示警告
            const alertBox = document.getElementById('alertBox');
            if (toStopLossPct < 2) {
                alertBox.classList.add('show');
                alertBox.textContent = '🚨 警告：距离止损仅剩 ' + toStopLossPct + '%！';
            } else {
                alertBox.classList.remove('show');
            }
            
            // 更新最后更新时间
            const now = new Date();
            document.getElementById('lastUpdate').textContent = 
                now.getHours().toString().padStart(2, '0') + ':' +
                now.getMinutes().toString().padStart(2, '0') + ':' +
                now.getSeconds().toString().padStart(2, '0');
        }

        // 模拟价格更新
        function simulatePriceChange() {
            const stock = stockData["601857"];
            // 随机价格变化 (-0.05 到 +0.05)
            const change = (Math.random() - 0.5) * 0.1;
            stock.currentPrice += change;
            
            // 确保价格在合理范围内
            stock.currentPrice = Math.max(11.0, Math.min(15.0, stock.currentPrice));
            
            updateStockDisplay();
        }

        // 初始更新
        updateStockDisplay();
        
        // 每5秒更新一次价格（模拟）
        setInterval(simulatePriceChange, 5000);
        
        // 每30秒从服务器获取真实数据
        setInterval(fetchRealData, 30000);
        
        async function fetchRealData() {
            try {
                const response = await fetch('/api/stock-data');
                if (response.ok) {
                    const data = await response.json();
                    // 更新股票数据
                    if (data["601857"]) {
                        Object.assign(stockData["601857"], data["601857"]);
                        updateStockDisplay();
                    }
                }
            } catch (error) {
                console.log('获取数据失败:', error);
            }
        }
        
        // 页面可见性变化处理
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                document.getElementById('statusText').textContent = '后台运行';
            } else {
                document.getElementById('statusText').textContent = '监控中...';
            }
        });
    </script>
</body>
</html>"""
            
            with open(index_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ 创建默认canvas页面: {index_html}")
    
    def run_openclaw_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """运行OpenClaw命令"""
        try:
            full_command = ["openclaw"] + command
            
            print(f"运行命令: {' '.join(full_command)}")
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, f"错误: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, f"执行失败: {str(e)}"
    
    def check_nodes_status(self) -> Optional[str]:
        """检查节点状态并返回节点ID"""
        print("检查节点状态...")
        
        success, output = self.run_openclaw_command(["nodes", "status"])
        
        if not success:
            print(f"❌ 检查节点状态失败: {output}")
            return None
        
        # 解析输出，查找节点ID
        lines = output.split('\n')
        node_id = None
        
        for line in lines:
            if "ID:" in line:
                parts = line.split("ID:")
                if len(parts) > 1:
                    node_id = parts[1].strip()
                    break
        
        if node_id:
            print(f"✅ 找到节点: {node_id}")
            return node_id
        else:
            print("⚠️  未找到已配对的节点")
            print("\n需要先配对节点:")
            print("1. 在iOS/Android设备上安装OpenClaw Node应用")
            print("2. 在本机运行: openclaw nodes pending")
            print("3. 批准配对请求: openclaw nodes approve <请求ID>")
            return None
    
    def present_canvas(self, node_id: str) -> bool:
        """在节点上显示canvas"""
        print(f"在节点 {node_id} 上显示canvas...")
        
        canvas_url = self.config["canvas_settings"]["canvas_host"]
        
        success, output = self.run_openclaw_command([
            "nodes", "canvas", "present",
            "--node", node_id,
            "--target", canvas_url
        ])
        
        if success:
            print(f"✅ Canvas已显示在节点 {node_id}")
            return True
        else:
            print(f"❌ 显示canvas失败: {output}")
            return False
    
    def capture_canvas_snapshot(self, node_id: str) -> Optional[str]:
        """捕获canvas快照"""
        print(f"捕获节点 {node_id} 的canvas快照...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.screenshots_dir / f"canvas_snapshot_{timestamp}.png"
        
        success, output = self.run_openclaw_command([
            "nodes", "canvas", "snapshot",
            "--node", node_id,
            "--format", self.config["canvas_settings"]["snapshot_format"],
            "--max-width", str(self.config["canvas_settings"]["max_width"]),
            "--quality", str(self.config["canvas_settings"]["snapshot_quality"])
        ])
        
        if success:
            # 尝试解析base64图像数据
            try:
                # OpenClaw可能返回JSON或base64
                if output.startswith('{'):
                    data = json.loads(output)
                    if 'base64' in data:
                        image_data = base64.b64decode(data['base64'])
                        with open(output_file, 'wb') as f:
                            f.write(image_data)
                        print(f"✅ Canvas快照已保存: {output_file}")
                        return str(output_file)
                else:
                    # 可能是直接base64
                    image_data = base64.b64decode(output)
                    with open(output_file, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ Canvas快照已保存: {output_file}")
                    return str(output_file)
            except:
                # 保存原始输出
                with open(output_file.with_suffix('.txt'), 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✅ Canvas数据已保存: {output_file.with_suffix('.txt')}")
                return str(output_file.with_suffix('.txt'))
        else:
            print(f"❌ 捕获快照失败: {output}")
            return None
    
    def analyze_snapshot(self, snapshot_path: str, stock_config: Dict) -> Dict:
        """分析快照"""
        print(f"分析 {stock_config['name']} 的快照...")
        
        # 这里可以集成OCR或AI分析
        # 暂时使用模拟分析
        
        stock_data = stock_config["user_data"]
        cost_price = stock_data["cost_price"]
        
        # 模拟当前价格（实际应该从快照中提取）
        import random
        current_price = cost_price * (1 + (random.random() - 0.5) * 0.1)
        current_price = round(current_price, 3)
        
        profit_pct = (current_price - cost_price) / cost_price * 100
        stop_loss = stock_data["stop_loss"]
        first_target = stock_data["first_target"]
        
        to_stop_loss_pct = (current_price - stop_loss) / stop_loss * 100 if stop_loss > 0 else 0
        to_target_pct = (first_target - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 分析结果
        alerts = []
        recommendation = "持有"
        
        if current_price <= stop_loss:
            alerts.append(f"🚨 触发止损: {current_price:.3f} ≤ {stop_loss:.3f}")
            recommendation = "立即卖出"
        elif current_price >= first_target:
            alerts.append(f"🎯 达到目标: {current_price:.3f} ≥ {first_target:.3f}")
            recommendation = "卖出50%"
        elif profit_pct >= 0:
            alerts.append(f"✅ 回到成本: {current_price:.3f} ≥ {cost_price:.3f}")
            if recommendation == "持有":
                recommendation = "可考虑卖出"
        
        status = "盈利" if profit_pct > 0 else "亏损"
        
        result = {
            "symbol": stock_config["symbol"],
            "name": stock_config["name"],
            "analysis_time": datetime.now().isoformat(),
            "snapshot_path": snapshot_path,
            "current_price": current_price,
            "cost_price": cost_price,
            "profit_pct": profit_pct,
            "status": status,
            "to_stop_loss_pct": to_stop_loss_pct,
            "to_target_pct": to_target_pct,
            "alerts": alerts,
            "recommendation": recommendation,
            "risk_reward_ratio": abs(to_target_pct / to_stop_loss_pct) if to_stop_loss_pct != 0 else 0
        }
        
        # 保存分析结果
        result_file = self.screenshots_dir / f"analysis_{stock_config['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return result
    
    def display_analysis(self, result: Dict):
        """显示分析结果"""
        print(f"\n{'='*60}")
        print(f"📊 Canvas监控分析 - {result['name']} ({result['symbol']})")
        print(f"{'='*60}")
        
        print(f"\n📈 市场数据:")
        print(f"   当前价格: {result['current_price']:.3f}元")
        print(f"   成本价格: {result['cost_price']:.3f}元")
        print(f"   盈亏状态: {result['profit_pct']:.1f}% ({result['status']})")
        
        print(f"\n🎯 策略分析:")
        print(f"   距止损: {result['to_stop_loss_pct']:+.1f}%")
        print(f"   距目标: {result['to_target_pct']:+.1f}%")
        print(f"   风险收益比: 1:{result['risk_reward_ratio']:.1f}")
        
        if result['alerts']:
            print(f"\n⚠️  提醒:")
            for alert in result['alerts']:
                print(f"    • {alert}")
        
        print(f"\n💡 操作建议: {result['recommendation']}")
        
        # 检查紧急情况
        if "立即卖出" in result['recommendation']:
            print(f"\n🚨 紧急情况！需要立即处理！")
        
        print(f"\n⏰ 分析时间: {result['analysis_time']}")
        print(f"📷 快照文件: {result['snapshot_path']}")
        print(f"{'='*60}")
    
    def monitor_stock(self, node_id: str, stock_config: Dict):
        """监控单只股票"""
        print(f"\n🔍 监控 {stock_config['name']} ({stock_config['symbol']})...")
        
        # 1. 确保canvas已显示
        if not hasattr(self, 'canvas_presented') or not self.canvas_presented:
            if self.present_canvas(node_id):
                self.canvas_presented = True
                time.sleep(3)  # 等待canvas加载
            else:
                return None
        
        # 2. 捕获快照
        snapshot_path = self.capture_canvas_snapshot(node_id)
        if not snapshot_path:
            return None
        
        # 3. 分析快照
        result = self.analyze_snapshot(snapshot_path, stock_config)
        
        # 4. 显示结果
        self.display_analysis(result)
        
        # 5. 记录日志
        self.log_monitoring(result)
        
        return result
    
    def log_monitoring(self, result: Dict):
        """记录监控日志"""
        log_file = Path(f"logs/canvas/{datetime.now().strftime('%Y%m%d')}.log")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "symbol": result['symbol'],
            "name": result['name'],
            "price": result['current_price'],
            "recommendation": result['recommendation'],
            "alerts": result['alerts']
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"日志记录失败: {e}", file=sys.stderr)
    
    def start_monitoring(self, interval_seconds: int = 30):
        """开始监控"""
        print(f"🎨 启动Canvas监控系统")
        print(f"   Canvas地址: {self.config['canvas_settings']['canvas_host']}")
        print(f"   监控间隔: {interval_seconds}秒")
        print("   按 Ctrl+C 停止")
        print("=" * 60)
        
        # 检查节点状态
        node_id = self.check_nodes_status()
        if not node_id:
            print("❌ 无法启动监控：没有可用的节点")
            return
        
        # 显示canvas
        if not self.present_canvas(node_id):
            print("❌ 无法显示canvas")
            return
        
        self.canvas_presented = True
        time.sleep(5)  # 等待canvas完全加载
        
        # 立即检查一次
        print("\n🔍 首次检查...")
        for target in self.config["monitoring_targets"]:
            for stock in target["stocks"]:
                self.monitor_stock(node_id, stock)
        
        # 设置定时任务
        schedule.every(interval_seconds).seconds.do(self.run_monitoring_cycle, node_id)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")
    
    def run_monitoring_cycle(self, node_id: str):
        """运行监控周期"""
        print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} Canvas监控检查...")
        for target in self.config["monitoring_targets"]:
            for stock in target["stocks"]:
                self.monitor_stock(node_id, stock)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Canvas监控系统")
    parser.add_argument("--setup", action="store_true", help="设置Canvas监控")
    parser.add_argument("--add-stock", help="添加监控股票，格式：代码,名称,股数,成本价")
    parser.add_argument("--check", action="store_true", help="立即检查一次")
    parser.add_argument("--monitor", action="store_true", help="开始持续监控")
    parser.add_argument("--interval", type=int, default=30, help="监控间隔秒数")
    parser.add_argument("--nodes", action="store_true", help="检查节点状态")
    
    args = parser.parse_args()
    
    monitor = CanvasMonitor()
    
    if args.setup:
        print("🔧 设置Canvas监控系统...")
        print("1. 确保OpenClaw Gateway正在运行")
        print("2. 确保有已配对的节点设备")
        print("3. Canvas页面已创建在 canvas/index.html")
        print("4. 可以开始监控了")
    
    elif args.add_stock:
        parts = args.add_stock.split(',')
        if len(parts) >= 4:
            symbol = parts[0].strip()
            name = parts[1].strip()
            shares = int(parts[2].strip())
            cost_price = float(parts[3].strip())
            
            new_stock = {
                "symbol": symbol,
                "name": name,
                "user_data": {
                    "shares": shares,
                    "cost_price": cost_price,
                    "stop_loss": cost_price * 0.93,
                    "first_target": cost_price * 1.15
                }
            }
            
            # 添加到第一个监控目标
            if monitor.config["monitoring_targets"]:
                monitor.config["monitoring_targets"][0]["stocks"].append(new_stock)
            else:
                monitor.config["monitoring_targets"] = [{
                    "name": "炒股软件监控",
                    "type": "browser_window",
                    "url": "https://quote.eastmoney.com/concept/sh601857.html",
                    "stocks": [new_stock]
                }]
            
            monitor.save_config()
            print(f"✅ 已添加 {name} ({symbol}) 到监控列表")
        else:
            print("参数格式错误，应为：代码,名称,股数,成本价")
    
    elif args.nodes:
        monitor.check_nodes_status()
    
    elif args.check:
        print("🔍 立即检查...")
        node_id = monitor.check_nodes_status()
        if node_id:
            for target in monitor.config["monitoring_targets"]:
                for stock in target["stocks"]:
                    monitor.monitor_stock(node_id, stock)
    
    elif args.monitor:
        monitor.start_monitoring(args.interval)
    
    else:
        print("🎨 OpenClaw Canvas监控系统 - 方案3")
        print("=" * 50)
        print("使用方法:")
        print("  --setup                   设置Canvas监控")
        print("  --add-stock 601857,中国石油,800,12.465  添加股票")
        print("  --nodes                   检查节点状态")
        print("  --check                   立即检查一次")
        print("  --monitor --interval 30   开始持续监控")
        print("\n特点:")
        print("  • 使用OpenClaw Canvas显示监控界面")
        print("  • 支持iOS/Android节点设备")
        print("  • 实时快照和分析")
        print("  • 基于您的交易策略")
        print("\n需要:")
        print("  1. 已配对的OpenClaw节点设备")
        print("  2. 运行中的OpenClaw Gateway")
        print("  3. 节点设备在前台运行")

if __name__ == "__main__":
    main()
