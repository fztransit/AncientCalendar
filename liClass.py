import math
from liFunc import *


class Li:
	def __init__(self, name, liyuan, yfa, srf, sz, qrf):  # 所有历法的共有属性（历名，历元，朔策(yfa/srf)，气策(sz/qrf)）
		self.lm = name
		self.ly = liyuan
		if yfa < srf: self.yfa = yfa + 29 * srf  # 只给出余分
		else: self.yfa = yfa
		self.srf = srf  # 朔日法
		self.yue = self.yfa / self.srf
		self.sdy, self.sxy = divide(self.yfa, self.srf)
		if sz < qrf: self.sz = sz + 365 * qrf
		else: self.sz = sz
		self.qrf = qrf
		self.sui = self.sz / self.qrf

	def bjsgz(self, bf):
		self.bsgzc = round(self.sui * bf % 60)  # 蔀/纪首干支差
		bs = 60 // math.gcd(self.bsgzc, 60)  # int(self.bsgzc * 60 / math.gcd(self.bsgzc, 60) / self.bsgzc)
		jf = bs * bf  # 甲子夜半朔旦冬至，四分历为纪法，非四分历即元法
		self.bsgz = [0] * bs  # 蔀/纪首干支序
		for i in range(bs):
			self.bsgz[i] = (i * self.bsgzc + self.lyrgz) % 60
		return jf

	def yrs(self, yxy):  # 判断大小月
		if yxy < self.srf - self.sxy:
			self.yueri = 29
			return 29
		else:
			self.yueri = 30
			return 30

	def wzqy(self, ydy_0, yxy_0, qdy_0, qxy_0, qxf_0, thisYue=True):  # 判断本月是否为无中气月（本月气大小余、朔大小余），无节气月亦适用
		if thisYue: ydy, yxy = qy(ydy_0, yxy_0, self.srf, self.sdy, self.sxy)[:2]
		else: ydy, yxy = ydy_0, yxy_0  # 输入即次月大小余
		qdy, qxy, qxf = qy(qdy_0, qxy_0, self.qrf, self.qdy, self.qxy, qxf_0, self.qxf, self.qfm)
		self.yrs(yxy)
		if (qdy - ydy) % 60 >= self.yueri:  # 本月应有之中气在次月
			return '闰', ydy, yxy, qdy_0, qxy_0, qxf_0  # 有闰返回下月朔及本月中气
		else:
			return '', ydy, yxy, qdy, qxy, qxf  # 无闰返回下月朔及下月中气

	def __repr__(self):
		return '{}-{}'.format(self.lm, self.type)

class Sfl(Li):
	type = 1  # 第一类：四分历
	yfa = 27759
	srf = 940
	bf = 76
	sz = 1461
	qrf = 4
	df = 32
	zs = 19
	zr = 7
	jys = 605
	qfm = 1
	qxf = 0

	def __init__(self, name, liyuan, **kwargs):
		self.sz *= (self.df / self.qrf)
		self.qrf = self.df
		Li.__init__(self, name, liyuan, self.yfa, self.srf, self.sz, self.qrf)
		self.qdy, self.qxy = divide(self.sz / 12, self.qrf)
		try:
			self.lyjzss = kwargs['lyjzss']
		except:
			self.lyjzss = ['冬至', '子', '子']
		self.basicData(kwargs)
		self.jf = self.bjsgz(self.bf)
		self.yf = self.jf * 60 // math.gcd(self.jf, 60)  # 元法（岁复甲子）

	def basicData(self, kwargs):
		# 可能存在的参数，不存在赋默认值
		self.zqi = self.sui / 12
		self.zq = self.zs * 12 	    # 章气=章岁*12
		self.zy = self.zq + self.zr  # 章月=章气+章闰=章岁*12+章闰
		self.qly = jieqi.index(self.lyjzss[0])
		self.jian = dizhi.index(self.lyjzss[1])
		self.suis = dizhi.index(self.lyjzss[2])
		if 6 < self.suis < 12: self.suis -= 12
		try: self.lyrgz = gz.index(kwargs['lyrgz'])
		except: self.lyrgz = 0
		try:
			self.bsry = kwargs['bsry']
			self.lyry = True  # 有闰余，历元不正
		except:
			self.bsry = 0
			self.lyry = False
		try: self.bm = kwargs['bm']
		except: self.bm = ['蔀']  # 无蔀/纪名

	def array(self, rank):  # 根据不同排表要求修改
		# 建表用数据（修改岁首月确定排表用的每年第一个月）
		rank = 1
		if rank == -1: self.ssy = self.suis if self.suis < 0 else 0     # 冬至和岁首的最小值
		elif rank == 0: self.ssy = 0                                    # 冬至起排
		elif rank == 1: self.ssy = self.suis                            # 从岁首起排
		elif rank == 2: self.ssy = self.suis if self.suis > 0 else 0    # 冬至和岁首的最大值
		if self.qly % 2 == 1:  # 节气为历元，而岁首为中气，需转换
			self.bsry = (((self.zqi/2) / self.yue * 228) - self.zr * ((self.qly+1) / 2 - self.ssy)) / 12  # 单位：月
		self.backYue = self.ssy - (self.qly + 1) // 2
		self.backQi = self.ssy - self.qly / 2
		self.jzy = self.jian - self.ssy  # 建正所在的月

	def dygz(self, dy):  # 由蔀首开始求的大余转为干支需加上蔀首干支序
		if dy == None: return ' 无 '
		gzdy = (dy + self.bsgz[self.rbs]) % 60
		return gz[gzdy]

	def syjn(self, year):  # 算外
		self.sy = -self.ly + self.jys * self.yf  # 上元
		jn = self.sy + year
		if year > 0: jn -= 1  # 实际为jn-=1; if year<0,jn+=1
		return jn


class Psl(Sfl, Li):
	type = 2  # 第二类：使用平朔平气法的历

	def __init__(self, name, liyuan, yfa, srf, sz, qrf, zhang, **kwargs):
		Li.__init__(self, name, liyuan, yfa, srf, sz, qrf)  # 指定父类的构造函数
		try:
			self.qrf = kwargs['df']  # 度法，纪法约/倍数
			self.sz = int(self.sz * self.qrf / qrf)
		except: pass
		if self.sz / 24 != self.sz // 24:
			self.qfm = 24
			self.qxf = int(self.sz - self.sz // 24 * 24) * 2
		else:
			self.qfm, self.qxf = 1, 0
		self.qdy, self.qxy = divide((self.sz - self.qxf // 2) / 12, self.qrf)
		self.zs, self.zr = zhang
		try: self.lyjzss = kwargs['lyjzss']
		except: self.lyjzss = ['冬至','寅','寅']
		try: self.jf = kwargs['jf']  # 纪法（夜半朔旦冬至）
		except: self.jf = qrf
		self.bf = qrf
		self.basicData(kwargs)
		self.yf = self.bjsgz(self.bf)  # 元法（甲子夜半朔旦冬至）
		try: self.jys = kwargs['jys']
		except: self.jys = 0
