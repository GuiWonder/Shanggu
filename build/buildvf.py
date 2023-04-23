import os, json
from shutil import copy, rmtree

os.makedirs('./tmp')
os.makedirs('./src')
shurl=[
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/OTF/SourceHanSans-VF.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/TTF/SourceHanSans-VF.ttf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/OTF/SourceHanSerif-VF.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/TTF/SourceHanSerif-VF.ttf"
]
for u1 in shurl: os.system(f'wget -P src {u1}')

cfg=json.load(open('./main/configs/config.json', 'r', encoding = 'utf-8'))
fnm=cfg['fontName'].replace(' ', '')
aa=('Sans-VF', 'Serif-VF')
for fod in aa:
	for ds in ['OTFs', 'TTFs', 'OTCTTC']:
		os.makedirs(f'./fonts/{fnm}{fod}_{ds}')
		copy('./LICENSE.txt', f'./fonts/{fnm}{fod}_{ds}/')

step01='python3 ./main/step01.py'
step02='python3 ./main/step02.py'

os.makedirs('./tmp/tmp01')
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		os.system(f"{step01} ./src/{item} ./tmp/tmp01/{item}")
rmtree('./src')

vrf=['', 'TC', 'SC', 'JP']
for item in os.listdir('./tmp/tmp01'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', fnm)
		fn1, fn2=aan.split('.')
		ftn=aan.split('-')[0]
		outd=f'{fn1}_{fn2.upper()}s'
		os.system(f"{step02} ./tmp/tmp01/{item} ./fonts/{outd}")
		os.system(f'mv ./fonts/{outd}/*.ttc ./fonts/{fn1}_OTCTTC/')

for fod in aa:
	os.system(f'7z a ./{fnm}{fod}_OTFs.7z ./fonts/{fnm}{fod}_OTFs/* -mx=9 -mfb=256 -md=512m')
	os.system(f'7z a ./{fnm}{fod}_TTFs.7z ./fonts/{fnm}{fod}_TTFs/* -mx=9 -mfb=256 -md=512m')
	os.system(f'7z a ./{fnm}{fod}_OTCTTC.7z ./fonts/{fnm}{fod}_OTCTTC/*')

rmtree('./tmp')
