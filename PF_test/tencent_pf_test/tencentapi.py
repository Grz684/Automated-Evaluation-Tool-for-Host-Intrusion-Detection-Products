import json
import os
import sqlite3

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cwp.v20180228 import cwp_client, models


class TencentApi:
    def __init__(self, secretid, secretkey, uuid):
        self.baseline_database = "tencent_cis_baseline_scan_items.db"
        self.secretid = secretid
        self.secretkey = secretkey
        self.uuid = uuid

    # 基线检测 CIS Ubuntu
    def start_baseline_detect(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.StartBaselineDetectRequest()
            params = {
                "Param": {
                    "RuleIds": [133],
                    "HostIds": [self.uuid]
                }
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个StartBaselineDetectResponse的实例，与请求对象对应
            resp = client.StartBaselineDetect(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    def scan_asset(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.ScanAssetRequest()
            params = {
                "AssetTypeIds": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],  # 全采集
                "Quuids": [self.uuid]
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ScanAssetResponse的实例，与请求对象对应
            resp = client.ScanAsset(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    def scan_malware(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.CreateScanMalwareSettingRequest()
            params = {
                "ScanPattern": 1,  # 0:全盘扫描； 1:快速扫描
                "HostType": 2,
                "QuuidList": [self.uuid],
                "EngineType": 1,
                "EnableMemShellScan": 1
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个CreateScanMalwareSettingResponse的实例，与请求对象对应
            resp = client.CreateScanMalwareSetting(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    # "VulCategories" 1: web-cms漏洞 2:应用漏洞 4: Linux软件漏洞 5: Windows系统漏洞 (多选英文;分隔) 6: emg漏洞
    # 是否是应急漏洞 0 否 1 是
    def scan_vul(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.ScanVulRequest()

            params = {
                "VulCategories": "1;2;4;5",
                "VulEmergency": 0,
                "VulLevels": "1;2;3;4",
                "HostType": 2,
                "QuuidList": [self.uuid]
            }

            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ScanVulResponse的实例，与请求对象对应
            resp = client.ScanVul(req)
            # 输出json格式的字符串回包
            print(resp.to_json_string())

        except TencentCloudSDKException as err:
            print(err)

    def describe_malware_list(self, ip):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeMalWareListRequest()
            params = {
                "Limit": 100,
                "Offset": 0,
                "Filters": [
                    {
                        "Name": "Status",
                        "Values": ["4"]
                    },
                    {
                        "Name": "IP",
                        "Values": [ip]
                    }
                ],
                "By": "LatestScanTime",
                "Order": "DESC"
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeMalWareListResponse的实例，与请求对象对应
            resp = client.DescribeMalWareList(req)
            response = resp.to_json_string()

            # 输出json格式的字符串回包
            json_obj = json.loads(response)
            formatted_json_str = json.dumps(json_obj, indent=4, sort_keys=True, ensure_ascii=False)
            # print(formatted_json_str)
            return response

        except TencentCloudSDKException as err:
            print(err)

    def modify_risk_events_status(self, ids):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.ModifyRiskEventsStatus()

            params = {
                "Ids": ids,
                "Operate": 5,
                "RiskType": "MALWARE"
            }

            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ScanVulResponse的实例，与请求对象对应
            resp = client.ModifyRiskEventsStatus(req)
            # 输出json格式的字符串回包
            print(resp)

        except TencentCloudSDKException as err:
            print(err)

    def describe_baseline_item_info(self):
        def create_table_and_connect_db(database_name):
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        item_id INTEGER PRIMARY KEY,
                        item_name TEXT,
                        item_desc TEXT,
                        is_passed_check TEXT
                    )
                """)

            conn.commit()
            return conn

        # 将数据插入到数据库
        def insert_data_to_db(conn, item_id, item_name, item_desc=None, is_passed_check=None):
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT OR REPLACE INTO items (item_id, item_name, item_desc, is_passed_check) VALUES (?, ?, ?, ?)
                """, (item_id, item_name, item_desc, is_passed_check))
            conn.commit()

        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 第一次请求，无偏移
            req1 = models.DescribeBaselineItemInfoRequest()
            params1 = {
                "Filters": [
                    {
                        "Name": "RuleId",
                        "Values": ["133"]
                    }
                ],
                "Limit": 100,
            }
            req1.from_json_string(json.dumps(params1))
            resp1 = client.DescribeBaselineItemInfo(req1)

            jsonString1 = resp1.to_json_string()
            jsonData1 = json.loads(jsonString1)

            # 第二次请求，偏移100
            req2 = models.DescribeBaselineItemInfoRequest()
            params2 = {
                "Filters": [
                    {
                        "Name": "RuleId",
                        "Values": ["133"]
                    }
                ],
                "Limit": 100,
                "Offset": 100
            }
            req2.from_json_string(json.dumps(params2))
            resp2 = client.DescribeBaselineItemInfo(req2)

            jsonString2 = resp2.to_json_string()
            jsonData2 = json.loads(jsonString2)

            # 合并两次请求结果
            merged_list = jsonData1['List'] + jsonData2['List']
            print(merged_list)
            print(len(merged_list))

            # 连接数据库
            if os.path.exists(self.baseline_database):
                os.remove(self.baseline_database)
            conn = create_table_and_connect_db(self.baseline_database)

            for item in merged_list:
                item_id = item['ItemId']
                item_name = item['ItemName']
                item_desc = item['ItemDesc']

                insert_data_to_db(conn, item_id, item_name, item_desc)

            conn.close()

        except TencentCloudSDKException as err:
            print(err)

    def describe_asset_host_total_count(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeAssetHostTotalCountRequest()
            params = {
                "Uuid": self.uuid,
                "Quuid": self.uuid
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeAssetHostTotalCountResponse的实例，与请求对象对应
            resp = client.DescribeAssetHostTotalCount(req)
            response = resp.to_json_string()
            # 输出json格式的字符串回包
            json_obj = json.loads(response)
            # formatted_json_str = json.dumps(json_obj, indent=4, sort_keys=True, ensure_ascii=False)
            assets_info = {}
            for type in json_obj['Types']:
                assets_info[type['Key']] = type['Value']
            # print(formatted_json_str)
            print(assets_info)
            return assets_info

        except TencentCloudSDKException as err:
            print(err)

    def describe_vul_list(self):

        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeVulListRequest()
            params = {
                "Limit": 100,
                "Filters": [
                    {
                        "Name": "Uuid",
                        "Values": [self.uuid]
                    }
                ]
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个DescribeVulListResponse的实例，与请求对象对应
            resp = client.DescribeVulList(req)
            response = resp.to_json_string()
            # 输出json格式的字符串回包
            json_obj = json.loads(response)
            vul_info = {}
            for item in json_obj['VulInfoList']:
                vul_info[item["CveId"]] = item['Name']
            print(vul_info)
            return vul_info

            # formatted_json_str = json.dumps(json_obj, indent=4, sort_keys=True, ensure_ascii=False)
            # print(formatted_json_str)

        except TencentCloudSDKException as err:
            print(err)

    def describe_baseline_item_detect_list(self):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
            # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
            cred = credential.Credential(self.secretid, self.secretkey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cwp.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = cwp_client.CwpClient(cred, "", clientProfile)

            # 第一次请求，无偏移
            req1 = models.DescribeBaselineItemDetectListRequest()
            params1 = {
                "Filters": [
                    {
                        "Name": "HostId",
                        "Values": [self.uuid]
                    },
                    {
                        "Name": "RuleId",
                        "Values": ["133"]
                    }
                ],
                "Limit": 100
            }
            req1.from_json_string(json.dumps(params1))
            resp1 = client.DescribeBaselineItemDetectList(req1)

            jsonString1 = resp1.to_json_string()
            jsonData1 = json.loads(jsonString1)

            # 第二次请求，偏移100
            req2 = models.DescribeBaselineItemDetectListRequest()
            params2 = {
                "Filters": [
                    {
                        "Name": "HostId",
                        "Values": [self.uuid]
                    },
                    {
                        "Name": "RuleId",
                        "Values": ["133"]
                    }
                ],
                "Limit": 100,
                "Offset": 100
            }
            req2.from_json_string(json.dumps(params2))
            resp2 = client.DescribeBaselineItemDetectList(req2)

            jsonString2 = resp2.to_json_string()
            jsonData2 = json.loads(jsonString2)

            # 合并两次请求结果
            merged_list = jsonData1['List'] + jsonData2['List']
            print(len(merged_list))

            # 连接数据库
            conn = sqlite3.connect(self.baseline_database)
            cursor = conn.cursor()

            for baseline_detect_item in merged_list:
                # 定义要更新的item_id和is_passed_check的值
                is_passed_check = "yes" if baseline_detect_item['PassedHostCount'] == 1 else "no"
                item_id = baseline_detect_item['ItemId']

                # 执行更新操作
                cursor.execute(f"UPDATE items SET is_passed_check = ? WHERE item_id = ?",
                               (is_passed_check, item_id))

            # 提交更改并关闭连接
            conn.commit()
            conn.close()

        except TencentCloudSDKException as err:
            print(err)


if __name__ == '__main__':
    tencentapi = TencentApi("AKIDqbGl9NyRkrwxpfNwEPO8jAQTL5iQG1b2", "MckjeP0QfhYCg2tX5RiKrCMN4iCZlolY",
                            "ebb72142-e05d-e812-505e-05bf0d7b4907")
    tencentapi.describe_baseline_item_info()
    tencentapi.describe_baseline_item_detect_list()
