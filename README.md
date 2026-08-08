[English](./README-EN.md#shanggu-fonts-尙古字體) [简体中文](./README-SC.md#shanggu-fonts-尙古字体) **繁體中文** [日本語](./README-JA.md#shanggu-fonts-尙古フォントしょうこフォント)

# Shanggu Fonts 尙古字體
基於思源系列的傳承字形（舊字形）CJK 字體家族系列

## 📌 概述
<b>Shanggu Fonts（尙古字體）</b>是一套基於[思源黑體（Source Han Sans）](https://github.com/adobe-fonts/source-han-sans)、[思源宋體（Source Han Serif）](https://github.com/adobe-fonts/source-han-serif)與[思源等寬（Source Han Mono）](https://github.com/adobe-fonts/source-han-mono)開發的 CJK 字體家族系列，以<b>傳承字形（舊字形）</b>為核心理念的開源字體專案。字體系列涵蓋黑體、明體與圓體等多種風格，並提供對應的簡轉體字體版本。

## 📺 預覽
![image](./pictures/pic0001.png)  
![image](./pictures/pic0002.png)  

## 📝 命名
專案名稱統一為<b>「尙古（Shanggu）」</b>。「尚」為「尙」的常用異體字，因此「尙古」亦常被寫作「尚古」。本字體系列實際採用的中文名稱為「尙古」，因此**您在電腦上搜尋本字體時，請使用「尙古」**。

### 1. 📚 字體系列
 | 英文 | 簡體中文 | 繁體中文 | 日文 |
 | :--: | :--: | :--: | :--: |
 | Shanggu Sans | 尙古黑体 | 尙古黑體 | 尙古角ゴシック |
 | Shanggu Serif | 尙古明体 | 尙古明體 | 尙古明朝 |
 | Shanggu Mono | 尙古等宽 | 尙古等寬 | 尙古等幅 |
 | Shanggu Round | 尙古圆体 | 尙古圓體 | 尙古丸ゴシック |

### 2. 📘 版本描述
 | 版本 | 描述 |
 | :--: | :--: |
 | 無附加名 | 舊字形增強版 |
 | TC | 繁體中文標點版 |
 | SC | 簡體中文標點版 |
 | JP | 日文標點版 |
 | ST（簡轉繁） | 簡轉繁字體 |

## 📑 字形規範與異體字處理
本字體未採用任何特定地區的現代字形標準，而是以更傳統的舊字形為設計基礎。主要參考了[一點字坊](https://github.com/ichitenfont)《[傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs)》，**但需說明的是，本字體並未完全遵循該標準**。若您對該標準的符合度有更高要求，建議選用一點字坊出品的相關字體。

### 1. 🔶 舊字形增強版（無附加名版本）
字體對常見的[新舊異體字](./main/configs/mulcodechar.dt)進行了統一處理，採用舊字形。例如：
- 青 → 靑
- 尚 → 尙
- 兑 → 兌
- 温 → 溫

舊字形增強版共提供一种變體版本，使用繁體中文置中標點。

### 2. 🌏 地區標點版（TC、SC、JP版本）
[新舊異體字](./main/configs/mulcodechar.dt)依照 Unicode 的分別編碼處理，不進行字形合併統一。

基於不同地區的標點符號差異，字體提供三種變體版本：
- **TC**（繁體）
- **SC**（簡體）
- **JP**（日文）

中日簡化形式差異採用以下處理方式：<br />
- 中日異體字位於同一個 Unicode 碼位時，使用不同的變體進行區分。<br />
![image](./pictures/pic0004.png)  
- 中日異體字位於不同 Unicode 碼位時，遵循各自的書寫規範，不作字形上的統一。<br />
![image](./pictures/pic0005.png)  

### 3. 🔁 自动簡轉繁字型（ST 版本）
字型具備「簡入繁出」功能。在處理「一簡對多繁」時，字型藉助 OpenType 特性，實現了基於上下文語境的「一簡對多繁」動態匹配。以「干」字為例：當檢測到後接「活」字時，系統會自動觸發「干→幹」的定向替換，輸出「幹活」；而當後接「燥」字時，則觸發「干→乾」的替換，輸出「乾燥」。這種基於語境的動態字形調用，有效提升了文字轉換的精準性。<br />
![image](./pictures/pic0003.png)  

## 📦 字型格式
提供多種格式以適應不同使用場景。<br />
 | 格式 | 描述 |
 | :--: | ---- |
 | OTF / OTC | OpenType CFF 原生格式 |
 | TTF / TTC | TrueType 格式，更高的軟體相容性 |
 | 可變字型 | 提供 CFF2 與 TrueType 兩種可變格式 |

## 📥 下載方式
所有字型檔案可於專案的 👉[Releases](https://github.com/GuiWonder/Shanggu/releases) 頁面下載取得。

## 📜 授權協議 (License)
本專案所有字型全部採用 [SIL Open Font License 1.1（OFL-1.1）](./LICENSE.txt) 授權：
- ✅ **免費使用**：無論個人或企業，皆可自由下載並用於任何商業設計。
- ✅ **可衍生**：允許在 [OFL-1.1](./LICENSE.txt) 授權條款下進行修改、擴充，並製作衍生字體。
- ⚠️ **限制事項**：不得單獨販售字型檔案本身。

## 📦 字體的製作過程
在[思源黑體 (Source Han Sans)](https://github.com/adobe-fonts/source-han-sans)、[思源宋體 (Source Han Serif)](https://github.com/adobe-fonts/source-han-serif) 日文版的基礎上，利用 locl 在地化特性與 UVS（變體選擇器）數據表，挑選調取字庫底層隱藏的、符合傳承規範的異體字形，重新編寫至底層 cmap（字元對應表）中，作為預設顯示字形。<br />
在對應關係確立後，進一步增補了許多重繪字形。其中，黑體增補 6,537 個字形（包含 817 個直接引入[秋空󠄁黑體 (ChiuKong Gothic)](https://github.com/ChiuMing-Neko/ChiuKongGothic)字形）；明體則同步完成了 6,659 個字形的重繪。

## 🙏 致謝

### 1. 🔤 字體
- [思源黑體 (Source Han Sans)](https://github.com/adobe-fonts/source-han-sans)
- [思源宋體 (Source Han Serif)](https://github.com/adobe-fonts/source-han-serif)
- [思源等寬 (Source Han Mono)](https://github.com/adobe-fonts/source-han-mono)
- [秋空󠄁黑體 (ChiuKong Gothic)](https://github.com/ChiuMing-Neko/ChiuKongGothic)

### 2. 🔨 相關工具
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko)
- [fontmake](https://github.com/googlefonts/fontmake)
- [otfcc](https://github.com/caryll/otfcc)

### 3. ⚪ 圓體轉換
- [Resource-Han-Rounded](https://github.com/CyanoHao/Resource-Han-Rounded)

### 4. 📖 參考內容
- [傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs) / [I.明體](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [OpenCC 開放中文轉換](https://github.com/BYVoid/OpenCC)

## 📬 聯絡方式
- 📩 Email: chunfengfly@outlook.com
