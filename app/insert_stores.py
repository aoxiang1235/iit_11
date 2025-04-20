import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

# 登录获取token
def get_token():
    login_data = {
        "username": "AliceDesign",
        "password": "hashed_pass1"
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

# 门店数据模板
stores = [
    {"store_type": "餐厅", "store_phone": "13800138001", "store_address": "北京市东城区王府井", "store_hours": "10:00-22:00", "store_photo": "http://example.com/restaurant1.jpg"},
    {"store_type": "服装店", "store_phone": "13800138002", "store_address": "北京市西城区西单", "store_hours": "09:00-21:00", "store_photo": "http://example.com/clothing1.jpg"},
    {"store_type": "超市", "store_phone": "13800138003", "store_address": "北京市朝阳区国贸", "store_hours": "08:00-22:00", "store_photo": "http://example.com/supermarket1.jpg"},
    {"store_type": "健身房", "store_phone": "13800138004", "store_address": "北京市海淀区五道口", "store_hours": "06:00-22:00", "store_photo": "http://example.com/gym1.jpg"},
    {"store_type": "美容院", "store_phone": "13800138005", "store_address": "北京市朝阳区三里屯", "store_hours": "10:00-20:00", "store_photo": "http://example.com/beauty1.jpg"},
    {"store_type": "电影院", "store_phone": "13800138006", "store_address": "北京市朝阳区望京", "store_hours": "10:00-24:00", "store_photo": "http://example.com/cinema1.jpg"},
    {"store_type": "KTV", "store_phone": "13800138007", "store_address": "北京市海淀区中关村", "store_hours": "12:00-02:00", "store_photo": "http://example.com/ktv1.jpg"},
    {"store_type": "网吧", "store_phone": "13800138008", "store_address": "北京市朝阳区建国门", "store_hours": "00:00-24:00", "store_photo": "http://example.com/internet1.jpg"},
    {"store_type": "花店", "store_phone": "13800138009", "store_address": "北京市东城区东直门", "store_hours": "09:00-21:00", "store_photo": "http://example.com/flower1.jpg"},
    {"store_type": "宠物店", "store_phone": "13800138010", "store_address": "北京市朝阳区双井", "store_hours": "09:00-20:00", "store_photo": "http://example.com/pet1.jpg"},
    {"store_type": "书店", "store_phone": "13800138011", "store_address": "北京市海淀区清华园", "store_hours": "09:00-21:00", "store_photo": "http://example.com/bookstore2.jpg"},
    {"store_type": "咖啡店", "store_phone": "13800138012", "store_address": "北京市朝阳区国贸", "store_hours": "08:00-22:00", "store_photo": "http://example.com/coffee2.jpg"},
    {"store_type": "甜品店", "store_phone": "13800138013", "store_address": "北京市西城区西单", "store_hours": "10:00-21:00", "store_photo": "http://example.com/dessert1.jpg"},
    {"store_type": "酒吧", "store_phone": "13800138014", "store_address": "北京市朝阳区三里屯", "store_hours": "18:00-02:00", "store_photo": "http://example.com/bar1.jpg"},
    {"store_type": "茶室", "store_phone": "13800138015", "store_address": "北京市东城区南锣鼓巷", "store_hours": "10:00-21:00", "store_photo": "http://example.com/tea1.jpg"},
    {"store_type": "文具店", "store_phone": "13800138016", "store_address": "北京市海淀区中关村", "store_hours": "09:00-20:00", "store_photo": "http://example.com/stationery1.jpg"},
    {"store_type": "数码店", "store_phone": "13800138017", "store_address": "北京市朝阳区望京", "store_hours": "10:00-21:00", "store_photo": "http://example.com/digital1.jpg"},
    {"store_type": "药店", "store_phone": "13800138018", "store_address": "北京市西城区西单", "store_hours": "08:00-22:00", "store_photo": "http://example.com/pharmacy1.jpg"},
    {"store_type": "水果店", "store_phone": "13800138019", "store_address": "北京市朝阳区双井", "store_hours": "07:00-21:00", "store_photo": "http://example.com/fruit1.jpg"},
    {"store_type": "便利店", "store_phone": "13800138020", "store_address": "北京市海淀区五道口", "store_hours": "00:00-24:00", "store_photo": "http://example.com/convenience1.jpg"}
]

def main():
    # 获取token
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 批量创建门店
    for store in stores:
        response = requests.post(
            f"{BASE_URL}/api/store/stores/apply",
            json=store,
            headers=headers
        )
        print(f"创建门店: {store['store_type']}")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        print("-" * 50)

if __name__ == "__main__":
    main() 