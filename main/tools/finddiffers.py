import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

def parseflnm(args):
	outfile=str()
	fontList=list()
	i = 0
	argn = len(args)
	while i < argn:
		arg  = args[i]
		i += 1
		if arg[0] != '-':
			fontList.append(arg)
		elif arg == "-o":
			outfile = args[i]
			i += 1
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if len(fontList)!=2:
		raise RuntimeError("You must specify two input fonts.")
	if not outfile:
		raise RuntimeError("You must specify output fonts.")
	return outfile, fontList

def subft(font, subst):
	nnnd=list()
	for fl in font.getGlyphOrder():
		if fl in subst or fl in ('.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'):
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
			if hasattr(fontsub, "FDSelect"):
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

def ckgl(cod):
	g1 = gs1[cmap1[cod]]
	g2 = gs2[cmap2[cod]]

	p1 = RecordingPen()
	p2 = RecordingPen()

	g1.draw(p1)
	g2.draw(p2)

	return p1.value==p2.value	

outfile, fontList=parseflnm(sys.argv[1:])
file1, file2=fontList[0], fontList[1]
font1 = TTFont(file1)
font1["cmap"].tables=[table for table in font1["cmap"].tables if table.format!=14]

cmap1 = font1.getBestCmap()
gs1 = font1.getGlyphSet()
font2 = TTFont(file2)
cmap2 = font2.getBestCmap()
gs2 = font2.getGlyphSet()
subgl=set()
subgl.add('.notdef')

print('Check outlines...')
for cod in cmap2:
	if not ckgl(cod):
		subgl.add(cmap1[cod])
print('Subset...')
subft(font1, subgl)
for table in font1["cmap"].tables:
	table.cmap={cd:table.cmap[cd] for cd in table.cmap if table.cmap[cd] in subgl}
del font1['GSUB']
del font1['GPOS']
print('Saving', outfile)
font1.save(outfile)
