import os, json, platform
from shutil import copy, rmtree

os.makedirs('./tmp')
os.makedirs('./src')
os.makedirs('./main/sourcehan10')
#os.makedirs('./main/ChiuKongGothic-CL')
ckgurl='https://github.com/ChiuMing-Neko/ChiuKongGothic/releases/download/v.1.300/ChiuKongGothic-CL.zip'

wtsans=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Normal', 'Regular']
for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-{wt}.otf')
os.system(f'wget -P tmp {ckgurl}')
os.system('7z e ./tmp/ChiuKongGothic-CL.zip -o./main/ChiuKongGothic-CL -aoa')

cfg=json.load(open('./main/configs/config.json', 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
fod='Rounded'

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
tord='python3 ./main/round.py'
os.system('chmod +x ./main/otfcc/*') 

os.makedirs('./tmp/ttf')
os.makedirs('./tmp/tmp01')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1]=='otf':
		os.system(f"{step01} ./src/{item} ./tmp/ttf/{item}")
rmtree('./src')
for item in os.listdir('./tmp/ttf'):
	if item.lower().split('.')[-1]=='otf':
		os.system(f"otf2ttf ./tmp/ttf/{item}")
for item in os.listdir('./tmp/ttf'):
	if item.lower().split('.')[-1]=='ttf':
		wt=item.split('.')[0].split('-')[-1]
		os.system(f"{tord} ./tmp/ttf/{item} ./tmp/tmp01/{item} {wt}")

xtf, xtc='ttf', 'TTC'
for nv in ['', 'TC', 'SC', 'JP', f'{xtc}s', 'FANTI']:
	os.makedirs(f'./fonts/{fnm}{fod}{nv}')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}{nv}/')
for item in os.listdir('./tmp/tmp01'):
	if item.lower().split('.')[-1]==xtf:
		aan=item.replace('SourceHanSans', fnm+fod)
		fn1, fn2=aan.split('-')
		os.system(f"{step02} ./tmp/tmp01/{item} ./fonts/{fn1}")

os.system(f'mv ./fonts/{fnm}{fod}/*.ttc ./fonts/{fnm}{fod}{xtc}s/')
os.system(f'mv ./fonts/{fnm}{fod}/*TC* ./fonts/{fnm}{fod}TC/')
os.system(f'mv ./fonts/{fnm}{fod}/*SC* ./fonts/{fnm}{fod}SC/')
os.system(f'mv ./fonts/{fnm}{fod}/*JP* ./fonts/{fnm}{fod}JP/')
os.system(f'mv ./fonts/{fnm}{fod}/*ST* ./fonts/{fnm}{fod}FANTI/')
os.system(f'7z a ./{fnm}{fod}{xtc}s.7z ./fonts/{fnm}{fod}{xtc}s/*')
otfs=list()
for vr in ['', 'TC', 'SC', 'JP', 'FANTI']:
	otfs.append(f'./fonts/{fnm}{fod}{vr}')
otff=' '.join(otfs)
os.system(f'7z a ./{fnm}{fod}TTFs.7z {otff} -mx=9 -mfb=256 -md=512m')

rmtree('./tmp')
