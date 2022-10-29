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
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/JapaneseHW/SourceHanSansHW-Regular.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/JapaneseHW/SourceHanSansHW-Bold.otf",
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
aa=('Mono', 'SansHW', 'Sans', 'Serif')
for fod in aa:
	os.makedirs(f'./fonts/{fnm}{fod}')
	os.makedirs(f'./fonts/{fnm}{fod}TC')
	os.makedirs(f'./fonts/{fnm}{fod}SC')
	os.makedirs(f'./fonts/{fnm}{fod}JP')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}SC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}JP/')
	if fod=='SansHW':
		continue
	os.makedirs(f'./fonts/{fnm}{fod}OTCs')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}OTCs/')

tocl='python3 ./main/sourcehantocl.py'
tootc='python3 ./main/otf2otc.py -t "CFF "=0 -o'
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('-')
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}/{aan} 2 y 3 2")
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}TC/{fn1}TC-{fn2} 2 n 3 1")
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}SC/{fn1}SC-{fn2} 2 n 2 2")
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}JP/{fn1}JP-{fn2} 2 n 1 1")
		if 'Sans' in item and ('Regular' in item or 'Bold' in item):
			continue
		os.system(f"{tootc} ./fonts/{fn1}OTCs/{aan.split('.')[0]}.ttc ./fonts/{fn1}/{aan} ./fonts/{fn1}TC/{fn1}TC-{fn2} ./fonts/{fn1}SC/{fn1}SC-{fn2} ./fonts/{fn1}JP/{fn1}JP-{fn2}")
hww=['Regular', 'Bold']
for wt in hww:
	if f'SourceHanSans-{wt}.otf' in os.listdir('./src'):
		flst=[
			f'./fonts/{fnm}Sans/{fnm}Sans-{wt}.otf', 
			f'./fonts/{fnm}SansTC/{fnm}SansTC-{wt}.otf', 
			f'./fonts/{fnm}SansSC/{fnm}SansSC-{wt}.otf', 
			f'./fonts/{fnm}SansJP/{fnm}SansJP-{wt}.otf', 
		]
		if f'SourceHanSansHW-{wt}.otf' in os.listdir('./src'):
			flsthw=[
				f'./fonts/{fnm}SansHW/{fnm}SansHW-{wt}.otf', 
				f'./fonts/{fnm}SansHWTC/{fnm}SansHWTC-{wt}.otf', 
				f'./fonts/{fnm}SansHWSC/{fnm}SansHWSC-{wt}.otf', 
				f'./fonts/{fnm}SansHWJP/{fnm}SansHWJP-{wt}.otf', 
			]
			flst+=flsthw
		fts=" ".join(flst)
		os.system(f"{tootc} ./fonts/{fnm}SansOTCs/{fnm}Sans-{wt}.ttc {fts}")
rmtree('./src')

for fod in ('Mono', 'Sans', 'Serif'):
	os.system(f'7z a {fnm}{fod}OTCs.7z ./fonts/{fnm}{fod}OTCs/*')
	otfs=[
		f'./fonts/{fnm}{fod}', 
		f'./fonts/{fnm}{fod}TC', 
		f'./fonts/{fnm}{fod}SC', 
		f'./fonts/{fnm}{fod}JP'
		]
	if fod=='Sans':
		otfhw=[
			f'./fonts/{fnm}{fod}HW', 
			f'./fonts/{fnm}{fod}HWTC', 
			f'./fonts/{fnm}{fod}HWSC', 
			f'./fonts/{fnm}{fod}HWJP'
		]
		otfs+=otfhw
	otff=' '.join(otfs)
	os.system(f'7z a {fnm}{fod}OTFs.7z {otff} -mx=9 -mfb=256 -md=256m')

os.system('git clone https://github.com/GuiWonder/TCFontCreator.git')
copytree('./TCFontCreator/main/datas', './main/datas')
rmtree('./TCFontCreator')
gototc=('Sans', 'Serif')
for fod in gototc:
	os.makedirs(f'./fonts/{fnm}{fod}ST')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}ST/')

totc='python3 ./main/converttotc.py'
for fod in gototc:
	for item in os.listdir(f'./fonts/{fnm}{fod}'):
		if item.lower().split('.')[-1] in ('otf', 'ttf'):
			os.system(f"{totc} ./fonts/{fnm}{fod}/{item} ./fonts/{fnm}{fod}ST/{item.replace('-', 'ST-')} st")
	os.system(f'7z a {fnm}{fod}FANTI.7z ./fonts/{fnm}{fod}ST/*')
rmtree('./main/datas')

rmtree('./fonts')
