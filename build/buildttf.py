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

wtsans=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Normal', 'Regular']
wtserif=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Regular', 'SemiBold']
for wt in wtsans:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-{wt}.otf')
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-mono/raw/master/{wt}/OTC/SourceHanMono-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-{wt}.otf')

for wt in wtserif:
	os.system(f'wget -P ./src https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-{wt}.otf')
	os.system(f'wget -P ./main/sourcehan10 https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-{wt}.otf')

os.system('wget -P ./bin https://github.com/Pal3love/Source-Han-TrueType/raw/main/binary/otrebuild_win.exe')
os.system('wget -P ./bin https://github.com/Pal3love/Source-Han-TrueType/raw/main/binary/otrebuild_mac')

cfg=json.load(open('./main/configs/config.json', 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Mono', 'Sans', 'Serif')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
os.makedirs('./tmp/tmp01')

for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		os.system(f"{step01} ./src/{item} ./tmp/tmp01/{item}")
rmtree('./src')

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

xtf, xtc='ttf', 'TTC'
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

for fod in ('Mono', 'Sans', 'Serif'):
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

rmtree('./fonts')
rmtree('./tmp')
