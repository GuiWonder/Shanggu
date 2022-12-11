import os, json
from shutil import copy, copytree, rmtree

shurl=[
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Bold.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Light.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Medium.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Normal.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-Regular.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Bold.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Light.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Medium.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-Regular.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-SemiBold.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Bold/OTC/SourceHanMono-Bold.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/ExtraLight/OTC/SourceHanMono-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Heavy/OTC/SourceHanMono-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Light/OTC/SourceHanMono-Light.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Medium/OTC/SourceHanMono-Medium.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Normal/OTC/SourceHanMono-Normal.otf",
	"https://github.com/adobe-fonts/source-han-mono/raw/master/Regular/OTC/SourceHanMono-Regular.otf"
]
os.makedirs('./src')
for u1 in shurl:
	os.system(f'wget -P src {u1} || exit 1')

os.system('chmod +x ./main/otfcc/*') 
cfg=json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), './main/config.json'), 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Mono', 'Sans', 'Serif')
for fod in aa:
	os.makedirs(f'./fonts/{fnm}{fod}')
	os.makedirs(f'./fonts/{fnm}{fod}TC')
	os.makedirs(f'./fonts/{fnm}{fod}SC')
	os.makedirs(f'./fonts/{fnm}{fod}JP')
	os.makedirs(f'./fonts/{fnm}{fod}OTCs')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}SC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}JP/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}OTCs/')
	if fod!='Mono':
		os.makedirs(f'./fonts/{fnm}{fod}FANTI')
		copy('./LICENSE.txt', f'./fonts/{fnm}{fod}FANTI/')

tocl='python3 ./main/sourcehantocl.py'
tootc='python3 ./main/otf2otc.py -o'
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('-')
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1} m")
		if 'Mono' not in item:
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
		else:
			fn2it=fn2.replace('.', 'It.')
			flst=[
				f'./fonts/{fn1}/{fn1}-{fn2}', 
				f'./fonts/{fn1}/{fn1}-{fn2it}', 
				f'./fonts/{fn1}/{fn1}TC-{fn2}', 
				f'./fonts/{fn1}/{fn1}TC-{fn2it}', 
				f'./fonts/{fn1}/{fn1}SC-{fn2}', 
				f'./fonts/{fn1}/{fn1}SC-{fn2it}', 
				f'./fonts/{fn1}/{fn1}JP-{fn2}', 
				f'./fonts/{fn1}/{fn1}JP-{fn2it}', 
			]
		flstall=' '.join(flst)
		os.system(f"{tootc} ./fonts/{fn1}OTCs/{fn1}-{fn2.split('.')[0]}.ttc {flstall}")
rmtree('./src')

for fod in ('Mono', 'Sans', 'Serif'):
	os.system(f'mv ./fonts/{fnm}{fod}/*TC* ./fonts/{fnm}{fod}TC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*SC* ./fonts/{fnm}{fod}SC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*JP* ./fonts/{fnm}{fod}JP/')
	if fod!='Mono':
		os.system(f'mv ./fonts/{fnm}{fod}/*ST* ./fonts/{fnm}{fod}FANTI/')
	os.system(f'7z a {fnm}{fod}OTCs.7z ./fonts/{fnm}{fod}OTCs/*')
	otfs=[
		f'./fonts/{fnm}{fod}', 
		f'./fonts/{fnm}{fod}TC', 
		f'./fonts/{fnm}{fod}SC', 
		f'./fonts/{fnm}{fod}JP'
		]
	if fod !='Mono':
		otfs.append(f'./fonts/{fnm}{fod}FANTI')
	otff=' '.join(otfs)
	os.system(f'7z a {fnm}{fod}OTFs.7z {otff} -mx=9 -mfb=256 -md=512m')

rmtree('./fonts')
