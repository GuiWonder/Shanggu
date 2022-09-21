import os
from shutil import copy, copytree, rmtree

os.system('git clone https://github.com/GuiWonder/TCFontCreator.git') 
os.system('chmod +x ./main/otfcc/*') 

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

aa=('AdvocateAncientMono', 'AdvocateAncientSansHW', 'AdvocateAncientSans', 'AdvocateAncientSerif')
for fod in aa:
	os.makedirs(f'./fonts/{fod}')
	os.makedirs(f'./fonts/{fod}TC')
	os.makedirs(f'./fonts/{fod}SC')
	os.makedirs(f'./fonts/{fod}JP')
	os.makedirs(f'./fonts/{fod}OTCs')
	copy('./main/LICENSE.txt', f'./fonts/{fod}/')
	copy('./main/LICENSE.txt', f'./fonts/{fod}TC/')
	copy('./main/LICENSE.txt', f'./fonts/{fod}SC/')
	copy('./main/LICENSE.txt', f'./fonts/{fod}JP/')
	copy('./main/LICENSE.txt', f'./fonts/{fod}OTCs/')
	if fod!='AdvocateAncientMono' and fod!='AdvocateAncientSansHW':
		os.makedirs(f'./fonts/{fod}ST')
		copy('./main/LICENSE.txt', f'./fonts/{fod}ST/')

tocl='python3 ./main/sourcehantocl.py'
tootc='python3 ./main/otf2otc.py -t "CFF "=0 -o'
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', 'AdvocateAncient')
		fn1, fn2=aan.split('-')
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}/{aan} y 3 2 2 2") 
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}TC/{fn1}TC-{fn2} n 3 1 2 2") 
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}SC/{fn1}SC-{fn2} n 2 2 2 2") 
		os.system(f"{tocl} ./src/{item} ./fonts/{fn1}JP/{fn1}JP-{fn2} n 1 1 2 2") 
		os.system(f"{tootc} ./fonts/{fn1}OTCs/{aan.split('.')[0]}.ttc ./fonts/{fn1}/{aan} ./fonts/{fn1}TC/{fn1}TC-{fn2} ./fonts/{fn1}SC/{fn1}SC-{fn2} ./fonts/{fn1}JP/{fn1}JP-{fn2}") 
rmtree('./src')
for fod in aa:
	os.system(f'7z a {fod}OTCs.7z ./fonts/{fod}OTCs/*') 
	os.system(f'7z a {fod}OTFs.7z ./fonts/{fod} ./fonts/{fod}TC ./fonts/{fod}SC ./fonts/{fod}JP -mx=9 -mfb=256 -md=256m')

totc='python3 ./main/converttotc.py'
copytree('./TCFontCreator/main/datas', './main/datas')
rmtree('./TCFontCreator') 
for fod in aa[2:]:
	for item in os.listdir(f'./fonts/{fod}'):
		if item.lower().split('.')[-1] in ('otf', 'ttf'):
			os.system(f"{totc} ./fonts/{fod}/{item} ./fonts/{fod}ST/{item.replace('-', 'ST-')} st") 
	os.system(f'7z a {fod}FANTI.7z ./fonts/{fod}ST/*') 
rmtree('./main/datas')

rmtree('./fonts')

