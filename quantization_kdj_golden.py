# 验证选股策略
# 月线KDJ

import datetime
import argparse
from utils import MyUtils
import pandas as pd 
import numpy as np 
import csv 

RESULT_FILE = "kdj_golden_result.csv"

def process_list(sourcePath, targetPath, list):
    targetFile = targetPath + RESULT_FILE
    file_object = open(targetFile, 'w+')
    title_str = "股票,是否计算,机会,总收益,明细\n" # 定义标题
    file_object.writelines(title_str) # 写入标题
    for item in list:
        # --------------------------- 获取股票日线月线KDJ等数据 ---------------------
        stockNum = MyUtils.parse_stocknum(item)
        sourceFileDaily = sourcePath + stockNum + MyUtils.DAILY_FULL_FILEPOSTFIX
        sourceFileMonthly = sourcePath + stockNum + MyUtils.MONTHLY_FULL_FILEPOSTFIX
        # 如果对应的日线和月线数据没生成， 说明该股票的数据不全， 不符合要求
        if not os.path.exists(sourceFileDaily) or not os.path.exists(sourceFileMonthly):  
            result = stockNum + "," + "不予计算" + "\n"
        else:  
            dataDaily = pd.read_csv(sourceFileDaily) 
            dataDaily['Date'] = pd.to_datetime(dataDaily['Date'], format='%Y-%m-%d') 
            dataDaily.set_index('Date', inplace=True)  # 将日期列设置为索引  
            dataDaily = dataDaily.sort_values(by='Date')   # 确保数据按日期排序  
            dataMonthly = pd.read_csv(sourceFileMonthly) 
            dataMonthly['Date'] = pd.to_datetime(dataMonthly['Date'], format='%Y-%m-%d') 
            dataMonthly.set_index('Date', inplace=True)  # 将日期列设置为索引  
            dataMonthly = dataMonthly.sort_values(by='Date')   # 确保数据按日期排序  

            #--------------------------- 验证kdj金叉的结果 ---------------------
            result = kdj_golden_verify_result(stockNum, dataDaily, dataMonthly)

        file_object.writelines(result) # 写入单只股票验证结果
    file_object.close()


def find_golden_cross_dates(sourceFile):  
    # 初始化变量来跟踪前一个交易日的KDJ值  
    prev_k = None  
    prev_d = None  
    prev_j = None  
    
    # 用于存储满足条件的金叉日期  
    golden_cross_dates = []  
    
    # 打开股票数据文件并读取数据  
    with open(sourceFile, 'r') as file:  
        reader = csv.DictReader(file)  
        for row in reader:  
            date = datetime.strptime(row['Date'], '%Y-%m-%d').date()  # 假设日期格式为'YYYY-MM-DD'  
            k = float(row['K'])  
            d = float(row['D'])  
            j = float(row['J'])  
            close = float(row['Close'])
    
            # 检查是否满足条件：J小于0且D小于30  
            if j < 0 and d < 30:  
                # 如果这是第一个满足条件的数据点，则保存前一个交易日的KDJ值  
                if prev_k is None:  
                    prev_k, prev_d, prev_j = k, d, j  
                else:  
                    # 检查是否发生金叉（即今天的K值大于D值，而昨天的K值小于D值）  
                    if k > d and prev_k <= prev_d:  
                        golden_cross_dates.append(date)  
                        print(f"Found golden cross on {date}")  
                        
                    # 重置条件，因为我们已经找到了一个可能的金叉点，接下来需要新的J<0和D<20的条件  
                    prev_k, prev_d, prev_j = None, None, None  
            else:  
                # 如果不满足J<0和D<20的条件，但仍需跟踪KDJ值以便后续比较  
                prev_k, prev_d, prev_j = k, d, j  
        return golden_cross_dates

def kdj_golden_verify_result(stockNum, dataDaily, dataMonthly):
    result = []
    with open(sourceFile, 'rb') as f:
        file_object = open(targetPath + RESULT_FILE, 'w+')
        title_str = "Date,Open,High,Low,Close,Volume\n" #定义标题
        file_object.writelines(title_str) #写入标题
        while True:
            stock_date = f.read(4) #0-3
            stock_open = f.read(4) #4-7
            
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            result= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_vol[0])+"\n"


def main(market, type):
    print(f"开始时间：", datetime.datetime.now().time()," 为 ",market, type)
    sourcePath = MyUtils.get_target_path(market) # 拿所有股票的日线月线，KDJ等数据
    sourceList = MyUtils.get_source_list(market, type) # 通过这个获取所有股票代码
    targetPath = MyUtils.OUTPUT_PATH

    process_list(sourcePath, targetPath, sourceList)
    print(f"结束时间：", datetime.datetime.now().time()," 为 ",market, type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="请输入股票市场参数 例 python quantization_kdj_golden.py SH DAY")  
    parser.add_argument("a", type=str, help="第一个参数股票市场， 输入 SH 上海 SZ 深圳")  
    args = parser.parse_args()
    # main(args.a, args.b, args.c)
    main("SH","DAY") #sh day
    main("SZ","DAY") #sz day
