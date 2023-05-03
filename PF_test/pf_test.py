import yaml as yaml

from tencent_pf_test.tencent_pf_test import TencentPFTest
from ali_pf_test.ali_pf_test import AliPFTest
from yunsuo_pf_test.yunsuo_pf_test import YunSuoPFTest

if __name__ == '__main__':
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)
    target_agent = config['pfinfo']['target_agent']
    function_id = config['pfinfo']['function_id']
    functions = ["pf_test_nothing", "pf_test_vul", "pf_test_assets", "pf_test_virus", "pf_test_baseline",
                 "pf_test_all_funcs"]

    if target_agent == 0:  # 腾讯云
        agent = config["pfinfo"]["tencent_agent"]
        ssh_hostname = str(agent["ssh_hostname"])
        ssh_username = str(agent["ssh_username"])
        ssh_password = str(agent["ssh_password"])
        accessKeyId = str(agent["accessKeyId"])
        accessKeySecret = str(agent["accessKeySecret"])
        uuid = str(agent["uuid"])
        tencent = TencentPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
        getattr(tencent, "tencent_" + functions[function_id])()

    elif target_agent == 1:  # 阿里云
        agent = config["pfinfo"]["aliyun_agent"]
        ssh_hostname = str(agent["ssh_hostname"])
        ssh_username = str(agent["ssh_username"])
        ssh_password = str(agent["ssh_password"])
        accessKeyId = str(agent["accessKeyId"])
        accessKeySecret = str(agent["accessKeySecret"])
        uuid = str(agent["uuid"])
        ali = AliPFTest(ssh_hostname, ssh_username, ssh_password, accessKeyId, accessKeySecret, uuid)
        getattr(ali, "ali_" + functions[function_id])()

    elif target_agent == 2:  # 奇安信
        agent = config["pfinfo"]["yunsuo_agent"]
        ssh_hostname = str(agent["ssh_hostname"])
        ssh_username = str(agent["ssh_username"])
        ssh_password = str(agent["ssh_password"])
        manage_center_ip = str(agent["manage_center_ip"])
        token = str(agent["token"])
        uuid = str(agent["uuid"])
        yunsuo = YunSuoPFTest(ssh_hostname, ssh_username, ssh_password, uuid, manage_center_ip, token)
        getattr(yunsuo, "yunsuo_" + functions[function_id])()

    elif target_agent == 3:  # 华为hisec
        pass
