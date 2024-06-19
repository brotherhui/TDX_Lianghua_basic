import talib  
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
import calendar  
from datetime import datetime  
  
# 导入股票数据   
data = pd.read_csv('d:\\quantization_data\\sh\\lday\\sh000001.day.csv')  
  
# 计算月末日期  
# def get_last_day_of_month(date):  
#     return date.replace(day=28) + pd.DateOffset(months=1) - pd.DateOffset(days=1)  
  
def get_last_day_of_month(date_str): 
        # 将字符串转换为datetime对象  
    date_object = datetime.strptime(date_str, "%Y-%m-%d")  
  
    # 提取年和月  
    year = date_object.year  
    month = date_object.month   

    # 判断是否为闰年  
    is_leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)  
    # 获取该月份的天数  
    days_in_month = calendar.monthrange(year, month)[1]  
    return datetime(year, month, days_in_month).date()  


# 初始化月线数据框架  
monthly_data = pd.DataFrame(columns=['Date', 'Close'])  
  
# 遍历日线数据，提取月线数据  
for index, row in data.iterrows():  
    current_date = row['Date']  
    current_close = row['Close']  
    last_day_of_month = get_last_day_of_month(current_date)  
      
    # 检查是否已经处理过该月的月线数据  
    if not monthly_data[(monthly_data['Date'] == last_day_of_month)].empty:  
        continue  
      
    # 添加月线数据到DataFrame中  
    monthly_data = monthly_data._append({'Date': last_day_of_month, 'Close': current_close}, ignore_index=True)  

print(monthly_data)
      
# 计算MACD指标（以EMA为例）  
monthly_data['EMA_12'] = monthly_data['Close'].ewm(span=12, adjust=False).mean()  
monthly_data['EMA_26'] = monthly_data['Close'].ewm(span=26, adjust=False).mean()  
monthly_data['MACD'] = monthly_data['EMA_12'] - monthly_data['EMA_26']  
monthly_data['Signal'] = monthly_data['MACD'].ewm(span=9, adjust=False).mean()  
monthly_data['MACD_Hist'] = monthly_data['MACD'] - monthly_data['Signal']  
print(monthly_data)
  
# 绘制MACD图表  
plt.figure(figsize=(10, 6))  
plt.plot(monthly_data['Date'], monthly_data['MACD'], label='MACD', linestyle='-')  
plt.plot(monthly_data['Date'], monthly_data['Signal'], label='Signal Line', linestyle='--')  
plt.bar(monthly_data['Date'], monthly_data['MACD_Hist'], label='MACD Hist', color='gray')  
plt.title('Monthly MACD Chart')  
plt.xlabel('Date')  
plt.ylabel('MACD / Signal Line / MACD Histogram')  
plt.legend(loc='upper left')  
plt.show()