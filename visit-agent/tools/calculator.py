"""计算器工具"""

import math
from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """计算数学表达式，支持加减乘除、幂运算、三角函数等

    Args:
        expression: 数学表达式，如 "2+3*4"、"sqrt(16)"、"1000/3"

    Returns:
        计算结果
    """
    # 安全的数学函数
    safe_dict = {
        "abs": abs,
        "round": round,
        "pow": pow,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "pi": math.pi,
        "e": math.e,
        "ceil": math.ceil,
        "floor": math.floor,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def estimate_budget(
    days: int,
    hotel_per_night: float = 300,
    meals_per_day: float = 150,
    transport_total: float = 500,
    tickets_total: float = 300,
    shopping: float = 500,
) -> str:
    """估算旅行预算

    Args:
        days: 旅行天数
        hotel_per_night: 每晚住宿费用（元），默认300
        meals_per_day: 每天餐饮费用（元），默认150
        transport_total: 交通总费用（元），默认500
        tickets_total: 门票总费用（元），默认300
        shopping: 购物预算（元），默认500

    Returns:
        预算明细和总计
    """
    hotel_total = hotel_per_night * (days - 1) if days > 1 else hotel_per_night
    meals_total = meals_per_day * days
    total = hotel_total + meals_total + transport_total + tickets_total + shopping

    return (
        f"💰 旅行预算估算（{days}天）\n"
        f"{'=' * 30}\n"
        f"🏨 住宿：{hotel_per_night}元 × {days - 1}晚 = {hotel_total}元\n"
        f"🍜 餐饮：{meals_per_day}元 × {days}天 = {meals_total}元\n"
        f"🚗 交通：{transport_total}元\n"
        f"🎫 门票：{tickets_total}元\n"
        f"🛍️ 购物：{shopping}元\n"
        f"{'=' * 30}\n"
        f"💵 总计：{total}元\n\n"
        f"💡 节省建议：\n"
        f"  • 选择经济型酒店可节省30-50%住宿费\n"
        f"  • 品尝当地小吃比餐厅更实惠\n"
        f"  • 使用公共交通代替打车"
    )
