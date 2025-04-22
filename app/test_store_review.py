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

def test_store_review_flow():
    """测试门店评价流程"""
    print("\n=== 测试门店评价流程 ===")
    
    # 1. 登录获取token
    print("\n1. 用户登录")
    token = get_token("BobAdminUpdated", "hashed_pass2")
    if not token:
        print("登录失败")
        return
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. 创建评价
    print("\n2. 创建评价")
    review_data = {
        "store_id": 1,
        "rating": 5,
        "review_text": "服务很好，环境优美，下次还会再来！"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/store-reviews",
        json=review_data,
        headers=headers
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 3. 获取门店评价
    print("\n3. 获取门店评价")
    response = requests.get(
        f"{BASE_URL}/api/store-reviews/store/1"
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 4. 获取用户评价
    print("\n4. 获取用户评价")
    response = requests.get(
        f"{BASE_URL}/api/store-reviews/my-reviews",
        headers=headers
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_store_review_flow() 