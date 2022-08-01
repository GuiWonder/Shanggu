import os, json, subprocess, platform, tempfile, gc, sys
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

fontver='1.000'
fontid='AAF'

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

	#exch='侾倜兎剪叟呀咎咠唹嚳墁奜媺嬴孼宬岈巓幃幰廋微徵恝惆惘搜撐於旅旣晧晷曁杓栲桯梏檉毒氓汋汒沿淤湔溲滾漰潛潤澔瀆瀛灼煎煢爟牘牙牚犢獌珵珹琱甿瘦瞎瞬砑稠稧穿窖竇箭篠簉糙糱絳綢緯繭續罔羸肓腴膄臝臾舛舜舞船艘芒茫萸蒯蕣虻蚌蜩蟃衮袞裒裯襁覿訝訹誥讀豹負賙贏贖趼輞迓邙郜鄰鉛鋥鎉鏹閼降隙雕靠颼馰騪驎驘鬋魍鮵鴉鵠鵩鵰麗麟黷匾喝櫝殺浧釁䐁丫夢拄晩覈覉遑隍聖'
	#exgl=getgname(exch)
	pen='"\'—‘’‚“”„‼⁇⁈⁉⸺⸻'
	pzhs='·’‘”“•≤≥≮≯！：；？'+pen
	pzht='·’‘”“•、。，．'+pen
	sip=str()
	sipch='将蒋残浅践与写泻惮禅箪蝉恋峦蛮変挛栾滦弯湾径茎弥称滞画'
	krd='丈乖乳交伴使侮侵便偉偏偠健偰傑僊僧僭免全公关具兼再冒冓冬凞刃分判券削割劘勇勉勝勤包化半卑博卻厖叉及史吏吸呈咬咲唐唳唾啄啓喓喞喫嘆嘲噓器嚚嚮圍坪堙堞塀塌塘塚墜墨壄壿复夔契奓妥姬姿娜娵婦媛媾嫌宵寐寒寧尊尋導尨屣層峯巡巨巽帽幣平庭廉廊廐廟廠延廷建廻弊弱彩徘忍忭急悔情愉慧慨憊憎懲⼾房所扇扈扉扱抱拐拒拳挺捨捩掃採揃揲援搆搔搨摩摯敏敷⽂斐斧斲旃昀晴暑暖曌曙曜更朕朗杖松柊栓校栴梅梗梛梢榻構槩槪欄次泡派浮海浸消渚港湧湮溝滋滕滬漢潔澘濦濯灞灰炷煙煮燏燿爨爵⽗爺牀牂牒⽛狀狡猪猶班琢瑞環璵甄甦甩畇畔癒癤盆益矩砲硝硬碑碟磨社祈祉祐祖祝神祢祥禍禎福禫程稱穀穢⽳突窙竄筵節簿籐籾粉精糖紋納級紛終絞絣綮総編緩練縛縢縫縵繁繩纛缾署⽻翁翌習翔翠翦翩翫翻翼耀者耕耗聡肇肖肩肺胞脈腱臭⾇艇花苒苣菔菜菟著蓮蓴蔑薄藤蘭虁虐虔虜虞蚊蚤蛀蝇蝙螽蟒蠨衂衆術衛褊褐覃視覯訟註評認誕誤誹請諏諞諭諮諸謁謄謙講謹譖豁貧貨賆資賊賓購贈距踛躍躸較輸轄迅迎近返迪迫迬迭述迷追退送逃逆透逐途通逝逞速造逢連逮週進逸遂遇遊運遍過道達違遘遠遣適遭遮遵遷選遺遼避邃還那邦邨都鄕采釜鉒鉼銎鋆鍵鎌鎖鏖门陬隆隊隣隻雇雙難雪雰霔靖静⾮靡靭靴鞭響頌頑頒頻類顧⾷飢飯飼飽飾養餓館駁駩騰驟骪鬅鬣鬮魔鮗鮫鱍鱏鶐鶹鶾鶿⿇麿黛鼂鼇鼈鼬⿐齹⿔龝廊朗𰻞衋䕡倂搤濊癢膋諲豃趿軶輧込鯞'
	trd='㈾㊩㊮㕙㗴㙇㙈㧻㨘㫵㯳㵆㵟㵪㵵㶏㹃㻇㻐㻗㻴䁓䃺䄲䅮䅼䈑䉠䜘䡱䤑䤵䥲䱻䱽䶉丸倯偺傂傦傴僈儆儚兂兓兝凐凭剎医匽匾區唬啝啿喒喼嘔嘬噆噳嚂堪塭塺墈壬夢婓婔尠屄岈岋岤峑幭弒弢归恐恬恮愖愝慪憩憼懱懵戡拰摠摳撮撯擎擏攠斟昊昞昶朂柭栃栐梤椕椹樞樧檶歁歅歋歐毆汆汛汵沉沷洖洰浧浻淭淲湛滘漒漚潖澂澞澬濸瀎灖牄犘獊瑏璁璥甂甌甍甚甝眾瞂瞘矏砑硂硹硿碪碰磃磘磡礣笌籴糂糌緰聰肏舋舔芔虥蚐蚜蟼蠛衊貙賃赹軠輙鈓銏銩鋷鍖鍤鎐鎦鎩鏂阠馤驄驅驔驖驚鸆麫黀黂黮鼢鼦鼩齖齱殺㖗㘚㮇㴲䒳䮐任偛偡傯刏勘啗嗖埾堔壏嶇嶵嶶弅恁憌拄掐掭掰掽揕揝搋摋擨敺斳枒栥棎榗榹檓檨淊溦溾漫璺睃穨篫篬簅籈籕羀羒脋臽蛧蛩蜭蝆蝨螥螩螶蟌贀贉跫踸軀邳鄋鄮鄸鄹醙醧醩醫銋錎閷閻闉陷鞏韈馛駏骺鬾鬿魀魊鰻鱋鱴鵀鵇鷖鷗麱黇黢黫䁥䓟䔽䕕䕡噶嵁暱楶櫙欿毉潜瑿蠀蠮醰黳釁佢僋冹卼厞叡啟塣壾奜悜戺揙楄檌溞瀩眅睙砨碥稨耛耩聖蛂蜧蝹螔覤覹觓豃豟豱豽貾贙趿踂軡軧軶鄑銇錓鎉鎪鏏陫頛馧驈驨鯞鯦鯫鵚鶣齴氯椂睩'
	trhkd='䭯䭰䭲䮖䴴䶜倡偈傮僣儥劊勂厭唱嗂嘈噲嚕堨壓尳峼嵑嶆嶱巀幵异彉徟徻愒愮愲慒憯懀懨揭撗擖擫敹昌暍曶曷曹替朁會朅栠桀椙楬榣榤槽樇檜檠櫓櫜櫝歇毼氌沓涾淍淐渠渴滍漕潃澮濌猒猖猣猲獚獦獪琩璯皾睭瞺矌碉碣磔磭磷穔穬穭筶篎粈粣粼糟糨糮羯聽菖葛薈藒蚩蝎蝬螖螬蟝蠍蠶蠽贕赻踏蹧蹸輵轕鄶鋯錔錩錭鍻鎥鑥閶陻鞜鞨韘韥飺饜馜馝馞馡馣馥騆騔魘魯鯧鰽鱠鶡黶齃齔喝㭼䂿儈厴堎惾抇擼朘稄糔羧耴薨踜靨黈鼭潛噆噶嶜甭甮唦挱鷬'
	if pun=='2':
		sip+=pzhs
	if pun=='3':
		trd+=pzht
	if simp=='2':
		sip+=sipch

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
	if setname=='1':
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
	elif setname=='2':
		font['OS_2']['achVendID']=fontid
		font['head']['fontRevision']=float(fontver)
		nname=list()
		for nj in font['name']:
			if nj['languageID']==1041:
				ns=dict(nj)
				nt=dict(nj)
				nh=dict(nj)
				ns['languageID']=2052
				ns['nameString']=ns['nameString'].replace('源ノ明朝', '尙古明体').replace('源ノ角ゴシック', '尙古黑体').replace('源ノ等幅', '尙古等宽')
				nt['languageID']=1028
				nt['nameString']=nt['nameString'].replace('源ノ明朝', '尙古明體').replace('源ノ角ゴシック', '尙古黑體').replace('源ノ等幅', '尙古等寬')
				nh['languageID']=3076
				nh['nameString']=nh['nameString'].replace('源ノ明朝', '尙古明體 香港').replace('源ノ角ゴシック', '尙古黑體 香港').replace('源ノ等幅', '尙古等寬 香港')
				nname.append(ns)
				nname.append(nt)
				nname.append(nh)
			#elif nj['nameID']>0 and nj['nameID']<7:
			elif nj['nameID']==3:
				ne=dict(nj)
				ne['nameString']=fontver+';'+fontid+';'+ne['nameString'].split(';')[2].replace('SourceHan', 'AdvocateAncient')
				nname.append(ne)
			elif nj['nameID']==5:
				ne=dict(nj)
				ne['nameString']='Version '+fontver
				nname.append(ne)
			elif nj['nameID']==11:
				ne=dict(nj)
				ne['nameString']='https://github.com/GuiWonder/SourceHanToClassic'
				nname.append(ne)
			elif nj['nameID']!=0 and nj['nameID']!=7 and nj['nameID']!=8:
			#else:
				ne=dict(nj)
				ne['nameString']=ne['nameString'].replace('Source Han', 'Advocate Ancient').replace('SourceHan', 'AdvocateAncient')
				nname.append(ne)
		font['name']=nname
		if 'CFF_' in font:
			font['CFF_']['notice']=''
			font['CFF_']['fontName']=font['CFF_']['fontName'].replace('SourceHan', 'AdvocateAncient')
			font['CFF_']['fullName']=font['CFF_']['fullName'].replace('Source Han', 'Advocate Ancient')
			font['CFF_']['familyName']=font['CFF_']['familyName'].replace('Source Han', 'Advocate Ancient')
			if 'fdArray' in font['CFF_']:
				nfd=dict()
				for k in font['CFF_']['fdArray'].keys():
					nfd[k.replace('SourceHan', 'AdvocateAncient')]=font['CFF_']['fdArray'][k]
				font['CFF_']['fdArray']=nfd
				for gl in font['glyf'].values():
					if 'CFF_fdSelect' in gl:
						gl['CFF_fdSelect']=gl['CFF_fdSelect'].replace('SourceHan', 'AdvocateAncient')
	if setname=='3':
		pname=enname.replace(' ', '')
		nname=list()
		for nj in font['name']:
			if nj['languageID']==1041:
				ns=dict(nj)
				nt=dict(nj)
				nh=dict(nj)
				ns['languageID']=2052
				ns['nameString']=ns['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nt['languageID']=1028
				nt['nameString']=nt['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nh['languageID']=3076
				nh['nameString']=nh['nameString'].replace('源ノ明朝', zhname).replace('源ノ角ゴシック', zhname).replace('源ノ等幅', zhname)
				nname.append(ns)
				nname.append(nt)
				nname.append(nh)
			#elif nj['nameID']>0 and nj['nameID']<7:
			else:
				ne=dict(nj)
				ne['nameString']=ne['nameString'].replace('Source Han Sans', enname).replace('SourceHanSans', pname).replace('Source Han Serif', enname).replace('SourceHanSerif', pname).replace('Source Han Mono', enname).replace('SourceHanMono', pname)
				nname.append(ne)
		font['name']=nname
		if 'CFF_' in font:
			font['CFF_']['fontName']=font['CFF_']['fontName'].replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)
			font['CFF_']['fullName']=font['CFF_']['fullName'].replace('Source Han Sans', enname).replace('Source Han Serif', enname).replace('Source Han Mono', enname)
			font['CFF_']['familyName']=font['CFF_']['familyName'].replace('Source Han Sans', enname).replace('Source Han Serif', enname).replace('Source Han Mono', enname)
			if 'fdArray' in font['CFF_']:
				nfd=dict()
				for k in font['CFF_']['fdArray'].keys():
					nfd[k.replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)]=font['CFF_']['fdArray'][k]
				font['CFF_']['fdArray']=nfd
				for gl in font['glyf'].values():
					if 'CFF_fdSelect' in gl:
						gl['CFF_fdSelect']=gl['CFF_fdSelect'].replace('SourceHanSans', pname).replace('SourceHanSerif', pname).replace('SourceHanMono', pname)

	print('正在生成字体...')
	#tmpfile='tmp.json'
	tmpfile = tempfile.mktemp('.json')
	with open(tmpfile, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	return tmpfile

print('====思源字体（日版）转传承字形====\n')
inf=str()
outf=str()
mch=str()
pun=str()
simp=str()
rmun=str()
setname=str()
enname=str()
zhname=str()
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
if len(sys.argv)<7:
	while mch not in {'y', 'n'}:
		mch=input('是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？(输入Y/N)：\n').lower()
	while pun not in {'1', '2', '3'}:
		pun=input('请选择标点：\n\t1.日本\n\t2.简体中文\n\t3.正体中文（居中）\n')
	while simp not in {'1', '2'}:
		simp=input('请选择简化字字形：\n\t1.日本\n\t2.中国大陆\n')
	while rmun not in {'y', 'n'}:
		rmun=input('是否移除未使用的字形(输入Y/N)：\n').lower()
else:
	mch=sys.argv[3].lower()
	pun=sys.argv[4]
	simp=sys.argv[5]
	rmun=sys.argv[6].lower()
if len(sys.argv)<8:
	while setname not in {'1', '2', '3'}:
		#setname=input('字体名称设置：\n\t1.使用思源原版字体名称\n\t2.使用尙古黑体、尙古明体\n\t3.我来命名\n')
		setname=input('字体名称设置：\n\t2.使用尙古黑体、尙古明体 Advocate Ancient\n\t3.我来命名\n')
else:
	setname=sys.argv[7]
if setname=='3':
	if len(sys.argv)<10:
		while not enname.strip():
			enname=input('请输入英文字体名称：\n')
		while not zhname.strip():
			zhname=input('请输入中字体名称：\n')
	else:
		enname=sys.argv[8]
		zhname=sys.argv[9]

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

