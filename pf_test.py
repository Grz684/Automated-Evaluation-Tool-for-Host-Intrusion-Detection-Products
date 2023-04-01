import configparser
from tencent_pf_test.tencent_pf_test import TencentPFTest
from ali_pf_test.ali_pf_test import AliPFTest
from yunsuo_pf_test.yunsuo_pf_test import YunSuoPFTest

if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read("config.conf", encoding='utf-8')
    target_agent = cf['pfinfo']['target_agent']
    ssh_hostname = cf['pfinfo']['ssh_hostname']
    ssh_username = cf['pfinfo']['ssh_username']
    ssh_password = cf['pfinfo']['ssh_password']
    accessKeyId = cf['pfinfo']['accessKeyId']
    accessKeySecret = cf['pfinfo']['accessKeySecret']
    uuid = cf['pfinfo']['uuid']
    function_id = cf['pfinfo']['function_id']
    functions = ["pf_test_nothing", "pf_test_vul", "pf_test_assets", "pf_test_virus", "pf_test_baseline",
                 "pf_test_all_funcs"]

    if target_agent == '0':  # 腾讯云
        tencent = TencentPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
        getattr(tencent, "tencent_" + functions[int(function_id)])()

    elif target_agent == '1':  # 阿里云
        ali = AliPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
        getattr(ali, "ali_" + functions[int(function_id)])()

    elif target_agent == '2':  # 奇安信
        yunsuo = YunSuoPFTest(ssh_hostname, ssh_username, ssh_password)
        getattr(yunsuo, "yunsuo_" + functions[int(function_id)])()

    elif target_agent == '3':  # 华为hisec
        pass
