import pandas as pd  
  
# 假设数据文件名为'stock_kdj_data.csv'，并且包含'Date', 'Close', 'K', 'D', 'J'等列  
def read_kdj_data(filename):  
    return pd.read_csv(filename, parse_dates=['Date'], index_col='Date')  
  
def find_next_golden_cross(df, start_position):  
    """从start_position开始搜索下一个金叉的位置"""  
    for i in range(start_position, len(df) - 1):  # 需要至少两行来检查金叉  
        previous_row = df.iloc[i]  
        current_row = df.iloc[i + 1]  
        if previous_row['K'] < previous_row['D'] and current_row['K'] > current_row['D']:  
            return i + 1  # 返回金叉发生的位置（当前行的索引）  
    return None  # 如果没有找到金叉，则返回None  
  
def find_next_death_cross(df, start_position):  
    """从start_position开始搜索下一个死叉的位置"""  
    for i in range(start_position, len(df) - 1):  # 需要至少两行来检查死叉  
        previous_row = df.iloc[i]  
        current_row = df.iloc[i + 1]  
        if previous_row['K'] > previous_row['D'] and current_row['K'] < current_row['D']:  
            return i + 1  # 返回死叉发生的位置（当前行的索引）  
    return None  # 如果没有找到死叉，则返回None  
  
def find_next_buy_condition(df, start_position):  
    """从start_position开始搜索下一个满足买入条件的位置"""  
    for i in range(start_position, len(df)):  
        row = df.iloc[i]  
        if row['D'] < 20 and row['J'] < 0:  
            return i  # 返回满足买入条件的行的索引  
    return None  # 如果没有找到满足条件的行，则返回Non

def find_next_sell_condition(df, start_position):  
    """从start_position开始搜索下一个满足卖出条件的位置"""  
    # 这里只是一个示例条件，你需要根据你的策略来定义卖出条件  
    for i in range(start_position, len(df)):  
        row = df.iloc[i]  
        if row['J'] > 100:  # 假设当J大于100时满足卖出条件  
            return i  
    return None  
  
def trade_logic(df, initial_position=0, cash=10000, shares=0):  
    """交易逻辑，根据CLOSE价格买入和卖出"""  
    position = initial_position  
    while position < len(df):  
        # 检查金叉并买入  
        next_golden_cross = find_next_golden_cross(df, position)  
        if next_golden_cross is not None:  
            # 使用CLOSE价格买入  
            golden_cross_time = df.index[next_golden_cross]  # 金叉时间  
            buy_price = df.iloc[next_golden_cross]['Close'] 
            shares_to_buy = int(cash // buy_price)  # 计算能买入的股票数量，取整数  
            if shares_to_buy > 0:  
                cost = shares_to_buy * buy_price  
                cash -= cost  
                shares += shares_to_buy  
                print(f"",golden_cross_time.strftime('%Y-%m-%d')," 买入:", str(shares_to_buy), "股，买入价格:", str(buy_price), ", 剩余现金:",str(cash)," 持有股票:",str(shares),"股,","持有金额:",str(cost))  
            position = next_golden_cross + 1  # 更新位置到金叉之后的下一个交易日  
        else:  
            # 如果没有找到金叉，检查卖出条件  
            next_sell = find_next_sell_condition(df, position)  
            if next_sell is not None:  
                # 使用CLOSE价格卖出  
                sell_price = df.at[next_sell, 'Close']  
                cash += shares * sell_price  # 更新现金余额  
                shares = 0  # 清空持有的股票数量  
                print(f"卖出所有股票 在索引 {next_sell}, CLOSE价格 {sell_price}, 获得现金 {cash}")  
                  
                # 检查在卖出之后的下一个交易日是否立即有金叉，如果有则再次买入  
                next_golden_cross_after_sell = find_next_golden_cross(df, next_sell + 1)  
                if next_golden_cross_after_sell is not None:  
                    # 递归调用或继续循环来处理这个新的金叉（这里使用循环）  
                    position = next_golden_cross_after_sell  
                    continue  # 继续循环处理新的金叉  
            break  # 如果没有找到金叉或卖出条件，结束循环  
    return cash, shares, position  
  
# 使用示例：  
data = read_kdj_data('d:\\quantization_data\\sh\\sh601888.month.full.csv')  # 读取数据（请确保文件路径正确）  
print(data.index)  
print(data.columns)

final_cash, final_shares, final_position = trade_logic(data)  
print(f"最终现金余额: {final_cash}, 最终持有股票数量: {final_shares}")