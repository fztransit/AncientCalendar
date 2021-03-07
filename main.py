import numpy as np
import pandas as pd
from liCalc import *
from liData import *
import os
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)


def liFrame(li, year):
	liList = calendar(li, year)
	flag = liList[0][-1].pop()
	liArray = np.array(liList)  # 转为np列表，方便直接读取列
	data = pd.DataFrame(liArray[:, 3:9], columns=['大余', '小余', '大余', '小余', '大余', '小余'])  # yfa、中气
	month = [yuefen[(int(yx)-li.jzy) % 12] for yx in liArray[:, 1]]  # 获取列表中的每一项
	data.insert(0, '年份', year)
	data.insert(1, '蔀名', gz[li.bsgz[li.rbs]])
	data.insert(2, '入蔀年', [li.rbn+1] * np.shape(liArray)[0])
	data.insert(3, '月份', np.char.add(list(liArray[:, 0]), month))  # 索引, 列名，数据内容
	sgz = [gz[(int(ydy)+li.bsgz[li.rbs]) % 60] for ydy in liArray[:, 3]]
	wgz = [gz[(int(ydy)+li.bsgz[li.rbs]) % 60] for ydy in liArray[:, 5]]
	wrq = [nlrq[(int(liArray[i][5]) - int(liArray[i][3])) % 60] for i in range(len(liArray[:, 5]))]
	zqgz = [gz[(int(qdy)+li.bsgz[li.rbs]) % 60] if qdy != None else None for qdy in liArray[:, 7]]
	zqrq = [nlrq[(int(liArray[i][7]) - int(liArray[i][3])) % 60] if liArray[i][7] != None else None for i in range(len(liArray[:, 7]))]
	data.insert(4, '朔', sgz)
	''' 加节气的排版 '''
	zqmb = jieqi[li.ssy*2::2] + jieqi[:li.ssy*2:2]
	jqmb = jieqi[li.ssy*2+1::2] + jieqi[1:li.ssy*2+1:2]
	if li.suis == -1: zqmb.insert(0, zqmb.pop())
	if flag == -1: jqmb.insert(0, jqmb.pop())  # 右移
	if None in liArray:  # 无中气
		wzq = np.where(liArray == None)[0][0]
		zqmb.insert(wzq, '')
		jqmb.append(jqmb[0])
	wjq = [i for i, item in enumerate(liArray[:, 9]) if None in item]
	if wjq:  # 无节气
		jqmb.insert(wjq[0], '')
		jqmb.pop()
	data.insert(7, '望', wgz)
	data.insert(8, '日期', wrq)
	data.insert(11, '名称', zqmb)
	data.insert(12, '中气', zqgz)
	data.insert(13, '日期', zqrq, allow_duplicates=True)
	jqdy = [x[0] for x in liArray[:, 9]]
	jqxy = [x[1] for x in liArray[:, 9]]
	jqgz = [gz[(int(qdy) + li.bsgz[li.rbs]) % 60] if qdy != None else None for qdy in jqdy]
	jqrq = [nlrq[(liArray[i][9][0] - liArray[i][3]) % 60] if liArray[i][9][0] != None else None for i in range(len(liArray[:, 9]))]
	data.insert(16, '名称', jqmb, allow_duplicates=True)
	data.insert(17, '节气', jqgz, allow_duplicates=True)
	data.insert(18, '日期', jqrq, allow_duplicates=True)
	data.insert(19, '大余', jqdy, allow_duplicates=True)
	data.insert(20, '小余', jqxy, allow_duplicates=True)
	data.insert(1, '历名', li.lm)
	data.insert(3, '干支', ganzhiYear(year))
	del data['蔀名']
	del data['入蔀年']
	return data

#data = liFrame(jjl, 550)
#print(data)


# 生成连续年份的历表
def data2csv(start_year, end_year, li):
	for i in range(end_year-start_year+1):
		if start_year + i == 0: continue
		data = liFrame(li, start_year + i)
		if i == 0:
			data.to_csv(li.lm + '.csv', sep=',', header=True, index=False, encoding='utf_8_sig', mode='w')
		else:
			data.columns = [''] * data.shape[1]
			data.to_csv(li.lm + '.csv', sep=',', header=True, index=False, encoding='utf_8_sig', mode='a')


for gll in gllb[2:]:
	start_year, end_year = gllb[:2]
	data2csv(start_year, end_year, gllb)


for bxnf in bxnb:
	start_year, end_year, li = bxnf
	data2csv(start_year, end_year, li)

