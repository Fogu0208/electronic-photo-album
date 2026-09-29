"""本地冒烟测试：验证登录 -> 带 Token 访问受保护接口 -> 静态图片"""
import json
import urllib.request

BASE = "http://127.0.0.1:8081"
OP = "http://127.0.0.1:5174"


def post(path, body, token=None):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


def get(path, token=None):
    req = urllib.request.Request(BASE + path)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())


print("1) 管理员登录:", json.dumps(post("/api/auth/login", {
    "username": "python222", "password": "123456", "role": "ADMIN"
}), ensure_ascii=False)[:220])

admin_token = post("/api/auth/login", {
    "username": "python222", "password": "123456", "role": "ADMIN"
})["data"]["token"]

print("2) 普通用户登录:", json.dumps(post("/api/auth/login", {
    "username": "zhangsan", "password": "123456", "role": "USER"
}), ensure_ascii=False)[:220])

user_token = post("/api/auth/login", {
    "username": "zhangsan", "password": "123456", "role": "USER"
})["data"]["token"]

for name, path in [("用户列表", "/api/user/page?pageNum=1&pageSize=3"),
                   ("相册列表", "/api/album/page?pageNum=1&pageSize=3"),
                   ("照片列表", "/api/photo/page?pageNum=1&pageSize=3"),
                   ("分类列表", "/api/category/list"),
                   ("公告列表", "/api/notice/list"),
                   ("统计概览", "/api/statistic/admin")]:
    try:
        res = get(path, admin_token)
        data = res.get("data")
        size = len(data) if isinstance(data, list) else str(data)[:120]
        print(f"3) {name}: code={res.get('code')} 数据量/内容={size}")
    except Exception as e:
        print(f"3) {name}: 失败 -> {e}")

print("4) 用户端相册广场:", json.dumps(get("/api/album/public/page?pageNum=1&pageSize=3", user_token),
                                       ensure_ascii=False)[:200])

# 静态图片：取一张库里照片的 url 试试能否下载
try:
    photos = get("/api/photo/page?pageNum=1&pageSize=1", admin_token)["data"]
    rows = photos.get("records") or photos.get("list") or []
    if rows:
        url = rows[0].get("url") or rows[0].get("imgUrl")
        print("5) 首张照片 url:", url)
        if url:
            with urllib.request.urlopen(BASE + url, timeout=10) as r:
                print("   直接访问后端静态资源: HTTP", r.status, "字节数=", len(r.read()))
            with urllib.request.urlopen(OP + url, timeout=10) as r:
                print("   经前端代理访问: HTTP", r.status, "字节数=", len(r.read()))
except Exception as e:
    print("5) 静态资源检查失败 ->", e)

print("=== 冒烟测试结束 ===")
