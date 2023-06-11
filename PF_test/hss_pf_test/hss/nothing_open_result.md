### 无功能开启性能数据：

在仅开启 nothing_open 功能的情况下，各进程组件性能测试结果如下（测试时间300s）：

| 进程名 | vcpu平均占用率 | RSS平均大小 | 读数据平均速率 | 写数据平均速率 | IOPS平均值 | network_io平均值 
| --- | --- | --- | --- | --- | --- | --- |
| hostwatch | 0.03% | 0.00MB | 0.00KB/s | 0.03KB/s | 0.03 | 0.10 
| hostguard | 1.70% | 0.07MB | 4.66KB/s | 0.27KB/s | 0.33 | 2.40 
| python | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 1.73% | 0.07MB | 4.66KB/s | 0.29KB/s | 0.37 | 2.50 

| 进程名 | vcpu最高占用率 | RSS最大值 | 读数据最高速率 | 写数据最高速率 | IOPS最大值 | network_io最大值 
| --- | --- | --- | --- | --- | --- | --- |
| hostwatch | 0.67% | 0.01MB | 0.00KB/s | 2.67KB/s | 1.00 | 3.00 
| hostguard | 4.67% | 0.07MB | 466.23KB/s | 4.00KB/s | 1.00 | 37.00 
| python | 0.00% | 0.00MB | 0.00KB/s | 0.00KB/s | 0.00 | 0.00 
| 全部进程 | 4.67% | 0.08MB | 466.23KB/s | 4.00KB/s | 1.00 | 37.00 
### 无功能开启性能数据图：

![fig](E:\Project\Python_project\graduation_project\PF_test\hss_pf_test\hss\nothing_open.png)
