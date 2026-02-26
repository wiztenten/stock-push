import requests
from datetime import datetime

WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/d5c7637a-3743-4b6d-bb61-1b6ab6310724"

portfolio = [
    {"name": "金鹤5", "code": "400208", "cost": 3.38, "shares": 1900},
    {"name": "诺普信", "code": "002215", "cost": 10.0735, "shares": 1600},
    {"name": "TCL中环", "code": "002129", "cost": 36.3438, "shares": 250},
]

def get_price(code):
    if code.startswith("00") or code.startswith("30"):
        url = f"https://qt.gtimg.cn/q=sz{code}"
    elif code.startswith("60"):
        url = f"https://qt.gtimg.cn/q=sh{code}"
    else:
        url = f"https://qt.gtimg.cn/q={code}"
    r = requests.get(url).text
    parts = r.split("~")
    return float(parts[3])

lines = []
total_profit = 0

for p in portfolio:
    try:
        price = get_price(p["code"])
    except:
        price = 0
    
    cost = p["cost"]
    shares = p["shares"]
    profit = (price - cost) * shares
    pct = (price - cost) / cost * 100 if cost > 0 else 0
    total_profit += profit
    
    lines.append(
        f"{p['name']}：现价{price:.2f} 成本{cost:.2f} 盈亏{profit:.0f}元 ({pct:.1f}%)"
    )

time_str = datetime.now().strftime("%Y-%m-%d %H:%M")

text = f"""【持仓分析 {time_str}】

{chr(10).join(lines)}

总盈亏：{total_profit:.0f}元"""

data = {
    "msg_type": "text",
    "content": {"text": text}
}

requests.post(WEBHOOK, json=data)
