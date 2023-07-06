import os, json
from shutil import copy, rmtree

os.makedirs('./tmp')
os.makedirs('./src')
os.makedirs('./main/sourcehan10')
#os.makedirs('./main/ChiuKongGothic-CL')
wtsans=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Normal', 'Regular']
wtserif=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Regular', 'SemiBold']
ckgurl='https://github.com/ChiuMing-Neko/ChiuKongGothic/releases/download/v.1.300/ChiuKongGothic-CL.zip'

for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-{wt}.otf')
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-mono/raw/master/{wt}/OTC/SourceHanMono-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-{wt}.otf')

for wt in wtserif:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-{wt}.otf')

os.system(f'wget -P tmp {ckgurl}')
os.system('7z e ./tmp/ChiuKongGothic-CL.zip -o./main/ChiuKongGothic-CL -aoa')

cfg=json.load(open('./main/configs/config.json', 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Mono', 'Sans', 'Serif')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
os.makedirs('./tmp/tmp01')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1]=='otf':
		os.system(f"{step01} ./src/{item} ./tmp/tmp01/{item}")

xtf, xtc='otf', 'OTC'
for fod in aa:
	for nv in ['', 'TC', 'SC', 'JP', f'{xtc}s']:
		os.makedirs(f'./fonts/{fnm}{fod}{nv}')
		copy('./LICENSE.txt', f'./fonts/{fnm}{fod}{nv}/')
	if fod!='Mono':
		os.makedirs(f'./fonts/{fnm}{fod}FANTI')
		copy('./LICENSE.txt', f'./fonts/{fnm}{fod}FANTI/')
for item in os.listdir('./tmp/tmp01'):
	if item.lower().split('.')[-1]==xtf:
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('-')
		os.system(f"{step02} ./tmp/tmp01/{item} ./fonts/{fn1}")

for fod in aa:
	os.system(f'mv ./fonts/{fnm}{fod}/*.ttc ./fonts/{fnm}{fod}{xtc}s/')
	os.system(f'mv ./fonts/{fnm}{fod}/*TC* ./fonts/{fnm}{fod}TC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*SC* ./fonts/{fnm}{fod}SC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*JP* ./fonts/{fnm}{fod}JP/')
	if fod!='Mono': os.system(f'mv ./fonts/{fnm}{fod}/*ST* ./fonts/{fnm}{fod}FANTI/')
	os.system(f'7z a ./{fnm}{fod}{xtc}s.7z ./fonts/{fnm}{fod}{xtc}s/*')
	otfs=list()
	for vr in ['', 'TC', 'SC', 'JP']:
		otfs.append(f'./fonts/{fnm}{fod}{vr}')
	if fod !='Mono':
		otfs.append(f'./fonts/{fnm}{fod}FANTI')
	otff=' '.join(otfs)
	os.system(f'7z a ./{fnm}{fod}{xtf.upper()}s.7z {otff} -mx=9 -mfb=256 -md=512m')

os.makedirs('./subset-differs-from-SHS-JP')
os.makedirs('./subset-differs-from-SHS-KR')
finddiffers='python3 ./main/tools/finddiffers.py'
for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Korean/SourceHanSansK-{wt}.otf')
	os.system(f"{finddiffers} -o ./subset-differs-from-SHS-JP/{fnm}SansTC-{wt}-subset.otf ./fonts/{fnm}SansTC/{fnm}SansTC-{wt}.otf ./src/SourceHanSans-{wt}.otf")
	os.system(f"{finddiffers} -o ./subset-differs-from-SHS-KR/{fnm}SansTC-{wt}-subset.otf ./fonts/{fnm}SansTC/{fnm}SansTC-{wt}.otf ./src/SourceHanSansK-{wt}.otf")
os.system(f'7z a ./subset-differs-from-SHS-JP.zip ./subset-differs-from-SHS-JP/*')
os.system(f'7z a ./subset-differs-from-SHS-KR.zip ./subset-differs-from-SHS-KR/*')


rmtree('./tmp')
