import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

# 测试登录接口
def test_login():
    login_data = {
        "username": "AliceNewUpdated",
        "password": "hashed_pass2"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=login_data,  # 使用 data 而不是 json
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"\n=== 测试登录 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.json()["access_token"]
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

# 测试查询所有用户
def test_query_all_users(token):
    try:
        response = requests.get(
            f"{BASE_URL}/api/userManger/queryAllUsers",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"\n=== 测试查询所有用户 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.json()
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None

# 测试更新用户信息
def test_update_profile(token, user_data):
    try:
        response = requests.put(
            f"{BASE_URL}/api/userManger/updateProfile",
            headers={"Authorization": f"Bearer {token}"},
            json=user_data
        )
        print(f"\n=== 测试更新用户信息 ===")
        print(f"请求数据: {json.dumps(user_data, indent=2, ensure_ascii=False)}")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

# 测试禁用/启用用户
def test_update_user_status(token, user_id, is_disabled):
    try:
        response = requests.put(
            f"{BASE_URL}/api/userManger/{user_id}/disable",
            headers={"Authorization": f"Bearer {token}"},
            json={"is_disabled": is_disabled}
        )
        print(f"\n=== 测试{'禁用' if is_disabled else '启用'}用户 ===")
        print(f"用户ID: {user_id}")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    # 查询所有用户
    token = test_login()
    if not token:
        print("登录失败")
        exit(1)
    
    users = test_query_all_users(token)
    if not users:
        print("查询用户失败")
        exit(1)
    
    # 找到一个普通用户进行测试
    normal_user = next((user for user in users if user["role"] == "normal"), None)
    if normal_user:
        # 测试更新用户信息
        token = test_login()  # 重新获取token
        update_data = {
            "phone_number": "+86987654321",
            "social_preference": "Lively"
        }
        test_update_profile(token, update_data)
        
        # 测试禁用用户
        token = test_login()  # 重新获取token
        test_update_user_status(token, normal_user["id"], True)
        
        # 测试启用用户
        token = test_login()  # 重新获取token
        test_update_user_status(token, normal_user["id"], False)
        
        # 再次查询所有用户，验证更改
        token = test_login()  # 重新获取token
        test_query_all_users(token) 