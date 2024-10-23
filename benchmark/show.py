import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rc("font",family='MicroSoft YaHei',weight="bold")
harmonyTest=pd.read_csv('Protocol_harmony_c.csv')["cost time"]
kelapaTest=pd.read_csv('Protocol_kelapa_c.csv')["cost time"]

data=[kelapaTest*1000,harmonyTest*1000]



fig, ax = plt.subplots()
box = ax.boxplot(data, patch_artist=True, notch=True, vert=True, showmeans=True)
for i in range(len(data)):
    # 获取中位数的位置
    median = box['medians'][i].get_ydata()[1]
    
    # 在箱型图上添加中位数的数值标签
    ax.text(i+0.8, median, f'{median:.4f}', color='black', ha='center')

for i in range(len(data)):
    # 获取箱型图中的各个部分
    box['boxes'][i].set_facecolor('lightblue')
    box['whiskers'][i*2].set_color('blue')
    box['whiskers'][i*2+1].set_color('blue')
    box['fliers'][i].set_markerfacecolor('red')
    #box['fliers'][i].set_markeredgecolor('red')
    box['means'][i].set_color('black')
    

ax.set_xticklabels(['kelapa(on x86 pc)', 'harmony(on x86 pc)'])
ax.set_title('不同协议时间开销箱型图')
ax.set_xlabel('测试协议名称')
ax.set_ylabel('时间开销(s)')
ax.legend()


fig,bx=plt.subplots()
bx.plot([i for i in range(len(data[0]))],data[0], label='Kelapa', color='blue')
bx.plot([i for i in range(len(data[1]))],data[1], label='Harmony', color='red')
bx.set_title('不同协议时间开销折线图')
bx.set_xlabel('测试序号')
bx.set_ylabel('时间开销(s)')
bx.legend()


plt.show()


# plt.plot([i for i in range(len(harmonyTest))],harmonyTest, label='Harmony', color='red')
# avg_val=np.mean(harmonyTest)
# plt.axhline(avg_val,color='red')


# plt.plot([i for i in range(len(kelapaTest))],kelapaTest, label='Kelapa', color='blue')
# avg_val=np.mean(kelapaTest)
# plt.axhline(avg_val,color='blue')


