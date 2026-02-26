from fontTools.ttLib import TTFont
from hpsh import *
from fontTools import subset
from datetime import datetime

CONFIG_JSON='config.json'
SOURCEHAN_CFG_JSON='sourcehan.json'
UVS_CFG_JSON='uvs.json'
SH10_CFG_JSON='sourcehan10.json'

JP_VARIANTS=[
	('𰰨', '芲'), ('𩑠', '頙'), ('鄉', '鄕'), ('唧', '喞'), ('𥄳', '眔')
]
RADICAL_VARIANTS=[
	('⽉', '月'), ('⻁', '虎'), ('⾳', '音'), ('⿓', '龍'),
	('⼾', '戶'), ('飠', '𩙿'), ('礻', '⺬')
]
SC_VARIANTS=[('𫜹', '彐'), ('𣽽', '潸')]

UVS_MULTIPLE=[
	('⺼', '月', 'E0100'), ('𱍐', '示', 'E0100'), ('䶹', '屮', 'E0101'),
	('𠾖', '器', 'E0100'), ('𡐨', '壄', 'E0100'), ('𤥨', '琢', 'E0101'),
	('𦤀', '臭', 'E0100'), ('𨺓', '隆', 'E0100'), ('𫜸', '叱', 'E0101'),
	('暨', '曁', 'E0101'), ('廄', '廏', 'E0101'), ('倂', '併', 'E0101')
]

LOCL_LANG_TAGS={
	'krgl': 'KOR', 'scgl': 'ZHS', 'tcgl': 'ZHT', 'hcgl': 'ZHH'
	}

def load_json(js_name):
	with open(os.path.join(SCRIPT_DIR, 'configs', js_name), 'r', encoding='utf-8') as f:
		return json.load(f)

def getuvs(cmap):
	uvs_map={}
	for subtable in cmap.tables:
		if subtable.format==14:
			for selector, records in subtable.uvsDict.items():
				for code, glyph in records:
					if code not in uvs_map:
						uvs_map[code]={}
					uvs_map[code][selector]=glyph
	return uvs_map

def cffinfo(font, config):
	if 'CFF ' in font:
		cff=font['CFF '].cff
		cff.fontNames[0]=cff.fontNames[0].replace('SourceHan', config['Name'].replace(' ', ''))
		cff[0].FamilyName=cff[0].FamilyName.replace('Source Han', config['Name'])
		cff[0].FullName=cff[0].FullName.replace('Source Han', config['Name'])
		cff[0].Notice=config['Copyright'].format(name=config['Name'], year=datetime.now().year)
		cff[0].CIDFontVersion=float(config['Version'])
		for dic in cff[0].FDArray:
			dic.FontName=dic.FontName.replace('SourceHan', config['Name'].replace(' ', ''))

def locglrpl(font, new_map, ssty, locl_data):
	locgls=dict()
	shset=load_json(SOURCEHAN_CFG_JSON)
	cmap=font.getBestCmap()
	for key, lang_tag in LOCL_LANG_TAGS.items():
		for ch in shset[key]:
			code=ord(ch)
			if code not in cmap: continue
			g1=cmap[code]
			assert g1 not in locgls, f'Code point U+{code:04X} ({ch}) already remapped'
			g2=glfrloc(g1, locl_data[lang_tag])
			if g2: locgls[g1]=g2
	for code in cmap:
		if cmap[code] in locgls:
			assert code not in new_map, f'Code point U+{code:04X} ({chr(cd)}) already remapped'
			new_map[code]=locgls[cmap[code]]
	if ssty!='Serif':
		for ch in shset['sans']:
			code=ord(ch)
			new_map[code]=glfrloc(cmap[code], locl_data['ZHT'])

def locvar(font, new_map, locl_data):
	cmap=font.getBestCmap()
	for ch1, ch2 in JP_VARIANTS + RADICAL_VARIANTS:
		code1, code2=ord(ch1), ord(ch2)
		if code2 in cmap:
			assert code1 not in new_map, f'Variant {ch1} already mapped'
			new_map[code1]=cmap[code2]
	for ch1, ch2 in SC_VARIANTS:
		code1, code2=ord(ch1), ord(ch2)
		if code2 in cmap:
			assert code1 not in new_map, f'Variant {ch1} already mapped'
			g2=glfrloc(cmap[code2], locl_data['ZHS'])
			if g2:
				new_map[code1]=g2

def setuvs(new_map, uvs_dict):
	uvs_cfg=load_json(UVS_CFG_JSON)
	tv={ord(ch): int(uv, 16) for ch, uv in uvs_cfg.items()}
	for c, sel in uvs_dict.items():
		if c in tv and tv[c] in sel:
			g=sel[tv[c]]
			if c in new_map:
				if new_map[c]==g: continue
				else: raise RuntimeError(f'UVS mapped diffent glyph at {chr(c)} U+{c:04X}: {new_map[c]} vs {g}')
			new_map[c]=g

	for ch1, ch2, ch3 in UVS_MULTIPLE:
		u1, u2, sel=ord(ch1), ord(ch2), int(ch3, 16)
		if u2 in uvs_dict and sel in uvs_dict[u2]:
			assert u1 not in new_map, f'UVS variant {ch2} already mapped'
			new_map[u1]=uvs_dict[u2][sel]

def getother(font, font2, repdict):
	logging.info('Processing glyphs from other fonts.')
	if 'CFF ' in font or 'CFF2' in font:
		if 'CFF2' in font:
			cff=font['CFF2'].cff
			cff2=font2['CFF2'].cff
		else:
			cff=font['CFF '].cff
			cff2=font2['CFF '].cff
		cff2.desubroutinize()
		for fontname in cff.keys():
			fontsub=cff[fontname]
			cs=fontsub.CharStrings
			for fontname2 in cff2.keys():
				fontsub2=cff2[fontname2]
				cs2=fontsub2.CharStrings
				for g1,g2 in repdict.items():
					cs[g1]=cs2[g2]
	for g1,g2 in repdict.items():
		for xmtx in ['hmtx', 'vmtx']:
			if xmtx in font and xmtx in font2:
				font[xmtx][g1] = font2[xmtx][g2]
		if 'VORG' in font and 'VORG' in font2:
			if g2 in set(font2['VORG'].VOriginRecords.keys()):
				font['VORG'].VOriginRecords[g1]=font2['VORG'].VOriginRecords[g2]
			elif g1 in set(font['VORG'].VOriginRecords.keys()):
				del font['VORG'].VOriginRecords[gl]
		if 'glyf' in font and 'glyf' in font2:
			font['glyf'].glyphs[g1]=font2['glyf'].glyphs[g2]
		if 'gvar' in font and 'gvar' in font2:
			font['gvar'].variations[g1]=font2['gvar'].variations[g2]

def newglyph(font, ssty, wt, exn, locl_data):
	cmap=font.getBestCmap()
	logging.info('Getting glyphs from  new.')
	filenew=os.path.join(SCRIPT_DIR, f'New/New{ssty}-{wt}.{exn}')
	if os.path.isfile(filenew):
		with TTFont(filenew) as font2:
			getnew=dict()
			cmap2=font2.getBestCmap()
			cnsp='写泻画瑶恋峦蛮挛栾滦弯湾'
			for c, g2 in cmap2.items():
				if c==0x20 or c not in cmap: continue
				if c==ord('笄'): continue
				ch=chr(c)
				logging.info(f'Found new character: {ch} (U+{c:04X})')
				if ch in cnsp: g1=glfrloc(cmap[c], locl_data['ZHS'])
				else: g1=cmap[c]
				getnew[g1]=g2
			loczhsnew=getloclk(font2, 'ZHS')
			for ch in '禅遥':
				logging.info(f'Found locl character: {ch} (U+{c:04X})')
				g1=glfrloc(cmap[ord(ch)], locl_data['ZHS'])
				g2=glfrloc(cmap2[ord(ch)], loczhsnew)
				getnew[g1]=g2
			getother(font, font2, getnew)
			font2.close()
			for table in font['cmap'].tables:
				if table.format==14:
					for uv in table.uvsDict:
						table.uvsDict[uv]=[cg for cg in table.uvsDict[uv] if cg[1] not in getnew.values()]
	else: logging.error('New font not found.')

	if wt=='VF': return
	logging.info('Getting glyphs from SourceHan 1.0x.')
	file10=os.path.join(SCRIPT_DIR, f'sourcehan10/SourceHan{ssty}-{wt}.{exn}')
	if os.path.isfile(file10):
		with TTFont(file10) as font10:
			get10=dict()
			sh10set=load_json(SH10_CFG_JSON)
			subsetter=subset.Subsetter()
			all10=sh10set[ssty]
			if ssty+'TC' in sh10set: all10+=sh10set[ssty+'TC']
			subsetter.populate(text=all10)
			subsetter.subset(font10)
			cmap10=font10.getBestCmap()
			for ch10 in sh10set[ssty]:
				c=ord(ch10)
				if c in cmap and c in cmap10:
					logging.info(f'Found 1.0 character: {ch10} (U+{c:04X})')
					get10[cmap[c]]=cmap10[c]
			loczht10=getloclk(font10, 'ZHT')
			if ssty+'TC' in sh10set:
				for ch10 in sh10set[ssty+'TC']:
					c=ord(ch10)
					gll=glfrloc(cmap10[c], loczht10)
					if c in cmap and gll:
						logging.info(f'Found 1.0 TC character: {ch10} (U+{c:04X})')
						get10[cmap[c]]=gll
			getother(font, font10, get10)
	else:
		logging.error('SourceHan 1.0x not found.')

def ckdlg(font, uvs_dict):
	rplg=dict()
	for ch in '月成':
		rplg[uvs_dict[ord(ch)][0xE0100]]=uvs_dict[ord(ch)][0xE0101]
	dllk=set()
	for ki in font['GSUB'].table.FeatureList.FeatureRecord:
		if ki.FeatureTag=='dlig': dllk.update(ki.Feature.LookupListIndex)
	for i in dllk:
		for st in font['GSUB'].table.LookupList.Lookup[i].SubTable:
			if st.LookupType==7: stbl=st.ExtSubTable
			else: stbl=st
			if stbl.LookupType!=4: continue
			for lgg in list(stbl.ligatures):
				for lg in list(stbl.ligatures[lgg]):
					for ilin in range(len(lg.Component)):
						if lg.Component[ilin] in rplg:
							lg.Component[ilin]=rplg[lg.Component[ilin]]

def cksploc(font, locl_data):
	cmap=font.getBestCmap()
	spdic={cmap[ord(ch)]:glfrloc(cmap[ord(ch)], locl_data['ZHS']) for ch in simpch}
	for lan in ['ZHT', 'ZHH']:
		for lki in locllki(font['GSUB'], lan):
			for st in font['GSUB'].table.LookupList.Lookup[lki].SubTable:
				if st.LookupType==7 and st.ExtSubTable.LookupType==1:
					tabl=st.ExtSubTable.mapping
				elif st.LookupType==1:
					tabl=st.mapping
				else:
					continue
				for spgs in spdic:
					if spgs in tabl:
						tabl[spgs]=spdic[spgs]

def subcff(cfftb, glyphs):
	ftcff=cfftb.cff
	for fontname in ftcff.keys():
		fontsub=ftcff[fontname]
		cs=fontsub.CharStrings
		for g in fontsub.charset:
			if g not in glyphs: continue
			c, _=cs.getItemAndSelector(g)
		if cs.charStringsAreIndexed:
			indices=[i for i,g in enumerate(fontsub.charset) if g in glyphs]
			csi=cs.charStringsIndex
			csi.items=[csi.items[i] for i in indices]
			del csi.file, csi.offsets
			if hasattr(fontsub, 'FDSelect'):
				sel=fontsub.FDSelect
				sel.format=None
				sel.gidArray=[sel.gidArray[i] for i in indices]
			newCharStrings={}
			for indicesIdx, charsetIdx in enumerate(indices):
				g=fontsub.charset[charsetIdx]
				if g in cs.charStrings:
					newCharStrings[g]=indicesIdx
			cs.charStrings=newCharStrings
		else:
			cs.charStrings={g:v
					  for g,v in cs.charStrings.items()
					  if g in glyphs}
		fontsub.charset=[g for g in fontsub.charset if g in glyphs]
		fontsub.numGlyphs=len(fontsub.charset)

def subgl(font):
	cmap=font.getBestCmap()
	usedg=set()
	usedg.add('.notdef')
	usedg.update(cmap.values())
	uvdic=getuvs(font['cmap'])
	for c in uvdic:
		for v in uvdic[c]: usedg.add(uvdic[c][v])
	useloc={cmap[ord(ch)] for ch in p_zhs+p_zht+simpch if ord(ch) in cmap}
	logging.info('Checking Lookup table.')
	loclks=list()
	for i in range(len(font['GSUB'].table.FeatureList.FeatureRecord)):
		if font['GSUB'].table.FeatureList.FeatureRecord[i].FeatureTag=='locl':
			loclks+=font['GSUB'].table.FeatureList.FeatureRecord[i].Feature.LookupListIndex
	for lki in set(loclks):
		for st in font['GSUB'].table.LookupList.Lookup[lki].SubTable:
			stbl=st.ExtSubTable if st.LookupType==7 else st
			assert stbl.LookupType==1
			tabl=stbl.mapping
			for k1 in list(tabl.keys()):
				if k1 in useloc or tabl[k1] in useloc:
					usedg.add(k1)
					usedg.add(tabl[k1])
				else:
					del tabl[k1]
	for ki in font['GSUB'].table.LookupList.Lookup:
		for st in ki.SubTable:
			stbl=st.ExtSubTable if st.LookupType==7 else st
			lktp=stbl.LookupType
			if lktp==1:
				tabl=stbl.mapping
				for g1, g2 in list(tabl.items()):
					if g1 in usedg:
						usedg.add(g2)
					else:
						del tabl[g1]
			elif lktp==3:
				for item in list(stbl.alternates.keys()):
					if item in usedg:
						usedg.update(set(stbl.alternates[item]))
					else:
						del stbl.alternates[item]
			elif lktp==4:
				for li in list(stbl.ligatures):
					for lg in list(stbl.ligatures[li]):
						a=list(lg.Component)
						a.append(li)
						if set(a).issubset(usedg):
							usedg.add(lg.LigGlyph)
						else:
							stbl.ligatures[li].remove(lg)
					if len(stbl.ligatures[li])<1:
						del stbl.ligatures[li]
			elif lktp==5:
				if hasattr(stbl, 'Coverage'):
					for tb in stbl.Coverage:
						usedg.update(tb.glyphs)
			elif lktp==6:
				for tb in stbl.BacktrackCoverage:
					usedg.update(tb.glyphs)
				for tb in stbl.InputCoverage:
					usedg.update(tb.glyphs)
				for tb in stbl.LookAheadCoverage:
					usedg.update(tb.glyphs)
			else: raise
	for ki in font['GPOS'].table.LookupList.Lookup:
		for st in ki.SubTable:
			stbl=st.ExtSubTable if st.LookupType==9 else st
			lktp=stbl.LookupType
			if lktp==1:
				coverage=stbl.Coverage
				coverage.glyphs=[g for g in coverage.glyphs if g in usedg]
			elif lktp==2:
				coverage=stbl.Coverage
				coverage.glyphs=[g for g in coverage.glyphs if g in usedg]
				if stbl.Format==1:
					for pair in stbl.PairSet:
						pair.PairValueRecord=[vr for vr in pair.PairValueRecord if vr.SecondGlyph in usedg]
				elif stbl.Format==2:
					stbl.ClassDef1.classDefs={cld:stbl.ClassDef1.classDefs[cld] for cld in stbl.ClassDef1.classDefs.keys() if cld in usedg}
					stbl.ClassDef2.classDefs={cld:stbl.ClassDef2.classDefs[cld] for cld in stbl.ClassDef2.classDefs.keys() if cld in usedg}
			elif lktp==4:
				markcoverage=stbl.MarkCoverage
				markcoverage.glyphs=[g for g in markcoverage.glyphs if g in usedg]
				basecoverage=stbl.BaseCoverage
				basecoverage.glyphs=[g for g in basecoverage.glyphs if g in usedg]
			else:
				raise
	nnnd=list()
	for fl in font.getGlyphOrder():
		if fl in usedg or fl in ('.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'):
			nnnd.append(fl)
		else:
			if 'VORG' in font and fl in font['VORG'].VOriginRecords:
				del font['VORG'].VOriginRecords[fl]
			if 'gvar' in font and fl in font['gvar'].variations:
				del font['gvar'].variations[fl]
			del font['hmtx'][fl]
			del font['vmtx'][fl]
	if 'CFF ' in font:
		subcff(font['CFF '], set(nnnd))
	elif 'CFF2' in font:
		subcff(font['CFF2'], set(nnnd))
	elif 'glyf' in font:
		font['glyf'].glyphs={g:font['glyf'].glyphs[g] for g in set(nnnd)}
	font.setGlyphOrder(nnnd)

def main(infile, outfile):
	logging.info('*' * 50)
	logging.info('==== Build Shanggu Fonts ====')
	logging.info(f'Input font: {infile}')
	logging.info(f'Output font: {outfile}')
	config=load_json(CONFIG_JSON)
	with TTFont(infile) as font:
		fpsn=font['name'].getDebugName(6)
		ssty=str()
		if 'Sans' in fpsn or 'Mono' in fpsn: ssty='Sans'
		elif 'Serif' in fpsn: ssty='Serif'
		else: raise
		if 'CFF ' in font or 'CFF2' in font: exn='otf'
		elif 'glyf' in font: exn='ttf'
		else: raise
		if 'fvar' in font: wt='VF'
		else:
			wtn={250:'ExtraLight', 300:'Light', 350:'Normal', 400:'Regular', 500:'Medium', 600:'SemiBold', 700:'Bold', 900:'Heavy'}
			wt=wtn[font['OS/2'].usWeightClass]
		logging.info(f'Detected {ssty} {wt} {exn.upper()} font.')
		cffinfo(font, config)
		uvsfill(font, isfill=True)
		new_map={}
		logging.info('Extracting locl mappings.')
		locl_data={
			lang: getloclk(font, lang)
			for lang in LOCL_LANG_TAGS.values()
		}
		logging.info(f'Loaded locl mappings for languages: {sorted(locl_data.keys())}')
		logging.info('Extracting uvs mappings.')
		uvs_dict=getuvs(font['cmap'])
		logging.info('Processing locl Variant.')
		locglrpl(font, new_map, ssty, locl_data)
		logging.info('Processing other Variant.')
		locvar(font, new_map, locl_data)
		logging.info('Processing uvs glyphs.')
		setuvs(new_map, uvs_dict)
		logging.info('Remap glyphs.')
		cmap=font.getBestCmap()
		for c, g in new_map.items():
			if c in cmap and cmap[c]==g: continue
			logging.info(f'Remap U+{c:04X} ({chr(c)}) to {g}')
			setcg(font['cmap'], c, g)
		logging.info('Checking lookups.')
		ckdlg(font, uvs_dict)
		logging.info('Getting glyphs from other fonts.')
		newglyph(font, ssty, wt, exn, locl_data)
		cksploc(font, locl_data)
		logging.info('Checking for unused glyphs.')
		subgl(font)
		uvsfill(font, isfill=False)
		logging.info(f'Saving font to {outfile}')
		font.save(outfile)
		logging.info('Done.')
		logging.info('*'*50)

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
