# TDX_Lianghua_basic
------------------如果大家觉得好， 请给个星------------------


仅仅用来记录下最初研究量化的代码， 数据是通达信免费下的日线前复权数据， 初学者可以简单参考一下思路 

通达信的数据下载在这里
D:\new_tdx\T0002\export

日线数据下载地址
首先: 通达信-选项-盘后数据下载
然后：通达信-选项-数据导出-高级导出
-- YY#XXXXXX.txt
-- 空格
-- 前复权
-- 生成导出头部
-- YYYY-MM-DD


新版量化程序在私仓，主要用来验证策略的历史战绩， 暂时不放出来了


# 安装

建议安装python 3.12...

python -m pip install --upgrade pip

pip install -r requirements.txt


## ta-lib安装
pip install ta-lib

1. 安装vc 14: 
https://visualstudio.microsoft.com/visual-cpp-build-tools 安装2015那个14.0和win10sdk
2. 解决： 安装windows支持包： https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-msvc.zip/download?use_mirror=jaist
Windows
Download ta-lib-0.4.0-msvc.zip and unzip to C:\ta-lib.

This is a 32-bit binary release. If you want to use 64-bit Python, you will need to build a 64-bit version of the library. Some unofficial instructions for building on 64-bit Windows 10 or Windows 11, here for reference:

Download and Unzip ta-lib-0.4.0-msvc.zip
Move the Unzipped Folder ta-lib to C:\
Download and Install Visual Studio Community (2015 or later)
Remember to Select [Visual C++] Feature
Build TA-Lib Library
From Windows Start Menu, Start [VS2015 x64 Native Tools Command Prompt]
Move to C:\ta-lib\c\make\cdr\win32\msvc
Build the Library nmake
You might also try these unofficial windows binaries for both 32-bit and 64-bit:

3. error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.38.33130\\bin\\HostX86\\x64\\link.exe' failed with exit code 1120
解决： 我的python是3.12， 使用pip install ta_lib-0.4.28-cp312-cp312-win_amd64.whl 这个
其他版本这里找找 https://github.com/cgohlke/talib-build/releases
下载https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 


## 第一部分：把通达信数据转换成csv数据， 这部分代码留作记录， 以后可能会用到

#通达信下载的.day数据时没有复权的， 计算不够准确， 配套的代码可以用来参考
1. 日线
python tdx_daytocsv.py SH DAY 
python test6.py 可以根据我的量化标准，验证单个数据， 但是由于部分数据未复权， 结果不准
