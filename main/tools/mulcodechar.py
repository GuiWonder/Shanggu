import os, sys
from fontTools.ttLib import TTFont

def setcg(code, glyf):
	for table in font["cmap"].tables:
		if (table.format==4 and code<=0xFFFF) or table.format==12 or code in table.cmap:
			table.cmap[code]=glyf

print('*'*50)
infile=sys.argv[1]
outfile=sys.argv[2]
font=TTFont(infile)
print('Merging multi-code Chinese characters...')
pydir=os.path.abspath(os.path.dirname(__file__))
cmap=font.getBestCmap()
with open(os.path.join(pydir, '../configs/mulcodechar.dt'), 'r', encoding='utf-8') as f:
	for line in f.readlines():
		litm=line.split('#')[0].strip()
		if '-' not in litm: continue
		s, t=litm.split(' ')[0].split('-')
		s, t=s.strip(), t.strip()
		if s and t and s!=t and ord(t) in cmap:
			print('Processing '+s+'-'+t)
			setcg(ord(s), cmap[ord(t)])
print('Saving fonts...')
newfont=TTFont(infile)
newfont['cmap']=font['cmap']
newfont.save(outfile)
print('Finished!')
print('*'*50)
