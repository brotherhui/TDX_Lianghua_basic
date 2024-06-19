import pandas as pd  
  
# python程序一行一行的读取含有KDJ，Close的日线数据， 
# 每一轮收益以后， 拿走中间过程中追加的本金， 用盈利和初始的10000本金，继续滚动
# 返回所有的买入时间，价格，股票数， 和卖出时间，价格，股票数。 并计算总收益

# 假设数据文件名为'stock_data.csv'，包含列'Date', 'K', 'D', 'J', 'Close'  
# file_name = 'D:\\quantization_data\\sh\\sh600559.month.full.csv'  
file_name = 'D:\\quantization_data\\qfq\\SH#600559.month.full.csv'  
# file_name = 'D:\\quantization_data\\sh\\sh601888.month.full.csv' 
# file_name = 'D:\\quantization_data\\sh\\sh000001.month.full.csv'
# file_name = 'D:\\quantization_data\\sh\\sh600599.month.full.csv'  
  
# 读取数据  
df = pd.read_csv(file_name)  
print(f"",{file_name})
  
# 初始化变量 
bloody_money_inital = 10000 # 初始投入， 始终不变



buy_price = 0  # 买入价格  
buy_dates = []  # 买入日期列表  
buy_prices = []  # 买入价格列表  
buy_shares = []  # 买入股票数量列表  
sell_dates = []  # 卖出日期列表  
sell_prices = []  # 卖出价格列表  
sell_shares = []  # 卖出股票数量列表  

total_earn = 0  # 总收益  
total_earn_percent = 1 # 总收益倍数

finished_round_num_total = 0 # 已完成轮数
finished_bloody_money_max = bloody_money_inital # 已完成的所有轮的， 过程中动用的总最大本金
finished_cash_earn_total = 0 # 已经完成的周期的总获利

# ------------------ 每轮记录
round_shares_num_initial = 0 # 本轮买入股票的初始数量，基础仓位， 取决于本轮投入
round_shares_price_initial = 0 # 本轮股票初始买入价格
round_cash_account_initial = bloody_money_inital # 本轮的初投入始金额

round_bloody_money_account = bloody_money_inital  # 本轮本金账户中的本金数量
round_cash_account = round_bloody_money_account  # 本轮当前证券账户的现金, 初始化为本金账户的本金

round_cash_invest_total = 0 # 本轮总投入
round_cash_earn_total = 0 # 本轮总收益=收回-投入
round_cash_return_total = 0 # 本轮总收回
round_shares_price_total = 0 # 本轮当前总持股金额

round_shares_holding_avg_price = 0 # 本轮持有股票的平均买入价格
round_shares_holding_num = 0  # 本轮持股总数量  

round_earn_percent_current = 0
round_num_current = 0 # 当前进行几轮

# 临时参数
num = 0 

# 设置交易标记  
d_below_20_flag = False  
j_below_0_flag = False  
gc_flag = False #金叉标志

d_above_50_flag = False

# 初始化补仓J位
j_below_5_flag = False


# 初始化变量  判断J高点位趋势
j_above_100_flag = False
falling_trend = False  # 标记J是否处于下降趋势  
j_peek_flag = False
# 本轮初始
new_round = True

# 遍历数据行  
for i in range(1, len(df)):  
    # 获取当前行数据  
    row = df.iloc[i]  
    prev_row = df.iloc[i - 1]  

    # 初始化本轮的基本数据， 每轮只初始化一次
    if new_round:
        new_round = False
        d_below_20_flag = False  
        j_below_0_flag = False  
        j_below_5_flag = False
        j_above_100_flag = False
        d_above_50_flag = False
        j_peak_flag = False
        round_shares_num_initial = 0
        gc_flag = False
        round_cash_invest_total = 0
        round_cash_return_total = 0
        round_num_current = 0
        round_cash_earn_total = 0
        round_earn_percent_current = 0
      
    if row['D'] < 20:  
        d_below_20_flag = True  

    if row['D'] > 50:  
        d_above_50_flag = True 

    if row['J'] < 0:  
        j_below_0_flag = True  
    if row['J'] < 5:  
        j_below_5_flag = True 

    # 判断J超过100， D>65, 找卖点， 必须是金叉以后
    if gc_flag and row['J'] > 100:  
        # print(f"",str(row['J']),{row['Date']})
        # 当J首次超过100时，设置标记并开始监视下降趋势  
        j_above_100_flag = True  
    if j_above_100_flag and row['D'] > 65 : 
        # print(f"",str(row['D']),str(row['J']),{row['Date']})
        j_peak_flag = True
    # elif j_above_100_flag and row['J'] < 100:  
        # # 如果J曾经超过100，并且现在小于100，检查是否是首次  
        # if not falling_trend:  
        #     # 如果是首次J<100并且处于下降趋势，记录日期并设置标记  
        #     falling_trend = True  


    if j_below_0_flag and row['K'] > prev_row['D'] and row['D'] > prev_row['D'] and not gc_flag:  
        buy_price = row['Close'] 
        if buy_price == 0:  
            print("错误：购买价格为零，无法计算能买入的股票数量。")  
        else:
            round_shares_num_initial = int(round_cash_account // buy_price)  # 计算能买入的股票数量，取整数

        round_shares_price_initial = buy_price
        shares_to_buy = round_shares_num_initial  # 计算能买入的股票数量，取整数  
        round_shares_holding_num += shares_to_buy  
        transaction_fee = round(shares_to_buy * row['Close'],1)

        # 减仓导致可用资金减少
        round_cash_account -= transaction_fee
        # 总投入增加， 当前投入增加
        round_cash_invest_total += transaction_fee

        round_shares_holding_avg_price =round(round_cash_invest_total/round_shares_holding_num,1)
        buy_dates.append(row['Date'])  
        buy_prices.append(buy_price)  
        round_shares_price_total = round(round_shares_holding_num*buy_price,1)  
        buy_shares.append(shares_to_buy) 
        #如果是第一次金叉， 记录轮数 
        if not gc_flag:
            num += 1
            print(f"---------------第",str(num),"周期---------------")
            round_num_current =1
        print(f"..买入时间: {row['Date']}, 买入价格(收盘): {buy_price}, 买入数: {shares_to_buy}, 本次投入：{transaction_fee}, 本轮总投入：{round_cash_invest_total}, 剩余股数: {round_shares_holding_num}, 剩余持有价值: {round_shares_price_total}, 持股均价: {round_shares_holding_avg_price}")  
        # 重置标记，因为已经买入  
        d_below_20_flag = False  
        j_below_0_flag = False  
        j_below_5_flag = False 
        j_above_100_flag = False 
        d_above_50_flag = False
        gc_flag = True
        # falling_trend = False
      
    elif row['K'] > prev_row['D'] and row['D'] > prev_row['D'] and round_shares_price_initial > row['Close'] and gc_flag:  
        buy_price = row['Close']   
        shares_to_buy = round_shares_num_initial  # 补仓相同的仓位 
        transaction_fee = round(shares_to_buy * buy_price,1)
        if round_cash_account < transaction_fee:  
            # 需要补充本金
            round_cash_account += transaction_fee # 手头的可用现金
            round_bloody_money_account  += transaction_fee # 补充本金

        round_shares_holding_num += shares_to_buy  
        # 补仓导致可用资金减少
        round_cash_account -= transaction_fee

        # 总投入增加， 当前投入增加
        round_cash_invest_total += transaction_fee

        round_shares_holding_avg_price =round(round_cash_invest_total/round_shares_holding_num,1) 
        buy_dates.append(row['Date'])  
        round_shares_price_total = round(round_shares_holding_num*buy_price,1)  
        buy_prices.append(buy_price)  
        buy_shares.append(shares_to_buy)  
        print(f"..补仓时间: {row['Date']}, 买入价格(收盘): {buy_price}, 买入数: {shares_to_buy}, 本次投入：{transaction_fee}, 本轮总投入：{round_cash_invest_total}, 剩余股数: {round_shares_holding_num}, 剩余持有价值: {round_shares_price_total}, 持股均价: {round_shares_holding_avg_price}, ")  
        j_below_5_flag = False
        
      
    # # J>100卖出逻辑  , 注意价格要大于均价, 要在J>100后， 抛物线向下且大于100的阶段获利，不能每个月大于100都获利回吐
    # elif round_shares_holding_num > 0 and j_above_100_flag and gc_flag and row['Close'] > round_shares_holding_avg_price: 
    #     sell_price = row['Close']   
    #     shares_to_sell = round_shares_holding_num * 0.5  # 卖出一半股票  
    #     transaction_fee = round(shares_to_sell * sell_price,1)
    #     round_cash_account += transaction_fee
    #     sell_dates.append(row['Date'])  
    #     sell_prices.append(sell_price)  
    #     sell_shares.append(shares_to_sell)  
    #     round_shares_holding_num -= shares_to_sell  
    #     round_cash_return_total += transaction_fee
    #     round_shares_price_total = round(round_shares_holding_num*sell_price,1) 
    #     print(f"..获利时间: {row['Date']}, 卖出价格: {sell_price}, 卖出数: {shares_to_sell}, 本次获利： {transaction_fee}, 剩余股数: {round_shares_holding_num}, 剩余持有价值: {round_shares_price_total}")
    #     # 不需要重置任何标记，因为可能再次卖出或买入  
      
    elif round_shares_holding_num > 0  and gc_flag and j_peak_flag and row['Close'] > round_shares_holding_avg_price:  
        # print(f"",str(row['K']),str(row['D']),str(row['J']),{row['Date']})
        sell_price = row['Close']   
        shares_to_sell = round_shares_holding_num  # 卖出剩余股票 
        transaction_fee = round(shares_to_sell * sell_price,1)
        round_cash_account = round(round_cash_account + transaction_fee)
        sell_dates.append(row['Date'])  
        sell_prices.append(sell_price)  
        # 本轮数据
        round_shares_holding_num = 0 
        finished_round_num_total += 1
        sell_shares.append(round_shares_holding_num)  
        round_cash_return_total += transaction_fee

        # 计算本轮的统计
        round_cash_earn_total = round(round_cash_return_total - round_cash_invest_total,1)
        percent = round(round_cash_earn_total/round_cash_invest_total,1)
        round_shares_price_total = 0
        finished_cash_earn_total = round(finished_cash_earn_total + round_cash_earn_total,1)
        # 比较这几轮结束的行情中最大动用过的本金
        if finished_bloody_money_max < round_bloody_money_account:
            finished_bloody_money_max = round_bloody_money_account 

        addintional_bloody_money = round(round_bloody_money_account - bloody_money_inital,1)
        print(f"..清仓时间: {row['Date']}, 卖出价格(收盘): {sell_price}, 卖出数: {shares_to_sell}, 本次收回：{transaction_fee}, 本轮总收回：{round_cash_return_total}, 纯利润：{round_cash_earn_total}")
        print(f"$$本轮总结: {row['Date']}, 本轮的初始准备金: {round_cash_account_initial}, 包含的初始血汗钱：{bloody_money_inital}, 本轮总投入：{round_cash_invest_total},本轮总收回：{round_cash_account}, 纯利润：{round_cash_earn_total}, 期间多投入血汗钱：{addintional_bloody_money},  获利比例: {percent}")    
        # 重置标记，因为已经卖出全部股票, 本轮结束  
        new_round = True  # 重置下一轮
        # 从可用现金中去掉额外投入的血汗钱， 只使用收入加上最开始的本金滚动， 注意顺序

        round_cash_account_initial  = round(round_cash_account_initial + round_cash_earn_total,1)
        round_cash_account = round_cash_account_initial
        round_bloody_money_account = bloody_money_inital
    else:
        round_shares_price_total = round(round_shares_holding_num*row['Close'],1)
        # 当前盈利 当前轮的总投入 - 当前持股价格
        round_cash_earn = round(row['Close'] * round_shares_holding_num - round_cash_invest_total, 1)

# 计算总收益  
round_bloody_money_account = round(round_bloody_money_account,1)
total_earn = round(round_cash_account-round_bloody_money_account,1)  # 假设最后还持有的股票按最后一天收盘价卖出  


if not round_cash_invest_total == 0:
    round_earn_percent_current = round(round_cash_earn/round_cash_invest_total,1)
finished_earn_percent_total = round(finished_cash_earn_total/bloody_money_inital,1)


# for date, price, num in zip(buy_dates, buy_prices, buy_shares):  
#     print(f"日期: {date}, 价格: {price}, 股票数: {num}")  
# print(f"\n卖出记录:")  
# for date, price, num in zip(sell_dates, sell_prices, sell_shares):  
#     print(f"日期: {date}, 价格: {price}, 股票数: {num}")  
print(f"---------------总结-------------------")
print(f"已完成周期: {finished_round_num_total}, 初始血汗钱: {bloody_money_inital}, 最多投入血汗钱：{finished_bloody_money_max}, 纯利润: {finished_cash_earn_total}, 总获利比例=纯利润/最初本金：{finished_earn_percent_total}")
print(f"进行中周期: {round_num_current}，当前准备金额投入: {round_cash_account_initial}, 包含血汗钱: {bloody_money_inital}, 最多投入血汗钱: {round_bloody_money_account}, 纯利润: {round_cash_earn}, 现在持股数:{round_shares_holding_num}, 当前持股价值：{round_shares_price_total}, 总获利比例：{round_earn_percent_current}")
# print(f"总周期数: {round_num_current}，总投入本金: {round_bloody_money_account}, 获利: {total_earn}, 现在持股数:{round_shares_holding_num}, 当前持股金额：{round_shares_price_total}, 总获利比例：{total_earn_percent}")






