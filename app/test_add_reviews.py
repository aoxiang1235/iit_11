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

def add_reviews():
    """添加多条评价数据"""
    print("\n=== 添加评价数据 ===")
    
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
    
    # 2. 创建多条评价
    reviews = [
        # 门店1的评价
        {
            "store_id": 1,
            "rating": 5,
            "review_text": "服务很好，环境优美，下次还会再来！"
        },
        {
            "store_id": 1,
            "rating": 4,
            "review_text": "菜品不错，服务态度好，就是价格稍贵。"
        },
        {
            "store_id": 1,
            "rating": 3,
            "review_text": "一般般，可以接受。"
        },
        {
            "store_id": 1,
            "rating": 2,
            "review_text": "服务态度不太好，等待时间太长。"
        },
        {
            "store_id": 1,
            "rating": 1,
            "review_text": "非常失望，不会再来了。"
        },
        
        # 门店2的评价
        {
            "store_id": 2,
            "rating": 5,
            "review_text": "环境很好，音乐很棒，服务很贴心！"
        },
        {
            "store_id": 2,
            "rating": 5,
            "review_text": "音响效果非常好，包厢很干净。"
        },
        {
            "store_id": 2,
            "rating": 4,
            "review_text": "整体不错，就是价格有点贵。"
        },
        {
            "store_id": 2,
            "rating": 4,
            "review_text": "服务态度很好，环境也不错。"
        },
        
        # 门店3的评价
        {
            "store_id": 3,
            "rating": 3,
            "review_text": "咖啡味道一般，环境还可以。"
        },
        {
            "store_id": 3,
            "rating": 2,
            "review_text": "服务态度不太好，咖啡也不够新鲜。"
        },
        {
            "store_id": 3,
            "rating": 1,
            "review_text": "非常失望，咖啡很淡，价格还贵。"
        },
        
        # 门店4的评价
        {
            "store_id": 4,
            "rating": 5,
            "review_text": "菜品非常好吃，服务很周到！"
        },
        {
            "store_id": 4,
            "rating": 5,
            "review_text": "环境很好，菜品很精致，推荐！"
        },
        {
            "store_id": 4,
            "rating": 4,
            "review_text": "味道不错，就是等待时间有点长。"
        },
        {
            "store_id": 4,
            "rating": 4,
            "review_text": "服务态度很好，菜品也很新鲜。"
        },
        {
            "store_id": 4,
            "rating": 3,
            "review_text": "一般般，可以接受。"
        }
    ]
    
    for i, review in enumerate(reviews, 1):
        print(f"\n添加第{i}条评价:")
        response = requests.post(
            f"{BASE_URL}/api/store-reviews",
            json=review,
            headers=headers
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        time.sleep(1)  # 添加延迟，避免请求过快
    
    # 3. 查看各门店的评价统计
    print("\n查看各门店的评分分布统计:")
    for store_id in range(1, 5):
        print(f"\n门店{store_id}的评分分布:")
        response = requests.get(
            f"{BASE_URL}/api/store/stores/stats/ratings?store_id={store_id}"
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        time.sleep(1)

if __name__ == "__main__":
    add_reviews() 