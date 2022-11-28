import os, json
from shutil import copy, rmtree

os.system('chmod +x ./main/otfcc/*')

shurl=[
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Bold.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Light.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Medium.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Regular.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-SemiBold.otf"
]
os.makedirs('./src')
for u1 in shurl:
	os.system(f'wget -P src {u1} || exit 1')

tocl01='python3 ./main/sourcehantocl.py'
os.makedirs(f'./fonts01')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1]=='otf':
		os.system(f"{tocl01} ./src/{item} ./fonts01/{item} s2")
rmtree('./src')

os.system(f"otf2ttf ./fonts01/*") 
cfg=json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), './main/config.json'), 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')

fod='Serif'
os.makedirs(f'./fonts/{fnm}{fod}')
os.makedirs(f'./fonts/{fnm}{fod}TC')
os.makedirs(f'./fonts/{fnm}{fod}SC')
os.makedirs(f'./fonts/{fnm}{fod}JP')
os.makedirs(f'./fonts/{fnm}{fod}TTCs')
os.makedirs(f'./fonts/{fnm}{fod}FANTI_TTFs')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}/')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TC/')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}SC/')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}JP/')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TTCs/')
copy('./LICENSE.txt', f'./fonts/{fnm}{fod}FANTI_TTFs/')

tocl='python3 ./main/toclmul.py'
tootc='otf2otc -o'
for item in os.listdir('./fonts01'):
	if item.lower().split('.')[-1]=='ttf':
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('-')
		os.system(f"{tocl} ./fonts01/{item} ./fonts/{fn1} 2")
		flst=[
			f'./fonts/{fn1}/{fn1}-{fn2}', 
			f'./fonts/{fn1}/{fn1}TC-{fn2}', 
			f'./fonts/{fn1}/{fn1}SC-{fn2}', 
			f'./fonts/{fn1}/{fn1}JP-{fn2}', 
			f'./fonts/{fn1}/{fn1}ST-{fn2}',
			f'./fonts/{fn1}/{fn1}HW-{fn2}', 
			f'./fonts/{fn1}/{fn1}HWTC-{fn2}', 
			f'./fonts/{fn1}/{fn1}HWSC-{fn2}', 
			f'./fonts/{fn1}/{fn1}HWJP-{fn2}', 
			f'./fonts/{fn1}/{fn1}HWST-{fn2}'
		]
		flstall=' '.join(flst)
		os.system(f"{tootc} ./fonts/{fn1}TTCs/{fn1}-{fn2.split('.')[0]}.ttc {flstall}")

os.system(f'mv ./fonts/{fnm}{fod}/*TC* ./fonts/{fnm}{fod}TC/')
os.system(f'mv ./fonts/{fnm}{fod}/*SC* ./fonts/{fnm}{fod}SC/')
os.system(f'mv ./fonts/{fnm}{fod}/*JP* ./fonts/{fnm}{fod}JP/')
os.system(f'mv ./fonts/{fnm}{fod}/*ST* ./fonts/{fnm}{fod}FANTI_TTFs/')

os.system(f'7z a {fnm}{fod}TTCs.7z ./fonts/{fnm}{fod}TTCs/*')
otfs=[
	f'./fonts/{fnm}{fod}', 
	f'./fonts/{fnm}{fod}TC', 
	f'./fonts/{fnm}{fod}SC', 
	f'./fonts/{fnm}{fod}JP', 
	f'./fonts/{fnm}{fod}FANTI_TTFs'
	]
otff=' '.join(otfs)
os.system(f'7z a {fnm}{fod}TTFs.7z {otff} -mx=9 -mfb=256 -md=256m')

rmtree('./fonts')
