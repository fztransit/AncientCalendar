from liClass import *


def tzs(li, year, rank=-1):  # rank=-1时历元为冬至即天正气朔，=1时即岁首气朔
	li.array(rank)
	# 基本推步算法
	jn = li.syjn(year)
	li.rbn = jn % li.bf  # +1入蔀年
	if li.type == 1: li.rbs = jn % li.jf // li.bf  # +1入蔀数
	else:
		if li.jf == li.bf: li.rbs = jn % li.yf // li.jf  # +1入纪数
		else: li.rbs = jn % li.yf // li.bf  # +1入蔀数
	jy = (li.rbn * li.zy) // li.zs  # 蔀内积月，每年235/19月
	li.ry = li.rbn * li.zy % li.zs  # 闰余 rbn * zy - jy * zf
	if li.bsry > 0:  # 首月中气非朔
		if li.lyry: jy -= li.bsry / li.zs  # 历元有闰余，转到无闰余日
		if li.ry + li.bsry >= li.zs: jy += 1  # 上一年有闰，需加回
	li.ry = (li.bsry + li.zy * li.rbn) % li.zs
	ydy, yxy = divide(jy * li.yfa, li.srf, True)  # 天正朔蔀内积日 = 积月 * 朔策(yfa / by)
	qdy, qxy = divide(li.rbn * li.sz, li.qrf, True)  # 中气积日 = 积年 * 岁长
	qxf = 0
	if (qdy - ydy) % 60 >= li.yrs(yxy):  # 首月为闰月
		ydy, yxy = qy(ydy, yxy, li.srf, li.sdy, li.sxy)[:2]
	# 根据历元和建正修改至天正冬至或岁首月
	if li.backYue != 0 and li.backQi != 0:  # 非天正冬至需回推
		ydy, yxy, qdy, qxy, qxf = epoch2tz(li, ydy, yxy, qdy, qxy, qxf)
	else: li.yrs(yxy)
	if li.rbn == 0 and li.ssy < li.qly/2:  # 回推时跨到上一蔀（岁首＜历元）
		ydy = (ydy + li.bsgzc) % 60
		qdy = (qdy + li.bsgzc) % 60
	return ydy, yxy, qdy, qxy, qxf


# 平朔平气法
def calendar(li, year, rank=1):  # 历表中是否排入节气，排序方式
	ydy, yxy, qdy, qxy, qxf = tzs(li, year, rank)
	li.wdy, li.wxy = qyfs(li.yfa, li.srf, 1 / 2)
	wdy, wxy = qy(ydy, yxy, li.srf, li.wdy, li.wxy)[:2]
	liList = [['', 0, ydx[li.yueri], [ydy, yxy], [wdy, wxy], [qdy, qxy]]]
	# 判断冬至月节气，或为大雪，或为小寒，或即无，其他月同理
	jqx = 0  # 每年出现的第一个节气，设为小寒
	wjq = False
	jdy1, jxy1, jxf1 = qy(qdy, qxy, li.qrf, -li.qdy // 2, -li.qxy // 2, qxf, -li.qxf//2, li.qfm)  # 大雪
	jdy2, jxy2, jxf2 = qy(qdy, qxy, li.qrf, li.qdy // 2, li.qxy // 2, qxf, li.qxf//2, li.qfm)    # 小寒
	if (jdy1 - ydy) % 60 >= li.yueri:  # 小雪不在冬至月，考虑大寒
		if (jdy2 - ydy) % 60 >= li.yueri:  # 小寒也不在，正月无节气
			ydy, yxy = qy(ydy, yxy, li.srf, li.sdy, li.sxy)[:2]
			jdy, jxy = jdy2, jxy2  # 必得二月小寒
			wjq = True
		else: jdy, jxy, jxf = jdy2, jxy2, jxf2  # 正月小寒
	else:
		jqx = -1
		jdy, jxy, jxf = jdy1, jxy1, jxf1  # 正月大雪
	if wjq:  # 首月无节气回推到上月起算
		ydy, yxy = qy(ydy, yxy, li.srf, -li.sdy, -li.sxy)[:2]
		jdy, jxy, jxf = qy(qdy, qxy, li.qrf, -li.qdy // 2, -li.qxy // 2, qxf, -li.qxf//2, li.qfm)
		liList[0].append([None, None, jqx])
	else: liList[0].append([jdy, jxy, jqx])
	# 生成历表
	j = 1  # i合朔次数，j月序
	for i in range(12):  # 共计算13月，无闰（或无气）时剔除最后一月
		run, ydy, yxy, qdy, qxy, qxf = li.wzqy(ydy, yxy, qdy, qxy, qxf)
		if li.ssy < li.qly/2 and li.rbn == 0 and j == li.qly // 2 and not run:  # 跨蔀
			ydy = (ydy - li.bsgzc) % 60
			qdy = (qdy - li.bsgzc) % 60
			jdy = (jdy - li.bsgzc) % 60  # 跨蔀
		wdy, wxy = qy(ydy, yxy, li.srf, li.wdy, li.wxy)[:2]
		if run:
			j -= 1
			liList.append([run, j%12, ydx[li.yueri], [ydy, yxy], [wdy, wxy], [None, None]])
		else:
			liList.append(['', j%12, ydx[li.yueri], [ydy, yxy], [wdy, wxy], [qdy, qxy]])
		wjq, ydy, yxy, jdy, jxy, jxf = li.wzqy(ydy, yxy, jdy, jxy, jxf, False)
		if wjq:
			liList[i+1].append([None, None])
		else: liList[i+1].append([jdy, jxy])
		j += 1
	if j == 13:
		liList.pop()  # k为0有无节气月（值必为FALSE），为1或11则无
	# x = 10 if liList[10][1] == 10 else 11
	if li.rbn == li.bf-1 and li.ssy > li.qly/2:  # 跨蔀首
		for m in range(11, len(liList)):
			for n in [3, 4, 5]:
				liList[m][n][0] = (liList[m][n][0] - li.bsgzc) % 60
			liList[m][6][0] = (liList[m][6][0] - li.bsgzc) % 60
	return liList  # 闰月或有无节气月输出13个月，否则输出12个月

