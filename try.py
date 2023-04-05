import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 时间字符串和格式
time_strings = ['09:29:34', '09:29:35', '09:29:36', '09:29:37']
time_format = '%H:%M:%S'

# 转换时间并归零
time_objects = [datetime.strptime(t, time_format) for t in time_strings]
time_zeroed = [(t - time_objects[0]).total_seconds() for t in time_objects]

# CPU 使用率数据
cpu1_usage = [10, 15, 20, 25]
cpu2_usage = [12, 17, 22, 27]
cpu3_usage = [14, 19, 24, 29]
cpu4_usage = [16, 21, 26, 31]

# 绘制折线图
plt.plot(time_zeroed, cpu1_usage, label='CPU1')
plt.plot(time_zeroed, cpu2_usage, label='CPU2')
plt.plot(time_zeroed, cpu3_usage, label='CPU3')
plt.plot(time_zeroed, cpu4_usage, label='CPU4')

plt.xlabel('Time (seconds)')
plt.ylabel('CPU Usage')
plt.title('CPU Usage vs Time')
plt.legend()

plt.show()
