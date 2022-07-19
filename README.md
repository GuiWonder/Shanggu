**繁體中文** [简体中文](README-SC.md#思源中文字体转为传承字形旧字形)
# 思源中文字型轉為傳承字形（舊字形）
* [思源中文字型](https://github.com/adobe-fonts)（使用日版）轉為傳承字形，思源黑體、思源宋體、思源等寬均可使用 
* [思源中文字体](https://github.com/adobe-fonts)（使用日版）转为传承字形，思源黑体、思源宋体、思源等宽均可使用
## 預覽
![image](./pic/Pic003.jpg)  
## 下載字型
可從 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 頁面下載字型。
## 關於字型名稱：
#### 1. 思源字型原版名稱（不更改名稱）： <br />Source Han Sans | 思源黑体 | 思源黑體 | 思源黑體 香港 | 源ノ角ゴシック | 본고딕，<br />Source Han Serif | 思源宋体 | 思源宋體 | 思源宋體 香港 | 源ノ明朝 | 본명조，<br />Source Han Mono | 思源等宽 | 思源等寬 | 思源等寬 香港 | 源ノ等幅 | 본모노
由於名稱與原版思源字型名稱完全相同，因此此版字型無法與原版思源字型共存，但可與 Google [noto-cjk](https://github.com/googlefonts/noto-cjk) 共存。
#### 2. Advocate Ancient Sans | 尙古黑体 | 尙古黑體 | 尙古黑體 香港，<br />Advocate Ancient Serif | 尙古明体 | 尙古明體 | 尙古明體 香港，<br />Advocate Ancient Mono | 尙古等宽 | 尙古等寬 | 尙古等寬 香港
此版字型可與原版思源字型共存，與上版相比，僅名稱不同。
#### 3. 指定其他字型名稱
可與原版思源字型共存，僅名稱不同。
## 繁體字型、簡轉繁字型
由於簡化字字形大都不是傳承字形，現提供繁體字型（簡轉繁字型）。目前提供兩種版本。
### 1. 普通繁體字型（簡轉繁字型）
簡繁字形為一對一，對於簡繁一對多使用單一常用字，多數簡化字可正確顯示為繁體。
此版字型名稱為：<br />
**Advocate Ancient Sans TC | 尙古黑體-繁體，Advocate Ancient Serif TC | 尙古明體-繁體**
### 2. 可處理簡繁一對多的繁體字型（簡轉繁字型）
使用詞彙，對於簡繁一對多，可根據文字自動匹配正確的字形，這樣大大減少了簡繁轉換出現錯別字的情況。此功能需要 OpenType 特性。<br />
此版字型名稱為：<br />
**Advocate Ancient Sans ST | 尙古黑體-繁體一對多，Advocate Ancient Serif ST | 尙古明體-繁體一對多**
<br /><br />
*注：繁體一對多字型中，由於詞彙佔用一部分字形空間，因此需要移除一部分字形，所顯示的字元數目要少一些（約一萬八字元）。*

## 轉換工具使用說明
### 1. 執行命令
執行命令`python sourcehantocl.py`
* 選項1：是否合併多個編碼的漢字，例如：青-靑 尚-尙 兑-兌 温-溫等？，輸入Y/N
* 選項2：標點選擇：1.日本 2.簡體中文 3.正體中文（居中）
* 選項3：簡化字字形選擇：1.日本 2.中國大陸
* 選項4：是否移除未使用的字形，輸入Y/N
* 選項5：設定字型名稱：1.使用思源原版字型名稱 2.使用尙古黑體、尙古明體 3.我來命名
* 選項6*：字型的英文名稱
* 選項7*：字型的中文名稱
### 2. 執行帶引數命令
將輸入輸出檔案與上述選項作為引數執行，例如：<br /> `python sourcehantocl.py SourceHanSans-Regular.otf MyFont-Regular.otf y 3 2 y 2`<br />
`python sourcehantocl.py SourceHanSans-Regular.otf MyFont-Regular.otf y 3 2 y 3 MyFont 新名稱`

## 字型用到的內容或參考的內容
* [Adobe Fonts](https://github.com/adobe-fonts) [思源黑體](https://github.com/adobe-fonts/source-han-sans) [思源宋體](https://github.com/adobe-fonts/source-han-serif) [思源等寬](https://github.com/adobe-fonts/source-han-mono)
* [otfcc](https://github.com/caryll/otfcc)
* [I.字坊](https://github.com/ichitenfont)的[傳承字形標準化檔案](https://github.com/ichitenfont/inheritedglyphs)及[I.明體](https://github.com/ichitenfont/I.Ming)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC) 的字典內容（有改動）。
* [《正確實現簡轉繁字型》](https://ayaka.shn.hk/s2tfont/hant/)

