import os, json, sys, logging

LOG_FORMAT="%(levelname)s: %(message)s"
logging.basicConfig(
	level=logging.INFO,
	format=LOG_FORMAT,
	handlers=[
		logging.StreamHandler(sys.stdout),
	]
)

SCRIPT_DIR=os.path.abspath(os.path.dirname(__file__))

p_en='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
p_zhs='·’‘”“•≤≥≮≯！：；？'+p_en
p_zht='·’‘”“•、。，．'+p_en
simpch='蒋将残浅践写泻惮禅箪蝉恋峦蛮挛栾滦弯湾径茎滞画遥瑶'#変与弥称

def setcg(cmap, code, glyph):
	for table in cmap.tables:
		if (table.format==4 and code<=0xFFFF) or table.format==12 or code in table.cmap:
			table.cmap[code]=glyph

def locllki(ftgsub, lang_tag):
	ftl, lkl=list(), list()
	for sr in ftgsub.table.ScriptList.ScriptRecord:
		for lsr in sr.Script.LangSysRecord:
			if lsr.LangSysTag.strip()==lang_tag:
				ftl+=lsr.LangSys.FeatureIndex
	for ki in ftl:
		ftg=ftgsub.table.FeatureList.FeatureRecord[ki].FeatureTag
		if ftg=='locl':
			lkl+=ftgsub.table.FeatureList.FeatureRecord[ki].Feature.LookupListIndex
	return sorted(set(lkl))

def getloclk(font, lang_tag):
	locdics=list()
	for lki in locllki(font["GSUB"], lang_tag):
		locrpl=dict()
		for st in font["GSUB"].table.LookupList.Lookup[lki].SubTable:
			if st.LookupType==7 and st.ExtSubTable.LookupType==1:
				tabl=st.ExtSubTable.mapping
			elif st.LookupType==1:
				tabl=st.mapping
			for g1 in tabl:
				locrpl[g1]=tabl[g1]
		locdics.append(locrpl)
	return locdics

def glfrloc(gl, loclk):
	for dc in loclk:
		if gl in dc: return dc[gl]

def uvsfill(font, isfill):
	cmap=font.getBestCmap()
	for table in font["cmap"].tables:
		if table.format == 14:
			for selector, records in list(table.uvsDict.items()):
				new_records=[]
				for code, glyph in records:
					if isfill and glyph is None:
						new_records.append((code, cmap.get(code)))
					elif not isfill and code in cmap and glyph == cmap[code]:
						new_records.append((code, None))
					else:
						new_records.append((code, glyph))
				table.uvsDict[selector]=new_records
