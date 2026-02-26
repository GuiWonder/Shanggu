import os, json

TAG='auto-build'
LAN='TC'

cfg=json.load(open('./main/configs/config.json', 'r', encoding='utf-8'))
styles=['Sans', 'Serif', 'Mono', 'Round']
fmts=['OTF', 'TTF', 'OTC', 'TTC']

def locnm(f, l):
	nmstrs=[cfg[l]['Name'] if l in cfg else cfg['Name'], ]
	for sty in styles:
		if sty in f:
			if l in cfg: nmstrs[-1]+=cfg[l][sty]
			else: nmstrs.append(sty)
			break
	else: return None
	if 'VF' in f:
		nmstrs.append(cfg[l]['VF'] if l in cfg else 'VF')
	for fmt in fmts:
		if fmt in f:
			nmstrs+=[fmt, cfg[l]['Format'] if l in cfg else 'Format']
			break
	else: return None
	return ' '.join(nmstrs)

cmdtg=f'gh release edit "{TAG}" --title "Update {TAG}" 2>/dev/null || gh release create "{TAG}" --draft --title "Release {TAG}"'
os.system(cmdtg)

for f in os.listdir():
	if f.split('.')[-1].lower() in ['7z', 'zip']:
		tgnm=str() if f.lower().endswith('.zip') else locnm(f, LAN)
		cmdup=f'gh release upload "{TAG}" "{f}'
		cmdup=f'gh release upload "{TAG}" "{f}'
		if tgnm: cmdup+=f'#{tgnm}" --clobber'
		else: cmdup+=f'" --clobber'
		os.system(cmdup)
