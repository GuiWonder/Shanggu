import os, json, threading
from shutil import copy, rmtree

os.makedirs('./tmp')
os.makedirs('./src')
shurl=[
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/OTF/SourceHanSans-VF.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/TTF/SourceHanSans-VF.ttf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/OTF/SourceHanSerif-VF.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/TTF/SourceHanSerif-VF.ttf"
]
for u1 in shurl:
	os.system(f'wget -P src {u1}')

cfg=json.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), './main/configs/config.json'), 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Sans-VF', 'Serif-VF')
for fod in aa:
	os.makedirs(f'./fonts/{fnm}{fod}_OTFs')
	os.makedirs(f'./fonts/{fnm}{fod}_TTFs')
	os.makedirs(f'./fonts/{fnm}{fod}_OTCTTC')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}_OTFs/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}_TTFs/')
	copy('./LICENSE.txt', f'./fonts/{fnm}{fod}_OTCTTC/')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'
tootc='otf2otc -o'

os.makedirs('./tmp/tmp01')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		os.system(f"{step01} ./src/{item} ./tmp/tmp01/{item}")

for item in os.listdir('./tmp/tmp01'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('.')
		ftn=aan.split('-')[0]
		outd=f'{fn1}_{fn2.upper()}s'
		os.system(f"{step02} ./tmp/tmp01/{item} ./fonts/{outd}")
		flst=[
			f'./fonts/{outd}/{ftn}-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}TC-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}SC-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}JP-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}ST-VF.{fn2}',
			f'./fonts/{outd}/{ftn}HW-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}HWTC-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}HWSC-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}HWJP-VF.{fn2}', 
			f'./fonts/{outd}/{ftn}HWST-VF.{fn2}'
		]
		flstall=' '.join(flst)
		os.system(f"{tootc} ./fonts/{ftn}-VF_OTCTTC/{ftn}-VF.{fn2}.ttc {flstall}")
rmtree('./src')
for fod in aa:
	os.system(f'7z a {fnm}{fod}_OTFs.7z ./fonts/{fnm}{fod}_OTFs/* -mx=9 -mfb=256 -md=512m')
	os.system(f'7z a {fnm}{fod}_TTFs.7z ./fonts/{fnm}{fod}_TTFs/* -mx=9 -mfb=256 -md=512m')
	os.system(f'7z a {fnm}{fod}_OTCTTC.7z ./fonts/{fnm}{fod}_OTCTTC/*')

rmtree('./fonts')
rmtree('./tmp')
