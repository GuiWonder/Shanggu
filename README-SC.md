[正體中文](../../#傳承化中文字型) **简体中文**

# 传承化中文字体
由[思源黑体](https://github.com/adobe-fonts/source-han-sans)、[思源宋体](https://github.com/adobe-fonts/source-han-serif)、[思源等宽](https://github.com/adobe-fonts/source-han-mono)日文版修改传承字形（旧字形）。1.004 版开始加入思源旧版（1.0x 版）字形，1.010 版开始加入[秋空󠄁黑体CL](https://github.com/ChiuMing-Neko/ChiuKongGothic)字形。

## 预览
![image](./pic/aa0001.png)  
![image](./pic/Pic0002.jpg)  
## 关于字体
### 说明
本项目字体名称为“ **尚古 Advocate Ancient Fonts** ”。
#### 1. [多编码汉字](./main/mulcodechar.txt)（如青-靑 尚-尙 兑-兌 温-溫等）合并为旧字形
> Advocate Ancient Sans | 尙古黑体 | 尙古黑體，<br />
> Advocate Ancient Serif | 尙古明体 | 尙古明體，<br />
> Advocate Ancient Mono | 尙古等宽 | 尙古等寬。<br />
#### 2. 多编码汉字分开编码
根据标点和简化字的不同，分为TC、SC、JP三种。<br />
> Advocate Ancient Sans TC | 尙古黑体TC | 尙古黑體TC，<br />
> Advocate Ancient Serif TC | 尙古明体TC | 尙古明體TC，<br />
> Advocate Ancient Mono TC | 尙古等宽TC | 尙古等寬TC<br />
> Advocate Ancient Sans SC | 尙古黑体SC | 尙古黑體SC，<br />
> Advocate Ancient Serif SC | 尙古明体SC | 尙古明體SC，<br />
> Advocate Ancient Mono SC | 尙古等宽SC | 尙古等寬SC，<br />
> Advocate Ancient Sans JP | 尙古黑体JP | 尙古黑體JP，<br />
> Advocate Ancient Serif JP | 尙古明体JP | 尙古明體JP，<br />
> Advocate Ancient Mono JP | 尙古等宽JP | 尙古等寬JP。<br />
#### 3. 简转繁体
简入繁出的字体，可根据文字内容动态匹配一简多繁的情况。
> Advocate Ancient Sans ST | 尙古黑体 转繁体 | 尙古黑體 轉繁體，<br />
> Advocate Ancient Serif ST | 尙古明体 转繁体 | 尙古明體 轉繁體。<br />

▼ 一简多繁测试，此功能使用 OpenType 特性。<br />
![image](./pic/FANTI1.png)  
![image](./pic/FANTI2.png)  
### 格式说明
#### 1. OpenType 格式(OTF/OTC)
原版格式。
#### 2. TrueType 格式(TTF/TTC)
基于 [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType) 无损转换，兼容性更好。
#### 3. TrueType hinted (TTF/TTC)
基于 [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf) 可实现 Windows 下低分辨率小字清晰，建议仅在 Windows 下使用。

## 下载字体
1. 可从本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 页面下载字体。
2. 可从[腾讯微云](https://share.weiyun.com/VEoOc5xK)下载 AdvocateAncient 系列字体。
## 授权
遵循 SIL Open Font License 1.1。
## 构建字体
### 1. 构建单个字体文件
运行命令`python sourcehantocl.py`
* 选项1：是否移除未使用的字形：1.移除这些字形 2.保留异体选择器中的字形 3.不移除任何字形
* 选项2：是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？输入Y/N
* 选项3：标点击择：1.日本 2.简体中文 3.正体中文（居中）
* 选项4：简化字字形选择：1.日本 2.中国大陆<br />

也可将输入输出文件与上述选项作为参数运行，例如：<br /> 
`python sourcehantocl.py SourceHanSans-Regular.otf AdvocateAncientSans-Regular.otf 2 y 3 2`<br />
### 2. 构建所有字体文件
运行命令`python3 buildotf.py` 或 `python3 buildttf.py`  运行环境为 Linux，需要足够的存储空间，构建 ttf 还需要 wine。

## 特别感谢
#### 1. 字图来源
- [思源黑体](https://github.com/adobe-fonts/source-han-sans) v2.004 v1.004
- [思源宋体](https://github.com/adobe-fonts/source-han-serif) v2.001 v1.001
- [思源等宽](https://github.com/adobe-fonts/source-han-mono) v1.002
- [秋空󠄁黑体CL](https://github.com/ChiuMing-Neko/ChiuKongGothic) v1.300
#### 2. 字体处理工具
- [otfcc](https://github.com/caryll/otfcc)
- [AFDKO](https://github.com/adobe-type-tools/afdko/)
#### 3. TrueType 格式转换
- [Source-Han-TrueType](https://github.com/Pal3love/Source-Han-TrueType)
- [Source Han Sans TTF](https://github.com/be5invis/source-han-sans-ttf)
#### 4. 字形参考
- [传承字形标准化文件](https://github.com/ichitenfont/inheritedglyphs) [I.明体](https://github.com/ichitenfont/I.Ming)
- [zi.tools 字統网](https://zi.tools/)
- [字形维基(GlyphWiki)](https://glyphwiki.org/)
#### 5. 简转繁参考
- [OpenCC 开放中文转换](https://github.com/BYVoid/OpenCC)
- [《正确实现简转繁字体》](https://ayaka.shn.hk/s2tfont/)*（旧版转繁体采用的方法）*
## 关于作者
- **Email：** chunfengfly@outlook.com
