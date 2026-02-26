import os, json, sys
from shutil import copy, rmtree

main_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main'))
if main_path not in sys.path:
	sys.path.append(main_path)

from step01 import main as step01
from step02 import main as step02

cfg=json.load(open('./main/configs/config.json', 'r', encoding='utf-8'))
fnm=cfg['Name'].replace(' ', '')

tmpvf='./tmpvf'
tmpsh='./tmpsh'

os.makedirs(tmpvf)
os.makedirs(tmpsh)
shurl=[
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/OTF/SourceHanSans-VF.otf",
	"https://github.com/adobe-fonts/source-han-sans/raw/release/Variable/TTF/SourceHanSans-VF.ttf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/OTF/SourceHanSerif-VF.otf",
	"https://github.com/adobe-fonts/source-han-serif/raw/release/Variable/TTF/SourceHanSerif-VF.ttf"
]
for u1 in shurl: os.system(f'wget -nv -P {tmpsh} {u1}')

for item in os.listdir(tmpsh):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		step01(f'{tmpsh}/{item}', f'{tmpvf}/{item}')
rmtree(tmpsh)

outs='./fonts'
os.makedirs(outs)

for item in os.listdir(tmpvf):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		step02(f'{tmpvf}/{item}', outs)
rmtree(tmpvf)

for item in os.listdir(outs):
	pth=f'{outs}/{item}'
	if os.path.isdir(pth):
		copy('./LICENSE.txt', pth)
		os.system(f'7z a ./{item}.7z {pth}/* -mx=9 -mfb=256 -md=512m -mmt=2')
	rmtree(pth)
