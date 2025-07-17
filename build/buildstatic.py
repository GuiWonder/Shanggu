import os, json, threading
from shutil import copy, rmtree

os.makedirs('./tmp')
os.makedirs('./tmp/tmpotf')
os.makedirs('./tmp/tmpttf')
os.makedirs('./tmp/tmprd')
os.makedirs('./src')
os.makedirs('./main/sourcehan10')
wtsans=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Normal', 'Regular']
wtserif=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Regular', 'SemiBold']

for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-{wt}.otf')
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-mono/raw/master/{wt}/OTC/SourceHanMono-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-{wt}.otf')
for wt in wtserif:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-{wt}.otf')

cfg=json.load(open('./main/configs/config.json', 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
sstyles=('Mono', 'Sans', 'Serif', 'Round')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
tottfbin='python3 ./main/tottf.py --post-format 3.0'
tord='python3 ./main/round.py'
os.system('chmod +x ./main/otfcc/*')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1]=='otf':
		os.system(f"{step01} ./src/{item} ./tmp/tmpotf/{item}")
rmtree('./src')

def tottf(stl):
	for item in os.listdir('./tmp/tmpotf'):
		if stl in item and item.lower().split('.')[-1]=='otf':
			ttfout=item.split('.')[0]+'.ttf'
			os.system(f'{tottfbin} -o ./tmp/tmpttf/{ttfout} ./tmp/tmpotf/{item}')
			if stl=='Sans':
				wt=item.split('.')[0].split('-')[-1]
				os.system(f"{tord} ./tmp/tmpttf/{ttfout} ./tmp/tmprd/{ttfout} {wt}")

thsans=threading.Thread(target=tottf, args=('Sans', ))
thserif=threading.Thread(target=tottf, args=('Serif', ))
thmono=threading.Thread(target=tottf, args=('Mono', ))
thsans.start()
thserif.start()
thmono.start()
thsans.join()
thserif.join()
thmono.join()

tfdirs=list()
for fmt in('otf', 'ttf', 'rd'):
	if fmt=='otf': xtc='OTC'
	else: xtc='TTC'

	for nv in ['', 'TC', 'SC', 'JP', f'{xtc}s', 'FANTI']:
		if fmt=='rd':
			tfdirs.append(f'./fonts/{fmt}/{fnm}Round{nv}/')
		else:
			tfdirs.append(f'./fonts/{fmt}/{fnm}Sans{nv}/')
			tfdirs.append(f'./fonts/{fmt}/{fnm}Serif{nv}/')
			if nv!='FANTI':
				tfdirs.append(f'./fonts/{fmt}/{fnm}Mono{nv}/')

for drr in tfdirs:
	os.makedirs(drr)
	copy('./LICENSE.txt', drr)

for fmt in('otf', 'ttf', 'rd'):
	if fmt=='otf': xtc='OTC'
	else: xtc='TTC'
	for item in os.listdir(f'./tmp/tmp{fmt}'):
		aan=item.replace('SourceHan', fnm)
		if fmt=='rd': aan=aan.replace('Sans', 'Round')
		fn1, fn2=aan.split('-')
		os.system(f"{step02} ./tmp/tmp{fmt}/{item} ./fonts/{fmt}/{fn1}")
		for m, t in (('*.ttc', f'{xtc}s'), ('*TC*', 'TC'), ('*SC*', 'SC'), ('*JP*', 'JP'), ('*ST*', 'FANTI')):
			tfd=f'./fonts/{fmt}/{fn1}{t}/'
			if os.path.exists(tfd):
				os.system(f'mv ./fonts/{fmt}/{fn1}/{m} {tfd}')
	if fmt!='rd':
		stls=('Mono', 'Sans', 'Serif')
	else:
		stls=('Round', )

	for stl in stls:
		os.system(f'7z a ./{fnm}{stl}{xtc}s.7z ./fonts/{fmt}/{fnm}{stl}{xtc}s/*')
		otfs=list()
		for vr in ['', 'TC', 'SC', 'JP']:
			otfs.append(f'./fonts/{fmt}/{fnm}{stl}{vr}')
		if stl!='Mono':
			otfs.append(f'./fonts/{fmt}/{fnm}{stl}FANTI')
		otff=' '.join(otfs)
		os.system(f'7z a ./{fnm}{stl}{fmt.replace("rd", "ttf").upper()}s.7z {otff} -mx=9 -mfb=256 -md=512m')

	rmtree(f'./tmp/tmp{fmt}')


# os.makedirs('./subset-differs-from-SHS-JP')
os.makedirs('./subset-differs-from-SHS-KR')
finddiffers='python3 ./main/tools/finddiffers.py'
for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Korean/SourceHanSansK-{wt}.otf')
	# os.system(f"{finddiffers} -o ./subset-differs-from-SHS-JP/{fnm}SansTC-{wt}-subset.otf ./fonts/otf/{fnm}SansTC/{fnm}SansTC-{wt}.otf ./src/SourceHanSans-{wt}.otf")
	os.system(f"{finddiffers} -o ./subset-differs-from-SHS-KR/{fnm}SansTC-{wt}-subset.otf ./fonts/otf/{fnm}SansTC/{fnm}SansTC-{wt}.otf ./src/SourceHanSansK-{wt}.otf")
# os.system(f'7z a ./subset-differs-from-SHS-JP.zip ./subset-differs-from-SHS-JP/*')
os.system(f'7z a ./subset-differs-from-SHS-KR.zip ./subset-differs-from-SHS-KR/*')

