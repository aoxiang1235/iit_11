import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

# 测试登录接口
def test_login():
    login_data = {
        "username": "AliceDesign",
        "password": "hashed_pass1"  # 修改为正确的密码
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    test_login() 