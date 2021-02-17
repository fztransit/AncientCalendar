from liName import *


def divide(dividend, divisor, flag=False):
	quotient = dividend // divisor
	remainder = dividend % divisor
	if flag: quotient %= 60
	return int(quotient), int(remainder)


def qyfs(yfa, rf, n):  # 大余转为整数，n朔为1，1/2为望，1/4为上弦
	yfa *= n
	if yfa != int(yfa):  # 非整数
		dy = int(yfa // rf)
		xy = yfa % rf
	else: dy, xy = divide(yfa, rf)  # 小余是整数
	return dy, xy


def qy(dy1, xy1, rf, dy2, xy2, xf1=0, xf2=0, fm=1, n=1):  # 被加/减数，日法，加/减数，被加/减数小分，加/减数小分，分母，加/减次数
	zf = ((dy1 * rf + xy1) * fm + xf1) + ((dy2 * rf + xy2) * fm + xf2) * n
	xf = zf % fm
	zy = (zf - xf) // fm
	dy = int(zy // rf)
	xy = zy % rf
	if fm == 1: return dy % 60, xy + xf, xf
	else: return dy % 60, int(xy), xf


def epoch2tz(li, ydy, yxy, qdy, qxy, qxf):  # 从历元改推到天正
	ydy, yxy = qy(ydy, yxy, li.srf, li.backYue * li.sdy, li.backYue * li.sxy)[:2]
	qdy, qxy, qxf = qy(qdy, qxy, li.qrf, li.qdy, li.qxy, qxf, li.qxf, li.qfm, li.backQi)
	li.yrs(yxy)
	if (qdy - ydy) % 60 >= li.yueri:  # 正月前有闰（未必该月即闰月），需加推一月
		x = li.backYue // abs(li.backYue)
		ydy, yxy = qy(ydy, yxy, li.srf, x * li.sdy, x * li.sxy)[:2]
	return ydy, yxy, int(qdy), int(qxy), qxf


# 百刻制
def heshuo(xy, rf):  # 求合朔时刻（小余，日法）
	chen = round((xy / rf) * 12 + 0.5, 14) # 时辰从上一日23时起
	chen_h = int(chen)
	chen_k = round(xy / rf * 100 - int(xy / rf * 12) * 100 / 12, 14)  # 该时辰内的刻数
	if chen_k < 100/24:
		hssj = dizhi[chen_h % 12] + '正' + ke[int(chen_k)] + '刻'
	else:
		chen_k -= 100 / 24
		hssj = dizhi[chen_h % 12] + '初' + ke[int(chen_k)] + '刻'
	return hssj


def ganzhiYear(year):
	if year == 0:
		ngz = ''
	elif year < 0:
		ngz = gz[(year - 3) % 60]
	else:
		ngz = gz[(year - 4) % 60]
	return ngz

