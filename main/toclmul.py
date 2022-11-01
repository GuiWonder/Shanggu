import os, json, subprocess, platform, tempfile, gc, sys

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'

def ckfile(f):
	f=f.strip()
	if not os.path.isfile(f):
		if os.path.isfile(f.strip('"')):
			return f.strip('"')
		elif os.path.isfile(f.strip("'")):
			return f.strip("'")
	return f

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

def replg(dic):
	for cd in list(font['cmap'].keys()):
		if font['cmap'][cd] in dic:
			print('处理', chr(int(cd)))
			font['cmap'][cd]=dic[font['cmap'][cd]]

def getgname(s):
	gn=set()
	for ch in s:
		cod=str(ord(ch))
		if cod in font['cmap']:
			gn.add(font['cmap'][cod])
	return gn

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
			relp=dict()
			for itm in a:
				if itm[0]!=itm[1]:
					relp[itm[0]]=itm[1]
			replg(relp)
	for punzh in zhp:
		print('处理', chr(int(punzh[0])))
		font['cmap'][punzh[0]]=punzh[1]

def gfmloc(g, loczh):
	for zhtb in loczh:
		ftype=font['GSUB']['lookups'][zhtb]['type']
		if ftype=='gsub_single':
			for subtable in font['GSUB']['lookups'][zhtb]['subtables']:
				if g in subtable:
					return subtable[g]
	return ""
###
def getscl(font2):
	scl = 1.0
	if font["head"]["unitsPerEm"] != font2["head"]["unitsPerEm"]:
		scl = font["head"]["unitsPerEm"] / font2["head"]["unitsPerEm"]
	return scl

def getfontgl(filec, cfgf):
	ofcfg=json.load(open(cfgf, 'r', encoding = 'utf-8'))
	fontoth = json.loads(subprocess.check_output((otfccdump, '--no-bom', filec)).decode("utf-8", "ignore"))
	if 'chars' in ofcfg:
		getotherch(fontoth, ofcfg['chars'])
	if 'uvs' in ofcfg:
		getotheruv(fontoth, ofcfg['uvs'])
	if 'charssp' in ofcfg:
		spch=ofcfg['charssp']
		for ch in spch:
			g1=gfmloc(font['cmap'][str(ord(ch))], loczhs)
			g2=fontoth['cmap'][str(ord(ch))]
			cpglyf(font['glyf'][g1], fontoth['glyf'][g2], 1.0)

def getotherch(font2, chars):
	scl = getscl(font2)
	for ch in chars:
		uni=str(ord(ch))
		if uni in font2['cmap'] and uni in font['cmap']:
			g1=font['cmap'][uni]
			g2=font2['cmap'][uni]
			print('处理', ch)
			font['glyf'][g1]=cpglyf(font['glyf'][g1], font2['glyf'][g2], scl)

def getotheruv(font2, uv):
	scl = getscl(font2)
	oldu=set()
	newu=dict()
	for ch in uv.keys():
		if str(ord(ch)) not in font['cmap']:
			continue
		print('处理', ch)
		g1=font['cmap'][str(ord(ch))]
		g2=font2['cmap_uvs'][str(ord(ch))+' '+str(int(uv[ch], 16))]
		font['glyf'][g1]=cpglyf(font['glyf'][g1], font2['glyf'][g2], scl)
		if g1 in font['cmap_uvs'].values():
			print('更正uvs', ch)
			oldu.add(g1)
			newu[str(ord(ch))+' '+str(int(uv[ch], 16))]=g1
	for u1 in set(font['cmap_uvs'].keys()):
		if font['cmap_uvs'][u1] in oldu:
			del font['cmap_uvs'][u1]
	for u2 in newu.keys():
		font['cmap_uvs'][u2]=newu[u2]

def cpglyf(gl1, gl2, scl):
	gnew=dict()
	if 'CFF_fdSelect' in gl1:
		gnew['CFF_fdSelect']=gl1['CFF_fdSelect']
	if 'CFF_CID' in gl1:
		gnew['CFF_CID']=gl1['CFF_CID']
	for k in gl2.keys():
		if k not in ('CFF_fdSelect', 'CFF_CID'):
			gnew[k]=gl2[k]
	if scl != 1.0:
		sclglyph(gnew, scl)
	return gnew

def sclglyph(glyph, scl):
	glyph['advanceWidth'] = round(glyph['advanceWidth'] * scl)
	if 'advanceHeight' in glyph:
		glyph['advanceHeight'] = round(glyph['advanceHeight'] * scl)
		glyph['verticalOrigin'] = round(glyph['verticalOrigin'] * scl)
	if 'contours' in glyph:
		for contour in glyph['contours']:
			for point in contour:
				point['x'] = round(point['x'] * scl);
				point['y'] = round(point['y'] * scl);
	if 'references' in glyph:
		for reference in glyph['references']:
			reference['x'] = round(scl * reference['x'])
			reference['y'] = round(scl * reference['y'])
	if 'stemH' in glyph:
		for stemh in glyph['stemH']:
			stemh['position'] = round(scl * stemh['position'])
			stemh['width'] = round(scl * stemh['width'])
	if 'stemV' in glyph:
		for stemv in glyph['stemV']:
			stemv['position'] = round(scl * stemv['position'])
			stemv['width'] = round(scl * stemv['width'])

def step1():
	rmun='2'
	jpre=dict()
	jpvar=[('𰰨', '芲'), ('𩑠', '頙')]
	for chs in jpvar:
		if str(ord(chs[1])) in font['cmap']:
			jpre[str(ord(chs[0]))]=font['cmap'][str(ord(chs[1]))]
	shset=json.load(open(os.path.join(pydir, 'sourcehan.json'), 'r', encoding = 'utf-8'))
	krch=shset['krgl']
	tcch=shset['tcgl']
	hcch=shset['hcgl']
	scch=shset['scgl']
	tbs=set()
	#for krtb in lockor:
	#	a=gettbs(krtb, xkrchg, False)
	#	if len(a)>200:
	#		tbs.update(a)
	if len(krch)>0:
		krchg=getgname(krch)
		for zhktb in lockor:
			a=gettbs(zhktb, krchg, True)
			tbs.update(a)
	if len(tcch)>0:
		tcchg=getgname(tcch)
		for zhttb in loczht:
			a=gettbs(zhttb, tcchg, True)
			tbs.update(a)
	if len(hcch)>0:
		hcchg=getgname(hcch)
		for zhhtb in loczhhk:
			a=gettbs(zhhtb, hcchg, True)
			tbs.update(a)
	if len(scch)>0:
		scchg=getgname(scch)
		for zhstb in loczhs:
			a=gettbs(zhstb, scchg, True)
			tbs.update(a)
	if len(tbs)>0:
		repva=dict()
		for itm in tbs:
			if itm[0]!=itm[1]:
				repva[itm[0]]=itm[1]
		replg(repva)
	else:
		print('未找到任何可用的本地化字形！')

	locscv=[('𫜹', '彐'), ('𣽽', '潸')]
	for lv1 in locscv:
		gv2=gfmloc(font['cmap'][str(ord(lv1[1]))], loczhs)
		if gv2:
			print('处理', lv1[0])
			font['cmap'][str(ord(lv1[0]))]=gv2

	for jco in jpre.keys():
		font['cmap'][jco]=jpre[jco]

	print('正在处理异体字信息...')
	dv=dict()
	uvsgly=set()
	for k in font['cmap_uvs'].keys():
		c, v=k.split(' ')
		if c not in dv:
			dv[c]=dict()
		dv[c][v]=font['cmap_uvs'][k]
		if rmun!='3':
			uvsgly.add(font['cmap_uvs'][k])
	tv=dict()
	with open(os.path.join(pydir, 'uvs-get-jp1-MARK.txt'), 'r', encoding='utf-8') as f:
		for line in f.readlines():
			line=line.strip()
			if line.startswith('#'):
				continue
			if line.endswith('X'):
				a=line.split(' ')
				tv[str(ord(a[0]))]=str(int(a[3].strip('X'), 16))
	for k in dv.keys():
		if k in tv:
			if tv[k] in dv[k]:
				print('处理', chr(int(k)))
				tch=dv[k][tv[k]]
				font['cmap'][k]=tch

	uvsmul=[('⺼', '月', 'E0100'), ('𱍐', '示', 'E0100'), ('䶹', '屮', 'E0101'), ('𠾖', '器', 'E0100'), ('𡐨', '壄', 'E0100'), ('𤥨', '琢', 'E0101'), ('𦤀', '臭', 'E0100'), ('𨺓', '隆', 'E0100'), ('𫜸', '叱', 'E0101')]
	for uvm in uvsmul:
		u1=str(ord(uvm[0]))
		u2=str(ord(uvm[1]))
		usel=str(int(uvm[2], 16))
		if u2 in dv and usel in dv[u2]:
			print('处理 ', uvm[0])
			font['cmap'][u1]=dv[u2][usel]

	radic=[('⽉', '月'), ('⻁', '虎'), ('⽛', '牙'), ('⾳', '音'), ('⿓', '龍')]
	for chs in radic:
		if str(ord(chs[1])) in font['cmap']:
			print('处理 ', chs[0])
			font['cmap'][str(ord(chs[0]))] = font['cmap'][str(ord(chs[1]))]
	
	print('正在检查其他字形...')
	if 'CFF_' in font:
		ffmt='.otf'
	else:
		ffmt='.ttf'
	ssty=str()
	if 'Sans' in fpn or 'Mono' in fpn:
		ssty='Sans'
	elif 'Serif' in fpn:
		ssty='Serif'
	wt=str()
	wtn={250:'ExtraLight', 300:'Light', 350:'Normal', 400:'Regular', 500:'Medium', 600:'SemiBold', 700:'Bold', 900:'Heavy'}
	if font['OS_2']['usWeightClass'] in wtn:
		wt=wtn[font['OS_2']['usWeightClass']]
	
	print('正在获取1.0版字形...')
	file10=os.path.join(pydir, f'sourcehan1.0/SourceHan{ssty}-{wt}{ffmt}')
	if os.path.isfile(file10):
		sh10set=json.load(open(os.path.join(pydir, 'sourcehan10.json'), 'r', encoding = 'utf-8'))
		font10 = json.loads(subprocess.check_output((otfccdump, '--no-bom', file10)).decode("utf-8", "ignore"))
		getotherch(font10, sh10set[ssty])
		del font10
	else:
		print('获取1.0版字形失败！')
	
	if ssty=='Sans':
		filec=os.path.join(pydir, f'ChiuKongGothic-CL/ChiuKongGothic-CL-{wt}{ffmt}')
		ckgcf=os.path.join(pydir, 'ChiuKongGothic-CL.json')
		if os.path.isfile(filec) and os.path.isfile(ckgcf):
			print('正在获取秋空黑体字形...')
			getfontgl(filec, ckgcf)

	usedg=set()
	usedg.update(font['cmap'].values())
	if rmun=='2':
		usedg.update(uvsgly)
	pungl=getgname(pzhs+pzht+simpcn)
	print('正在检查本地化替换表...')
	for subs in loc:
		ftype=font['GSUB']['lookups'][subs]['type']
		for subtable in font['GSUB']['lookups'][subs]['subtables']:
			for j, t in list(subtable.items()):
				if ftype=='gsub_single':
					if j in pungl or t in pungl:
						usedg.add(j)
						usedg.add(t)
					else:
						del subtable[j]
	if rmun=='1' or rmun=='2':
		print('正在移除字形...')
		if 'GSUB' in font:
			for lkn in font['GSUB']['lookupOrder']:
				if lkn in font['GSUB']['lookups']:
					lookup=font['GSUB']['lookups'][lkn]
					if lookup['type'] == 'gsub_single':
						for subtable in lookup['subtables']:
							for g1, g2 in list(subtable.items()):
								if g1 in usedg:
									usedg.add(g2)
					elif lookup['type'] == 'gsub_alternate':
						for subtable in lookup['subtables']:
							for item in set(subtable.keys()):
								if item in usedg:
									usedg.update(set(subtable[item]))
					elif lookup['type'] == 'gsub_ligature': 
						for subtable in lookup['subtables']:
							for item in subtable['substitutions']:
								if set(item['from']).issubset(usedg):
									usedg.add(item['to'])
					elif lookup['type'] == 'gsub_chaining':
						for subtable in lookup['subtables']:
							for ls in subtable['match']:
								for l1 in ls:
									usedg.update(set(l1))
		
		unusegl=set()
		unusegl.update(set(font['glyph_order']))
		notg={'.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'}
		unusegl.difference_update(notg)
		unusegl.difference_update(usedg)
		for ugl in unusegl:
			font['glyph_order'].remove(ugl)
			del font['glyf'][ugl]
		
		print('正在检查Lookup表...')
		if 'GSUB' in font:
			for lookup in font['GSUB']['lookups'].values():
				if lookup['type'] == 'gsub_single':
					for subtable in lookup['subtables']:
						for g1, g2 in list(subtable.items()):
							if g1 in unusegl or g2 in unusegl:
								del subtable[g1]
				elif lookup['type'] == 'gsub_alternate':
					for subtable in lookup['subtables']:
						for item in set(subtable.keys()):
							if item in unusegl or len(set(subtable[item]).intersection(unusegl))>0:
								del subtable[item]
				elif lookup['type'] == 'gsub_ligature': 
					for subtable in lookup['subtables']:
						s1=list()
						for item in subtable['substitutions']:
							if item['to'] not in unusegl and len(set(item['from']).intersection(unusegl))<1:
								s1.append(item)
						subtable['substitutions']=s1
				elif lookup['type'] == 'gsub_chaining':
					for subtable in lookup['subtables']:
						for ls in subtable['match']:
							for l1 in ls:
								l1=list(set(l1).difference(unusegl))
		if 'GPOS' in font:
			for lookup in font['GPOS']['lookups'].values():
				if lookup['type'] == 'gpos_single':
					for subtable in lookup['subtables']:
						for item in list(subtable.keys()):
							if item in unusegl:
								del subtable[item]
				elif lookup['type'] == 'gpos_pair':
					for subtable in lookup['subtables']:
						for item in list(subtable['first'].keys()):
							if item in unusegl:
								del subtable['first'][item]
						for item in list(subtable['second'].keys()):
							if item in unusegl:
								del subtable['second'][item]
				elif lookup['type'] == 'gpos_mark_to_base':
					nsb=list()
					for subtable in lookup['subtables']:
						gs=set(subtable['marks'].keys()).union(set(subtable['bases'].keys()))
						if len(gs.intersection(unusegl))<1:
							nsb.append(subtable)
					lookup['subtables']=nsb

###
def rmloc():
	print('正在移除本地化替换表...')
	for subs in loc:
		del font['GSUB']['lookups'][subs]
		f1todel = set()
		for f1 in font['GSUB']['features'].keys():
			if subs in font['GSUB']['features'][f1]:
				font['GSUB']['features'][f1].remove(subs)
			if len(font['GSUB']['features'][f1]) == 0:
				f1todel.add(f1)
		for f1 in f1todel:
			del font['GSUB']['features'][f1]

def setinf():
	font['OS_2']['achVendID']=cfg['fontID']
	font['head']['fontRevision']=float(cfg['fontVersion'])
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

def mkname(hwit=''):
	if hwit=='hw':
		hw=' HW'
	else:
		hw=''
	isit=hwit=='it'
	if isit:
		toit='It'
		toitl=' Italic'
	else:
		toit=''
		toitl=''
	scn=[cfg['fontNameSC']+'黑体', cfg['fontNameSC']+'明体', cfg['fontNameSC']+'等宽']
	tcn=[cfg['fontNameTC']+'黑體', cfg['fontNameTC']+'明體', cfg['fontNameTC']+'等寬']
	locn=""
	if mch=='n' and pun=='2'and simp=='2':
		locn=' SC'
	elif mch=='n' and pun=='1' and simp=='1':
		locn=' JP'
	elif mch=='n' and pun=='3':
		locn=' TC'
	locnp=locn.strip()
	
	ofn=dict()
	for nj in font['name']:
		if nj['languageID']==1033:
			if nj['nameID']==1:
				ofn['enn']=nj['nameString']
			if nj['nameID']==16:
				ofn['ennzx']=nj['nameString']
			if nj['nameID']==2:
				ofn['enfml']=nj['nameString']
			if nj['nameID']==17:
				ofn['enfmlzx']=nj['nameString']
			if nj['nameID']==13:
				ofn['cpsp']=nj['nameString']
			if nj['nameID']==14:
				ofn['cpurl']=nj['nameString']
		if nj['languageID']==1041:
			if nj['nameID']==1:
				ofn['jpn']=nj['nameString']
			if nj['nameID']==16:
				ofn['jpnzx']=nj['nameString']
	newname=list()
	if 'ennzx' in ofn:
		oenn=ofn['ennzx']
		ojpn=ofn['jpnzx']
		fml=ofn['enfmlzx']
	else:
		oenn=ofn['enn']
		ojpn=ofn['jpn']
		fml=ofn['enfml']
	if isit:
		ofn['enfml']=toitl.strip()
	fenn=oenn.replace('Source Han', fnn)
	ftcn=ojpn.replace('源ノ角ゴシック', tcn[0]).replace('源ノ明朝', tcn[1]).replace('源ノ等幅', tcn[2])
	fscn=ojpn.replace('源ノ角ゴシック', scn[0]).replace('源ノ明朝', scn[1]).replace('源ノ等幅', scn[2])
	fenn+=hw+locn
	ftcn+=locnp+hw
	fscn+=locnp+hw
	fpsn=(fenn+'-'+fpn.split('-')[-1]+toit).replace(' ', '')
	fbsh=cfg['fontVersion']+';'+cfg['fontID']+';'+fpsn
	if 'ennzx' in ofn:
		shen=fenn+' '+fml
		shtcn=ftcn+' '+fml
		shscn=fscn+' '+fml
	else:
		shen=fenn
		shtcn=ftcn
		shscn=fscn
		
	for lanid in (1028, 3076):
		newname+=[
			{'languageID': lanid,'nameID': 1,'nameString': shtcn}, 
			{'languageID': lanid,'nameID': 2,'nameString': ofn['enfml']}, 
			{'languageID': lanid,'nameID': 4,'nameString': shtcn+toitl}
			]
		if 'ennzx' in ofn:
			newname+=[
				{'languageID': lanid,'nameID': 16,'nameString': ftcn}, 
				{'languageID': lanid,'nameID': 17,'nameString': fml+toitl}
				]
	newname+=[
		{'languageID': 2052,'nameID': 1,'nameString': shscn}, 
		{'languageID': 2052,'nameID': 2,'nameString': ofn['enfml']}, 
		{'languageID': 2052,'nameID': 4,'nameString': shscn+toitl}
		]
	if 'ennzx' in ofn:
		newname+=[
			{'languageID': 2052,'nameID': 16,'nameString': fscn}, 
			{'languageID': 2052,'nameID': 17,'nameString': fml+toitl}
			]
	newname+=[
		{'languageID': 1033,'nameID': 1,'nameString': shen}, 
		{'languageID': 1033,'nameID': 2,'nameString': ofn['enfml']}, 
		{'languageID': 1033,'nameID': 3,'nameString': fbsh}, 
		{'languageID': 1033,'nameID': 4,'nameString': shen+toitl}, 
		{'languageID': 1033,'nameID': 5,'nameString': 'Version '+cfg['fontVersion']}, 
		{'languageID': 1033,'nameID': 6,'nameString': fpsn}, 
		{'languageID': 1033,'nameID': 9,'nameString': cfg['fontDesigner']}, 
		{'languageID': 1033,'nameID': 10,'nameString': cfg['fontDiscript']}, 
		{'languageID': 1033,'nameID': 11,'nameString': cfg['fontVURL']}, 
		{'languageID': 1033,'nameID': 13,'nameString': ofn['cpsp']}, 
		{'languageID': 1033,'nameID': 14,'nameString': ofn['cpurl']}
		]
	if 'ennzx' in ofn:
		newname+=[
			{'languageID': 1033,'nameID': 16,'nameString': fenn}, 
			{'languageID': 1033,'nameID': 17,'nameString': fml+toitl}
			]
	for nl in newname:
		nl['platformID']=3
		nl['encodingID']=1
	return newname, fpsn

def mkcmap():
	if pun=='2':
		setpun(pzhs, loczhs)
	elif pun=='3':
		setpun(pzht, loczht)
	if simp=='2':
		tbs=set()
		simpg=getgname(simpcn)
		for zhstb in loczhs:
			a=gettbs(zhstb, simpg, True)
			tbs.update(a)
			repsp=dict()
			for itm in tbs:
				if itm[0]!=itm[1]:
					repsp[itm[0]]=itm[1]
			replg(repsp)
			
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

def hwcmap():
	hw=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¥­‑₩␣'
	hwlk=dict()
	for lk in font['GSUB']['lookups'].keys():
		if lk.split('_')[1]=='hwid':
			for sb in font['GSUB']['lookups'][lk]['subtables']:
				for k1 in sb.keys():
					hwlk[k1]=sb[k1]
			break
	for ch in hw:
		try:
			print('处理', ch)
			font['cmap'][str(ord(ch))]=hwlk[font['cmap'][str(ord(ch))]]
		except:
			print('ERROR: No glyph for', ch)

def hwgpos():
	torm=['kern', 'palt', 'vkrn', 'vpal']
	rmlk=list()
	for lk in font['GPOS']['lookups'].keys():
		if lk.split('_')[1] in torm:
			rmlk.append(lk)
	rmft=list()
	for ft in font['GPOS']['features'].keys():
		for ftrn in font['GPOS']['features'][ft]:
			if ftrn in rmlk:
				rmft.append(ft)
				break
	for lang in list(font['GPOS']['languages'].keys()):
		for ft in set(font['GPOS']['languages'][lang]['features']):
			if ft in rmft:
				font['GPOS']['languages'][lang]['features'].remove(ft)
		if len(font['GPOS']['languages'][lang]['features'])==0:
			del font['GPOS']['languages'][lang]
	for ft in rmft:
		del font['GPOS']['features'][ft]
	for lk in rmlk:
		del font['GPOS']['lookups'][lk]
		font['GPOS']['lookupOrder'].remove(lk)

def itcmap():
	itch='!"#$%&\'()*,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{}¡¢£¤¥§¨©ª«­®¯°²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĀāĂăĐđĒēĚěĨĩĪīŃńŇňŌōŎŏŒœŨũŪūŬŭƒƠơƯưǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǸǹɑɡʻ̄πḾḿẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ‐‑‒–—‘’‚“”„†‡•…‰′″‵‹›‼⁇⁈⁉⁴₩₫€ℓ№™⋯ﬁﬂ🄯'
	itlk=dict()
	for lk in font['GSUB']['lookups'].keys():
		if lk.split('_')[1]=='ital':
			for sb in font['GSUB']['lookups'][lk]['subtables']:
				for k1 in sb.keys():
					itlk[k1]=sb[k1]
			break
	for ch in itch:
		try:
			font['cmap'][str(ord(ch))]=itlk[font['cmap'][str(ord(ch))]]
		except:
			print('WARNING: No glyph for', ch)
	for uv in font['cmap_uvs']:
		if font['cmap_uvs'][uv] in itlk:
			font['cmap_uvs'][uv]=itlk[font['cmap_uvs'][uv]]

def itgsub():
	font['head']['macStyle']['italic']=True
	font['OS_2']['fsSelection']['italic']=True
	for lan in font['GSUB']['languages'].keys():
		for lft in set(font['GSUB']['languages'][lan]['features']):
			if 'ital' in lft:
				font['GSUB']['languages'][lan]['features'].remove(lft)
	for ft in list(font['GSUB']['features'].keys()):
		if 'ital' in ft:
			del font['GSUB']['features'][ft]
	for lk in list(font['GSUB']['lookups'].keys()):
		if 'ital' in lk:
			del font['GSUB']['lookups'][lk]
			font['GSUB']['lookupOrder'].remove(lk)

def getvcmp():
	a1=dict()
	font['cmap']=dict(orcmp)
	a1['name'], a1['file']=mkname()
	mkcmap()
	a1['cmap']=dict(font['cmap'])
	if 'Mono' not in fpn:
		a1['namehw'], a1['filehw']=mkname('hw')
		hwcmap()
		a1['cmaphw']=dict(font['cmap'])
	else:
		a1['nameit'], a1['fileit']=mkname('it')
		itcmap()
		a1['cmapit']=dict(font['cmap'])
	return a1

print('====思源字体（日版）转传承字形-批量====\n')
inf=sys.argv[1]
outd=sys.argv[2]
cfg=json.load(open(os.path.join(pydir, 'config.json'), 'r', encoding = 'utf-8'))
fnn=cfg['fontName']
fnnps=fnn.replace(' ', '')
print('正在载入字体...')
font = json.loads(subprocess.check_output((otfccdump, '--no-bom', inf)).decode("utf-8", "ignore"))
fpn=str()
for n1 in font['name']:
	if n1['nameID']==6 and '-' in n1['nameString']:
		fpn=n1['nameString']
		break

print('获取本地化替换表...')
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

pen='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
pzhs='·’‘”“•≤≥≮≯！：；？'+pen
pzht='·’‘”“•、。，．'+pen
simpcn='蒋残浅践写泻惮禅箪蝉恋峦蛮挛栾滦弯湾径茎弥称滞画遥瑶'#変将与
if len(sys.argv)<4 or sys.argv[3]!='2':
	step1()
setinf()
orcmp=dict(font['cmap'])
print('Build AA')
mch, pun, simp='y', '3', '2'
AA=getvcmp()
mch, pun, simp='n', '3', '1'
AATC=getvcmp()
mch, pun, simp='n', '2', '2'
AASC=getvcmp()
mch, pun, simp='n', '1', '1'
AAJP=getvcmp()
print('正在生成字体...')
for aa1 in (AA, AATC, AASC, AAJP):
	aa1['file']=os.path.join(outd, aa1['file']+'.otf')
	font['cmap']=aa1['cmap']
	font['name']=aa1['name']
	aa1['tmp']=tempfile.mktemp('.json')
	with open(aa1['tmp'], 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	print('=')
if 'Mono' not in fpn:
	hwgpos()
	for aa1 in (AA, AATC, AASC, AAJP):
		aa1['filehw']=os.path.join(outd, aa1['filehw']+'.otf')
		font['cmap']=aa1['cmaphw']
		font['name']=aa1['namehw']
		aa1['tmphw']=tempfile.mktemp('.json')
		with open(aa1['tmphw'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		print('=')
else:
	itgsub()
	for aa1 in (AA, AATC, AASC, AAJP):
		aa1['fileit']=os.path.join(outd, aa1['fileit']+'.otf')
		font['cmap']=aa1['cmapit']
		font['name']=aa1['nameit']
		aa1['tmpit']=tempfile.mktemp('.json')
		with open(aa1['tmpit'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		print('=')
	
print('正在生成OTFs...')
del font
gc.collect()
for aa1 in (AA, AATC, AASC, AAJP):
	subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', aa1['file'], aa1['tmp']))
	os.remove(aa1['tmp'])
	print('=')
if 'Mono' not in fpn:
	for aa1 in (AA, AATC, AASC, AAJP):
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', aa1['filehw'], aa1['tmphw']))
		os.remove(aa1['tmphw'])
		print('=')
else:
	for aa1 in (AA, AATC, AASC, AAJP):
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', aa1['fileit'], aa1['tmpit']))
		os.remove(aa1['tmpit'])
		print('=')
	
print('完成!')
