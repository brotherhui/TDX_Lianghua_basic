import struct
import datetime
import argparse
import concurrent.futures  
from utils import MyUtils
import pandas as pd  

# 处理一个list的股票日数据
def process_list(sourcePath, targetPath, list):
    for item in list:
        stockNum = MyUtils.parse_stocknum(item)
        # --------------------------- day文件转csv ---------------------
        # 将通达信的day文件转为可读的日CSV文件
        sourceFile = sourcePath + item
        targetFile = targetPath + stockNum + MyUtils.DAILY_CSV_FILEPOSTFIX
        day2csv(sourceFile,targetFile)

        # --------------------------- 日线数据处理 ---------------------
        # 开始使用日线CSV文件作为源文件
        sourceFile = targetPath + stockNum + MyUtils.DAILY_CSV_FILEPOSTFIX
        targetFile = targetPath + stockNum + MyUtils.DAILY_FULL_FILEPOSTFIX
        # 丰富日线数据
        enrichDaily(sourceFile,targetFile)
        targetFile = targetPath + stockNum + MyUtils.MONTHLY_CSV_FILEPOSTFIX
        # 日线转月线数据
        day2month(sourceFile,targetFile)

        # --------------------------- 月线数据处理 ---------------------
        # 开始使用月线CSV文件作为源文件
        sourceFile = targetPath + stockNum + MyUtils.MONTHLY_CSV_FILEPOSTFIX
        # 丰富月线数据
        targetFile = targetPath + stockNum + MyUtils.MONTHLY_FULL_FILEPOSTFIX
        enrichMonthly(sourceFile,targetFile)

# 将day后缀的文件转换成csv文件
def day2csv(sourceFile,targetFile):
    with open(sourceFile, 'rb') as f:
        file_object = open(targetFile, 'w+')
        title_str = "Date,Open,High,Low,Close,Volume\n" #定义标题
        file_object.writelines(title_str) #写入标题
        while True:
            stock_date = f.read(4) #0-3
            stock_open = f.read(4) #4-7
            stock_high = f.read(4) #8-11
            stock_low= f.read(4) #12-15
            stock_close = f.read(4) #16-19
            stock_amount = f.read(4) #20-23
            stock_vol = f.read(4) #24-27
            stock_reservation = f.read(4) #28-31

            # date,open,high,low,close,amount,vol,reservation
            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)     # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)     #开盘价*100
            stock_high = struct.unpack("l", stock_high)     #最高价*100
            stock_low= struct.unpack("l", stock_low)        #最低价*100
            stock_close = struct.unpack("l", stock_close)   #收盘价*100
            stock_amount = struct.unpack("f", stock_amount) #成交额
            stock_vol = struct.unpack("l", stock_vol)       #成交量(手)
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_vol[0])+"\n"
            print(list)
            file_object.writelines(list)
        file_object.close()

# 将day信息丰富起来
def enrichDaily(sourceFile,targetFile):
    # 读取日线数据  
    data = pd.read_csv(sourceFile) 
    data.set_index('Date', inplace=True)  # 将日期列设置为索引  
    data = data.sort_values(by='Date')   # 确保数据按日期排序  

    #如果日线太少， 不必要继续
    if data.shape[0] > 12:  
        MyUtils.calculate_kdj(data, 9,3,3)
        MyUtils.calculate_macd(data)
        # 将结果按日期保存为CSV文件  
        data.to_csv(targetFile, index=True)


# 将日线数据转为月线数据
def day2month(sourceFile,targetFile):
    # 读取日线数据  
    data = pd.read_csv(sourceFile) 
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d') 
    data.set_index('Date', inplace=True)  # 将日期列设置为索引  
    data = data.sort_values(by='Date')   # 确保数据按日期排序  

    monthly_data = MyUtils.day2month(data)
    MyUtils.fullfil_dataframe(monthly_data)
    # 将结果按日期保存为CSV文件  
    monthly_data.to_csv(targetFile, index=True)    

# 将月线数据丰富起来
def enrichMonthly(sourceFile,targetFile):
    # 读取月线数据  
    data = pd.read_csv(sourceFile) 
    print(sourceFile)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d') 
    data.set_index('Date', inplace=True)  # 将日期列设置为索引  
    data = data.sort_values(by='Date')   # 确保数据按日期排序  

    #如果月线太少， 不必要继续
    if data.shape[0] > 9:  
        # 注意，如果月线数据是连续的， 可以直接处理， 但是对于月线数据为0 比如停盘了一段时间的股票， 需要使用前复权数据， 但是通达信数据没有前复权。 
        # 所以这里我会采用分段处理的方式， 以volume为0分拆dataframe, 每一部分单独计算KDJ. 这样的数据不够精准， 但是结果接近
        # MyUtils.calculate_kdj_with_zero_volume(data, 9,3,3)
        MyUtils.calculate_kdj(data, 9,3,3)
        MyUtils.calculate_macd(data)
        # 将结果按日期保存为CSV文件  
        data.to_csv(targetFile, index=True)


def main(market, type, threadsnum):
    print(f"开始时间：", datetime.datetime.now().time()," 为 ",market, type)
    sourcePath = MyUtils.get_source_path(market, type)
    targetPath = MyUtils.get_target_path(market)
    sourceList = MyUtils.get_source_list(market, type)
    #判断是否使用多协程执行
    if not threadsnum or threadsnum <= 1:
        # 直接执行， 4358个文件， 耗时5分钟 
        process_list(sourcePath, targetPath, sourceList)
    else:
        # 利用多协程执行, 还没有单线程快... 
        # 4358个文件，10个协程，耗时8分钟
        splitedList = MyUtils.split_list(sourceList, threadsnum)
        # 创建一个 ThreadPoolExecutor 实例，线程数等于给定的任意数量  
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadsnum) as executor:  
            # 提交协程到线程池执行   
            futures = [executor.submit(process_list, sourcePath, targetPath , lst) for lst in splitedList]   
            # 等待所有协程执行完毕  
            for future in concurrent.futures.as_completed(futures):  
                # 获取协程的返回值（如果有的话）  
                result = future.result()  

    print(f"结束时间：", datetime.datetime.now().time()," 为 ",market, type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="请输入股票市场参数 例 python tdx_daytocsv.py SH DAY 1")  
    parser.add_argument("a", type=str, help="第一个参数股票市场， 输入 SH 上海 SZ 深圳")  
    parser.add_argument("b", type=str, help="数据类型 日线 DAY")  
    parser.add_argument("c", type=int, help="协程数量 建议 1")  
    args = parser.parse_args()
    # main(args.a, args.b, args.c)
    main("SH","DAY",1) #sh day
    # main("SZ","DAY",1) #sz day

