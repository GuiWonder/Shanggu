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

aa=('AdvocateAncientMono', 'AdvocateAncientSans', 'AdvocateAncientSerif')
for fod in aa:
	os.makedirs(f'./fonts/{fod}')
	os.makedirs(f'./fonts/{fod}SC')
	copy('./LICENSE.txt', f'./fonts/{fod}/')
	copy('./LICENSE.txt', f'./fonts/{fod}SC/')
	if not fod.endswith('Mono'):
		os.makedirs(f'./fonts/{fod}ST')
		copy('./LICENSE.txt', f'./fonts/{fod}ST/')

tocl='python3 ./main/sourcehantocl.py'
for item in os.listdir('./src'):
	if item.lower().split('.')[-1] in ('otf', 'ttf'):
		aan=item.replace('SourceHan', 'AdvocateAncient')
		os.system(f"{tocl} ./src/{item} ./fonts/{aan.split('-')[0]}/{aan} y 3 2 2 2") 
		os.system(f"{tocl} ./src/{item} ./fonts/{aan.split('-')[0]}SC/{aan.replace('-', 'SC-')} n 2 2 2 2") 
rmtree('./src')

totc='python3 ./main/converttotc.py'
copytree('./TCFontCreator/main/datas', './main/datas')
os.system('rm -rf ./TCFontCreator') 
for fod in aa[1:]:
	for item in os.listdir(f'./fonts/{fod}'):
		if item.lower().split('.')[-1] in ('otf', 'ttf'):
			os.system(f"{totc} ./fonts/{fod}/{item} ./fonts/{fod}ST/{item.replace('-', 'ST-')} st") 
rmtree('./main/datas')

for fa in aa:
	os.system(f'7z a {fa}.7z ./fonts/{fa}/*') 
	os.system(f'7z a {fa}SC.7z ./fonts/{fa}SC/*') 
	if not fa.endswith('Mono'):
		os.system(f'7z a {fa}ST.7z ./fonts/{fa}ST/*') 
rmtree('./fonts')

