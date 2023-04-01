# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List
import json
import numpy as np

from alibabacloud_sas20181203.client import Client as Sas20181203Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sas20181203 import models as sas_20181203_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

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
    def main(
            accessKeyId, accessKeySecret
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client(accessKeyId, accessKeySecret)
        describe_secure_suggestion_request = sas_20181203_models.DescribeSecureSuggestionRequest()
        describe_susp_events_request = sas_20181203_models.DescribeSuspEventsRequest(source_ip='10.10.21.140')
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = client.describe_susp_events_with_options(describe_susp_events_request, runtime)
            jsonData = json.dumps(response.body.to_map(), ensure_ascii=False, indent=4)

            print(jsonData)
            # print(client.describe_secure_suggestion_with_options(describe_secure_suggestion_request, runtime))
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error)

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        # 工程代码泄露可能会导致AccessKey泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('accessKeyId', 'accessKeySecret')
        describe_secure_suggestion_request = sas_20181203_models.DescribeSecureSuggestionRequest()
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.describe_secure_suggestion_with_options_async(describe_secure_suggestion_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(accessKeyId="LTAI5tBs4GxSpDBsx6ZzSiY8", accessKeySecret="xgdTMmZHG4jOTa2Mt7P9jxsH6Kd0in")
