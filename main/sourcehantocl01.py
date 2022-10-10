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

def getother(fname, gtext):
	with open(gtext, 'r', encoding='utf-8') as f:
		s10=f.read().strip()
		font10 = json.loads(subprocess.check_output((otfccdump, '--no-bom', fname)).decode("utf-8", "ignore"))
		scl = 1.0
		if font["head"]["unitsPerEm"] != font10["head"]["unitsPerEm"]:
			scl = font["head"]["unitsPerEm"] / font10["head"]["unitsPerEm"]
		for ch in s10:
			uni=str(ord(ch))
			if uni in font10['cmap'] and uni in font['cmap']:
				g1=font['cmap'][uni]
				g2=font10['cmap'][uni]
				if g1=='.notdef' or g2=='.notdef':
					continue
				print('处理', ch)
				gnew=dict()
				if 'CFF_fdSelect' in font['glyf'][g1]:
					gnew['CFF_fdSelect']=font['glyf'][g1]['CFF_fdSelect']
				if 'CFF_CID' in font['glyf'][g1]:
					gnew['CFF_CID']=font['glyf'][g1]['CFF_CID']
				for k in font10['glyf'][g2].keys():
					if k not in ('CFF_fdSelect', 'CFF_CID'):
						gnew[k]=font10['glyf'][g2][k]
				font['glyf'][g1]=gnew
				if scl != 1.0:
					sclglyph(font['glyf'][g1], scl)

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

def gfmloc(g, loczh):
	for zhtb in loczh:
		ftype=font['GSUB']['lookups'][zhtb]['type']
		if ftype=='gsub_single':
			for subtable in font['GSUB']['lookups'][zhtb]['subtables']:
				if g in subtable:
					return subtable[g]
	return ""

def creattmp():
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

	#exch='侾倜兎剪叟呀咎咠唹嚳墁奜媺嬴孼宬岈巓幃幰廋微徵恝惆惘搜撐於旅旣晧晷曁杓栲桯梏檉毒氓汋汒沿淤湔溲滾漰潛潤澔瀆瀛灼煎煢爟牘牙牚犢獌珵珹琱甿瘦瞎瞬砑稠稧穿窖竇箭篠簉糙糱絳綢緯繭續罔羸肓腴膄臝臾舛舜舞船艘芒茫萸蒯蕣虻蚌蜩蟃衮袞裒裯襁覿訝訹誥讀豹負賙贏贖趼輞迓邙郜鄰鉛鋥鎉鏹閼降隙雕靠颼馰騪驎驘鬋魍鮵鴉鵠鵩鵰麗麟黷匾喝櫝殺浧釁䐁丫夢拄晩覈覉遑隍偰'
	#exgl=getgname(exch)
	krd='丈乖乳交伴使侮侵便偉偏偠健傑僊僧免全公关具兼再冒冓冬凞刃分判券削割劘勇勉勝勤包化半卑博卻厖叉及史吏吸呈咬咲唐唳唾啄啓喓喞喫嘆嘲噓器嚚嚮圍坪堙堞塀塌塘塚墜墨壄壿复夔契奓妥姬姿娜娵婦媛媾嫌宵寐寒寧尊尋導尨屣層峯巡巨巽帽幣平庭廉廊廐廟廠延廷建廻弊弱彩徘忍忭急悔情愉慧慨憊憎懲⼾房所扇扈扉扱抱拐拒拳挺捨捩掃採揃揲援搆搔搨摩摯敏敷⽂斐斧斲旃昀晴暑暖曌曙曜更朕朗杖松柊栓校栴梅梗梛梢榻構槩槪欄次泡派浮海浸消渚港湧湮溝滋滕滬漢潔澘濦濯灞灰炷煙煮燏燿爨爵⽗爺牀牂牒⽛狀狡猪猶班琢瑞環璵甄甦甩畇畔癒癤盆益矩砲硝硬碑碟磨社祈祉祐祖祝神祢祥禍禎福禫程稱穀穢⽳突窙竄筵節簿籐籾粉精糖紋納級紛終絞絣綮総編緩練縛縢縫縵繁繩纛缾署⽻翁翌習翔翠翦翩翫翻翼耀者耕耗聡肇肖肩肺胞脈腱臭⾇艇花苒苣菔菜菟著蓮蓴薄藤蘭虁虐虔虜虞蚊蚤蛀蝇蝙螽蟒蠨衂衆術衛褊褐覃視覯訟註評認誕誤誹請諏諞諭諮諸謁謄謙講謹譖豁貧貨賆資賊賓購贈距踛躍躸較輸轄迅迎近返迪迫迬迭述迷追退送逃逆透逐途通逝逞速造逢連逮週進逸遂遇遊運遍過道達違遘遠遣適遭遮遵遷選遺遼避邃還那邦邨都鄕采釜鉒鉼銎鋆鍵鎌鎖鏖门陬隆隊隣隻雇雙難雪雰霔靖静⾮靡靭靴鞭響頌頑頒頻類顧⾷飢飯飼飽飾養餓館駁駩騰驟骪鬅鬣鬮魔鮗鮫鱍鱏鶐鶹鶾鶿⿇麿黛鼂鼇鼈鼬⿐齹⿔龝廊朗𰻞衋倂搤濊癢膋諲豃趿軶輧込鯞聖冒'
	trd='㈾㊩㊮㕙㗴㙇㙈㧻㨘㫵㯳㵆㵟㵪㵵㶏㹃㻇㻐㻗㻴䁓䃺䄲䅮䅼䈑䉠䜘䡱䤑䤵䥲䱻䱽䶉丸倯偺傂傦傴僈儆儚兂兓兝凐剎医匽匾區唬啝啿喒喼嘔嘬噳嚂堪塭塺墈夢婓婔尠屄岈岋岤峑幭弒弢恐恮愖愝慪憼懱懵戡摠摳撮撯擎擏攠斟昊昞昶朂柭栃栐梤椕椹樞樧檶歁歅歋歐毆汆汛汵沉沷洖洰浧浻淭淲湛滘漒漚潖澂澞澬濸瀎灖牄犘獊瑏璁璥甂甌甍甚甝眾瞂瞘矏砑硂硹硿碪碰磃磘磡礣笌籴糂糌緰聰肏舋芔虥蚐蚜蟼蠛衊貙赹輙銏銩鋷鍖鍤鎐鎦鎩鏂阠馤驄驅驔驖驚鸆麫黀黂黮鼢鼦鼩齖齱殺㖗㘚㮇㴲䒳䮐偛偡傯刏勘啗嗖埾堔壏嶇嶵嶶弅憌拄掐掭掰掽揕揝搋摋擨敺斳枒栥棎榗榹檓檨淊溦溾漫璺睃穨篫篬簅籈籕羀羒脋臽蛧蛩蜭蝆蝨螥螩螶蟌贀贉跫踸軀邳鄋鄮鄸鄹醙醧醩醫錎閷閻闉陷鞏韈馛駏骺鬾鬿魀魊鰻鱋鱴鵇鷖鷗麱黇黢黫䁥䓟䔽䕕䕡嵁暱楶櫙欿毉潜瑿蠀蠮醰黳釁佢僋冹卼厞叡啟塣壾奜悜戺揙楄檌溞瀩眅睙砨碥稨耛耩蛂蜧蝹螔覤覹觓豟豱豽貾贙踂軡軧鄑銇錓鎉鎪鏏陫頛馧驈驨鯦鯫鵚鶣齴氯椂睩䔄熎䬙蘨蘣蘳嫹擙鐭蔑蕞莈敬䏰归犟'#壬任凭拰恁栠軠鈓賃銋鵀舌恬舔甜舐憩湉
	trhkd='䭯䭰䭲䮖䴴䶜倡偈傮僣儥劊勂厭唱嗂嘈噲嚕堨壓尳峼嵑嶆嶱巀幵异彉徟徻愒愮愲慒懀懨揭撗擖擫敹昌暍曶曷曹替會桀椙楬榣榤槽樇檜檠櫓櫜櫝歇毼氌沓涾淍淐渠渴滍漕潃澮濌猒猖猣猲獚獦獪琩璯皾睭瞺矌碉碣磔磭磷穔穬穭筶篎粈粣粼糟糨糮羯聽菖葛薈藒蚩蝎蝬螖螬蟝蠍蠽贕赻踏蹧蹸輵轕鄶鋯錔錩錭鍻鎥鑥閶陻鞜鞨韘韥飺饜馜馝馞馡馣馥騆騔魘魯鯧鰽鱠鶡黶齃齔喝㭼䂿儈厴堎惾抇擼朘稄糔羧耴薨踜靨黈鼭噶嶜甭甮唦挱鷬朁僭噆憯潛蠶'#栠朅
	sip='萏'

	pen='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
	pzhs='·’‘”“•≤≥≮≯！：；？'+pen
	pzht='·’‘”“•、。，．'+pen
	sipch='将蒋残浅践与写泻惮禅箪蝉恋峦蛮挛栾滦弯湾径茎弥称滞画遥瑶'#変
	pungl=getgname(pzhs+pzht+sipch)

	tbs=set()
	#for krtb in lockor:
	#	a=gettbs(krtb, exgl, False)
	#	if len(a)>200:
	#		tbs.update(a)
	if len(krd)>0:
		krdg=getgname(krd)
		for zhktb in lockor:
			a=gettbs(zhktb, krdg, True)
			tbs.update(a)
	if len(trd)>0:
		trdg=getgname(trd)
		for zhttb in loczht:
			a=gettbs(zhttb, trdg, True)
			tbs.update(a)
	if len(trhkd)>0:
		trhkdg=getgname(trhkd)
		for zhhtb in loczhhk:
			a=gettbs(zhhtb, trhkdg, True)
			tbs.update(a)
	if len(sip)>0:
		simpg=getgname(sip)
		for zhstb in loczhs:
			a=gettbs(zhstb, simpg, True)
			tbs.update(a)

	if len(tbs)>0:
		for itm in tbs:
			gettrch(itm[0], itm[1])
	else:
		print('未找到任何可用的本地化字形！')

	locscv=[('𫜹', '彐')]
	for lv1 in locscv:
		gv2=gfmloc(font['cmap'][str(ord(lv1[1]))], loczhs)
		if gv2:
			print('处理', lv1[0])
			font['cmap'][str(ord(lv1[0]))]=gv2

	print('正在检查本地化列表...')
	vgl=set()
	allpun=set()
	for subs in loc:
		if rmun=='1' or rmun=='2':
			ftype=font['GSUB']['lookups'][subs]['type']
			for subtable in font['GSUB']['lookups'][subs]['subtables']:
				for j, t in list(subtable.items()):
					if ftype=='gsub_single':
						vgl.add(t)
						vgl.add(j)
						if j in pungl or t in pungl:
							allpun.add(j)
							allpun.add(t)
			vgl.difference_update(allpun)

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

	uvsmul=[('⺼', '月', 'E0100'), ('𱍐', '示', 'E0100'), ('䶹', '屮', 'E0101')]
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

	fpn=str()
	for n1 in font['name']:
		if n1['nameID']==6 and '-' in n1['nameString']:
			fpn=n1['nameString']
			break
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
	text10=os.path.join(pydir, 'sourcehan1.0.txt')
	if os.path.isfile(file10) and os.path.isfile(text10):
		getother(file10, text10)
	else:
		print('获取1.0版字形失败！')

	#if ssty=='Sans':
	#	print('正在获取秋空黑体字形...')
	#	filec=os.path.join(pydir, f'ChiuKongGothic-CL/ChiuKongGothic-CL-{wt}{ffmt}')
	#	textc=os.path.join(pydir, 'ChiuKongGothic-CL.txt')
	#	if os.path.isfile(filec) and os.path.isfile(textc):
	#		getother(filec, textc)
	#	else:
	#		print('获取秋空黑体字形失败！')

	if rmun=='2':
		vgl.difference_update(uvsgly)
	elif rmun=='1':
		vgl.update(uvsgly)
	if rmun=='1' or rmun=='2':
		print('正在移除字形...')
		glyph_codes = build_glyph_codes()
		isrm=set()
		for v1 in vgl:
			if len(glyph_codes[v1])<1:
				#print('移除', v1)
				isrm.add(v1)
				del glyph_codes[v1]
				try:
					font['glyph_order'].remove(v1)
				except ValueError:
					pass
				del font['glyf'][v1]
		print('正在检查Lookup表...')
		if 'GSUB' in font:
			for lookup in font['GSUB']['lookups'].values():
				if lookup['type'] == 'gsub_single':
					for subtable in lookup['subtables']:
						for g1, g2 in list(subtable.items()):
							if g1 in isrm or g2 in isrm:
								del subtable[g1]
				elif lookup['type'] == 'gsub_alternate':
					for subtable in lookup['subtables']:
						for item in set(subtable.keys()):
							if item in isrm or len(set(subtable[item]).intersection(isrm))>0:
								del subtable[item]
				elif lookup['type'] == 'gsub_ligature': 
					for subtable in lookup['subtables']:
						s1=list()
						for item in subtable['substitutions']:
							if item['to'] not in isrm and len(set(item['from']).intersection(isrm))<1:
								s1.append(item)
						subtable['substitutions']=s1
				elif lookup['type'] == 'gsub_chaining':
					for subtable in lookup['subtables']:
						for ls in subtable['match']:
							for l1 in ls:
								l1=list(set(l1).difference(isrm))
		if 'GPOS' in font:
			for lookup in font['GPOS']['lookups'].values():
				if lookup['type'] == 'gpos_single':
					for subtable in lookup['subtables']:
						for item in list(subtable.keys()):
							if item in isrm:
								del subtable[item]
				elif lookup['type'] == 'gpos_pair':
					for subtable in lookup['subtables']:
						for item in list(subtable['first'].keys()):
							if item in isrm:
								del subtable['first'][item]
						for item in list(subtable['second'].keys()):
							if item in isrm:
								del subtable['second'][item]
				elif lookup['type'] == 'gpos_mark_to_base':
					nsb=list()
					for subtable in lookup['subtables']:
						gs=set(subtable['marks'].keys()).union(set(subtable['bases'].keys()))
						if len(gs.intersection(isrm))<1:
							nsb.append(subtable)
					lookup['subtables']=nsb

	print('正在设置字体名称...')
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

	print('正在生成字体...')
	tmpfile = tempfile.mktemp('.json')
	with open(tmpfile, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	return tmpfile

print('====思源字体（日版）转传承字形====\n')
inf=str()
outf=str()
rmun=str()
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
if len(sys.argv)>3:
	rmun=sys.argv[3].lower()
else:
	while rmun not in {'1', '2', '3','y', 'n'}:
		rmun=input('是否移除未使用的字形：\n\t1.移除这些字形\n\t2.保留异体选择器中的字形\n\t3.不移除任何字形\n').lower()
if rmun=='y':
	rmun='1'
if rmun=='n':
	rmun='3'

print('正在载入字体...')
font = json.loads(subprocess.check_output((otfccdump, '--no-bom', inf)).decode("utf-8", "ignore"))
glyph_codes = build_glyph_codes()
tmpfile=creattmp()

for x in set(locals().keys()):
	if x not in ('os', 'subprocess', 'otfccbuild', 'outf', 'tmpfile', 'gc'):
		del locals()[x]
gc.collect()
print('正在生成字体文件...')
subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', outf, tmpfile))
os.remove(tmpfile)
print('完成!')
