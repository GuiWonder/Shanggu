import os, json, sys, copy
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables

pydir=os.path.abspath(os.path.dirname(__file__))
cfg=json.load(open(os.path.join(pydir, 'configs/config.json'), 'r', encoding='utf-8'))

def setcg(code, glyf):
	for table in font["cmap"].tables:
		if (table.format==4 and code<=0xFFFF) or table.format==12 or code in table.cmap:
			table.cmap[code]=glyf
def glfrtxt(txt):
	cmap=font.getBestCmap()
	glys=list()
	for ch in txt:
		if ord(ch) in cmap and cmap[ord(ch)] not in glys:
			glys.append(cmap[ord(ch)])
	return glys
def getlki(fture):
	lks=list()
	for ki in fture:
		ftg=font["GSUB"].table.FeatureList.FeatureRecord[ki].FeatureTag
		if ftg=='locl':
			lks+=font["GSUB"].table.FeatureList.FeatureRecord[ki].Feature.LookupListIndex
	return list(dict.fromkeys(lks))
def getlkdef():
	lks=list()
	for sr in font["GSUB"].table.ScriptList.ScriptRecord:
		for lsr in sr.Script.DefaultLangSys.FeatureIndex:
			ftg=font["GSUB"].table.FeatureList.FeatureRecord[lsr].FeatureTag
			if ftg=='locl':
				lks+=font["GSUB"].table.FeatureList.FeatureRecord[lsr].Feature.LookupListIndex
	return list(dict.fromkeys(lks))
def locllk():
	fjan, fkor, fzhs, fzht, fzhh=(list() for i in range(5))
	for sr in font["GSUB"].table.ScriptList.ScriptRecord:
		for lsr in sr.Script.LangSysRecord:
			if lsr.LangSysTag.strip()=='JAN':
				fjan+=lsr.LangSys.FeatureIndex
			elif lsr.LangSysTag.strip()=='KOR':
				fkor+=lsr.LangSys.FeatureIndex
			elif lsr.LangSysTag.strip()=='ZHS':
				fzhs+=lsr.LangSys.FeatureIndex
			elif lsr.LangSysTag.strip()=='ZHT':
				fzht+=lsr.LangSys.FeatureIndex
			elif lsr.LangSysTag.strip()=='ZHH':
				fzhh+=lsr.LangSys.FeatureIndex
	return getlki(fjan), getlki(fkor), getlki(fzhs), getlki(fzht), getlki(fzhh)
def glyrepl(repdic):
	for table in font["cmap"].tables:
		for cd in table.cmap:
			if table.cmap[cd] in repdic:
				table.cmap[cd]=repdic[table.cmap[cd]]
				print('Remaping', chr(cd))
def glfrloc(gl, loclk):
	for lki in loclk:
		for st in font["GSUB"].table.LookupList.Lookup[lki].SubTable:
			if st.LookupType==7 and st.ExtSubTable.LookupType==1:
				tabl=st.ExtSubTable.mapping
			elif st.LookupType==1:
				tabl=st.mapping
			if gl in tabl:
				return tabl[gl]
	return ''

def nfname(ithw=''):
	if not font["name"].getDebugName(17):
		wt=font["name"].getDebugName(2)
	else:
		wt=font["name"].getDebugName(17)
	isit='Italic' in wt or 'it' in ithw.lower()
	wt=wt.replace('Italic', '').strip()
	if not wt: wt='Regular'
	ishw='HW' in fpsn or 'hw' in ithw.lower()
	itml, itm, hwm=str(), str(), str()
	if ishw: hwm=' HW'
	if isit: itml, itm=' Italic', 'It'
	locn=str()
	if mch=='n' and pun=='2'and simp=='2':
		locn=' SC'
	elif mch=='n' and pun=='1' and simp=='1':
		locn=' JP'
	elif mch=='n' and pun=='3':
		locn=' TC'
	if 'Sans' in fpsn:
		fmlName=cfg['fontName']+' Sans'+hwm+locn
		scn=cfg['fontNameSC']+'黑体'+locn.strip()+hwm
		tcn=cfg['fontNameTC']+'黑體'+locn.strip()+hwm
	elif 'Serif' in fpsn:
		fmlName=cfg['fontName']+' Serif'+hwm+locn
		scn=cfg['fontNameSC']+'明体'+locn.strip()+hwm
		tcn=cfg['fontNameTC']+'明體'+locn.strip()+hwm
	elif 'Mono' in fpsn:
		fmlName=cfg['fontName']+' Mono'+hwm+locn
		scn=cfg['fontNameSC']+'等宽'+locn.strip()+hwm
		tcn=cfg['fontNameTC']+'等寬'+locn.strip()+hwm
	else:
		raise
	ftName=fmlName
	ftNamesc=scn
	ftNametc=tcn
	if wt not in ('Regular', 'Bold'):
		ftName+=' '+wt
		ftNamesc+=' '+wt
		ftNametc+=' '+wt
	subfamily='Regular'
	if isit:
		if wt=='Bold':
			subfamily='Bold Italic'
		else:
			subfamily='Italic'
	elif wt=='Bold':
		subfamily='Bold'
	psName=fmlName.replace(' ', '')+'-'+fpsn.split('-')[-1].replace('It', '')+itm
	uniqID=cfg['fontVersion']+';'+cfg['fontID'].strip()+';'+psName
	#if wt=='Bold':
	if wt in ('Regular', 'Bold') and not (isit and wt=='Regular'):
		fullName=ftName+' '+wt+itml
		fullNamesc=ftNamesc+' '+wt+itml
		fullNametc=ftNametc+' '+wt+itml
	else:
		fullName=ftName+itml
		fullNamesc=ftNamesc+itml
		fullNametc=ftNametc+itml
	newnane=newTable('name')
	newnane.setName(cfg['fontCopyright'], 0, 3, 1, 1033)
	newnane.setName(ftName, 1, 3, 1, 1033)
	newnane.setName(subfamily, 2, 3, 1, 1033)
	newnane.setName(uniqID, 3, 3, 1, 1033)
	newnane.setName(fullName, 4, 3, 1, 1033)
	newnane.setName('Version '+cfg['fontVersion'], 5, 3, 1, 1033)
	newnane.setName(psName, 6, 3, 1, 1033)
	newnane.setName(cfg['fontDesigner'], 9, 3, 1, 1033)
	newnane.setName(cfg['fontDiscript'], 10, 3, 1, 1033)
	newnane.setName(cfg['fontVURL'], 11, 3, 1, 1033)
	newnane.setName(font["name"].getDebugName(13), 13, 3, 1, 1033)
	newnane.setName(font["name"].getDebugName(14), 14, 3, 1, 1033)
	if wt not in ('Regular', 'Bold'):
		newnane.setName(fmlName, 16, 3, 1, 1033)
		newnane.setName(wt+itml, 17, 3, 1, 1033)
	for lanid in (1028, 3076):
		newnane.setName(ftNametc, 1, 3, 1, lanid)
		newnane.setName(subfamily, 2, 3, 1, lanid)
		newnane.setName(fullNametc, 4, 3, 1, lanid)
		if wt not in ('Regular', 'Bold'):
			newnane.setName(tcn, 16, 3, 1, lanid)
			newnane.setName(wt+itml, 17, 3, 1, lanid)
	newnane.setName(ftNamesc, 1, 3, 1, 2052)
	newnane.setName(subfamily, 2, 3, 1, 2052)
	newnane.setName(fullNamesc, 4, 3, 1, 2052)
	if wt not in ('Regular', 'Bold'):
		newnane.setName(scn, 16, 3, 1, 2052)
		newnane.setName(wt+itml, 17, 3, 1, 2052)
	return newnane
def rmlk(tbnm, i):
	font[tbnm].table.LookupList.Lookup.pop(i)
	for ki in font[tbnm].table.FeatureList.FeatureRecord:
		newft=list()
		for j in ki.Feature.LookupListIndex:
			if j==i:
				continue
			elif j>i:
				newft.append(j-1)
			else:
				newft.append(j)
		ki.Feature.LookupListIndex=newft
	if tbnm=='GSUB':
		for lkp in font[tbnm].table.LookupList.Lookup:
			for st in lkp.SubTable:
				if st.LookupType in (5, 6) and hasattr(st, 'SubstLookupRecord'):
					for sbrcd in st.SubstLookupRecord:
						if sbrcd.LookupListIndex>i:
							sbrcd.LookupListIndex-=1
def rmft(tbnm, i):
	font[tbnm].table.FeatureList.FeatureRecord.pop(i)
	for sr in font[tbnm].table.ScriptList.ScriptRecord:
		newdl=list()
		for j in sr.Script.DefaultLangSys.FeatureIndex:
			if j==i:
				continue
			elif j>i:
				newdl.append(j-1)
			else:
				newdl.append(j)
		sr.Script.DefaultLangSys.FeatureIndex=newdl
		for lsr in sr.Script.LangSysRecord:
			newln=list()
			for j in lsr.LangSys.FeatureIndex:
				if j==i:
					continue
				elif j>i:
					newln.append(j-1)
				else:
					newln.append(j)
			lsr.LangSys.FeatureIndex=newln
def rmloc():
	loclks, locfts=list(), list()
	for i in range(len(font["GSUB"].table.FeatureList.FeatureRecord)):
		if font["GSUB"].table.FeatureList.FeatureRecord[i].FeatureTag=='locl':
			loclks+=font["GSUB"].table.FeatureList.FeatureRecord[i].Feature.LookupListIndex
			locfts.append(i)
	loclks=list(set(loclks))
	loclks.sort(reverse=True)
	locfts=list(set(locfts))
	locfts.sort(reverse=True)
	for i in locfts:
		rmft('GSUB', i)
	for i in loclks:
		rmlk('GSUB', i)
def setpun(pzh, loczh):
	pg=glfrtxt(pzh)
	rplg=dict()
	for tb in loczh:
		for glin in pg:
			if glin not in rplg:
				lk=font["GSUB"].table.LookupList.Lookup[tb]
				for st in lk.SubTable:
					if st.LookupType==7 and st.ExtSubTable.LookupType==1:
						tabl=st.ExtSubTable.mapping
					elif st.LookupType==1:
						tabl=st.mapping
					if glin in tabl:
						rplg[glin]=tabl[glin]
	glyrepl(rplg)
def mkcmp():
	cmap=font.getBestCmap()
	if pun=='2':
		setpun(pzhs, lkzhs)
		dfltvt('ZHS')
	elif pun=='3':
		setpun(pzht, lkzht)
		dfltvt('ZHT')
	else:
		dfltvt('JAN')
	if simp=='2':
		repsp=dict()
		simpg=glfrtxt(simpcn)
		for gc in simpg:
			repsp[gc]=glfrloc(gc, lkzhs)
		glyrepl(repsp)
	if mch=='y':
		print('Merging multi-code Chinese characters...')
		with open(os.path.join(pydir, 'configs/mulcodechar.dt'), 'r', encoding='utf-8') as f:
			for line in f.readlines():
				litm=line.split('#')[0].strip()
				if '-' not in litm: continue
				s, t=litm.split(' ')[0].split('-')
				s, t=s.strip(), t.strip()
				if s and t and s!=t and ord(t) in cmap:
					print('Processing '+s+'-'+t)
					setcg(ord(s), cmap[ord(t)])
def hwcmp():
	print('Build HW...')
	cmap=font.getBestCmap()
	hw=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¥­‑₩␣'
	rephw=dict()
	hwlk=set()
	for ki in font["GSUB"].table.FeatureList.FeatureRecord:
		if ki.FeatureTag=='hwid':
			hwlk.update(ki.Feature.LookupListIndex)
	for i in hwlk:
		for st in font["GSUB"].table.LookupList.Lookup[i].SubTable:
			assert st.LookupType==1
			tabl=st.mapping
			for ch in hw:
				gl=cmap[ord(ch)]
				if gl in tabl and gl not in rephw:
					print('Processing', ch)
					rephw[gl]=tabl[gl]
				else:
					print('No HW glyph for', ch)
	glyrepl(rephw)
def hwgps():
	torm=['kern', 'palt', 'vkrn', 'vpal']
	hwlks, hwfts=list(), list()
	for i in range(len(font["GPOS"].table.FeatureList.FeatureRecord)):
		if font["GPOS"].table.FeatureList.FeatureRecord[i].FeatureTag in torm:
			hwlks+=font["GPOS"].table.FeatureList.FeatureRecord[i].Feature.LookupListIndex
			hwfts.append(i)
	hwlks=list(set(hwlks))
	hwlks.sort(reverse=True)
	hwfts=list(set(hwfts))
	hwfts.sort(reverse=True)
	for i in hwfts:
		rmft('GPOS', i)
	for i in hwlks:
		rmlk('GPOS', i)
def itcmp():
	print('Build It...')
	itlk, itft=list(), list()
	for i in range(len(font["GSUB"].table.FeatureList.FeatureRecord)):
		if font["GSUB"].table.FeatureList.FeatureRecord[i].FeatureTag=='ital':
			itlk+=font["GSUB"].table.FeatureList.FeatureRecord[i].Feature.LookupListIndex
			font["GSUB"].table.FeatureList.FeatureRecord[i].Feature.LookupListIndex.clear()
			itft.append(i)
	itlk=list(set(itlk))
	itlk.sort(reverse=True)
	itft=list(set(itft))
	itft.sort(reverse=True)
	for i in itlk:
		for st in font["GSUB"].table.LookupList.Lookup[i].SubTable:
			assert st.LookupType==1
			tabl=st.mapping
			glyrepl(tabl)
	for i in itft:
		rmft('GSUB', i)
	for i in itlk:
		rmlk('GSUB', i)
def stnm(nameobj):
	fnn=cfg['fontName']
	fnnp=fnn.replace(' ', '')
	tc='ST'
	zhnt=' 轉繁體'
	zhns=' 转繁体'
	rpln=[
		(fnn+' Sans', fnn+' Sans '+tc), 
		(fnn+' Serif', fnn+' Serif '+tc), 
		(fnn+' Mono', fnn+' Mono '+tc), 
		(fnnp+'Sans', fnnp+'Sans'+tc), 
		(fnnp+'Serif', fnnp+'Serif'+tc), 
		(fnnp+'Mono', fnnp+'Mono'+tc), 
		('黑體', '黑體'+zhnt), 
		('明體', '明體'+zhnt), 
		('等寬', '等寬'+zhnt), 
		('黑体', '黑体'+zhns), 
		('明体', '明体'+zhns), 
		('等宽', '等宽'+zhns), 
		('ST HW', 'HW ST'), 
		('STHW', 'HWST')
	]
	for n1 in nameobj.names:
		nstr=str(n1)
		for rp in rpln:
			 nstr=nstr.replace(rp[0], rp[1])
		nameobj.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return nameobj
def stlks():
	cmap=font.getBestCmap()
	glod=font.getGlyphOrder()
	stmul=otTables.Lookup()
	stsig=otTables.Lookup()
	stsig1=otTables.Lookup()
	stsig2=otTables.Lookup()
	stsig3=otTables.Lookup()
	stlkups=[stmul, stsig, stsig1, stsig2, stsig3]
	sgtb, sgtb1, sgtb2, sgtb3=dict(), dict(), dict(), dict()
	for lk in stlkups[1:]:
		lk.LookupType=1
		lk.LookupFlag=0
	sgsb=otTables.SingleSubst()
	sgsb1=otTables.SingleSubst()
	sgsb2=otTables.SingleSubst()
	sgsb3=otTables.SingleSubst()
	stsig.SubTable=[sgsb]
	stsig1.SubTable=[sgsb1]
	stsig2.SubTable=[sgsb2]
	stsig3.SubTable=[sgsb3]
	stmul.SubTable=list()
	stmul.LookupType=6
	stmul.LookupFlag=0
	with open(os.path.join(pydir, 'configs/stonem.dt'),'r',encoding='utf-8') as f:
		bkcov=list()
		lahcov=list()
		ltc=dict()
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '-' not in litm: continue
			sb=dict()
			ls=litm.strip().split(' ')
			s, t=ls[0].split('-')
			dics=ls[1:]
			sg=cmap[ord(s)]
			tg=cmap[ord(t)]
			i=dics.index(s)
			assert i>-1
			bkcov=dics[0:i]
			bkcov.reverse()
			lahcov=dics[i+1:]
			if sg!=tg and tg not in ltc:
				if sg not in sgtb1:
					sgtb1[sg]=tg
					ltc[tg]=2
				elif sg not in sgtb2:
					sgtb2[sg]=tg
					ltc[tg]=3
				elif sg not in sgtb3:
					sgtb3[sg]=tg
					ltc[tg]=4
				else:
					raise
			bklst=list()
			for strs in bkcov:
				cvobjbk=otTables.Coverage()
				cvobjbk.glyphs=list(set([cmap[ord(ch)] for ch in strs]))
				assert len(cvobjbk.glyphs)>0, strs
				cvobjbk.glyphs=list(sorted([g for g in cvobjbk.glyphs], key=lambda g:glod.index(g)))
				bklst.append(cvobjbk)
			ahlst=list()
			for strs in lahcov:
				cvobjah=otTables.Coverage()
				cvobjah.glyphs=list(set([cmap[ord(ch)] for ch in strs]))
				assert len(cvobjah.glyphs)>0, strs
				cvobjah.glyphs=list(sorted([g for g in cvobjah.glyphs], key=lambda g:glod.index(g)))
				ahlst.append(cvobjah)
			cvobjip=otTables.Coverage()
			cvobjip.glyphs=[cmap[ord(s)]]
			mulsb=otTables.ChainContextSubst()
			mulsb.Format=3
			mulsb.BacktrackCoverage=bklst
			mulsb.InputCoverage=[cvobjip]
			mulsb.LookAheadCoverage=ahlst
			if sg!=tg:
				sblrd=otTables.SubstLookupRecord()
				sblrd.SequenceIndex=0
				sblrd.LookupListIndex=ltc[tg]
				mulsb.SubstLookupRecord=[sblrd]
			stmul.SubTable.append(mulsb)
	sgsb1.mapping=sgtb1
	sgsb2.mapping=sgtb2
	sgsb3.mapping=sgtb3
	with open(os.path.join(pydir, 'configs/stoneo.dt'),'r',encoding='utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '-' not in litm: continue
			s, t=litm.split(' ')[0].split('-')
			s, t=s.strip(), t.strip()
			if s and t and s!=t and ord(s) in cmap and ord(t) in cmap and cmap[ord(s)]!=cmap[ord(t)]:
				sgtb[cmap[ord(s)]]=cmap[ord(t)]
	sgsb.mapping=sgtb
	for lkp in font["GSUB"].table.LookupList.Lookup:
		for st in lkp.SubTable:
			if st.LookupType in (5, 6) and hasattr(st, 'SubstLookupRecord'):
				for sbrcd in st.SubstLookupRecord:
					sbrcd.LookupListIndex+=len(stlkups)
	for ft in font["GSUB"].table.FeatureList.FeatureRecord:
		ft.Feature.LookupListIndex=[i+len(stlkups) for i in ft.Feature.LookupListIndex]
	font["GSUB"].table.LookupList.Lookup=stlkups+font["GSUB"].table.LookupList.Lookup
	stft=otTables.FeatureRecord()
	stft.Feature=otTables.Feature()
	stft.FeatureTag='ccmp'
	stft.Feature.LookupListIndex=[0, 1]
	font["GSUB"].table.FeatureList.FeatureRecord.insert(0, stft)
	for sr in font["GSUB"].table.ScriptList.ScriptRecord:
		sr.Script.DefaultLangSys.FeatureIndex=[i+1 for i in sr.Script.DefaultLangSys.FeatureIndex]
		sr.Script.DefaultLangSys.FeatureIndex.insert(0, 0)
		for lsr in sr.Script.LangSysRecord:
			lsr.LangSys.FeatureIndex=[i+1 for i in lsr.LangSys.FeatureIndex]
			lsr.LangSys.FeatureIndex.insert(0, 0)
def stcmp():
	cmap=font.getBestCmap()
	with open(os.path.join(pydir, 'configs/stoneo.dt'),'r',encoding='utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '-' not in litm: continue
			s, t=litm.split(' ')[0].split('-')
			s, t=s.strip(), t.strip()
			if s and t and s!=t and ord(s) not in cmap and ord(t) in cmap:
				setcg(ord(s), cmap[ord(t)])
def dftfont():
	font['cmap']=copy.deepcopy(ftcmap)
	font['name']=copy.deepcopy(ftname)
	font['GSUB']=copy.deepcopy(ftgsub)
	font['GPOS']=copy.deepcopy(ftgpos)
	cmap=font.getBestCmap()
def getvarmap():
	a1=dict()
	dftfont()
	mkcmp()
	rmloc()
	a1['name']=mkname()
	a1['file']=a1['name'].getDebugName(6)
	a1['GSUB']=copy.deepcopy(font['GSUB'])
	a1['GPOS']=copy.deepcopy(font['GPOS'])
	a1['cmap']=copy.deepcopy(font['cmap'])
	dftfont()
	if 'Mono' not in fpsn:
		mkcmp()
		hwcmp()
		hwgps()
		rmloc()
		a1['namehw']=mkname('hw')
		a1['filehw']=a1['namehw'].getDebugName(6)
		a1['GSUBhw']=copy.deepcopy(font['GSUB'])
		a1['GPOShw']=copy.deepcopy(font['GPOS'])
		a1['cmaphw']=copy.deepcopy(font['cmap'])
	else:
		mkcmp()
		itcmp()
		rmloc()
		a1['nameit']=mkname('it')
		a1['fileit']=a1['nameit'].getDebugName(6)
		a1['GSUBit']=copy.deepcopy(font['GSUB'])
		a1['GPOSit']=copy.deepcopy(font['GPOS'])
		a1['cmapit']=copy.deepcopy(font['cmap'])
	return a1
def getstmap():
	font['cmap']=copy.deepcopy(AA['cmap'])
	font['name']=copy.deepcopy(AA['name'])
	font['GSUB']=copy.deepcopy(AA['GSUB'])
	font['GPOS']=copy.deepcopy(AA['GPOS'])
	cmap=font.getBestCmap()
	stcmp()
	stlks()
	AA['namest']=stnm(copy.deepcopy(AA['name']))
	AA['filest']=AA['namest'].getDebugName(6)
	AA['GSUBst']=copy.deepcopy(font['GSUB'])
	AA['GPOSst']=copy.deepcopy(font['GPOS'])
	AA['cmapst']=copy.deepcopy(font['cmap'])
	font['name']=copy.deepcopy(AA['namehw'])
	if 'Mono' not in fpsn:
		hwcmp()
		hwgps()
	else:
		itcmp()
	AA['namest2']=stnm(copy.deepcopy(AA['namehw']))
	AA['filest2']=AA['namest2'].getDebugName(6)
	AA['GSUBst2']=copy.deepcopy(font['GSUB'])
	AA['GPOSst2']=copy.deepcopy(font['GPOS'])
	AA['cmapst2']=copy.deepcopy(font['cmap'])
def svfont(svcmp, svnm, svgs, svgp, svfile, toit=False):
	if 'VF' in svfile:
		svfile=svfile.split('-')[0].replace('VF', '-VF')
	fontsv=TTFont(infile, recalcTimestamp=False)
	fontsv['OS/2'].achVendID=cfg['fontID']
	fontsv['head'].fontRevision=float(cfg['fontVersion'])
	if toit:
		if fontsv['head'].macStyle<2:
			fontsv['head'].macStyle+=2
		if fontsv['OS/2'].fsSelection%2==0:
			fontsv['OS/2'].fsSelection+=1
	fontsv['cmap']=svcmp
	fontsv['name']=svnm
	fontsv['GSUB']=svgs
	fontsv['GPOS']=svgp
	svfl=os.path.join(outdir, svfile+'.'+exn)
	print('Saving ', svfl)
	fontsv.save(svfl)
	fontsv.close()
def svfonts():
	for aa1 in (AA, AATC, AASC, AAJP):
		svfont(aa1['cmap'], aa1['name'], aa1['GSUB'], aa1['GPOS'], aa1['file'])
		if 'Mono' not in fpsn:
			svfont(aa1['cmaphw'], aa1['namehw'], aa1['GSUBhw'], aa1['GPOShw'], aa1['filehw'])
		else:
			svfont(aa1['cmapit'], aa1['nameit'], aa1['GSUBit'], aa1['GPOSit'], aa1['fileit'], True)
	if 'Mono' not in fpsn:
		svfont(AA['cmapst'], AA['namest'], AA['GSUBst'], AA['GPOSst'], AA['filest'])
		svfont(AA['cmapst2'], AA['namest2'], AA['GSUBst2'], AA['GPOSst2'], AA['filest2'])
def vfname(hw=''):
	ishw='hw'in hw.lower()
	hwm=str()
	if ishw: hwm=' HW'
	locn=str()
	if mch=='n' and pun=='2'and simp=='2':
		locn=' SC'
	elif mch=='n' and pun=='1' and simp=='1':
		locn=' JP'
	elif mch=='n' and pun=='3':
		locn=' TC'
	if 'Sans' in fpsn:
		fmlName=cfg['fontName']+' Sans'+hwm+locn
		scn=cfg['fontNameSC']+'黑体'+locn.strip()+hwm+' VF'
		tcn=cfg['fontNameTC']+'黑體'+locn.strip()+hwm+' VF'
	elif 'Serif' in fpsn:
		fmlName=cfg['fontName']+' Serif'+hwm+locn
		scn=cfg['fontNameSC']+'明体'+locn.strip()+hwm+' VF'
		tcn=cfg['fontNameTC']+'明體'+locn.strip()+hwm+' VF'
	elif 'Mono' in fpsn:
		fmlName=cfg['fontName']+' Mono'+hwm+locn
		scn=cfg['fontNameSC']+'等宽'+locn.strip()+hwm+' VF'
		tcn=cfg['fontNameTC']+'等寬'+locn.strip()+hwm+' VF'
	else:
		raise
	ftNamesc=scn
	ftNametc=tcn

	rpln=[
		('Source Han Sans', fmlName), 
		('Source Han Serif', fmlName), 
		('SourceHanSans', fmlName.replace(' ', '')), 
		('SourceHanSerif', fmlName.replace(' ', '')), 
	]
	psName=fpsn
	for rp in rpln:
		 psName=psName.replace(rp[0], rp[1])
	uniqID=cfg['fontVersion']+';'+cfg['fontID'].strip()+';'+psName
	newnane=newTable('name')
	newnane.names=list()
	for n1 in font['name'].names:
		if n1.langID==0x411:
			continue
		if n1.nameID==0:
			n1.string=cfg['fontCopyright']
		elif n1.nameID==3:
			n1.string=uniqID
		elif n1.nameID==5:
			n1.string='Version '+cfg['fontVersion']
		elif n1.nameID==9:
			n1.string=cfg['fontDesigner']
		elif n1.nameID==10:
			n1.string=cfg['fontDiscript']
		elif n1.nameID==11:
			n1.string=cfg['fontVURL']
		elif n1.nameID in (7, 8):
			continue
		else:
			nstr=str(n1)
			for rp in rpln:
				 nstr=nstr.replace(rp[0], rp[1])
			n1.string=nstr
		newnane.names.append(n1)
	for lanid in (1028, 3076):
		newnane.setName(ftNametc, 1, 3, 1, lanid)
		newnane.setName('Regular', 2, 3, 1, lanid)
		newnane.setName(ftNametc, 4, 3, 1, lanid)
		newnane.setName('ExtraLight', 17, 3, 1, lanid)
	newnane.setName(ftNamesc, 1, 3, 1, 2052)
	newnane.setName('Regular', 2, 3, 1, 2052)
	newnane.setName(ftNamesc, 4, 3, 1, 2052)
	newnane.setName('ExtraLight', 17, 3, 1, 2052)
	return newnane
def mkname(ithw=''):
	if 'VF' in fpsn:
		return vfname(ithw)
	else:
		return nfname(ithw)
def dfltvt(lng):
	for posub in ('GSUB', 'GPOS'):
		vtzh=list()
		for sr in font[posub].table.ScriptList.ScriptRecord:
			for lsr in sr.Script.LangSysRecord:
				if lsr.LangSysTag.strip()==lng:
					for ki in lsr.LangSys.FeatureIndex:
						if vtzh: break
						if font[posub].table.FeatureList.FeatureRecord[ki].FeatureTag=='vert':
							vtzh=font[posub].table.FeatureList.FeatureRecord[ki].Feature.LookupListIndex
		for sr in font[posub].table.ScriptList.ScriptRecord:
			for lsr in sr.Script.DefaultLangSys.FeatureIndex:
				if font[posub].table.FeatureList.FeatureRecord[lsr].FeatureTag=='vert':
					font[posub].table.FeatureList.FeatureRecord[lsr].Feature.LookupListIndex=vtzh
					break
			for lsr in sr.Script.LangSysRecord:
					for ki in lsr.LangSys.FeatureIndex:
						if font[posub].table.FeatureList.FeatureRecord[ki].FeatureTag=='vert':
							font[posub].table.FeatureList.FeatureRecord[ki].Feature.LookupListIndex=vtzh
							break

print('*'*50)
print('====Build Advocate Ancient Fonts====\n')
infile=sys.argv[1]
outdir=sys.argv[2]
font=TTFont(infile)
pen='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
pzhs='·’‘”“•≤≥≮≯！：；？'+pen
pzht='·’‘”“•、。，．'+pen
pzht=pzht.replace('’', '').replace('‘', '').replace('”', '').replace('“', '')
simpcn='蒋残浅践写泻惮禅箪蝉恋峦蛮挛栾滦弯湾径茎弥称滞画遥瑶'#変将与
fpsn=font["name"].getDebugName(6)
print('Getting the localized lookups table...')
lkdef=getlkdef()
lkjan, lkkor, lkzhs, lkzht, lkzhh=locllk()
print('Lookup index', lkdef, lkjan, lkkor, lkzhs, lkzht, lkzhh)
ftcmap=copy.deepcopy(font['cmap'])
ftname=copy.deepcopy(font['name'])
ftgsub=copy.deepcopy(font['GSUB'])
ftgpos=copy.deepcopy(font['GPOS'])
mch, pun, simp='y', '3', '2'
AA=getvarmap()
mch, pun, simp='n', '3', '1'
AATC=getvarmap()
mch, pun, simp='n', '2', '2'
AASC=getvarmap()
mch, pun, simp='n', '1', '1'
AAJP=getvarmap()
if 'Mono' not in fpsn:
	getstmap()
exn=infile.split('.')[-1].lower()
print('Saving fonts...')
font.close()
svfonts()
print('Finished!')
print('*'*50)
