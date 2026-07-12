"""景点搜索工具"""

from langchain_core.tools import tool


# 模拟景点数据（实际应用可接入高德/Google Places API）
PLACES_DATA = {
    "北京": [
        {"name": "故宫博物院", "type": "历史古迹", "rating": 4.8, "price": "60元", "duration": "3-4小时", "address": "东城区景山前街4号", "highlights": ["太和殿", "乾清宫", "御花园"], "tips": ["提前网上预约", "周一闭馆"]},
        {"name": "长城（八达岭）", "type": "历史古迹", "rating": 4.7, "price": "40元", "duration": "4-5小时", "address": "延庆区八达岭镇", "highlights": ["好汉坡", "望京石", "烽火台"], "tips": ["穿舒适鞋子", "带够水"]},
        {"name": "天坛公园", "type": "历史古迹", "rating": 4.7, "price": "15元", "duration": "2-3小时", "address": "东城区天坛东里1号", "highlights": ["祈年殿", "回音壁", "圜丘"], "tips": ["清晨可看晨练"]},
        {"name": "颐和园", "type": "皇家园林", "rating": 4.7, "price": "30元", "duration": "3-4小时", "address": "海淀区新建宫门路19号", "highlights": ["长廊", "佛香阁", "昆明湖"], "tips": ["可乘船游览"]},
        {"name": "天安门广场", "type": "地标建筑", "rating": 4.6, "price": "免费", "duration": "1-2小时", "address": "东城区东长安街", "highlights": ["升旗仪式", "人民英雄纪念碑"], "tips": ["早起看升旗"]},
        {"name": "南锣鼓巷", "type": "特色街区", "rating": 4.3, "price": "免费", "duration": "2-3小时", "address": "东城区南锣鼓巷", "highlights": ["胡同文化", "特色小吃", "文创店"], "tips": ["周末人多"]},
    ],
    "上海": [
        {"name": "外滩", "type": "地标建筑", "rating": 4.7, "price": "免费", "duration": "1-2小时", "address": "黄浦区中山东一路", "highlights": ["万国建筑群", "陆家嘴夜景"], "tips": ["夜景更美"]},
        {"name": "东方明珠", "type": "现代建筑", "rating": 4.5, "price": "199元", "duration": "2-3小时", "address": "浦东新区世纪大道1号", "highlights": ["观光层", "旋转餐厅", "历史陈列馆"], "tips": ["建议傍晚去"]},
        {"name": "豫园", "type": "古典园林", "rating": 4.4, "price": "40元", "duration": "2-3小时", "address": "黄浦区安仁街137号", "highlights": ["假山", "古建筑", "豫园商城"], "tips": ["可品尝南翔小笼"]},
        {"name": "迪士尼乐园", "type": "主题公园", "rating": 4.6, "price": "475元", "duration": "1天", "address": "浦东新区川沙镇", "highlights": ["创极速光轮", "加勒比海盗", "烟花秀"], "tips": ["下载APP抢快速通道"]},
    ],
    "西安": [
        {"name": "兵马俑", "type": "历史古迹", "rating": 4.8, "price": "120元", "duration": "3-4小时", "address": "临潼区秦陵北路", "highlights": ["一号坑", "二号坑", "铜车马"], "tips": ["建议请导游讲解"]},
        {"name": "古城墙", "type": "历史古迹", "rating": 4.6, "price": "54元", "duration": "2-3小时", "address": "碑林区南大街", "highlights": ["骑行城墙", "城门楼"], "tips": ["可租自行车"]},
        {"name": "大雁塔", "type": "历史古迹", "rating": 4.5, "price": "40元", "duration": "1-2小时", "address": "雁塔区慈恩路", "highlights": ["塔顶俯瞰", "音乐喷泉"], "tips": ["喷泉晚上有表演"]},
        {"name": "回民街", "type": "美食街区", "rating": 4.3, "price": "免费", "duration": "2-3小时", "address": "莲湖区北院门", "highlights": ["羊肉泡馍", "肉夹馍", "凉皮"], "tips": ["注意清真礼仪"]},
    ],
    "成都": [
        {"name": "大熊猫繁育研究基地", "type": "动物园", "rating": 4.7, "price": "55元", "duration": "3-4小时", "address": "成华区熊猫大道1375号", "highlights": ["大熊猫", "小熊猫", "熊猫幼仔"], "tips": ["早上去熊猫更活跃"]},
        {"name": "武侯祠", "type": "历史古迹", "rating": 4.6, "price": "50元", "duration": "2-3小时", "address": "武侯区武侯祠大街231号", "highlights": ["诸葛亮殿", "刘备殿", "锦里古街"], "tips": ["可连同锦里一起逛"]},
        {"name": "锦里古街", "type": "特色街区", "rating": 4.4, "price": "免费", "duration": "2-3小时", "address": "武侯区锦里古街", "highlights": ["小吃", "茶馆", "手工艺品"], "tips": ["晚上灯笼很美"]},
        {"name": "都江堰", "type": "历史古迹", "rating": 4.7, "price": "80元", "duration": "4-5小时", "address": "都江堰市", "highlights": ["鱼嘴", "飞沙堰", "宝瓶口"], "tips": ["了解水利原理"]},
    ],
    "杭州": [
        {"name": "西湖", "type": "自然风光", "rating": 4.8, "price": "免费", "duration": "4-5小时", "address": "西湖区", "highlights": ["断桥残雪", "三潭印月", "雷峰塔"], "tips": ["骑行或步行最佳"]},
        {"name": "灵隐寺", "type": "寺庙", "rating": 4.6, "price": "75元", "duration": "2-3小时", "address": "西湖区灵隐路", "highlights": ["大雄宝殿", "飞来峰石刻"], "tips": ["注意着装得体"]},
        {"name": "千岛湖", "type": "自然风光", "rating": 4.5, "price": "150元", "duration": "1天", "address": "淳安县", "highlights": ["梅峰岛", "月光岛", "龙山岛"], "tips": ["建议乘船游览"]},
    ],
}


@tool
def search_places(city: str, place_type: str = "") -> str:
    """搜索指定城市的景点

    Args:
        city: 城市名称，如 "北京"、"上海"
        place_type: 景点类型筛选，如 "历史古迹"、"自然风光"、"美食街区"

    Returns:
        景点列表信息
    """
    if city not in PLACES_DATA:
        return f"暂无{city}的景点数据，支持的城市：{', '.join(PLACES_DATA.keys())}"

    places = PLACES_DATA[city]

    if place_type:
        places = [p for p in places if place_type in p["type"]]
        if not places:
            return f"{city}没有找到类型为「{place_type}」的景点"

    result = f"📍 {city}热门景点：\n\n"
    for i, place in enumerate(places, 1):
        result += (
            f"{i}. 【{place['name']}】\n"
            f"   类型：{place['type']} | 评分：{'⭐' * int(place['rating'])} {place['rating']}\n"
            f"   门票：{place['price']} | 建议游览：{place['duration']}\n"
            f"   地址：{place['address']}\n\n"
        )

    return result


@tool
def get_place_details(city: str, place_name: str) -> str:
    """获取指定景点的详细信息

    Args:
        city: 城市名称
        place_name: 景点名称

    Returns:
        景点详细信息
    """
    if city not in PLACES_DATA:
        return f"暂无{city}的景点数据"

    for place in PLACES_DATA[city]:
        if place_name in place["name"] or place["name"] in place_name:
            return (
                f"📍 {place['name']} 详细信息\n"
                f"{'=' * 40}\n"
                f"类型：{place['type']}\n"
                f"评分：{'⭐' * int(place['rating'])} {place['rating']}\n"
                f"门票：{place['price']}\n"
                f"建议游览时间：{place['duration']}\n"
                f"地址：{place['address']}\n\n"
                f"🎯 亮点：\n" + "\n".join(f"  • {h}" for h in place["highlights"]) + "\n\n"
                f"💡 小贴士：\n" + "\n".join(f"  • {t}" for t in place["tips"])
            )

    return f"未找到「{place_name}」的信息，请检查景点名称"
