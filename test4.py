import pandas as pd  


# D<20, J<0 金叉买入
# 如果没涨过J>100, J<0时金叉补 100只
# 一直到J>100以后， 出一半， 再等到死叉后全部卖出

# 假设数据文件名为'stock_kdj_data.csv'，并且包含'Date', 'Close', 'K', 'D', 'J'等列  
def read_kdj_data(filename):  
    return pd.read_csv(filename, parse_dates=['Date'], index_col='Date')  
  
def find_previous_j_below_0(kdj_data, start_idx):  
    """  
    从start_idx开始向前查找是否存在J<0的情况  
    """  
    for i in range(start_idx - 1, -1, -1):  
        if kdj_data.iloc[i]['J'] < 0:  
            return True  
    return False  
  
def find_previous_d_below_20(kdj_data, start_idx):  
    """  
    从start_idx开始向前查找是否存在D<20的情况  
    """  
    for i in range(start_idx - 1, -1, -1):  
        if kdj_data.iloc[i]['D'] < 20:  
            return True  
    return False  
  
def find_next_golden_cross(kdj_data, start_idx):  
    """  
    从start_idx开始向后查找下一个满足条件的金叉（K线上穿D线，且金叉之前有J<0和D<20）  
    """  
    for i in range(start_idx, len(kdj_data) - 1):  
        if kdj_data.iloc[i]['K'] > kdj_data.iloc[i]['D'] and kdj_data.iloc[i-1]['K'] <= kdj_data.iloc[i-1]['D']:  
            if find_previous_j_below_0(kdj_data, i) and find_previous_d_below_20(kdj_data, i):  
                return i  
    return None  
  
def find_next_j_above_100(kdj_data, start_idx):  
    """  
    从start_idx开始向后查找下一个J值大于100的位置，并返回该位置的时间和收盘价  
    """  
    for i in range(start_idx, len(kdj_data)):  
        if kdj_data.iloc[i]['J'] > 100:  
            return kdj_data.index[i], kdj_data.iloc[i]['Close']  # 返回时间和收盘价  
    return None, None  # 如果没有找到，返回None  
  
def find_next_dead_cross(kdj_data, j_above_100_time, start_idx):  
    """  
    从start_idx开始向后查找下一个死叉（K线下穿D线），确保死叉之前有J>100的情况  
    """  
    for i in range(start_idx, len(kdj_data) - 1):  
        if kdj_data.iloc[i]['K'] < kdj_data.iloc[i]['D'] and kdj_data.iloc[i-1]['K'] >= kdj_data.iloc[i-1]['D']:  
            # 检查死叉之前是否有J>100的情况  
            if j_above_100_time is not None and j_above_100_time < kdj_data.index[i]:  
                return i  # 如果有，返回死叉索引  
    return None  # 如果没有找到死叉或不满足条件，返回None  
  

def find_signals(kdj_data):  
    """  
    查找整个数据集中的金叉和死叉信号，并记录每次事件时的收盘价和日期  
    确保金叉之前有J<0和D<20的条件（不必同时），死叉之前有J>100的条件  
    """  
    golden_crosses = []  # 存储金叉信号  
    dead_crosses = []    # 存储死叉信号
    details = []
    start_idx = 0        # 搜索的起始索引  
    # 盈利周期， 尚未盈利， 总收益， 详细情况
    margin = 1
    while start_idx < len(kdj_data) - 1:  # 确保至少有两个数据点来判断交叉  
        # 查找满足条件的金叉  
        gc_idx = find_next_golden_cross(kdj_data, start_idx)  
        if gc_idx is not None:  
            golden_cross_time = kdj_data.index[gc_idx]  # 金叉时间  
            golden_cross_close = kdj_data.iloc[gc_idx]['Close']  # 金叉收盘价  
            golden_crosses.append((golden_cross_time, golden_cross_close))  
            temp = " 金叉:"+ golden_cross_time.strftime('%Y-%m-%d') + " 收盘价：" + str(golden_cross_close) 

            #从金叉位置开始， 一天天的查看数据， 判断是否满足补仓或者死叉的条件



            # 从金叉位置开始查找J>100的情况  
            j_above_100_time, j_above_100_close = find_next_j_above_100(kdj_data, gc_idx + 1)  
            # 否则如果找到了J>100的情况，查找死叉
            if j_above_100_time is not None:  
                temp += " 高位:"+ j_above_100_time.strftime('%Y-%m-%d') + " 收盘价：" + str(j_above_100_close)
                dc_idx = find_next_dead_cross(kdj_data, j_above_100_time, start_idx if gc_idx == start_idx else gc_idx)  
                if dc_idx is not None:  
                    dead_cross_time = kdj_data.index[dc_idx]  # 死叉时间  
                    dead_cross_close = kdj_data.iloc[dc_idx]['Close']  # 死叉收盘价  
                    dead_crosses.append((dead_cross_time, dead_cross_close))  
                    temp += " 死叉:"+ dead_cross_time.strftime('%Y-%m-%d') + " 收盘价：" + str(dead_cross_close)
                    details.append(temp)
                    margin = margin * round((dead_cross_close * 0.5 + j_above_100_close * 0.5 )/golden_cross_close,1)
                    start_idx = dc_idx  # 更新查找起点为死叉位置  
                    continue  # 继续下一次循环，查找下一个金叉信号  

            # 如果没有找到死叉或J>100的情况，将起点设置为数据末尾以结束循环（或更新为下一个可能的起点）  
            start_idx = len(kdj_data) - 1 if gc_idx == start_idx else gc_idx  
            break  # 如果没有找到符合条件的死叉，结束当前金叉后的搜索  
          
        # 如果没有找到金叉或已经处理过最后一个金叉，结束循环  
        start_idx = len(kdj_data) - 1  
        break  # 结束整个搜索过程，因为没有更多的金叉可以查找了  
      
    return golden_crosses, dead_crosses, details, margin  # 返回找到的所有金叉和死叉信号及其对应的收盘价和日期信息  
  
# 使用示例：读取数据并查找信号（请确保数据文件路径和名称正确）  
kdj_data = read_kdj_data('d:\\quantization_data\\sh\\sh600559.month.full.csv')  # 读取数据（请确保文件路径正确）  
golden_crosses, dead_crosses,details, margin  = find_signals(kdj_data)  # 查找金叉和死叉信号并记录时间和收盘价信息（已包含J>100的条件检查）  
# 打印结果到控制台或进行其他处理（如保存到文件等）...
print( details, "总收益 ",margin)

kdj_data = read_kdj_data('d:\\quantization_data\\sh\\sh605117.month.full.csv')  # 读取数据（请确保文件路径正确）  
golden_crosses, dead_crosses,details, margin  = find_signals(kdj_data)  # 查找金叉和死叉信号并记录时间和收盘价信息（已包含J>100的条件检查）  
# 打印结果到控制台或进行其他处理（如保存到文件等）...
print( details, "总收益 ",margin) 


kdj_data = read_kdj_data('d:\\quantization_data\\sh\\sh601888.month.full.csv')  # 读取数据（请确保文件路径正确）  
golden_crosses, dead_crosses,details, margin  = find_signals(kdj_data)  # 查找金叉和死叉信号并记录时间和收盘价信息（已包含J>100的条件检查）  
# 打印结果到控制台或进行其他处理（如保存到文件等）...
print( details, "总收益 ",margin) 