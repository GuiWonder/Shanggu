[English](./README-EN.md#shanggu-fonts-尙古字體) [简体中文](./README-SC.md#shanggu-fonts-尙古字体) [繁體中文](../../#shanggu-fonts-尙古字體) **日本語**

# Shanggu Fonts 尙古フォント（しょうこフォント）
源ノシリーズに基づいた、伝承字形（旧字形）CJKフォントファミリー

## 📌 概要
<b>Shanggu Fonts（尙古フォント）</b>は、[源ノ角ゴシック（Source Han Sans）](https://github.com/adobe-fonts/source-han-sans)、[源ノ明朝（Source Han Serif）](https://github.com/adobe-fonts/source-han-serif)、[源ノ等幅（Source Han Mono）](https://github.com/adobe-fonts/source-han-mono)をベースに開発された、<b>伝承字形（旧字形）</b>を核心コンセプトとするオープンソースのCJKフォントファミリープロジェクトです。ゴシック体、明朝体、丸ゴシック体など多岐にわたるスタイルを網羅し、簡体字から繁体字への動的変換（簡転繁）バージョンも提供しています。

## 📺 プレビュー
![image](./pictures/pic0001.png)  
![image](./pictures/pic0002.png)  

## 📝 命名について
プロジェクト名は一貫して<b>「尙古（Shanggu）」</b>としています。「尚」は「尙」の常用される異体字であるため「尚古」と表記されることもありますが、本フォントシリーズが正式に採用している漢字名は「尙古」です。**コンピュータでこのフォントを検索する際は、「尙古」をご使用ください**。

### 1. 📚 フォントシリーズ
 | 英語 | 簡体字中国語 | 繁体字中国語 | 日本語 |
 | :--: | :--: | :--: | :--: |
 | Shanggu Sans | 尙古黑体 | 尙古黑體 | 尙古角ゴシック |
 | Shanggu Serif | 尙古明体 | 尙古明體 | 尙古明朝 |
 | Shanggu Mono | 尙古等宽 | 尙古等寬 | 尙古等幅 |
 | Shanggu Round | 尙古圆体 | 尙古圓體 | 尙古丸ゴシック |

### 2. 📘 バージョン説明
 | バージョン | 説明 |
 | :--: | :--: |
 | 接尾辞なし | 旧字形強化版 |
 | TC | 繁体字中国語句読点版 |
 | SC | 簡体字中国語句読点版 |
 | JP | 日本語句読点版 |
 | ST（簡転繁） | 簡体字から繁体字への動的変換フォント |

## 📑 字形規範と異体字の処理
本フォントは特定の地域の現代字形基準を採用せず、より伝統的な旧字形を設計の基礎としています。主に[一点字坊](https://github.com/ichitenfont) の [伝承字形標準化ドキュメント](https://github.com/ichitenfont/inheritedglyphs) を参照していますが、**本フォントは当該標準に完全に準拠しているわけではない**ことにご注意ください。当該標準への高い準拠度を求める場合は、一点字坊が制作した関連フォントの使用を推奨します。

### 1. 🔶 旧字形強化版（接尾辞なしバージョン）
一般的な[新旧異体字](./main/configs/mulcodechar.dt)に対して統一的な処理を行い、旧字形を採用しています。例：
- 青 → 靑
- 尚 → 尙
- 兑 → 兌
- 温 → 溫

旧字形強化版は、繁体字中国語のセンター配置の句読点を使用したバリアントを提供します。

### 2. 🌏 地域別句読点版（TC、SC、JPバージョン）
[新旧異体字](./main/configs/mulcodechar.dt)はUnicodeの個別符号化に従って処理され、字形の統合・統一は行われません。

各地域の句読点の差異に基づき、以下の3つのバリアントを提供します。
- **TC**（繁体字）
- **SC**（簡体字）
- **JP**（日本語）

日中の漢字の簡略化の差異については以下の通り処理しています：
- 日中の異体字が同一のUnicodeコードポイントにある場合、異なるバリアントで区別します。  
![image](./pictures/pic0004.png)  
- 日中の異体字が異なるUnicodeコードポイントにある場合、それぞれの筆記規範に従い、字形の統一は行いません。  
![image](./pictures/pic0005.png)  

### 3. 🔁 自動簡繁変換フォント（STバージョン）
「簡体字入力・繁体字出力」機能を備え、OpenType機能を利用して文脈に応じた一簡多繁（一つの簡体字に対し複数の繁体字候補がある場合）の動的マッチングが可能です。  
![image](./pictures/pic0003.png)  

## 📦 フォント形式
使用シーンに合わせて複数の形式を提供しています。
 | 形式 | 説明 |
 | :--: | ---- |
 | OTF / OTC | OpenType CFF ネイティブ形式 |
 | TTF / TTC | TrueType 形式、高いソフトウェア互換性 |
 | バリアブルフォント | CFF2 および TrueType の両バリアブル形式を提供 |

## 📥 ダウンロード方法
すべてのフォントファイルはプロジェクトの 👉 [Releases](https://github.com/GuiWonder/Shanggu/releases) ページからダウンロード可能です。

## 📜 ライセンス (License)
本プロジェクトのすべてのフォントは [SIL Open Font License 1.1 (OFL-1.1)](./LICENSE.txt) の下でライセンスされています：
- ✅ **無料利用**: 個人・法人を問わず、あらゆる商業デザインに自由にダウンロードして利用可能です。
- ✅ **派生可能**: [OFL-1.1](./LICENSE.txt) の条項の下で、修正、拡張、および派生フォントの制作が許可されています。
- ⚠️ **禁止事項**: フォントファイル単体での販売は禁止されています。

## 🙏 謝辞

### 1. 🔤 フォント
- [源ノ角ゴシック (Source Han Sans)](https://github.com/adobe-fonts/source-han-sans)
- [源ノ明朝 (Source Han Serif)](https://github.com/adobe-fonts/source-han-serif)
- [源ノ等幅 (Source Han Mono)](https://github.com/adobe-fonts/source-han-mono)
- [秋空󠄁ゴシック (ChiuKong Gothic)](https://github.com/ChiuMing-Neko/ChiuKongGothic)

### 2. 🔨 関連ツール
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko)
- [fontmake](https://github.com/googlefonts/fontmake)
- [otfcc](https://github.com/caryll/otfcc)

### 3. ⚪ 丸ゴシック変換
- [Resource-Han-Rounded](https://github.com/CyanoHao/Resource-Han-Rounded)

### 4. 📖 参考資料
- [伝承字形標準化ドキュメント](https://github.com/ichitenfont/inheritedglyphs) / [I.明朝](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [OpenCC (Open Chinese Convert)](https://github.com/BYVoid/OpenCC)

## 📬 連絡先
- 📩 Email: chunfengfly@outlook.com
