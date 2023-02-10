import os, json, platform, threading
from shutil import copy, rmtree

otrebuild='./bin/otrebuild_win.exe'
if platform.system() in ('Mac', 'Darwin'):
	otrebuild='./bin/otrebuild_mac'
if platform.system()=='Linux':
	otrebuild='wine '+otrebuild

os.makedirs('./tmp')
os.makedirs('./src')
os.makedirs('./main/sourcehan10')
os.makedirs('./main/ChiuKongGothic-CL')
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
shurl10=[
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Bold.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Light.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Medium.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Normal.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-Regular.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-Bold.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-ExtraLight.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-Heavy.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-Light.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-Medium.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-Regular.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-SemiBold.otf"
]
ckgurl='https://github.com/ChiuMing-Neko/ChiuKongGothic/releases/download/v.1.300/ChiuKongGothic-CL.zip'
for u1 in shurl:
	os.system(f'wget -P src {u1}')
for u1 in shurl10:
	os.system(f'wget -P ./main/sourcehan10 {u1}')
os.system(f'wget -P tmp https://github.com/ChiuMing-Neko/ChiuKongGothic/releases/download/v.1.300/ChiuKongGothic-CL.zip')
os.system('7z e ./tmp/ChiuKongGothic-CL.zip -o./main/ChiuKongGothic-CL -aoa')

os.system('wget -P ./bin https://github.com/Pal3love/Source-Han-TrueType/raw/main/binary/otrebuild_win.exe')
os.system('wget -P ./bin https://github.com/Pal3love/Source-Han-TrueType/raw/main/binary/otrebuild_mac')

cfg=json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), './main/configs/config.json'), 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Mono', 'Sans', 'Serif')
for fod in aa:
	os.makedirs(f'./fonts/{fnm}{fod}')
	os.makedirs(f'./fonts/{fnm}{fod}TC')
	os.makedirs(f'./fonts/{fnm}{fod}SC')
	os.makedirs(f'./fonts/{fnm}{fod}JP')
	os.makedirs(f'./fonts/{fnm}{fod}TTCs')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}SC/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}JP/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}TTCs/')
	if fod!='Mono':
		os.makedirs(f'./fonts/{fnm}{fod}FANTI')
		copy('./LICENSE.txt', f'./fonts/{fnm}{fod}FANTI/')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
tootc='otf2otc -o'
os.makedirs('./tmp/tmp01')

def tosp1(stl):
	for item in os.listdir('./src'):
		if stl in item and item.lower().split('.')[-1]=='otf':
			os.system(f"{step01} ./src/{item} ./tmp/tmp01/{item}")

th1sans=threading.Thread(target=tosp1, args=('Sans', ))
th1serif=threading.Thread(target=tosp1, args=('Serif', ))
th1mono=threading.Thread(target=tosp1, args=('Mono', ))
th1sans.start()
th1serif.start()
th1mono.start()
th1sans.join()
th1serif.join()
th1mono.join()

def tottf(stl):
	for item in os.listdir('./tmp/tmp01'):
		if stl in item and item.lower().split('.')[-1]=='otf':
			ttfout=item.split('.')[0]+'.ttf'
			os.system(f'{otrebuild} --otf2ttf --UPM 2048 --removeGlyphNames --O1 -o ./tmp/tmp01/{ttfout} ./tmp/tmp01/{item}')

thsans=threading.Thread(target=tottf, args=('Sans', ))
thserif=threading.Thread(target=tottf, args=('Serif', ))
thmono=threading.Thread(target=tottf, args=('Mono', ))
thsans.start()
thserif.start()
thmono.start()
thsans.join()
thserif.join()
thmono.join()

for item in os.listdir('./tmp/tmp01'):
	if item.lower().split('.')[-1]=='ttf':
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('-')
		os.system(f"{step02} ./tmp/tmp01/{item} ./fonts/{fn1}")
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
		os.system(f"{tootc} ./fonts/{fn1}TTCs/{fn1}-{fn2.split('.')[0]}.ttc {flstall}")
rmtree('./src')

for fod in ('Mono', 'Sans', 'Serif'):
	os.system(f'mv ./fonts/{fnm}{fod}/*TC* ./fonts/{fnm}{fod}TC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*SC* ./fonts/{fnm}{fod}SC/')
	os.system(f'mv ./fonts/{fnm}{fod}/*JP* ./fonts/{fnm}{fod}JP/')
	if fod!='Mono':
		os.system(f'mv ./fonts/{fnm}{fod}/*ST* ./fonts/{fnm}{fod}FANTI/')
	os.system(f'7z a {fnm}{fod}TTCs.7z ./fonts/{fnm}{fod}TTCs/*')
	otfs=[
		f'./fonts/{fnm}{fod}', 
		f'./fonts/{fnm}{fod}TC', 
		f'./fonts/{fnm}{fod}SC', 
		f'./fonts/{fnm}{fod}JP'
		]
	if fod !='Mono':
		otfs.append(f'./fonts/{fnm}{fod}FANTI')
	otff=' '.join(otfs)
	os.system(f'7z a {fnm}{fod}TTFs.7z {otff} -mx=9 -mfb=256 -md=512m')

rmtree('./fonts')
rmtree('./tmp')
