[English](./README-EN.md#shanggu-fonts-尙古字體) **简体中文** [繁體中文](../../#shanggu-fonts-尙古字體) [日本語](./README-JA.md#shanggu-fonts-尙古フォントしょうこフォント)

# Shanggu Fonts 尙古字体
基于思源系列的传承字形（旧字形）CJK 字体家族系列

## 📌 概述
<b>Shanggu Fonts（尙古字体）</b>是一套基于[思源黑体（Source Han Sans）](https://github.com/adobe-fonts/source-han-sans)、[思源宋体（Source Han Serif）](https://github.com/adobe-fonts/source-han-serif)与[思源等宽（Source Han Mono）](https://github.com/adobe-fonts/source-han-mono)开发的 CJK 字体家族系列，以<b>传承字形（旧字形）</b>为核心理念的开源字体项目。字体系列涵盖黑体、明体与圆体等多种风格，并提供对应的简转体字体版本。

## 📺 预览
![image](./pictures/pic0001.png)  
![image](./pictures/pic0002.png)  

## 📝 命名
项目名称统一为<b>“尙古（Shanggu）”</b>。“尚”为“尙”的常用异体字，因此“尙古”亦常被写作“尚古”。本字体系列实际采用的中文名称为“尙古”，因此**您在电脑上搜寻本字体时，请使用“尙古”**。

### 1. 📚 字体系列
 | 英文 | 简体中文 | 繁体中文 | 日文 |
 | :--: | :--: | :--: | :--: |
 | Shanggu Sans | 尙古黑体 | 尙古黑體 | 尙古角ゴシック |
 | Shanggu Serif | 尙古明体 | 尙古明體 | 尙古明朝 |
 | Shanggu Mono | 尙古等宽 | 尙古等寬 | 尙古等幅 |
 | Shanggu Round | 尙古圆体 | 尙古圓體 | 尙古丸ゴシック |

### 2. 📘 版本描述
 | 版本 | 描述 |
 | :--: | :--: |
 | 无附加名 | 旧字形增强版 |
 | TC | 繁体中文标点版 |
 | SC | 简体中文标点版 |
 | JP | 日文标点版 |
 | ST（简转繁） | 简转繁字体 |

## 📑 字形规范与异体字处理
本字体未采用任何特定地区的现代字形标准，而是以更传统的旧字形为设计基础。主要参考了[一点字坊](https://github.com/ichitenfont)《[传承字形标准化文件](https://github.com/ichitenfont/inheritedglyphs)》，**但需说明的是，本字体并未完全遵循该标准**。若您对该标准的符合度有更高要求，建议选用一点字坊出品的相关字体。

### 1. 🔶 旧字形增强版（无附加名版本）
字体对常见的[新旧异体字](./main/configs/mulcodechar.dt)进行了统一处理，采用旧字形。例如：
- 青 → 靑
- 尚 → 尙
- 兑 → 兌
- 温 → 溫

旧字形增强版共提供一种变体版本，使用繁体中文居中标点。

### 2. 🌏 地区标点版（TC、SC、JP版本）
[新旧异体字](./main/configs/mulcodechar.dt)依照 Unicode 的分别编码处理，不进行字形合并统一。

基于不同地区的标点符号差异，字体提供三种变体版本：
- **TC**（繁体）
- **SC**（简体）
- **JP**（日文）

中日简化形式差异采用以下处理方式：<br />
- 中日异体字位于同一个 Unicode 码位时，使用不同的变体进行区分。<br />
![image](./pictures/pic0004.png)  
- 中日异体字位于不同 Unicode 码位时，遵循各自的书写规范，不作字形上的统一。<br />
![image](./pictures/pic0005.png)  

### 3. 🔁 自动简转繁字体（ST 版本）
具备“简入繁出”功能, 可依据文本内容动态匹配一简多繁的情况（基于 OpenType 特性）。<br />
![image](./pictures/pic0003.png)  

## 📦 字体格式
提供多种格式以适应不同使用场景。<br />
 | 格式 | 描述 |
 | :--: | ---- |
 | OTF / OTC | OpenType CFF 原生格式 |
 | TTF / TTC | TrueType 格式，更高的软件兼容性 |
 | 可变字体 | 提供 CFF2 与 TrueType 两种可变格式 |

## 📥 下载方式
所有字体文件可于项目的 👉[Releases](https://github.com/GuiWonder/Shanggu/releases) 页面下载取得。

## 📜 授权协议 (License)
本项目所有字体全部采用 [SIL Open Font License 1.1（OFL-1.1）](./LICENSE.txt) 授权：
- ✅ **免费使用**：无论个人或企业，皆可自由下载并用于任何商业设计。
- ✅ **可衍生**：允许在 [OFL-1.1](./LICENSE.txt) 授权条款下进行修改、扩充，并制作衍生字体。
- ⚠️ **限制事项**：不得单独售卖字体文件本身。

## 🙏 致谢

### 1. 🔤 字体
- [思源黑体 (Source Han Sans)](https://github.com/adobe-fonts/source-han-sans)
- [思源宋体 (Source Han Serif)](https://github.com/adobe-fonts/source-han-serif)
- [思源等宽 (Source Han Mono)](https://github.com/adobe-fonts/source-han-mono)
- [秋空󠄁黑体 (ChiuKong Gothic)](https://github.com/ChiuMing-Neko/ChiuKongGothic)

### 2. 🔨 相关工具
- [FontTools](https://github.com/fonttools/fonttools)
- [AFDKO](https://github.com/adobe-type-tools/afdko)
- [fontmake](https://github.com/googlefonts/fontmake)
- [otfcc](https://github.com/caryll/otfcc)

### 3. ⚪ 圆体转换
- [Resource-Han-Rounded](https://github.com/CyanoHao/Resource-Han-Rounded)

### 4. 📖 参考内容
- [传承字形标准化文件](https://github.com/ichitenfont/inheritedglyphs) / [I.明体](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [OpenCC 开放中文转换](https://github.com/BYVoid/OpenCC)

## 📬 联系方式
- 📩 Email: chunfengfly@outlook.com
