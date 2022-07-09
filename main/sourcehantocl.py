import os, json, subprocess, platform, gc
from collections import defaultdict

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() == 'Mac':
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'

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
def creattmp(mch, pun, simp):
	print('获取本地化列表...')
	loc=set()
	lockor=set()
	loczhs=set()
	loczht=set()
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

	exch='侾倜兎剪叟呀咎咠唹嚳墁奜媺嬴孼宬岈巓幃幰廋微徵恝惆惘搜撐於旅旣晧晷曁杓栲桯梏檉毒氓汋汒沿淤湔溲滾漰潛潤澔瀆瀛灼煎煢爟牘牙牚犢獌珵珹琱甿瘦瞎瞬砑稠稧穿窖竇箭篠簉糙糱絳綢緯繭續罔羸肓腴膄臝臾舛舜舞船艘芒茫萸蒯蕣虻蚌蜩蟃衮袞裒裯襁覿訝訹誥讀豹負賙贏贖趼輞迓邙郜鄰鉛鋥鎉鏹閼降隙雕靠颼馰騪驎驘鬋魍鮵鴉鵠鵩鵰麗麟黷'
	sipmch='寿写将弥弯径恋条残涙浅滞涛湾炉画皐禅祷称茎蒋蚕蛮変践鋳覇'
	pzhs='·’‘”“•≤≥≮≯！：；？'
	pzht='·’‘”“•、。，．'
	exgl=getgname(exch)
	sip=str()
	trd=str()
	if pun=='2':
		sip+=pzhs
	if pun=='3':
		trd+=pzht
	if simp=='2':
		sip+=sipmch

	tbs=set()
	for krtb in lockor:
		a=gettbs(krtb, exgl, False)
		if len(a)>200:
			tbs.update(a)
	if len(sip)>0:
		simpg=getgname(sip)
		for zhstb in loczhs:
			a=gettbs(zhstb, simpg, True)
			tbs.update(a)
	if len(trd)>0:
		trdg=getgname(trd)
		for zhttb in loczht:
			a=gettbs(zhttb, trdg, True)
			tbs.update(a)
	if len(tbs)>0:
		for itm in tbs:
			gettrch(itm[0], itm[1])
	else:
		print('未找到任何可用的本地化字形！')

	print('正在移除本地化列表...')
	vgl=set()
	for subs in loc:
		if rmun=='y':
			ftype=font['GSUB']['lookups'][subs]['type']
			for subtable in font['GSUB']['lookups'][subs]['subtables']:
				for j, t in list(subtable.items()):
					if ftype=='gsub_single':
						vgl.add(t)
						vgl.add(j)

		del font['GSUB']['lookups'][subs]
		f1todel = set()
		for f1 in font['GSUB']['features'].keys():
			if subs in font['GSUB']['features'][f1]:
				font['GSUB']['features'][f1].remove(subs)
			if len(font['GSUB']['features'][f1]) == 0:
				f1todel.add(f1)
				continue
		for  f1 in f1todel:
			del font['GSUB']['features'][f1]
	print('正在处理异体字信息...')
	dv=dict()
	for k in font['cmap_uvs'].keys():
		c, v=k.split(' ')
		if c not in dv:
			dv[c]=dict()
		dv[c][v]=font['cmap_uvs'][k]
	tv=dict()
	with open('uvs-get-jp1-MARK.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			if line.startswith('#'):
				continue
			line=line.strip()
			if line.endswith('X'):
				a=line.split(' ')
				tv[str(ord(a[0]))]=str(int(a[3].strip('X'), 16))

	for k in dv.keys():
		if k in tv:
			if tv[k] in dv[k]:
				print('处理', chr(int(k)))
				tch=dv[k][tv[k]]
				font['cmap'][k]=tch
	if mch=='y':
		print('正在合并多编码汉字...')
		vartab=list()
		with open('mulcodechar.txt', 'r', encoding='utf-8') as f:
			for line in f.readlines():
				line = line.strip()
				if line.startswith('#') or '\t' not in line:
					continue
				s, t = line.strip().split('\t')
				if s and t and s != t:
					vartab.append((s, t))
		for chs in vartab:
			unis=str(ord(chs[0]))
			unit=str(ord(chs[1]))
			if unit in font['cmap']:
				print('处理 '+chs[0]+'-'+chs[1])
				gn=font['cmap'][unit]
				font['cmap'][unis] = gn
	if rmun=='y':
		print('正在移除字形...')
		glyph_codes = build_glyph_codes()
		for v1 in vgl:
			if len(glyph_codes[v1])<1:
				#print('移除', v1)
				del glyph_codes[v1]
				try:
					font['glyph_order'].remove(v1)
				except ValueError:
					pass
				del font['glyf'][v1]

	print('正在设置字体名称...')
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
	print('正在生成字体...')
	tmpfile='tmp.json'
	with open(tmpfile, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	return tmpfile
inf=str()
outf=str()
print('====思源字体（日版）转传承字形====\n')
while not os.path.isfile(inf):
	inf=input('请输入字体文件路径（或拖入文件）：\n')
	inf=ckfile(inf)
	if not os.path.isfile(inf):
		print('文件不存在，请重新选择！\n')
while not outf.strip():
	outf=input('请输入输出文件：\n')
mch=str()
while mch not in {'y', 'n'}:
	mch=input('是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？(输入Y/N)：\n').lower()
pun=str()
while pun not in {'1', '2', '3'}:
	pun=input('请选择标点：\n\t1.日本.\n\t2.简体中文\n\t3.正体中文（居中）\n')
simp=str()
while simp not in {'1', '2'}:
	simp=input('请选择简化字字形：\n\t1.日本\n\t2.中国大陆\n')
rmun=str()
while rmun not in {'y', 'n'}:
	rmun=input('是否移除未使用的字形(输入Y/N)：\n').lower()

print('正在载入字体...')
font = json.loads(subprocess.check_output((otfccdump, '--no-bom', inf)).decode("utf-8", "ignore"))
glyph_codes = build_glyph_codes()
tmpfile=creattmp(mch, pun, simp)

for x in set(locals().keys()):
	if x not in ('os', 'subprocess', 'otfccbuild', 'outf', 'tmpfile', 'gc'):
		del locals()[x]
gc.collect()
print('正在生成字体文件...')
subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', outf, tmpfile))
os.remove(tmpfile)
print('完成!')

