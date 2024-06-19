import talib  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
  
# 导入股票数据   
data = pd.read_csv('d:\\quantization_data\\sh\\lday\\sh000001.day.csv')  
  
  # 提取特定日期范围内的数据  
date_range = pd.date_range(start='2023-12-01', end='2024-01-31')

# 截取"Date"列中的特定时间段数据  
data = data.loc[pd.to_datetime(data["Date"]).isin(date_range)]  
  
# 显示截取后的数据  
print(data)

# 计算MACD指标  
# 计算 MACD  
data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()  
data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()  
data['MACD'] = data['EMA_12'] - data['EMA_26']  
data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()  
data['MACD_Hist'] = data['MACD'] - data['Signal']  
  
# 绘制 MACD 图表  
plt.figure(figsize=(10, 6))  
plt.plot(data['Date'], data['MACD'], label='MACD', linestyle='-')  
plt.plot(data['Date'], data['Signal'], label='Signal Line', linestyle='--')  
plt.bar(data['Date'], data['MACD_Hist'], label='MACD Hist', color='gray')  
plt.title('MACD Chart')  
plt.xlabel('Date')  
plt.ylabel('MACD / Signal Line / MACD Histogram')  
plt.legend(loc='upper left')  
plt.show()