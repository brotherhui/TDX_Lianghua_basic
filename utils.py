import os
import calendar  
from datetime import datetime 
import numpy as np  
import pandas as pd  
import talib

class MyUtils:  

    SH_PATH="sh"
    SZ_PATH="sz"
    DAY_PATH = "lday"
    TDX_PATH="d:\\new_tdx\\vipdoc"
    OUTPUT_PATH="d:\\quantization_data"
    SLASH = "\\"
    DAILY_FILEPOSTFIX = ".day"
    DAILY_CSV_FILEPOSTFIX = ".day.csv"
    DAILY_FULL_FILEPOSTFIX = ".day.full.csv"
    MONTHLY_CSV_FILEPOSTFIX = ".month.csv"
    MONTHLY_FULL_FILEPOSTFIX = ".month.full.csv"


    SH_PARAM = "SH"
    SZ_PARAM = "SZ"
    DAY_PARAM = "DAY"
    
    # 获取股票市场的文件路径
    @staticmethod  
    def get_source_path(market, type):
        if market == MyUtils.SH_PARAM:
            path = MyUtils.TDX_PATH + MyUtils.SLASH + MyUtils.SH_PATH
        if market == MyUtils.SZ_PARAM:
            path = MyUtils.TDX_PATH + MyUtils.SLASH + MyUtils.SZ_PATH  
        if type == MyUtils.DAY_PARAM:
            path += MyUtils.SLASH + MyUtils.DAY_PATH + MyUtils.SLASH
        return path

    # 获取输出文件路径
    @staticmethod  
    def get_target_path(market):
        if market == MyUtils.SH_PARAM:
            path = MyUtils.OUTPUT_PATH + MyUtils.SLASH + MyUtils.SH_PATH + MyUtils.SLASH
        if market == MyUtils.SZ_PARAM:
            path = MyUtils.OUTPUT_PATH + MyUtils.SLASH + MyUtils.SZ_PATH + MyUtils.SLASH

        if not os.path.exists(path):  
            os.makedirs(path)
        return path

    # 获取股票数据文件名列表
    @staticmethod
    def get_source_list(market, type):
        listFile=[]
        listFile = os.listdir(MyUtils.get_source_path(market, type))
        return listFile

    #获得股票代码
    @staticmethod
    def parse_stocknum(filename):  
        # 使用split()方法按点分割文件名，最多分割一次  
        parts = filename.split('.', 1)  
        # 返回第一个部分，即第一个点之前的所有内容  
        return parts[0]  

    # 获取目标文件名称
    @staticmethod
    def get_filename(stockNumber, type):
        return stockNumber + type

    # 将所有的股票日数据文件分成多个组
    @staticmethod
    def split_list(lst, num_parts):  
        # 计算每份的长度  
        part_length = len(lst) // num_parts  
        # 创建子列表  
        sub_lists = [lst[i*part_length:(i+1)*part_length] for i in range(num_parts)]  
        # 处理剩余的元素  
        remaining = len(lst) % num_parts  
        for i in range(remaining):  
            sub_lists[i].append(lst[part_length * num_parts + i])  
        return sub_lists  
    

    # 计算月末日期  
    # def get_last_day_of_month(date):  
    #     return date.replace(day=28) + pd.DateOffset(months=1) - pd.DateOffset(days=1)  
    @staticmethod
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
    

    @staticmethod
    def calculate_macd(data, n=9, m1=3, m2=3): 
        # 计算MACD指标
        # 计算12日EMA和26日EMA  
        data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()  
        data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean() 
        # 计算DIF（离差值）  
        data['DIF'] = data['EMA12'] - data['EMA26']  
        # 计算DEA（MACD线，即DIF的9日EMA）  
        data['DEA'] = data['DIF'].ewm(span=9, adjust=False).mean()  
        # 计算MACD柱状图  
        data['MACD'] = data['DIF'] - data['DEA']  #？？？？？这个跟通达信的数据有点奇怪， 差了一倍
    

    # @staticmethod
    # def calculate_kdj(data, n=9, m1=3, m2=3):  
    #     """  
    #     计算KDJ指标  
    #     :param data: 包含'High', 'Low', 'Close'列的pandas DataFrame  
    #     :param n: 计算RSV的周期  
    #     :param m1: K值的平滑周期  
    #     :param m2: D值的平滑周期  
    #     :return: 包含'K', 'D', 'J'的DataFrame  
    #     """  
    #     # 确保数据按日期排序  
    #     low_list=data['Low'].rolling(window=n).min()
    #     low_list.fillna(value=data['Low'].expanding().min(), inplace=True)
    #     high_list = data['High'].rolling(window=n).max()
    #     high_list.fillna(value=data['High'].expanding().max(), inplace=True)

    #     rsv = (data['Close'] - low_list) / (high_list - low_list) * 100
    #     data['K'] = rsv.ewm(com=2).mean()
    #     data['D'] = data['K'].ewm(com=2).mean()
    #     data['J'] = 3 * data['K'] - 2 * data['D']

    # 不准。。。。
    # @staticmethod 
    # def calculate_kdj(df, n=9, m1=3, m2=3):  
    #     # 计算KDJ   
    #     df['K'], df['D'] = talib.STOCH(df['High'].values,
    #                             df['Low'].values,
    #                             df['Close'].values,
    #                             fastk_period=9,
    #                             slowk_period=3,
    #                             slowk_matype=0,
    #                             slowd_period=3,
    #                             slowd_matype=0)
    #     # 处理停盘数据（示例：使用前一天的收盘价作为停盘日的价格）  
    #     df.loc[df['Close'].isnull(), 'Close'] = df['Close'].shift(1)  
        
    #     # 重新计算KDJ  
    #     df['K'], df['D'] = talib.STOCH(df['High'].values,
    #                             df['Low'].values,
    #                             df['Close'].values,
    #                             fastk_period=9,
    #                             slowk_period=3,
    #                             slowk_matype=0,
    #                             slowd_period=3,
    #                             slowd_matype=0)
    #     df['J'] = list(map(lambda x,y: 3*x-2*y,df['K'], df['D']))


    @staticmethod
    def calculate_kdj(data, n=9, m1=3, m2=3):  
        """  
        计算KDJ指标  
        :param data: 包含'High', 'Low', 'Close'列的pandas DataFrame  
        :param n: 计算RSV的周期  
        :param m1: K值的平滑周期  
        :param m2: D值的平滑周期  
        :return: 包含'K', 'D', 'J'的DataFrame  
        """  
        # 确保数据按日期排序  
        # data = data.sort_index()  
    
        # # 处理停盘数据（示例：使用前一天的收盘价作为停盘日的价格）  
        # # 没有用。。。。
        data.loc[data['Close'].isnull(), 'Close'] = data['Close'].shift(1) 


        # 计算周期内的最低价和最高价  
        data['Low_n']= data['Low'].rolling(window=n, min_periods=1, center=False).min()  
        data['High_n']= data['High'].rolling(window=n, min_periods=1, center=False).max()  
    
        # # 计算RSV（未成熟随机值）  
        data['RSV'] = (data['Close'] - data['Low_n']) / (data['High_n'] - data['Low_n']) * 100  
        data['RSV'] = data['RSV'].fillna(0)  # 处理NaN值  

        # 计算K值  
        k_values = pd.Series(index=data.index)  
        k_values[:n] = 50  # 初始化K值，这里设为50  
        k_values[n:] = data['RSV'][n:].ewm(com=m1-1, adjust=False).mean()  # 使用指数加权移动平均计算K值  
        data['K'] = k_values
        # 计算D值  
        d_values = pd.Series(index=data.index)  
        d_values[:n] = 50  # 初始化D值，这里设为50  
        d_values[n:] = k_values[n:].ewm(com=m2-1, adjust=False).mean()  # 使用K值的指数加权移动平均计算D值  
        data['D'] = d_values
        # 计算J值  
        j_values = 3 * k_values - 2 * d_values  
        data['J'] = j_values
        

    #尝试分开计算KDJ, 如果volume为0的部分， 跳过去
    @staticmethod
    def calculate_kdj_with_zero_volume(df,  n=9, m1=3, m2=3):  
        split_dfs = []  
        
        # 使用布尔索引来找到volume为0的所有行，并将它们添加到列表中  
        # 注意：由于可能存在多个连续的0，我们需要使用cumsum来创建分组标签  
        df['group'] = (df['Volume'] == 0).cumsum()  
   
        # 遍历每个组，并创建对应的DataFrame  
        for group in df['group'].unique():  
            if group == 0:  # 忽略初始的group 0，因为它不包含任何行  
                continue  
            group_df = df[df['group'] == group]  
            if group_df.shape[0] > 9:
                MyUtils.calculate_kdj(group_df,  n=9, m1=3, m2=3)
                split_dfs.append(group_df)  
        
        # # 删除添加的临时'group'列  
        # for df_group in split_dfs:  
        #     df_group.drop(columns=['group'], inplace=True)  
        
        # 现在split_dfs包含了所有按volume为0切分的DataFrame组  
        for i, df_group in enumerate(split_dfs):  
            print(f"DataFrame for group {i + 1}:")  
            print(df_group)  
            print()  # 打印一个空行以便于区分不同的组
        
        # 将分组后的DataFrame按顺序组合成同一个DataFrame  
        # combined_df = pd.concat(split_dfs, ignore_index=True)   
        # df = combined_df
  
        
    @staticmethod
    def day2month(data):
        # 将日线数据转换为月线数据  
        # 我们可以选择每月的最后一个交易日的数据，或者使用每月的开盘价、收盘价、最高价和最低价的统计值  
        # 初始化月线数据框架  
        monthly_data = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])  
        monthly_data['Date'] = monthly_data.index
        monthly_data = data.resample('ME').agg({  
            'Open': 'first',  # 每月的第一个交易日的开盘价  
            'High': 'max',    # 每月的最高价  
            'Low': 'min',     # 每月的最低价  
            'Close': 'last',   # 每月的最后一个交易日的收盘价  
            'Volume': 'sum'  # 每月的总成交量
        }) 
        # # # 排除数据以后， KDJ就不准了。。。。
        # # 排除没有数据的月份（即删除含有NaN值的行）  
        # monthly_data = monthly_data.dropna(how='all')  # 删除所有列都是NaN的行 

        # # 排除'Volume'为0的行  
        # monthly_data = monthly_data[monthly_data['Volume'].ne(0)]  

        return monthly_data
  
    @staticmethod
    def find_golden_cross(data):   
        
        # 初始化变量和结果列表  
        golden_cross_dates = []  
        j_below_zero = False  
        d_below_twenty = False  
        previous_k = previous_d = 0  
        
        # 逐行检查数据  
        for date, row in data.iterrows():  
            k, d, j = row['K'], row['D'], row['J']  
            
            # 检查J是否小于0和D是否小于20  
            if j < 0:  
                j_below_zero = True  
            if d < 20:  
                d_below_twenty = True  
            
            # 检查金叉条件：K线上穿D线，并且之前J小于0且D小于20  
            if k > d and previous_k <= previous_d and j_below_zero and d_below_twenty:  
                golden_cross_dates.append(date)  
                # 重置条件，因为我们已经找到了一个金叉  
                j_below_zero = False  
                d_below_twenty = False  
            
            # 更新之前的K和D值  
            previous_k, previous_d = k, d  
        
        return golden_cross_dates  

    @staticmethod
    def find_next_golden_cross(data: pd.DataFrame, start_row=0):  
        """  
        找到第一个满足条件的金叉日期：J小于0，D小于20之后的金叉，从指定行开始搜索  
        
        :param data: pandas读取的数据  
        :param start_row: 从哪一行开始搜索（默认为0，即从第一行开始）  
        :return: (第一个满足条件的金叉日期, 找到金叉时的行数)  
        """  
        
        # 初始化变量  
        j_below_zero = False  
        d_below_twenty = False  
        previous_k = previous_d = float('nan')  # 使用NaN来确保第一次迭代不会触发金叉条件  
        first_golden_cross_date = None  
        first_golden_cross_row = None  
        
        # 从指定行开始逐行检查数据  
        for i, row in data.iloc[start_row:].iterrows():  
            k, d, j = row['K'], row['D'], row['J']  
            current_row_number = start_row + data.iloc[start_row:].index.get_loc(i)  # 获取当前行在整个DataFrame中的行号（从start_row开始计数）  
            
            # 检查J是否小于0和D是否小于20  
            if j < 0:  
                j_below_zero = True  
                
            if d < 20:  
                d_below_twenty = True  
            
            # 检查金叉条件：K线上穿D线，并且之前存在J小于0且D小于20的情况  
            if k > d and (previous_k is float('nan') or k >= previous_k) and (previous_d is float('nan') or d > previous_d) and j_below_zero and d_below_twenty:  
                first_golden_cross_date = i  # 记录金叉日期  
                first_golden_cross_row = current_row_number  # 记录金叉时的行数（从0开始计数）  
                break  # 找到第一个金叉后退出循环  
            
            # 更新之前的K和D值  
            previous_k, previous_d = k, d  
        
        # 返回第一个金叉日期和金叉时的行数（如果没有找到金叉，则为None）  
        return first_golden_cross_date, first_golden_cross_row  


    # 定义一个函数来查找J的最高点  
    @staticmethod
    def find_j_peak(data: pd.DataFrame, start_idx: int):  
        j_peak_date = None 
        j_peak_value = -1  
        in_range = False  
        for i in range(start_idx, len(data)):  
            if data['J'].iloc[i] > 100: # and data['D'].iloc[i] > 65:  
                in_range = True  
                if data['J'].iloc[i] > j_peak_value:  
                    j_peak_value = data['J'].iloc[i]  
                    j_peak_date = data.index[i] 
                    j_peak_price =  data["Close"][i] 
            elif in_range and (data['J'].iloc[i] <= 100 or data['D'].iloc[i] <= 65):  
                break  
        data =[j_peak_date, j_peak_price]
        return data

    @staticmethod
    def find_j_above_100_and_dead_cross(kdj_data: pd.DataFrame, start_position: int):  
        """  
        在KDJ数据中找到第一个J>100的位置以及随后的第一个KDJ死叉位置。  
        
        :param kdj_data: 包含KDJ指标的Pandas DataFrame，需要包含'Date', 'K', 'D', 'J', 'Close'列  
        :param start_position: 从哪一行开始搜索（默认为0，即从第一行开始）  
        :return: 第一个J>100时的日期和收盘价，以及随后的第一个KDJ死叉的日期和收盘价  
        """  
        # 从指定位置开始搜索  
        kdj_data = kdj_data.iloc[start_position:]  
        
        # 找到第一个J>100的位置  
        j_above_100 = kdj_data[kdj_data['J'] > 100]  
        if j_above_100.empty:  
            return None, None, None, None  # 如果没有找到J>100的情况，返回None  
        
        first_j_above_100_date = j_above_100.index[0]  
        first_j_above_100_close = j_above_100.at[first_j_above_100_date, 'Close']  
        
        # 从J>100的位置开始搜索死叉  
        dead_cross = None  
        for i in range(j_above_100.index[0] + 1, len(kdj_data)):  
            if kdj_data.at[kdj_data.index[i], 'K'] < kdj_data.at[kdj_data.index[i], 'D']:  
                # 检查前一个是否是金叉，以确保当前是死叉  
                if i > 1 and kdj_data.at[kdj_data.index[i-1], 'K'] > kdj_data.at[kdj_data.index[i-1], 'D']:  
                    dead_cross = kdj_data.index[i]  
                    break  
        
        if dead_cross is not None:  
            dead_cross_date = dead_cross  
            dead_cross_close = kdj_data.at[dead_cross, 'Close']  
        else:  
            dead_cross_date = None  
            dead_cross_close = None  
        
        return first_j_above_100_date, first_j_above_100_close, dead_cross_date, dead_cross_close  
    
    @staticmethod
    def fullfil_dataframe(df):
        # 创建一个布尔序列，标记所有 Volume 不为 0 的行  
        nonzero_volume_mask = df['Volume'] != 0  
        
        # 使用 mask 获取 Volume 不为 0 的行的索引  
        nonzero_indices = df[nonzero_volume_mask].index.tolist()  
        
        # 初始化一个变量来跟踪最后一个非零 Volume 的行  
        last_nonzero_row = None  
        
        # 遍历 DataFrame 的每一行  
        for index, row in df.iterrows():  
            if row['Volume'] == 0 and last_nonzero_row is not None:  
                # 如果当前行 Volume 为 0，且存在最后一个非零 Volume 的行，则进行替换  
                df.loc[index] = df.loc[last_nonzero_row]  
            elif row['Volume'] != 0:  
                # 更新最后一个非零 Volume 的行索引  
                last_nonzero_row = index  