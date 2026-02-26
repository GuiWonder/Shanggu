from copy import deepcopy
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from afdko import otf2otc
from hpsh import *
from datetime import datetime

cfg=json.load(open(os.path.join(SCRIPT_DIR, 'configs/config.json'), 'r', encoding='utf-8'))

def glyrepl(font, repdic):
	for table in font['cmap'].tables:
		for cd in table.cmap:
			if table.cmap[cd] in repdic:
				old_glyph=table.cmap[cd]
				new_glyph=repdic[old_glyph]
				table.cmap[cd]=new_glyph
				logging.info(f'Remap U+{cd:04X} ({chr(cd)}) from {old_glyph} to {new_glyph}')

def givename(oldname, vk, isvf=False):
	locn=vk[:2].upper()
	oldps=oldname.getDebugName(6)
	wt=oldname.getDebugName(17)
	if not wt: wt=oldname.getDebugName(2)
	isit='Italic' in wt or 'it' in vk.lower()
	wt=wt.replace('Italic', '').strip()
	if not wt: wt='Regular'
	ishw='HW' in oldps or 'hw' in vk.lower()
	if isit: itnm, itps=' Italic', 'It'
	else: itnm=itps=str()
	for psty in ['Sans', 'Serif', 'Mono', 'Round']:
		if psty in oldps:
			style=psty
			break
	else: raise
	nmobj=dict()
	mylans=['EN', 'TC', 'SC', 'JA']
	for l in mylans:
		if l in cfg:
			ftfml=cfg[l]['Name']+cfg[l][style]
			if locn!='NM':
				vloc=' '+cfg[l]['ST'] if locn=='ST' else locn
				ftfml+=vloc
			if ishw: ftfml+=' HW'
		else:
			ftfml=cfg['Name']+' '+style
			if ishw: ftfml+=' HW'
			if locn!='NM': ftfml+=' '+locn
		if 'VF' in oldps: ftfml+=' VF'
		ftnm=ftfml
		if not isvf and wt not in ('Regular', 'Bold'):
			ftnm+=' '+wt
		ftfull=ftfml+' '+wt+itnm
		nmobj[l]={'fml': ftfml, 'nm': ftnm, 'full': ftfull}
	lansid={'EN':[1033, ], 'TC':[1028, 3076, 5124], 'SC':[2052, 4100], 'JA':[1041, ]}
	enlan=1033
	if isit: subfml='Bold Italic' if wt=='Bold' else 'Italic'
	else: subfml='Bold' if wt=='Bold' else 'Regular'
	fmlnm=nmobj['EN']['fml']
	psname=fmlnm.replace(' ', '')+'-'+oldps.split('-')[-1].replace('It', '')+itps
	uniqID=cfg['Version']+';'+cfg['ID'].strip()+';'+psname
	Copyright=cfg['Copyright'].format(name=cfg['Name'], year=datetime.now().year)
	newnane=newTable('name')
	idmap={0:Copyright, 3:uniqID, 5:'Version '+cfg['Version'], 6:psname,
		9:cfg['Designer'], 10:cfg['Discript'], 11:cfg['VURL'],
		13:oldname.getDebugName(13), 14:oldname.getDebugName(14)}
	for i, v in idmap.items():
		newnane.setName(v, i, 3, 1, enlan)
	for l in mylans:
		for lanid in lansid[l]:
			newnane.setName(nmobj[l]['nm'], 1, 3, 1, lanid)
			newnane.setName(nmobj[l]['full'], 4, 3, 1, lanid)
			newnane.setName(subfml, 2, 3, 1, lanid)
			if wt not in ('Regular', 'Bold'):
				newnane.setName(wt+itnm, 17, 3, 1, lanid)
				if not isvf:
					newnane.setName(nmobj[l]['fml'], 16, 3, 1, lanid)
	if isvf:
		oldnm=oldps.split('-')[0]
		newnm=fmlnm.replace(' ', '')
		for n1 in oldname.names:
			if n1.nameID<255: continue
			nstr=str(n1).replace(oldnm, newnm)
			newnane.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return newnane

def rmlk(font, tbnm, i):
	font[tbnm].table.LookupList.Lookup.pop(i)
	for ki in font[tbnm].table.FeatureList.FeatureRecord:
		newft=list()
		for j in ki.Feature.LookupListIndex:
			if j>i: newft.append(j-1)
			elif j<i: newft.append(j)
		ki.Feature.LookupListIndex=newft
	if tbnm=='GSUB':
		for lkp in font[tbnm].table.LookupList.Lookup:
			for st in lkp.SubTable:
				if st.LookupType in (5, 6):
					if hasattr(st, 'SubstLookupRecord'):
						for sbrcd in st.SubstLookupRecord:
							if sbrcd.LookupListIndex>i:
								sbrcd.LookupListIndex-=1
					if hasattr(st, 'ChainSubClassSet'):
						for rul in st.ChainSubClassSet:
							if hasattr(rul, 'ChainSubClassRule'):
								for subr in rul.ChainSubClassRule:
									for sbrcd in subr.SubstLookupRecord:
										if sbrcd.LookupListIndex>i:
											sbrcd.LookupListIndex-=1

def rmft(font, tbnm, i):
	font[tbnm].table.FeatureList.FeatureRecord.pop(i)
	for sr in font[tbnm].table.ScriptList.ScriptRecord:
		newdl=list()
		for j in sr.Script.DefaultLangSys.FeatureIndex:
			if j>i: newdl.append(j-1)
			elif j<i: newdl.append(j)
		sr.Script.DefaultLangSys.FeatureIndex=newdl
		for lsr in sr.Script.LangSysRecord:
			newln=list()
			for j in lsr.LangSys.FeatureIndex:
				if j>i: newln.append(j-1)
				elif j<i: newln.append(j)
			lsr.LangSys.FeatureIndex=newln

def rmloc(font):
	for posub in ('GSUB', 'GPOS'):
		keepft, keeplk=set(), set()
		ftrcd=font[posub].table.FeatureList.FeatureRecord
		lklst=font[posub].table.LookupList.Lookup
		for sr in font[posub].table.ScriptList.ScriptRecord:
			for j in sr.Script.DefaultLangSys.FeatureIndex:
				if ftrcd[j].FeatureTag!='locl': keepft.add(j)
			sr.Script.LangSysRecord.clear()
		for i in keepft:
			for j in ftrcd[i].Feature.LookupListIndex: keeplk.add(j)
		if posub=='GSUB':
			for lkp in lklst:
				for st in lkp.SubTable:
					if st.LookupType in (5, 6):
						if hasattr(st, 'SubstLookupRecord'):
							for sbrcd in st.SubstLookupRecord:
								keeplk.add(sbrcd.LookupListIndex)
						if hasattr(st, 'ChainSubClassSet'):
							for rul in st.ChainSubClassSet:
								if hasattr(rul, 'ChainSubClassRule'):
									for subr in rul.ChainSubClassRule:
										for sbrcd in subr.SubstLookupRecord:
											keeplk.add(sbrcd.LookupListIndex)
		locfts={i for i in range(len(ftrcd)) if i not in keepft}
		loclks={i for i in range(len(lklst)) if i not in keeplk}
		loclks=sorted(loclks, reverse=True)
		locfts=sorted(locfts, reverse=True)
		for i in locfts: rmft(font, posub, i)
		for i in loclks: rmlk(font, posub, i)

def mkcmp(option, font, k):
	cmap=font.getBestCmap()
	pgl=set()
	if 'sc'==k:
		pgl={cmap[ord(ch)] for ch in p_zhs if ord(ch) in cmap}
		dfltloc='ZHS'
	elif k in ('tc', 'nm'):
		pgl={cmap[ord(ch)] for ch in p_zht if ch not in '’‘”“' and ord(ch) in cmap}
		dfltloc='ZHT'
	elif 'jp'==k:
		dfltloc='JAN'
	if 'jp'!=k:
		rplg=dict()
		for tb in option.loczh[dfltloc]:
			for glin in pgl:
				if glin not in rplg and glin in tb:
					rplg[glin]=tb[glin]
		glyrepl(font, rplg)
	dfltvt(font, dfltloc)
	#if k=='SC' or k=='':
	if k!='jp':
		repsp=dict()
		simpg={cmap[ord(ch)] for ch in simpch if ord(ch) in cmap}
		for gc in simpg:
			repsp[gc]=glfrloc(gc, option.loczh['ZHS'])
		glyrepl(font, repsp)
	if k=='nm':
		logging.info('Merging multi-code Chinese characters.')
		with open(os.path.join(SCRIPT_DIR, 'configs/mulcodechar.dt'), 'r', encoding='utf-8') as f:
			for line in f.readlines():
				litm=line.split('#')[0].strip()
				if '-' not in litm: continue
				s, t=litm.split(' ')[0].split('-')
				s, t=s.strip(), t.strip()
				if s and t and s!=t and ord(t) in cmap:
					logging.info('Processing '+s+'-'+t)
					setcg(font['cmap'], ord(s), cmap[ord(t)])
	for table in font['cmap'].tables:
		if table.format==6:
			if k in ('tc', 'nm'): table.platEncID=2
			elif 'sc'==k: table.platEncID=25

def dfltvt(font, lng):
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

def hwcmp(font):
	logging.info('Build HW.')
	cmap=font.getBestCmap()
	hw=' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ¥­‑₩␣'
	rephw=dict()
	hwlk=set()
	for ki in font['GSUB'].table.FeatureList.FeatureRecord:
		if ki.FeatureTag=='hwid':
			hwlk.update(ki.Feature.LookupListIndex)
	for i in hwlk:
		for st in font['GSUB'].table.LookupList.Lookup[i].SubTable:
			assert st.LookupType==1
			tabl=st.mapping
			for ch in hw:
				gl=cmap[ord(ch)]
				if gl in tabl and gl not in rephw:
					logging.info(f'Processing HW: {ch}')
					rephw[gl]=tabl[gl]
				else:
					logging.debug(f'No HW glyph for {ch}')
	glyrepl(font, rephw)

def hwgps(font):
	torm=['kern', 'palt', 'vkrn', 'vpal']
	hwlks, hwfts=list(), list()
	for i, ft in enumerate(font['GPOS'].table.FeatureList.FeatureRecord):
		if ft.FeatureTag in torm:
			hwlks+=ft.Feature.LookupListIndex
			hwfts.append(i)
	hwlks=sorted(set(hwlks), reverse=True)
	hwfts=sorted(set(hwfts), reverse=True)
	for i in hwfts: rmft(font, 'GPOS', i)
	for i in hwlks: rmlk(font, 'GPOS', i)

def itcmp(font):
	logging.info('Build It.')
	itlk, itft=list(), list()
	for i, lk in enumerate(font['GSUB'].table.FeatureList.FeatureRecord):
		if lk.FeatureTag=='ital':
			itlk+=lk.Feature.LookupListIndex
			lk.Feature.LookupListIndex.clear()
			itft.append(i)
	itlk=sorted(set(itlk), reverse=True)
	itft=sorted(set(itft), reverse=True)
	for i in itlk:
		for st in font['GSUB'].table.LookupList.Lookup[i].SubTable:
			assert st.LookupType==1
			tabl=st.mapping
			glyrepl(font, tabl)
	for i in itft: rmft(font, 'GSUB', i)
	for i in itlk: rmlk(font, 'GSUB', i)

def stlks(font, chrdic, phrdic):
	cmap=font.getBestCmap()
	glod=font.getGlyphOrder()
	def newlk(lktype, flag=0):
		lk=otTables.Lookup()
		lk.LookupType=lktype
		lk.LookupFlag=flag
		lk.SubTable=list()
		return lk
	stmul=newlk(6)
	stsig=newlk(1)
	mylkps=[stmul, stsig]
	exmps=list()
	tglki=dict()
	for phdc in phrdic:
		s, t=phdc['s'], phdc['t']
		sg, tg=cmap[ord(s)], cmap[ord(t)]
		if sg!=tg and tg not in tglki:
			for i, m in enumerate(exmps):
				if sg not in m:
					m[sg]=tg
					tglki[tg]=len(mylkps)+i
					break
			else:
				tglki[tg]=len(mylkps)+len(exmps)
				exmps.append({sg:tg})
		dics=phdc['p']
		i=dics.index(s)
		assert i>-1
		bkcov=dics[0:i]
		bkcov.reverse()
		lahcov=dics[i+1:]
		bklst, ahlst=list(), list()
		for lst, cov in [(bklst, bkcov), (ahlst, lahcov)]:
			for strs in cov:
				glyphs=set([cmap[ord(ch)] for ch in strs])
				assert len(glyphs)>0, strs
				cvobj=otTables.Coverage()
				cvobj.glyphs=sorted(glyphs, key=lambda g:glod.index(g))
				lst.append(cvobj)
		cvobjip=otTables.Coverage()
		cvobjip.glyphs=[sg]
		mulsb=otTables.ChainContextSubst()
		mulsb.Format=3
		mulsb.BacktrackCoverage=bklst
		mulsb.InputCoverage=[cvobjip]
		mulsb.LookAheadCoverage=ahlst
		if sg!=tg:
			sblrd=otTables.SubstLookupRecord()
			sblrd.SequenceIndex=0
			sblrd.LookupListIndex=tglki[tg]
			mulsb.SubstLookupRecord=[sblrd]
		stmul.SubTable.append(mulsb)
	for mp in exmps:
		exsb=otTables.SingleSubst()
		exsb.mapping=mp
		exlk=newlk(1)
		exlk.SubTable=[exsb]
		mylkps.append(exlk)
	sgtb=dict()
	for s, t in list(chrdic.items()):
		if ord(s) in cmap and ord(t) in cmap and cmap[ord(s)]!=cmap[ord(t)]:
			sgtb[cmap[ord(s)]]=cmap[ord(t)]
	sgsb=otTables.SingleSubst()
	sgsb.mapping=sgtb
	stsig.SubTable=[sgsb]
	offset=len(mylkps)
	lklst=font['GSUB'].table.LookupList
	ftlst=font['GSUB'].table.FeatureList
	srlst=font['GSUB'].table.ScriptList
	for lkp in lklst.Lookup:
		for st in lkp.SubTable:
			if st.LookupType in (5, 6):
				if hasattr(st, 'SubstLookupRecord'):
					for sbrcd in st.SubstLookupRecord:
						sbrcd.LookupListIndex+=offset
				if hasattr(st, 'ChainSubClassSet'):
					for rul in st.ChainSubClassSet:
						if hasattr(rul, 'ChainSubClassRule'):
							for subr in rul.ChainSubClassRule:
								for sbrcd in subr.SubstLookupRecord:
									sbrcd.LookupListIndex+=offset
	lklst.Lookup=mylkps+lklst.Lookup
	for ft in ftlst.FeatureRecord:
		ft.Feature.LookupListIndex=[i+offset for i in ft.Feature.LookupListIndex]
	mytg='ccmp'
	tgidxs=[i for i, r in enumerate(ftlst.FeatureRecord) if r.FeatureTag==mytg]
	if tgidxs:
		for idx in tgidxs:
			feat=ftlst.FeatureRecord[idx].Feature
			ftlks={0, 1}
			ftlks.update(feat.LookupListIndex)
			feat.LookupListIndex=sorted(ftlks)
			feat.LookupCount=len(feat.LookupListIndex)
	else: raise

def stcmp(font, chrdic):
	cmap=font.getBestCmap()
	for s, t in list(chrdic.items()):
		if ord(s) not in cmap and ord(t) in cmap:
			setcg(font['cmap'], ord(s), cmap[ord(t)])

def getstdic():
	newdic=dict()
	with open(os.path.join(SCRIPT_DIR, 'configs/stoneo.dt'),'r',encoding='utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '-' not in litm: continue
			s, t=litm.split(' ')[0].split('-')
			s, t=s.strip(), t.strip()
			if s and t and s!=t:
				newdic[s]=t
	for s in list(newdic.keys()):
		while newdic[s] in newdic: newdic[s]=newdic[newdic[s]]
	newlst=list()
	with open(os.path.join(SCRIPT_DIR, 'configs/stonem.dt'),'r',encoding='utf-8') as f:
		for line in f.readlines():
			litm=line.split('#')[0].strip()
			if '-' not in litm: continue
			dic1=dict()
			ls=litm.strip().split(' ')
			s, t=ls[0].split('-')
			dic1['s'], dic1['t']=s, t
			dic1['p']=ls[1:]
			newlst.append(dic1)
	return newdic, newlst

def buildot(option, k):
	isvf=option.isvf
	font=option.vfonts[k]
	font['name']=givename(option.oldname, k, isvf=isvf)
	for tb in ('cmap', 'GSUB', 'GPOS'):
		if 'it' in k or 'hw' in k:
			upfont=option.vfonts[k[:2]]
			font[tb]=deepcopy(upfont[tb])
		elif 'st'==k:
			font[tb]=deepcopy(option.vfonts['nm'][tb])
	if 'hw' in k:
		hwcmp(font)
		hwgps(font)
	elif 'it' in k:
		itcmp(font)
	elif 'st' in k:
		chrdic, phrdic=getstdic()
		stcmp(font, chrdic)
		stlks(font, chrdic, phrdic)
	else:
		uvsfill(font, True)
		mkcmp(option, font, k)
		rmloc(font)

def tctfdir(option):
	ftnm=option.vfonts['nm']['name'].getDebugName(6).split('-')[0]
	if ftnm.endswith('VF'): ftnm=ftnm[:-2]
	dirfmt=option.exn.upper()
	tfdir=ftnm+'VF_'+dirfmt+'s' if option.isvf else ftnm+dirfmt+'s'
	tcdir=ftnm+'VF_TTCs' if option.isvf else ftnm+dirfmt[0]+'TCs'
	return os.path.join(option.outdir, tfdir), os.path.join(option.outdir, tcdir)

def saveall(option):
	tfdir, tcdir=tctfdir(option)
	os.makedirs(tfdir, exist_ok=True)
	os.makedirs(tcdir, exist_ok=True)
	inttc=list()
	ttcpth=str()
	for k in option.vks:
		font=option.vfonts[k]
		uvsfill(font, False)
		flnm=font['name'].getDebugName(6)
		fmlnm=flnm.split('-')[0]
		dirnm=tfdir if option.isvf else os.path.join(tfdir, fmlnm.replace('HW', ''))
		os.makedirs(dirnm, exist_ok=True)
		if 'VF' in flnm: flnm=fmlnm.replace('VF', '-VF')
		otfpth=os.path.join(dirnm, flnm+'.'+option.exn)
		if k=='nm':
			ttcnm=flnm+'.'+option.exn+'.ttc' if option.isvf else flnm+'.ttc'
			ttcpth=os.path.join(tcdir, ttcnm)
		inttc.append(otfpth)
		fontsv=TTFont(option.infile, recalcTimestamp=False)
		fontsv['OS/2'].achVendID=cfg['ID']
		fontsv['head'].fontRevision=float(cfg['Version'])
		if 'it' in k:
			fontsv['head'].macStyle|=0b10
			fontsv['OS/2'].fsSelection|=1
			fontsv['OS/2'].fsSelection&=~0b1000000
		for tb in ('name', 'cmap', 'GSUB', 'GPOS'):
			fontsv[tb]=font[tb]
		if 'glyf' in fontsv:
			fontsv['head'].yMax=fontsv['hhea'].ascender
			fontsv['head'].yMin=fontsv['hhea'].descender
		logging.info(f'Saving {otfpth}')
		fontsv.save(otfpth)
		fontsv.close()
	logging.info(f'Saving {ttcpth}')
	otf2otc.run(['-o', ttcpth]+inttc)

class Option:
	def __init__(self):
		self.infile=None
		self.outdir=None
		self.exn=None
		self.isvf=None
		self.oldps=None
		self.oldname=None
		self.loczh=dict()
		self.vfonts=dict()
		self.vks=list()

def main(infile, outdir):
	logging.info('*'*50)
	logging.info('====Build Shanggu Fonts====\n')
	logging.info(f'Input font: {infile}')
	logging.info(f'Output dir: {outdir}')
	option=Option()
	option.infile=infile
	option.outdir=outdir
	option.exn=infile.split('.')[-1].lower()
	with TTFont(option.infile) as font:
		option.cmap=font.getBestCmap()
		option.oldname=font['name']
		option.oldps=font['name'].getDebugName(6)
		option.isvf='fvar' in font
		logging.info('Getting the localized lookups table.')
		for ltg in ('ZHS', 'ZHT'):
			option.loczh[ltg]=getloclk(font, ltg)
	notmono='Mono' not in option.oldps
	varks=['nm', 'tc', 'sc', 'jp']
	if notmono: varks.append('st')
	for k in varks:
		kex=k+'hw' if notmono else k+'it'
		for k2 in (k, kex):
			option.vks.append(k2)
			option.vfonts[k2]=TTFont(option.infile)
			buildot(option, k2)
	logging.info('Saving fonts.')
	saveall(option)
	logging.info('Finished!')
	logging.info('*'*50)

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
