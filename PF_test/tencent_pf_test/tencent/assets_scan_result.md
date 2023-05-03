### 资产扫描性能数据：

在仅开启 assets_scan 功能的情况下，各进程组件性能测试结果如下（测试时间229s）：

| 进程名 | vcpu平均占用率 | 驻留物理内存平均大小（RSS） | 读数据平均速率 | 写数据平均速率 
| --- | --- | --- | --- | --- |
| YDService | 2.57% | 68.12MB | 9.21KB/s | 26.55KB/s 
| YDLive | 0.05% | 0.67MB | 0.00KB/s | 0.00KB/s 
| YDFlame | 5.65% | 11.33MB | 9.21KB/s | 23.67KB/s 
| 全部进程 | 8.26% | 80.12MB | 18.41KB/s | 50.22KB/s 
### 资产扫描性能数据图：

![vul_scan_fig](E:\Project\Python_project\graduation_project\PF_test\tencent_pf_test\tencent\assets_scan.png)
### 资产扫描结果：

共扫描到992项资产，资产分类情况为：

system: 1

account: 34

port: 8

app: 6

process: 36

database: 0

webapp: 0

webservice: 0

webframe: 0

weblocation: 0

jar: 0

initservice: 36

plantask: 11

env: 34

coremodule: 81

package: 745

