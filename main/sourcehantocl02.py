import os, json, subprocess, platform, tempfile, gc, sys
from collections import defaultdict

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'

fontver='1.008'
fontid='AAF'

def build_glyph_codes():
	glyph_codes = defaultdict(list)
	for codepoint, glyph_name in font['cmap'].items():
		glyph_codes[glyph_name].append(codepoint)
	return glyph_codes
def gettbs(chtat, tbg, isin):
	tb1=set()
	ftype=font['GSUB']['lookups'][chtat]['type']
	for subtable in font['GSUB']['lookups'][chtat]['subtables']:
		for j, t in list(subtable.items()):
			if ftype=='gsub_single':
				cht=t
			elif ftype=='gsub_alternate' and len(t)==1:
				cht=t[0]
			else:
				continue
			if (isin and j in tbg) or ((not isin) and (j not in tbg)):
				tb1.add((j, cht))
	return tb1
def gettrch(j, t):
	if j==t:
		return
	for cod in glyph_codes[j]:
		print('处理', chr(int(cod)))
		font['cmap'][str(cod)] = t
		glyph_codes[t].append(cod)
	glyph_codes[j].clear()
def getgname(s):
	gn=set()
	for ch in s:
		cod=str(ord(ch))
		if cod in font['cmap']:
			gn.add(font['cmap'][cod])
	return gn

def ckfile(f):
	f=f.strip()
	if not os.path.isfile(f):
		if os.path.isfile(f.strip('"')):
			return f.strip('"')
		elif os.path.isfile(f.strip("'")):
			return f.strip("'")
	return f

def setpun(pzh, loczh):
	pg=getgname(pzh)
	zhp=list()
	etb=set()
	ztb=set()
	for tb in loczh:
		allen=0
		for ctb in font['GSUB']['lookups'][tb]['subtables']:
			allen+=len(ctb)
		if allen>60:
			ztb.add(tb)
		else:
			etb.add(tb)
	for tb in ztb:
		for subtable in font['GSUB']['lookups'][tb]['subtables']:
			for j, t in list(subtable.items()):
				for p1 in pzh:
					cod=str(ord(p1))
					if cod in font['cmap']:
						g=font['cmap'][cod]
						if g==j:
							zhp.append((cod, t))
	for tb in etb:
		a=gettbs(tb, pg, True)
		if len(a)>0:
			for itm in a:
				gettrch(itm[0], itm[1])
	for punzh in zhp:
		print('处理', chr(int(punzh[0])))
		font['cmap'][punzh[0]]=punzh[1]

def creattmp(mch, pun, simp):
	print('获取本地化列表...')
	loc=set()
	lockor=set()
	loczhs=set()
	loczht=set()
	loczhhk=set()
	for lang in font['GSUB']['languages'].keys():
		for fs in font['GSUB']['languages'][lang]['features']:
			if fs.split('_')[0]=='locl':
				loc.update(set(font['GSUB']['features'][fs]))
				if lang.split('_')[-1].strip()=='KOR':
					lockor.update(set(font['GSUB']['features'][fs]))
				elif lang.split('_')[-1].strip()=='ZHS':
					loczhs.update(set(font['GSUB']['features'][fs]))
				elif lang.split('_')[-1].strip()=='ZHT':
					loczht.update(set(font['GSUB']['features'][fs]))
				elif lang.split('_')[-1].strip()=='ZHH':
					loczhhk.update(set(font['GSUB']['features'][fs]))

	#exgl=getgname(exch)
	pen='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
	pzhs='·’‘”“•≤≥≮≯！：；？'+pen
	pzht='·’‘”“•、。，．'+pen
	sip=str()
	sipch='将蒋残浅践与写泻惮禅箪蝉恋峦蛮挛栾滦弯湾径茎弥称滞画遥瑶'#変
	if simp=='2':
		sip+=sipch
	tbs=set()
	if len(sip)>0:
		simpg=getgname(sip)
		for zhstb in loczhs:
			a=gettbs(zhstb, simpg, True)
			tbs.update(a)

	if pun=='2':
		setpun(pzhs, loczhs)
	if pun=='3':
		setpun(pzht, loczht)
	if len(tbs)>0:
		for itm in tbs:
			gettrch(itm[0], itm[1])
	else:
		print('未找到任何可用的本地化字形！')

	print('正在移除本地化列表...')
	for subs in loc:
		del font['GSUB']['lookups'][subs]
		f1todel = set()
		for f1 in font['GSUB']['features'].keys():
			if subs in font['GSUB']['features'][f1]:
				font['GSUB']['features'][f1].remove(subs)
			if len(font['GSUB']['features'][f1]) == 0:
				f1todel.add(f1)
				continue
		for f1 in f1todel:
			del font['GSUB']['features'][f1]

	if mch=='y':
		print('正在合并多编码汉字...')
		vartab=list()
		with open(os.path.join(pydir, 'mulcodechar.txt'), 'r', encoding='utf-8') as f:
			for line in f.readlines():
				line = line.strip()
				if line.startswith('#') or '\t' not in line:
					continue
				s, t = line.strip().split('\t')
				if s and t and s != t:
					if str(ord(t)) in font['cmap']:
						print('处理 '+s+'-'+t)
						font['cmap'][str(ord(s))] = font['cmap'][str(ord(t))]

	fpn=str()
	for n1 in font['name']:
		if n1['nameID']==6 and '-' in n1['nameString']:
			fpn=n1['nameString']
			break

	print('正在设置字体名称...')
	if setname=='1':
		nname=list()
		for nj in font['name']:
			if nj['languageID']==1041:
				nk=dict(nj)
				ns=dict(nj)
				nt=dict(nj)
				nh=dict(nj)
				nk['languageID']=1042
				nk['nameString']=nk['nameString'].replace('源ノ明朝', '본명조').replace('源ノ角ゴシック', '본고딕').replace('源ノ等幅', '본모노')
				ns['languageID']=2052
				ns['nameString']=ns['nameString'].replace('源ノ明朝', '思源宋体').replace('源ノ角ゴシック', '思源黑体').replace('源ノ等幅', '思源等宽')
				nt['languageID']=1028
				nt['nameString']=nt['nameString'].replace('源ノ明朝', '思源宋體').replace('源ノ角ゴシック', '思源黑體').replace('源ノ等幅', '思源等寬')
				nh['languageID']=3076
				nh['nameString']=nh['nameString'].replace('源ノ明朝', '思源宋體 香港').replace('源ノ角ゴシック', '思源黑體 香港').replace('源ノ等幅', '思源等寬 香港')
				nname.append(nk)
				nname.append(ns)
				nname.append(nt)
				nname.append(nh)
		font['name']=font['name']+nname
	elif setname=='2':
		fnn='Advocate Ancient'
		fnnps='AdvocateAncient'
		if 'CFF_' in font:
			font['CFF_']['notice']=''
			font['CFF_']['fontName']=font['CFF_']['fontName'].replace('SourceHan', fnnps)
			font['CFF_']['fullName']=font['CFF_']['fullName'].replace('Source Han', fnn)
			font['CFF_']['familyName']=font['CFF_']['familyName'].replace('Source Han', fnn)
			if 'fdArray' in font['CFF_']:
				nfd=dict()
				for k in font['CFF_']['fdArray'].keys():
					nfd[k.replace('SourceHan', fnnps)]=font['CFF_']['fdArray'][k]
				font['CFF_']['fdArray']=nfd
				for gl in font['glyf'].values():
					if 'CFF_fdSelect' in gl:
						gl['CFF_fdSelect']=gl['CFF_fdSelect'].replace('SourceHan', fnnps)

		font['OS_2']['achVendID']=fontid
		font['head']['fontRevision']=float(fontver)

		enn=['Advocate Ancient Sans', 'Advocate Ancient Serif', 'Advocate Ancient Mono']
		ennps=['AdvocateAncientSans', 'AdvocateAncientSerif', 'AdvocateAncientMono']
		scn=['尙古黑体', '尙古明体', '尙古等宽']
		tcn=['尙古黑體', '尙古明體', '尙古等寬']
		locn=""
		if mch=='n' and pun=='2'and simp=='2':
			locn='SC'
		elif mch=='n' and pun=='1' and simp=='1':
			locn='JP'
		elif mch=='n' and pun=='3':
			locn='TC'
		nname=list()
		for nj in font['name']:
			if nj['languageID']==1041:
				ns=dict(nj)
				nt=dict(nj)
				nh=dict(nj)
				if 'JP'==locn:
					njn=dict(nj)
					njn['nameString']=njn['nameString'].replace('源ノ', '尙古')
					nname.append(njn)
				ns['languageID']=2052
				ns['nameString']=ns['nameString'].replace('源ノ角ゴシック', scn[0]+locn).replace('源ノ明朝', scn[1]+locn).replace('源ノ等幅', scn[2]+locn)
				nt['languageID']=1028
				nt['nameString']=nt['nameString'].replace('源ノ角ゴシック', tcn[0]+locn).replace('源ノ明朝', tcn[1]+locn).replace('源ノ等幅', tcn[2]+locn)
				nh['languageID']=3076
				nh['nameString']=nh['nameString'].replace('源ノ角ゴシック', tcn[0]+locn).replace('源ノ明朝', tcn[1]+locn).replace('源ノ等幅', tcn[2]+locn)
				nname.append(ns)
				nname.append(nt)
				nname.append(nh)
			#elif nj['nameID']>0 and nj['nameID']<7:
			elif nj['nameID']==3:
				ne=dict(nj)
				ne['nameString']=fontver+';'+fontid+';'+fpn.replace('SourceHanSans', ennps[0]+locn).replace('SourceHanSerif', ennps[1]+locn).replace('SourceHanMono', ennps[2]+locn)
				nname.append(ne)
			elif nj['nameID']==5:
				ne=dict(nj)
				ne['nameString']='Version '+fontver
				nname.append(ne)
			elif nj['nameID']==11:
				ne=dict(nj)
				ne['nameString']='https://github.com/GuiWonder/SourceHanToClassic'
				nname.append(ne)
			elif nj['nameID']!=0 and nj['nameID']!=7 and nj['nameID']!=8:
			#else:
				ne=dict(nj)
				ne['nameString']=ne['nameString'].replace('Source Han Sans', enn[0]+' '+locn).replace('Source Han Serif', enn[1]+' '+locn).replace('Source Han Mono', enn[2]+' '+locn).replace('SourceHanSans', ennps[0]+locn).replace('SourceHanSerif', ennps[1]+locn).replace('SourceHanMono', ennps[2]+locn)
				nname.append(ne)
		font['name']=nname
	
	elif setname=='3':
		pname=enname.replace(' ', '')
		nname=list()
		for nj in font['name']:
			if nj['languageID']==1041:
				ns=dict(nj)
				nt=dict(nj)
				nh=dict(nj)
				ns['languageID']=2052
				ns['nameString']=ns['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nt['languageID']=1028
				nt['nameString']=nt['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nh['languageID']=3076
				nh['nameString']=nh['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nname.append(ns)
				nname.append(nt)
				nname.append(nh)
			#elif nj['nameID']>0 and nj['nameID']<7:
			else:
				ne=dict(nj)
				ne['nameString']=ne['nameString'].replace('Source Han Sans', enname).replace('SourceHanSans', pname).replace('Source Han Serif', enname).replace('SourceHanSerif', pname).replace('Source Han Mono', enname).replace('SourceHanMono', pname)
				nname.append(ne)
		font['name']=nname
		if 'CFF_' in font:
			font['CFF_']['fontName']=font['CFF_']['fontName'].replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)
			font['CFF_']['fullName']=font['CFF_']['fullName'].replace('Source Han Sans', enname).replace('Source Han Serif', enname).replace('Source Han Mono', enname)
			font['CFF_']['familyName']=font['CFF_']['familyName'].replace('Source Han Sans', enname).replace('Source Han Serif', enname).replace('Source Han Mono', enname)
			if 'fdArray' in font['CFF_']:
				nfd=dict()
				for k in font['CFF_']['fdArray'].keys():
					nfd[k.replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)]=font['CFF_']['fdArray'][k]
				font['CFF_']['fdArray']=nfd
				for gl in font['glyf'].values():
					if 'CFF_fdSelect' in gl:
						gl['CFF_fdSelect']=gl['CFF_fdSelect'].replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)

	print('正在生成字体...')
	tmpfile = tempfile.mktemp('.json')
	with open(tmpfile, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	return tmpfile

print('====思源字体（日版）转传承字形====\n')
inf=str()
outf=str()
mch=str()
pun=str()
simp=str()
setname=str()
enname=str()
zhname=str()
if len(sys.argv)<3:
	while not os.path.isfile(inf):
		inf=input('请输入字体文件路径（或拖入文件）：\n')
		inf=ckfile(inf)
		if not os.path.isfile(inf):
			print('文件不存在，请重新选择！\n')
	while not outf.strip():
		outf=input('请输入输出文件：\n')
else:
	inf=sys.argv[1]
	outf=sys.argv[2]
if len(sys.argv)<6:
	while mch not in {'y', 'n'}:
		mch=input('是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？(输入Y/N)：\n').lower()
	while pun not in {'1', '2', '3'}:
		pun=input('请选择标点：\n\t1.日本\n\t2.简体中文\n\t3.正体中文（居中）\n')
	while simp not in {'1', '2'}:
		simp=input('请选择简化字字形：\n\t1.日本\n\t2.中国大陆\n')
else:
	mch=sys.argv[3].lower()
	pun=sys.argv[4]
	simp=sys.argv[5]

if len(sys.argv)<7:
	while setname not in {'1', '2', '3'}:
		#setname=input('字体名称设置：\n\t1.使用思源原版字体名称\n\t2.使用尙古黑体、尙古明体\n\t3.我来命名\n')
		setname=input('字体名称设置：\n\t2.使用尙古黑体、尙古明体 Advocate Ancient\n\t3.我来命名\n')
else:
	setname=sys.argv[6]
if setname=='3':
	if len(sys.argv)<10:
		while not enname.strip():
			enname=input('请输入英文字体名称：\n')
		while not zhname.strip():
			zhname=input('请输入中字体名称：\n')
	else:
		enname=sys.argv[7]
		zhname=sys.argv[8]

print('正在载入字体...')
font = json.loads(subprocess.check_output((otfccdump, '--no-bom', inf)).decode("utf-8", "ignore"))
glyph_codes = build_glyph_codes()
tmpfile=creattmp(mch, pun, simp)

for x in set(locals().keys()):
	if x not in ('os', 'subprocess', 'otfccbuild', 'outf', 'tmpfile', 'gc'):
		del locals()[x]
gc.collect()
print('正在生成字体文件...')
subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', outf, tmpfile))
os.remove(tmpfile)
print('完成!')
