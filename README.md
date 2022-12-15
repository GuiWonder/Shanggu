**正體中文** [简体中文](./README-SC.md#传承化中文字体)

# 傳承化中文字型
由[思源黑體](https://github.com/adobe-fonts/source-han-sans)、[思源宋體](https://github.com/adobe-fonts/source-han-serif)、[思源等寬](https://github.com/adobe-fonts/source-han-mono)日文版修改傳承字形（舊字形）。1.004 版開始加入思源舊版（1.0x 版）字形，1.010 版開始加入[秋空󠄁黑體CL](https://github.com/ChiuMing-Neko/ChiuKongGothic)字形。
## 預覽
![image](./pic/aa0001.png)  
![image](./pic/Pic0002.jpg)  
## 關於字型
### 說明
本專案字型名稱為「 **尚古 Advocate Ancient Fonts** 」 。
#### 1. [多編碼漢字](./main/mulcodechar.txt)（如青-靑 尚-尙 兑-兌 温-溫等）合併為舊字形
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
![image](./pic/FANTI1.png)  
![image](./pic/FANTI2.png)  
### 格式說明
#### 1. OpenType 格式(OTF/OTC)
原版格式。
#### 2. TrueType 格式(TTF/TTC)
基於 [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType) 無損轉換，兼容性更好。
#### 3. TrueType hented (TTF/TTC)
基於 [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf) 可實現 Windows 下低解析度小字清晰，建議僅在 Windows 下使用。

## 下載字型
1. 可從本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 頁面下載字型。
2. 可從[騰訊微雲](https://share.weiyun.com/VEoOc5xK)下載 AdvocateAncient 系列字型。
## 授權
遵循 SIL Open Font License 1.1。
## 構建字型檔
### 1. 構建單個字型檔
執行命令`python sourcehantocl.py`
* 選項1：是否移除未使用的字形：1.移除這些字形 2.保留異體選擇器中的字形 3.不移除任何字形
* 選項2：是否合併多個編碼的漢字，例如：青-靑 尚-尙 兑-兌 温-溫等？輸入Y/N
* 選項3：標點選擇：1.日本 2.簡體中文 3.正體中文（居中）
* 選項4：簡化字字形選擇：1.日本 2.中國大陸  <br />

也可將輸入輸出檔案與上述選項作為引數執行，例如：<br /> 
`python sourcehantocl.py SourceHanSans-Regular.otf AdvocateAncientSans-Regular.otf 2 y 3 2`<br />
### 2. 構建所有字型檔
執行命令`python3 buildotf.py` 或 `python3 buildttf.py`  執行環境為 Linux，需要足夠存儲空間，構建 ttf 還需要 wine。
## 特別感謝
#### 1. 字圖來源
- [思源黑體](https://github.com/adobe-fonts/source-han-sans) v2.004 v1.004
- [思源宋體](https://github.com/adobe-fonts/source-han-serif) v2.001 v1.001
- [思源等寬](https://github.com/adobe-fonts/source-han-mono) v1.002
- [秋空󠄁黑體CL](https://github.com/ChiuMing-Neko/ChiuKongGothic) v1.300
#### 2. 字型處理工具
- [otfcc](https://github.com/caryll/otfcc)
- [AFDKO](https://github.com/adobe-type-tools/afdko/)
#### 3. TrueType 格式轉換
- [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType)
- [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf)
#### 4. 字形參考
- [傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs) [I.明體](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [字形維基(GlyphWiki)](https://glyphwiki.org/)
#### 5. 簡轉繁參考
- [OpenCC 開放中文轉換](https://github.com/BYVoid/OpenCC)
- [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)*（舊版轉繁體採用的方法）*
## 關於作者
- **Email：** chunfengfly@outlook.com
