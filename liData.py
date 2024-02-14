from liClass import *

# Sfl参数：历名, 历元，lyjzss=[历元，建正，岁首], bsry=蔀首闰余, lyrgz=历元日干支
# Sfl默认值：lyjzss=['冬至','子','子'], bsry=0，lyrgz='甲子'
# Psl参数：历名, 历元，月法，朔日法，岁周，气日法，[章岁，章闰]，df=度法，jys=积元数，bm=[蔀/纪名]
# Psl默认值：df=蔀法，jys=0，bm=['蔀']，lyjzss=['冬至','寅','寅'],
# 各历法参数名称不同，可能混淆，应根据各数据意义填入。本程序中各变量含义：
#   月法/朔日法＝朔策（月法可填入朔余）。四分历月法即蔀日，朔日法即蔀月。
#   岁周/气日法＝岁实。（岁周可填入斗分，不用岁差的历法岁周即周天）
#   关系：(月法/朔日法)*(章月/章岁)＝岁周/气日法
#   度法：指定时气日法为度法
#   章法：朔旦冬至齐同
#   蔀法：夜半朔旦冬至齐同，无小余。蔀名设为'纪'则称纪法（其他名称同理）。
#   纪法：甲子夜半朔旦冬至齐同。无蔀法之平朔历同四分历之蔀法，夜半朔旦冬至齐同。
#   元法：岁复甲子（上元岁名）。无蔀法之平朔历同四分历之纪法，甲子夜半朔旦冬至齐同。
#   积元数：近元至上元元数，用来求上元积年。

hdl = Sfl('黄帝历', -1350)
zxl = Sfl('颛顼历', -1506, lyjzss=['立春','寅','亥'], lyrgz='己巳')
xl = Sfl('夏历',    -1076, lyjzss=['雨水','寅','寅'])
rxl = Sfl('真夏历', -1076, lyjzss=['冬至','寅','子'])
yl = Sfl('殷历',    -1567)
zl = Sfl('周历',    -1624)
ll0 = Sfl('鲁历0',  -4881)
ll1 = Sfl('鲁历1',  -2001, bsry=1)
tcl = Psl('太初历', -104, 2392, 81, 562120, 1539, [19,7], df=4617, jys=31, bm=['统','天','地','人'])
sfl = Sfl('四分历', -1681, lyjzss=['冬至','寅','寅'])
qxl = Psl('乾象历', -104, 43026, 1457, 215130, 589, [19,7], jys=3, bm=['纪','内','外'])
jcl = Psl('景初历', -3809, 134630, 4559, 673150, 1843, [19,7], bm=['纪'])
jjl = Psl('姜岌历', -83457, 179044, 6063, 605, 2451, [19,7], bm=['纪'])
xsl = Psl('玄始历', -61027, 2629759, 89052, 1759, 7200, [600, 221], jf=72000)
yjl = Psl('元嘉历', -5261, 22207, 752, 222070, 608, [19,7], df=304, lyjzss=['雨水','寅','寅'], bm=['纪'])
dml = Psl('大明历', -51477, 116321, 3939, 14423804, 39491, [391,144], bm=['纪'])
zgl = Psl('正光历', -167229, 2213377, 74952, 2213377, 6060, [505,186], jf=60600)
xhl = Psl('兴和历', -293457, 6158017, 208530, 6158017, 16860, [562,207], jf=168600)
lxsl = Psl('孝孙历', -434517, 33783, 1144, 1966, 8047, [619, 228], jf=160940)
tbl = Psl('天保历', -109977, 8641687, 292635, 8641687, 23660, [676,249], bm=['纪'])
thl = Psl('天和历', -875227, 153991, 290160, 5731, 23460, [391,144])
dxl = Psl('大象历', -40975, 1581749, 53563, 3167, 12992, [448,165])
khl = Psl('开皇历', -4128417, 5372209, 181920, 25063, 102960, [429,158])
dyl = Psl('大业历', -1427037, 33783, 1144, 15573963, 42640, [410,151], bm=['纪'])

lb = [hdl, zxl, xl, rxl, yl, zl, ll0, ll1, tcl, sfl, qxl, xsl, yjl, dml, zgl, xhl, tbl, dxl, khl, dyl]

gllb = [-427, -104, hdl, zxl, xl, rxl, yl, zl, ll0, ll1]
wbxnb = [jjl, lxsl]  # 未颁行历法
bxnb = [[-104, 84, tcl], [85, 263, sfl], [223, 280, qxl], [237, 451, jcl], [402, 522, xsl], [445, 509, yjl], [510, 589, dml],
        [523, 558, zgl], [540, 550, xhl], [551, 557, tbl], [566, 578, thl], [579, 583, dxl], [584, 596, dxl], [597, 618, dyl]]