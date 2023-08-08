# coding: utf-8

import pandas as pd
import os 


file_name = []
ls = os.listdir()  # 列出当前工作目录下的所有的文件和目录
for i in range(0, len(ls)):
    if ls[i][0] == '.':  # 防止隐藏文件
        pass
    else:
        file_name.append(ls[i])
file_name = sorted(file_name, key=lambda x: int(x[:-5]))
print(file_name)


#---------存为不同的文件------------#
for file_ele in file_name:
    real_file_ele = 'chinamil'+'/'+file_ele
    df = pd.read_excel(real_file_ele, 'Sheet',header=None)
    df_first_line = df.head(1)
    df_other = df.iloc[2:]
    df_after = pd.concat([df_first_line,df_other],ignore_index=True)
    df_after_en = df_after.iloc[:, 0] # 取第1列
    df_after_zh = df_after.iloc[:, 1] # 取第2列
    write_name_en = file_ele[:-5] + 'eng.txt'
    write_name_zh = file_ele[:-5] + 'zh.txt'
    df_after_en.to_csv(write_name_en, sep='\t', index=False,header=None)
    df_after_zh.to_csv(write_name_zh, sep='\t', index=False,header=None)


#---------------存为同一个 txt ---------------#
for file_ele in file_name:
    real_file_ele = 'chinamil'+'/'+file_ele
    df = pd.read_excel(real_file_ele, 'Sheet',header=None)
    df_first_line = df.head(1)
    df_other = df.iloc[2:]
    print(df_other)
    df_after = pd.concat([df_first_line,df_after],ignore_index=True)
    df_after_en = df_after.iloc[:, 0] # 取第1列
    df_after_zh = df_after.iloc[:, 1] # 取第2列
    write_name_en = 'eng.txt'
    write_name_zh = 'zh.txt'
    df_after_en.to_csv(write_name_en, sep='\t', index=False,header=None,mode='a')
    df_after_zh.to_csv(write_name_zh, sep='\t', index=False,header=None,mode='a')

