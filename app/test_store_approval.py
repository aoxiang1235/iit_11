import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def get_token(username: str, password: str) -> str:
    """获取访问令牌"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": username,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_store_approval_flow():
    """测试商家入驻和审批流程"""
    print("\n=== 测试商家入驻和审批流程 ===")
    
    # 1. 注册商家用户
    print("\n1. 注册商家用户")
    merchant_data = {
        "username": "TestMerchant",
        "account": "test@merchant.com",
        "password": "test123",
        "phone_number": "13800138000",
        "social_preference": "Balanced"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=merchant_data
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 2. 商家登录
    print("\n2. 商家登录")
    merchant_token = get_token("TestMerchant", "test123")
    if not merchant_token:
        print("商家登录失败")
        return
        
    merchant_headers = {
        "Authorization": f"Bearer {merchant_token}",
        "Content-Type": "application/json"
    }
    
    # 3. 商家申请门店
    print("\n3. 商家申请门店")
    store_data = {
        "store_type": "餐厅",
        "store_phone": "13800138001",
        "store_address": "北京市朝阳区测试路1号",
        "store_hours": "10:00-22:00",
        "store_photo": "http://example.com/test.jpg"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/store/stores/apply",
        json=store_data,
        headers=merchant_headers
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        store_id = response.json()["id"]
        
        # 4. 管理员登录
        print("\n4. 管理员登录")
        admin_token = get_token("AdminUser", "admin123")
        if not admin_token:
            print("管理员登录失败")
            return
            
        admin_headers = {
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json"
        }
        
        # 5. 管理员审核门店
        print("\n5. 管理员审核门店")
        approval_data = {
            "is_pass": 1  # 1表示通过
        }
        
        response = requests.put(
            f"{BASE_URL}/api/store/stores/{store_id}",
            json=approval_data,
            headers=admin_headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 6. 商家查看门店状态
        print("\n6. 商家查看门店状态")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/{store_id}",
            headers=merchant_headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_store_approval_flow() 