import requests
import json
import time

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

def test_rating_stats():
    """测试评分统计相关接口"""
    print("\n=== 测试评分统计接口 ===")
    
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
    
    # 2. 测试获取所有评分分布
    print("\n2. 获取所有评分分布")
    response = requests.get(
        f"{BASE_URL}/api/store/stores/stats/ratings"
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 3. 测试获取特定门店的评分分布
    print("\n3. 获取特定门店的评分分布")
    for store_id in range(1, 5):
        print(f"\n门店{store_id}的评分分布:")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/stats/ratings?store_id={store_id}"
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        time.sleep(1)
    
    # 4. 测试获取特定评分的数量
    print("\n4. 获取特定评分的数量")
    for rating in range(1, 6):
        print(f"\n{rating}星评价的数量:")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/stats/ratings?rating={rating}"
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        time.sleep(1)
    
    # 5. 测试获取特定门店的特定评分数量
    print("\n5. 获取特定门店的特定评分数量")
    for store_id in range(1, 5):
        for rating in range(1, 6):
            print(f"\n门店{store_id}的{rating}星评价数量:")
            response = requests.get(
                f"{BASE_URL}/api/store/stores/stats/ratings?store_id={store_id}&rating={rating}"
            )
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            time.sleep(1)
    
    # 6. 测试获取商家类型统计
    print("\n6. 获取商家类型统计")
    response = requests.get(
        f"{BASE_URL}/api/store/stores/stats/types"
    )
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 7. 测试获取特定商家的类型统计
    print("\n7. 获取特定商家的类型统计")
    for store_id in range(1, 5):
        print(f"\n门店{store_id}的类型统计:")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/stats/types?store_id={store_id}"
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        time.sleep(1)

if __name__ == "__main__":
    test_rating_stats() 