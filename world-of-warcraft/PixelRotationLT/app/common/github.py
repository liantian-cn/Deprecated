import base64
import http.client
import json
from urllib.parse import quote

# 替换为您的 GitHub 访问令牌、仓库所有者、仓库名称和路径
ACCESS_TOKEN = ""
OWNER = "liantian-cn"
REPO = "PixelRotationLTProfile"


def get_github_directory_contents(access_token=ACCESS_TOKEN, owner=OWNER, repo=REPO, path=""):
    # 设置请求头
    headers = {
        "Authorization": f"token {access_token}",
        'X-GitHub-Api-Version': '2022-11-28',
        "User-Agent": repo
    }

    # 创建连接
    conn = http.client.HTTPSConnection("api.github.com")

    if path.endswith("/"):
        path = path[:-1]


    # 构建请求的 URL
    url = f"/repos/{owner}/{repo}/contents/{path}"
    # print(url)
    # 发送 GET 请求
    conn.request("GET", url, headers=headers)

    # 获取响应
    response = conn.getresponse()
    # print(response.status)
    data = response.read()
    # print(data)

    try:

        if response.status == 200:
            items = json.loads(data)
            # 过滤掉文件名以"."开头的文件
            contents = [item for item in items if not item['name'].startswith('.')]
        else:
            raise ValueError(f"请求失败，状态码: {response.status}, 消息: {data.decode()}")
    except Exception as e:
        print(e)
        raise ValueError(f"发生错误: {e}")
    finally:
        conn.close()

    return contents


def create_github_file(file_name, content, path="", access_token=ACCESS_TOKEN, owner=OWNER, repo=REPO, ):
    headers = {
        "Authorization": f"token {access_token}",
        'X-GitHub-Api-Version': '2022-11-28',
        "User-Agent": repo,
        "Content-Type": "application/json"
    }

    conn = http.client.HTTPSConnection("api.github.com")
    url = f"/repos/{owner}/{repo}/contents/{path}{file_name}"
    encoded_content = base64.b64encode(content.encode()).decode()
    encoded_url = quote(url)

    data = {
        "message": f"Add {file_name}",
        "content": encoded_content,
        "branch": "main"  # 根据需要指定分支
    }

    try:
        conn.request("PUT", encoded_url, json.dumps(data), headers)
        response = conn.getresponse()
        response_data = response.read()

        if response.status == 201:
            print(f"文件 '{file_name}' 创建成功！")
        else:
            raise ValueError(f"请求失败，状态码: {response.status}, 消息: {response_data.decode()}")
    except Exception as e:
        raise ValueError(f"发生错误: {e}")
    finally:
        conn.close()


def update_github_file(file_name, content, path="", access_token=ACCESS_TOKEN, owner=OWNER, repo=REPO, ):
    headers = {
        "Authorization": f"token {access_token}",
        'X-GitHub-Api-Version': '2022-11-28',
        "User-Agent": repo,
        "Content-Type": "application/json"
    }

    conn = http.client.HTTPSConnection("api.github.com")
    url = f"/repos/{owner}/{repo}/contents/{path}{file_name}"
    encoded_content = base64.b64encode(content.encode()).decode()
    encoded_url = quote(url)

    try:
        # 请求获取文件的信息
        conn.request("GET", encoded_url, headers=headers)
        response = conn.getresponse()

        if response.status == 200:
            file_info = json.loads(response.read())
            sha = file_info['sha']

            data = {
                "message": f"Update {file_name}",
                "content": encoded_content,
                "sha": sha,
                "branch": "main"  # 根据需要指定分支
            }

            # 发送 PUT 请求以更新文件
            conn.request("PUT", encoded_url, json.dumps(data), headers)
            response = conn.getresponse()
            response_data = response.read()

            if response.status == 200:
                print(f"文件 '{file_name}' 更新成功！")
            else:
                print(f"更新失败，状态码: {response.status}, 消息: {response_data.decode()}")
        elif response.status == 404:
            print(f"文件 '{file_name}' 不存在，可以创建新的文件。")
            create_github_file(access_token=access_token, owner=owner, repo=repo, path=path, file_name=file_name,
                               content=content)
        else:
            raise ValueError(f"请求失败，状态码: {response.status}, 消息: {response.read().decode()}")
    except Exception as e:
        raise ValueError(f"发生错误: {e}")
    finally:
        conn.close()


def download_github_file(file_name, path="", access_token=ACCESS_TOKEN, owner=OWNER, repo=REPO, ):
    headers = {
        "Authorization": f"token {access_token}",
        'X-GitHub-Api-Version': '2022-11-28',
        "User-Agent": repo
    }

    conn = http.client.HTTPSConnection("api.github.com")
    url = f"/repos/{owner}/{repo}/contents/{path}{file_name}"
    # print(url)
    encoded_url = quote(url)
    try:
        # 发送 GET 请求以获取文件内容
        conn.request("GET", encoded_url, headers=headers)
        response = conn.getresponse()

        if response.status == 200:
            file_info = json.loads(response.read())
            # 提取文件内容并解码
            file_content = base64.b64decode(file_info['content']).decode()
            # print(f"文件 '{file_name}' 的内容:\n{file_content}")
            return file_content
        else:
            raise ValueError(f"下载失败，状态码: {response.status}, 消息: {response.read().decode()}")
    except Exception as e:
        raise ValueError(f"发生错误: {e}")
    finally:
        conn.close()


def list_cloud_profile(path=""):
    contents = get_github_directory_contents(path=path)
    profiles = []
    for item in contents:
        if (item['type'] == 'file') and (not item['name'].startswith('.')):
            profiles.append(item['name'].replace(".json", ""))
    return profiles


def get_cloud_profile(profile_name, path=""):
    # print(path)
    content = download_github_file(f"{profile_name}.json", path=path)
    return json.loads(content)


def save_cloud_profile(profile_name, profile, path=""):
    data = json.dumps(profile, indent=4)
    # print(data)
    update_github_file(f"{profile_name}.json", data, path=path)
