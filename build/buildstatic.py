import os, json, sys
from shutil import copy, rmtree
from concurrent.futures import ThreadPoolExecutor, as_completed

main_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main'))
if main_path not in sys.path:
	sys.path.append(main_path)

from step01 import main as step01
from step02 import main as step02
from tottf import main as tottf
from round import main as toround

cfg=json.load(open('./main/configs/config.json', 'r', encoding='utf-8'))
fnm=cfg['Name'].replace(' ', '')

tmpotf, tmpttf, tmprd='./tmpotf', './tmpttf', './tmprd'
tmps=[tmpotf, tmpttf, tmprd]
tmpsh='./tmpsh'
for t in tmps: os.makedirs(t)
os.makedirs(tmpsh)
sh10='./main/sourcehan10'
os.makedirs(sh10)

wtsans=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Normal', 'Regular']
wtserif=['Bold', 'ExtraLight', 'Heavy', 'Light', 'Medium', 'Regular', 'SemiBold']

def down(pth, url):
	os.system(f'wget -nv -P {pth} {url}')

for wt in wtsans:
	down(tmpsh, f'https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Japanese/SourceHanSans-{wt}.otf')
	down(tmpsh, f'https://github.com/adobe-fonts/source-han-mono/raw/master/{wt}/OTC/SourceHanMono-{wt}.otf')
	down(sh10, f'https://github.com/adobe-fonts/source-han-sans/raw/1.004R/OTF/Japanese/SourceHanSans-{wt}.otf')
for wt in wtserif:
	down(tmpsh, f'https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/Japanese/SourceHanSerif-{wt}.otf')
	down(sh10, f'https://github.com/adobe-fonts/source-han-serif/raw/1.001R/OTF/Japanese/SourceHanSerif-{wt}.otf')

def build1(item):
	shpth=f'{tmpsh}/{item}'
	otfpth=f'{tmpotf}/{item}'
	ttfname=item.split('.')[0]+'.ttf'
	ttfpth=f'{tmpttf}/{ttfname}'
	step01(shpth, otfpth)
	tottf(['--post-format', '3.0', '-o',ttfpth, otfpth])

def buildrd(item):
	ttfpth=f'{tmpttf}/{item}'
	rdpth=f'{tmprd}/{item}'
	wt=item.split('.')[0].split('-')[-1]
	toround(ttfpth, rdpth, wt)

def convert(fs, builder, max_workers):
	with ThreadPoolExecutor(max_workers=max_workers) as ex:
		futures = [ex.submit(builder, f) for f in fs]
		for future in as_completed(futures):
			try:
				future.result()
			except Exception as e:
				ex.shutdown(wait=False, cancel_futures=True)
				print(f'Error: Convert faild {e}')
				sys.exit(1)

shotfs=[f for f in os.listdir(tmpsh) if f.endswith('.otf')]
convert(shotfs, build1, 4)
rmtree(tmpsh)

ttfsans=[f for f in os.listdir(tmpttf) if 'Sans' in f and f.endswith('.ttf')]
convert(ttfsans, buildrd, 2)

outs='./fonts'
os.makedirs(outs)

for xdir in tmps:
	for item in os.listdir(xdir):
		if item.lower().split('.')[-1] in ('otf', 'ttf'):
			step02(f'{xdir}/{item}', outs)
	rmtree(xdir)

for item in os.listdir(outs):
	pth=f'{outs}/{item}'
	if os.path.isdir(pth):
		copy('./LICENSE.txt', pth)
		os.system(f'7z a ./{item}.7z {pth}/* -mx=9 -mfb=256 -md=512m -mmt=2')

from tools.finddiffers import main as finddiffers
# os.makedirs('./subset-differs-from-SHS-JP')
os.makedirs('./subset-differs-from-SHS-KR')
for wt in wtsans:
	down(tmpsh, f'https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/Korean/SourceHanSansK-{wt}.otf')
	# finddiffers(['-o', f'./subset-differs-from-SHS-JP/{fnm}SansTC-{wt}-subset.otf', f'{outs}/{fnm}SansOTFs/{fnm}SansTC/{fnm}SansTC-{wt}.otf', f'{tmpsh}/SourceHanSans-{wt}.otf'])
	finddiffers(['-o', f'./subset-differs-from-SHS-KR/{fnm}SansTC-{wt}-subset.otf', f'{outs}/{fnm}SansOTFs/{fnm}SansTC/{fnm}SansTC-{wt}.otf', f'{tmpsh}/SourceHanSansK-{wt}.otf'])
# os.system(f'7z a ./subset-differs-from-SHS-JP.zip ./subset-differs-from-SHS-JP/*')
os.system(f'7z a ./subset-differs-from-SHS-KR.zip ./subset-differs-from-SHS-KR/*')
