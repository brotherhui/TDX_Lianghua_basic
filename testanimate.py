import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib.animation as animation  
  
# 假设您有一个包含日线数据的CSV文件，名为"daily_data.csv"  
# 文件包含'Open', 'High', 'Low', 'Close'列  
  
# 读取日线数据  
data = pd.read_csv('d:\\quantization_data\\sh\\lday\\sh000001.day.csv', index_col=0)  
  
# 计算MACD指标  
data['MACD'] = data['Close'].ewm(span=12, min_periods=12).mean() - data['Close'].ewm(span=26, min_periods=26).mean()  
data['Signal'] = data['MACD'].ewm(span=9, min_periods=9).mean()  
data['MACD_Hist'] = data['MACD'] - data['Signal']  
  
# 创建动态图表  
fig, ax = plt.subplots()  
line, = ax.plot([], [], 'k', animated=True)  
  
# 更新图表函数  
def update(i):  
    line.set_data(data[data.index <= i]['MACD_Hist'].values, data[data.index <= i]['MACD'].values)  
    return line,  
  
# 动态绘制图表  
ani = animation.FuncAnimation(fig, update, frames=range(len(data)), interval=500)  
plt.show()