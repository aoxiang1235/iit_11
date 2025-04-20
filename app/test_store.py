import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def register_merchant():
    """注册商家用户"""
    print("\n=== 注册商家用户 ===")
    register_data = {
        "username": "DavidMerchant",
        "account": "david@merchant.com",
        "password": "hashed_pass4",
        "phone_number": "+86123456789",
        "social_preference": "Balanced"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=register_data
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def get_token(username: str, password: str):
    """获取访问令牌"""
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

def test_merchant_flow():
    """测试商家用户流程"""
    print("\n=== 测试商家用户流程 ===")
    
    # 1. 注册商家用户
    if not register_merchant():
        print("注册商家用户失败")
        return
    
    # 2. 使用商家账户登录
    print("\n2. 商家用户登录")
    merchant_token = get_token("DavidMerchant", "hashed_pass4")
    headers = {
        "Authorization": f"Bearer {merchant_token}",
        "Content-Type": "application/json"
    }
    
    # 3. 申请门店
    print("\n3. 申请门店")
    store_data = {
        "store_type": "餐厅",
        "store_phone": "13800138001",
        "store_address": "北京市东城区王府井大街1号",
        "store_hours": "10:00-22:00",
        "store_photo": "http://example.com/restaurant1.jpg"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/store/stores/apply",
        json=store_data,
        headers=headers
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        store_id = response.json()["id"]
        
        # 4. 获取我的门店列表
        print("\n4. 获取我的门店列表")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/my/stores",
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 5. 更新门店信息
        print("\n5. 更新门店信息")
        update_data = {
            "store_hours": "09:00-23:00",
            "store_phone": "13800138002"
        }
        response = requests.put(
            f"{BASE_URL}/api/store/stores/{store_id}",
            json=update_data,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 6. 获取门店详情
        print("\n6. 获取门店详情")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/{store_id}",
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_merchant_flow() 