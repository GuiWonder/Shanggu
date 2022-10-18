**繁體中文** [简体中文](./README-SC.md#思源中文传承化字体)

# 思源中文傳承化字體
由[思源黑體](https://github.com/adobe-fonts/source-han-sans)、[思源宋體](https://github.com/adobe-fonts/source-han-serif)、[思源等寬](https://github.com/adobe-fonts/source-han-mono)日文版修改傳承字形（舊字形）字體。1.004 版開始加入思源舊版（1.0x 版）字形。

## 預覽
![image](./pic/aa0001.png)  
![image](./pic/Pic0002.jpg)  
與舊報紙對比<br />
![image](./pic/Pic0005.jpg)  
## 關於字體
### 名稱
當前字體命名為“ **尚古 Advocate Ancient Fonts** 。
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
#### 3. 簡轉繁體，目前使用詞彙方案
> Advocate Ancient Sans ST | 尙古黑體 轉繁體，<br />
> Advocate Ancient Serif ST | 尙古明體 轉繁體。<br />
### 格式
目前提供 OTF 與 OTC 兩種格式。

## 下載字體
1. 可從本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 頁面下載字體。
2. 可從[騰訊微雲](https://share.weiyun.com/VEoOc5xK)下載 AdvocateAncient 系列字體。

## 使用工具生成字體
### 1. 執行命令
執行命令`python sourcehantocl.py`
* 選項1：是否移除未使用的字形：1.移除這些字形 2.保留異體選擇器中的字形 3.不移除任何字形
* 選項2：是否合併多個編碼的漢字，例如：青-靑 尚-尙 兑-兌 温-溫等？輸入Y/N
* 選項3：標點選擇：1.日本 2.簡體中文 3.正體中文（居中）
* 選項4：簡化字字形選擇：1.日本 2.中國大陸
* 可在 config.json 中設定字體名稱
### 2. 執行帶引數命令
將輸入輸出檔案與上述選項作為引數執行，例如：<br /> 
`python sourcehantocl.py SourceHanSans-Regular.otf AdvocateAncientSans-Regular.otf 2 y 3 2`<br />

## 特別感謝
* [Adobe Fonts](https://github.com/adobe-fonts) [思源黑體](https://github.com/adobe-fonts/source-han-sans) [思源宋體](https://github.com/adobe-fonts/source-han-serif) [思源等寬](https://github.com/adobe-fonts/source-han-mono)
* [otfcc](https://github.com/caryll/otfcc)
* [I.字坊](https://github.com/ichitenfont)的[傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs)及[I.明體](https://github.com/ichitenfont/I.Ming)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC) 
* [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)
* [AFDKO](https://github.com/adobe-type-tools/afdko/)
## 關於作者
- **Email：** chunfengfly@outlook.com
