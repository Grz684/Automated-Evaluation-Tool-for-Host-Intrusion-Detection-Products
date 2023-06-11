# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import json
import sqlite3
import sys

from typing import List

from alibabacloud_sas20181203.client import Client as Sas20181203Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sas20181203 import models as sas_20181203_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_sas20181203 import models as sas_models


class AliApi:
    def __init__(self, accessKeyId, accessKeySecret, uuid):
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.uuid = uuid

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Sas20181203Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'tds.aliyuncs.com'
        return Sas20181203Client(config)

    @staticmethod
    def create_api_info() -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='ModifyStartVulScan',
            # 接口版本,
            version='2018-12-03',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    """
    auto_breaking：表示自动拦截。
    webshell_cloud_breaking：表示网站后门连接防御。
    alinet：表示恶意网络行为防御。
    alisecguard：表示客户端自保护。
    """

    def operate_suspicious_target_config(
            self,
            type,
            config
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        operate_suspicious_target_config_request = sas_20181203_models.OperateSuspiciousTargetConfigRequest(
            lang='en',
            type=type,
            target_type='uuid',
            target_operations="[{\"targetType\":\"uuid\",\"target\":\"" + self.uuid + "\",\"flag\":\"" + config + "\"}]"
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.operate_suspicious_target_config_with_options(operate_suspicious_target_config_request,
                                                                            runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)

            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    """
    cve：Linux软件漏洞
    sys：Windows系统漏
    cms：Web-CMS漏洞
    emg：应急漏洞
    """

    def modify_vul_target_config_request(
            self,
            type,
            config
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        modify_vul_target_config_request = sas_20181203_models.ModifyVulTargetConfigRequest(
            type=type,
            source_ip='10.10.21.106',
            uuid='inet-ebb4b2df-384f-451d-a0be-9be0512bb8ae',
            config=config
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.modify_vul_target_config_with_options(modify_vul_target_config_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)

            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # """ 扫描
    # cve：Linux软件漏洞
    # sys：Windows系统漏洞
    # cms：Web - CMS漏洞
    # emg：应急漏洞
    # app：应用漏洞
    # """
    # def modify_start_vulscan(
    #         self,
    #         type
    # ) -> None:
    #     # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
    #     client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
    #     params = AliApi.create_api_info()
    #     # query params
    #     queries = {}
    #     queries['Types'] = type
    #     queries['Uuids'] = self.uuid
    #     # runtime options
    #     runtime = util_models.RuntimeOptions()
    #     request = open_api_models.OpenApiRequest(
    #         query=OpenApiUtilClient.query(queries)
    #     )
    #     # 复制代码运行请自行打印 API 的返回值
    #     # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode
    #     response = client.call_api(params, request, runtime)
    #     print(response)

    """
    OVAL_ENTITY：CVE漏洞
    SYSVUL：系统漏洞
    CMS：CMS漏洞
    SCA：应用漏洞
    """

    def vul_scan(
            self,
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        modify_push_all_task_request = sas_20181203_models.ModifyPushAllTaskRequest(
            uuids=self.uuid,
            tasks="OVAL_ENTITY,CMS,SYSVUL,SCA"
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.modify_push_all_task_with_options(modify_push_all_task_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)
            print("已下发漏洞扫描任务：")
            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # 病毒扫描
    def start_virus_scan_task(
            self
    ) -> None:
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        # query_group_request = sas_models.DescribeAllGroupsRequest()
        # query_group_response = client.describe_all_groups(query_group_request)
        # body = query_group_response.body
        # group_info = body.groups[0]
        # group_info_id = group_info.group_id
        # group_info_name = group_info.group_name
        start_virus_scan_task_json = {
            'type': 'uuid',
            'name': 'localhost',
            'target': self.uuid
        }
        start_virus_scan_task_jsons = [
            start_virus_scan_task_json
        ]
        target_info_str = UtilClient.to_jsonstring(start_virus_scan_task_jsons)
        request = sas_models.StartVirusScanTaskRequest(
            target_info=target_info_str
        )
        response = client.start_virus_scan_task(request)
        print("已下发恶意软件扫描任务：")
        print(response.body)

    # 资产采集
    def assets_scan(
            self
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        modify_push_all_task_request = sas_20181203_models.ModifyPushAllTaskRequest(
            uuids=self.uuid,
            tasks="ACCOUNT_SNAPSHOT,PORT_SNAPSHOT,PROC_SNAPSHOT,SCA_SNAPSHOT,SOFTWARE_SNAPSHOT,"
                  "CROND_SNAPSHOT,AUTORUN_SNAPSHOT,LKM_SNAPSHOT,SCA_PROXY_SNAPSHOT"
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.modify_push_all_task_with_options(modify_push_all_task_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)
            print("已下发资产采集任务：")
            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    # 基线扫描（CIS Ubuntu）
    def baseline_scan(
            self
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        exec_strategy_request = sas_20181203_models.ExecStrategyRequest(
            strategy_id=39517894,
            lang='en'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.exec_strategy_with_options(exec_strategy_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)
            print("已下发基线扫描任务：")
            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    def describe_susp_events(
            self
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        describe_susp_events_request = sas_20181203_models.DescribeSuspEventsRequest(
            dealed='N',
            levels="serious,suspicious,remind",
            # parent_event_types='网站后门',
            uuids=self.uuid,
            page_size='100'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.describe_susp_events_with_options(describe_susp_events_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)
            data = json.loads(jsonData)
            return data
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    def handle_security_events(
            self,
            ids
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        handle_security_events_request = sas_20181203_models.HandleSecurityEventsRequest(
            security_event_ids=ids,
            operation_code='ignore'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.handle_security_events_with_options(handle_security_events_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)
            # print(response)
            print(jsonData)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    def get_baseline_scan_items(
            self,
    ) -> None:
        def create_table_and_connect_db(database_name):
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        check_id INTEGER PRIMARY KEY,
                        check_item TEXT,
                        check_type TEXT,
                        description TEXT
                    )
                """)

            conn.commit()
            return conn

        # 将数据插入到数据库
        def insert_data_to_db(conn, check_id, check_item=None, check_type=None, description=None):
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT OR REPLACE INTO items (check_id, check_item, check_type, description) VALUES (?, ?, ?, ?)
                """, (check_id, check_item, check_type, description))
            conn.commit()

        conn = create_table_and_connect_db("ali_cis_baseline_scan_items.db")
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        list_check_item_warning_summary_request = sas_20181203_models.ListCheckItemWarningSummaryRequest(
            risk_type='cis',
            page_size=200
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.list_check_item_warning_summary_with_options(list_check_item_warning_summary_request, runtime)
            jsonObj = json.dumps(response.body.to_map())
            jsonData = json.loads(jsonObj)

            for item in jsonData['List']:
                check_id = item['CheckId']
                check_item = item['CheckItem']
                check_type = item['CheckType']
                description = item['Description']

                # print(f'CheckItem: {check_item}')
                # print(f'CheckType: {check_type}')
                # print(f'Description: {description}')
                # print('---')

                # 删除特殊字符
                check_item = check_item.replace('\r', '').replace('\n', '')
                insert_data_to_db(conn, check_id, check_item, check_type, description)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    def describe_baseline_check_warnings(
        self
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = AliApi.create_client(self.accessKeyId, self.accessKeySecret)
        describe_check_warnings_request = sas_20181203_models.DescribeCheckWarningsRequest(
            uuid='inet-ebb4b2df-384f-451d-a0be-9be0512bb8ae',
            risk_id=62,
            page_size=200
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.describe_check_warnings_with_options(describe_check_warnings_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)




if __name__ == '__main__':
    aliapi = AliApi("LTAI5tKzriqKJux8AWn72mDh", "DQDSg6t6IMih9MnGlykw0SYvGv20h9",
                    "inet-ebb4b2df-384f-451d-a0be-9be0512bb8ae")
    aliapi.baseline_scan()

    # aliapi.operate_suspicious_target_config('auto_breaking', 'del')
    # aliapi.operate_suspicious_target_config('webshell_cloud_breaking', 'del')
    # aliapi.operate_suspicious_target_config('alinet', 'del')
    # aliapi.operate_suspicious_target_config('alisecguard', 'del')
    # aliapi.modify_vul_target_config_request('cve', 'off')
    # aliapi.modify_vul_target_config_request('sys', 'off')
    # aliapi.modify_vul_target_config_request('cms', 'off')
    # aliapi.modify_vul_target_config_request('emg', 'off')
    # aliapi.operate_suspicious_target_config('auto_breaking', 'add')
    # aliapi.operate_suspicious_target_config('webshell_cloud_breaking', 'add')
    # aliapi.operate_suspicious_target_config('alinet', 'add')
    # aliapi.operate_suspicious_target_config('alisecguard', 'add')
    # aliapi.modify_vul_target_config_request('cve', 'on')
    # aliapi.modify_vul_target_config_request('sys', 'on')
    # aliapi.modify_vul_target_config_request('cms', 'on')
    # aliapi.modify_vul_target_config_request('emg', 'on')
