import numpy as np
import matplotlib.pyplot as plt
x=range(180)
y=[]
z=[]
kopt=(0.33/0.07)**0.5
for i in x:
    g=np.sin((i+1)/2/180*np.pi)
    g=g*40*kopt/100
    y.append(np.arcsin(g)*2/np.pi*180)
for i in x:
    g=np.sin((i+1)/2/180*np.pi)
    g=g*40*kopt/100
    z.append(np.arcsin(g)*2/np.pi*180*1.5)
print(x)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 用来正常显示中文标签 微软雅黑-Microsoft YaHei,黑体-SimHei,仿宋-FangSong
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
p=[]
p2=[]
for i in range(180):
    p.append(0.45*0.9*20*100*np.sin((x[i]+1)/2/180*np.pi)*np.sin(y[i]/2/180*np.pi)*228.549/0.45/0.9/20/100)
    p2.append(0.45*0.9*20*100*np.sin((x[i]+1)/2/180*np.pi)*np.sin(z[i]/2/180*np.pi)*228.549/0.45/0.9/20/100)
print(y)
plt.title("偏移条件下的传输功率")
plt.plot(x,y,label='原边脉宽角')
#plt.plot(x,z,label='改进后原边脉宽角')
plt.plot(x,p,label='最大传输功率')
plt.xlabel('beta/°')
#plt.plot(x,p2,label='改进后最大传输功率')
plt.legend()
plt.show()