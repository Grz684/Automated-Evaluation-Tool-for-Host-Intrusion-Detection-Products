import requests
import json
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_baseline_scan_task(token, machine_uuids, items, timeout=-1, sub_task_count=1):
    url = "http://10.10.21.119/kernelApi/kernelScanSrv/seTaskController/scanTask"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'token': token,
        'machineUuids': machine_uuids,
        'operate': 'run',
        'items': items,
        'timeout': timeout,
        'subTaskCount': sub_task_count
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    if response.status_code == 200:
        if response_data['code'] == '1':
            return response_data['data']['taskUuid']
        else:
            raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def get_token():
    url = "https://10.10.21.119/kernelApi/kernelCommonSrv/tokenInfoController/getToken"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, verify=False)

    if response.status_code == 200:
        if response.text:
            response_data = response.json()
            if response_data['code'] == '1':
                return response_data['data']['token']
            else:
                raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
        else:
            raise Exception("Error: Empty response from server")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def get_authorize_info(token):
    url = "https://10.10.21.119/kernelApi/kernelCommonSrv/dictionaryController/getAuthorizeInfo"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'token': token
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    response_data = response.json()
    print(response_data)

    if response.status_code == 200:
        if response_data['code'] == '1':
            return response_data['data']
        else:
            raise Exception(f"Error {response_data['code']}: {response_data['msg']}")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    try:
        token = get_token()
        authorize_info = get_authorize_info(token)
        print("获取授权信息成功，授权信息：")
        print(authorize_info)
    except Exception as e:
        print("获取授权信息失败，错误信息：")
        print(e)

    # try:
    #     token = get_token()
    #     print("获取token成功，token值：")
    #     print(token)
    # except Exception as e:
    #     print("获取token失败，错误信息：")
    #     print(e)
    #
    # token = "your_token"
    # machine_uuids = ["server1", "server2"]
    # items = [
    #     {
    #         'itemId': 1,
    #         'op': 'check'
    #     },
    #     {
    #         'itemId': 2,
    #         'op': 'check'
    #     }
    # ]
    # timeout = -1
    # sub_task_count = 1
    #
    # try:
    #     task_uuid = create_baseline_scan_task(token, machine_uuids, items, timeout, sub_task_count)
    #     print("任务创建成功，任务UUID：")
    #     print(task_uuid)
    # except Exception as e:
    #     print("任务创建失败，错误信息：")
    #     print(e)
