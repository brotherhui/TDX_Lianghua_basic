import pandas as pd  
  
# 假设您的股票日线数据存储在CSV文件中，并且包含'Date', 'J', 'K', 'D'等列  
# 读取CSV文件到DataFrame中  
df = pd.read_csv('d:\\quantization_data\\sh\\sh000001.month.full.csv')  
df['Date'] = pd.to_datetime(df['Date'])  # 确保日期列被正确解析为日期时间对象  
df.set_index('Date', inplace=True)  # 设置日期为索引  
  
# 初始化空列表来存储结果  
golden_cross_dates = []  
j_peaks_dates = []  
dead_cross_dates = []  
  
# 定义一个函数来查找J的最高点  
def find_j_peak(data, start_idx):  
    j_peak_date = None  
    j_peak_value = -1  
    in_range = False  
    for i in range(start_idx, len(data)):  
        if data['J'].iloc[i] > 100 and data['D'].iloc[i] > 65:  
            in_range = True  
            if data['J'].iloc[i] > j_peak_value:  
                j_peak_value = data['J'].iloc[i]  
                j_peak_date = data.index[i] 
                j_peak_price =  data["Close"][i] 
        elif in_range and (data['J'].iloc[i] <= 100 or data['D'].iloc[i] <= 65):  
            break  
    return j_peak_date
  
# 遍历数据来查找金叉和后续的J最高点及死叉  
i = 0  
while i < len(df) - 1:  
    if df['J'].iloc[i] < 0 and df['D'].iloc[i] < 20:  
        # 查找金叉  
        j = i + 1  
        while j < len(df) - 1 and not (df['K'].iloc[j] > df['D'].iloc[j] and df['K'].iloc[j-1] <= df['D'].iloc[j-1]):  
            j += 1  
        if j < len(df) - 1:  # 确保金叉发生在数据范围内  
            golden_cross_date = df.index[j]  
            golden_price = df["Close"][j]
            golden_cross_dates.append((golden_cross_date, golden_price))
              
            # 查找金叉后的J最高点  
            j_peak_date = find_j_peak(df, j)  
            if j_peak_date is not None:  
                j_peaks_dates.append((golden_cross_date, golden_price, j_peak_date))  
                  
                # 查找从J最高点向下的死叉  
                k = df.index.get_loc(j_peak_date) + 1  
                while k < len(df) - 1 and not (df['K'].iloc[k] < df['D'].iloc[k] and df['K'].iloc[k-1] >= df['D'].iloc[k-1]):  
                    k += 1  
                if k < len(df) - 1:  # 确保死叉发生在数据范围内  
                    dead_cross_date = df.index[k]
                    dead_price = df["Close"][k]
                    dead_cross_dates.append((golden_cross_date,golden_price, j_peak_date, dead_cross_date, dead_price))  
                      
                # 将索引移动到死叉之后，继续查找下一个金叉  
                i = k  
            else:  
                # 如果没有找到J最高点，则移动到数据末尾或下一个可能的金叉点之前的位置  
                i = j + 1 if j + 1 < len(df) else len(df) - 1  
        else:  
            # 如果金叉发生在数据末尾，则结束循环  
            break  
    else:  
        # 如果当前点不满足J<0和D<20的条件，则移动到下一个点  
        i += 1  
  
# 输出结果  
print("金叉日期:", [(gc.strftime('%Y-%m-%d'), gp) for gc, gp in golden_cross_dates])  
print("金叉到J最高点日期:", [(gc.strftime('%Y-%m-%d'),gp, jp.strftime('%Y-%m-%d')) for gc,gp, jp in j_peaks_dates])  
print("盈利周期:", [(gc.strftime('%Y-%m-%d'),gp, jp.strftime('%Y-%m-%d'), dc.strftime('%Y-%m-%d'), dp) for gc,gp, jp, dc, dp in dead_cross_dates])