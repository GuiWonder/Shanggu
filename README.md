**正體中文** [简体中文](./README-SC.md#传承字形泛中日韩字体)

# 傳承字形泛中日韓字型
一套傳承字形泛中日韓字型，基於[思源黑體](https://github.com/adobe-fonts/source-han-sans)、[思源宋體](https://github.com/adobe-fonts/source-han-serif)、[思源等寬](https://github.com/adobe-fonts/source-han-mono)以及思源系列衍生字型。本開放原始碼專案提供了多種不同風格、不同格式的字型以滿足不同需要，本專案還提供了建置這些字型時的所有原始碼。

## 預覽
![image](./pictures/Pic0001.png)  
![image](./pictures/Pic0002.jpg)  
## 關於字型
### 說明
本專案字型名稱為「 **尚古 Advocate Ancient Fonts** 」 。
#### 1. [多編碼漢字](./main/configs/mulcodechar.dt)（如青-靑 尚-尙 兑-兌 温-溫等）合併為舊字形
> Advocate Ancient Sans | 尙古黑体 | 尙古黑體，<br />
> Advocate Ancient Serif | 尙古明体 | 尙古明體，<br />
> Advocate Ancient Mono | 尙古等宽 | 尙古等寬。<br />
#### 2. 多編碼漢字分開編碼
根據標點和簡化字的不同，分為TC、SC、JP三種。<br />
> Advocate Ancient Sans TC | 尙古黑体TC | 尙古黑體TC，<br />
> Advocate Ancient Serif TC | 尙古明体TC | 尙古明體TC，<br />
> Advocate Ancient Mono TC | 尙古等宽TC | 尙古等寬TC<br />
> Advocate Ancient Sans SC | 尙古黑体SC | 尙古黑體SC，<br />
> Advocate Ancient Serif SC | 尙古明体SC | 尙古明體SC，<br />
> Advocate Ancient Mono SC | 尙古等宽SC | 尙古等寬SC，<br />
> Advocate Ancient Sans JP | 尙古黑体JP | 尙古黑體JP，<br />
> Advocate Ancient Serif JP | 尙古明体JP | 尙古明體JP，<br />
> Advocate Ancient Mono JP | 尙古等宽JP | 尙古等寬JP。<br />
#### 3. 簡轉繁體
簡入繁出的字型，可根據文字内容動態匹配一簡多繁的情況。
> Advocate Ancient Sans ST | 尙古黑体 转繁体 | 尙古黑體 轉繁體，<br />
> Advocate Ancient Serif ST | 尙古明体 转繁体 | 尙古明體 轉繁體。<br />

▼ 一簡多繁測試，此功能使用 OpenType 特性。<br />
![image](./pictures/FANTI.png)  

### 格式說明
#### 1. OpenType 格式(OTF/OTC)
原版格式。
#### 2. TrueType 格式(TTF/TTC)
基於 [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType) 無損轉換，兼容性較好。
#### ~3. TrueType hinted (TTF/TTC)~
~基於 [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf) 可實現 Windows 下低解析度小字清晰，建議僅在 Windows 下使用。~
#### 4. 可變字型
包括 OpenType 和 TrueType 格式。由於資源限制，此版本不包含舊版思源黑體、思源宋體的字圖。

## 下載字型
1. 可從本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 頁面下載字型（推薦）。
2. 可從[騰訊微雲](https://share.weiyun.com/VEoOc5xK)下載 AdvocateAncient 系列字型。
## 授權
遵循 [SIL Open Font License 1.1](./LICENSE.txt)。

## 特別感謝
#### 1. 字圖來源
- [思源黑體](https://github.com/adobe-fonts/source-han-sans) v2.004 v1.004
- [思源宋體](https://github.com/adobe-fonts/source-han-serif) v2.001 v1.001
- [思源等寬](https://github.com/adobe-fonts/source-han-mono) v1.002
- [秋空󠄁黑體CL](https://github.com/ChiuMing-Neko/ChiuKongGothic) v1.300
- [初夏明朝體](https://github.com/GuiWonder/EarlySummerMincho) v1.000
#### 2. 字型處理工具
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko/)
- [otfcc](https://github.com/caryll/otfcc)
#### 3. TrueType 格式轉換及處理
- [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType)
- [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf)
- [Resource-Han-Rounded](https://github.com/CyanoHao/Resource-Han-Rounded)
#### 4. 字形參考
- [傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs) [I.明體](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [字形維基(GlyphWiki)](https://glyphwiki.org/)
#### 5. 簡轉繁參考
- [OpenCC 開放中文轉換](https://github.com/BYVoid/OpenCC)
#### 6. 舊版用到的工具或參考
- [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)
## 關於作者
- **Email：** chunfengfly@outlook.com

## 小工具使用說明
小工具位於`main/tools/`目錄，使用時需要安裝 [FontTools](https://github.com/fonttools/fonttools)。此工具僅適用於本字型及**一部分**其他字型。
#### 1. [多編碼漢字](./main/configs/mulcodechar.dt)（如青-靑 尚-尙 兑-兌 温-溫等）合併為舊字形工具
由於此處理方法常常帶有爭議性，此工具可满足一些需求。  
使用前可根據個人需要修改 [mulcodechar.dt](./main/configs/mulcodechar.dt)。此工具一般可在 2 秒內完成。  
使用方法：執行 `python mulcodechar.py InFont.otf OutFont.otf`  
#### 2. 差集提取工具
此工具可提取本字型與思源不同的字形。  
使用方法：執行 `python finddiffers.py -o OutFont.otf AdvocateAncientSansTC-Regular.otf SourceHanSans-Regular.otf`
