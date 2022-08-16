[繁體中文](https://github.com/GuiWonder/SourceHanToClassic#思源中文字体转为传承字形) **简体中文**
# 思源中文字体转为传承字形
* [思源中文字体](https://github.com/adobe-fonts)（使用日版）转为传承字形（旧字形），思源黑体、思源宋体、思源等宽均可用。
## 预览
![image](./pic/Pic003.jpg)  
与旧报纸对比<br />
![image](./pic/Pic002.png)  
## 下载字体
1. 可从本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 页面下载字体。
2. 可从[腾讯微云](https://share.weiyun.com/VEoOc5xK)下载 AdvocateAncient 系列字体。
## 关于字体名称：

当前字体命名为“ **尚古 Advocate Ancient Fonts** ”，共 7 套，每套 7 种粗细，字体名称如下：<br />
**Advocate Ancient Sans | 尙古黑体 | 尙古黑體 | 尙古黑體 香港，<br />
Advocate Ancient Serif | 尙古明体 | 尙古明體 | 尙古明體 香港，<br />
Advocate Ancient Mono | 尙古等宽 | 尙古等寬 | 尙古等寬 香港<br />
Advocate Ancient Sans TC | 尙古黑體-繁體，<br />
Advocate Ancient Serif TC | 尙古明體-繁體，<br />
Advocate Ancient Sans ST | 尙古黑體-準繁體，<br />
Advocate Ancient Serif ST | 尙古明體-準繁體。**

## 繁体字体、简转繁字体
由于一些简化字没有传承字形，现提供繁体字体（简转繁字体）。目前提供两种版本。
### 1. 普通繁体字体（简转繁字体）
简繁字形为一对一，对于简繁一对多使用单一常用字，多数简繁一对多的简化字可正确显示为繁体。
此版字体名称为：<br />
**Advocate Ancient Sans TC | 尙古黑体-繁体，<br />
Advocate Ancient Serif TC | 尙古明体-繁体。**
### 2. 可处理简繁一对多的繁体字体（简转繁字体）
使用词汇，对于简繁一对多，可根据文本自动匹配正确的字形，这样大大减少了简繁转换错的情况。此功能需要 OpenType 特性。<br />
此版字体名称为：<br />
**Advocate Ancient Sans ST | 尙古黑体-準繁體，<br />
Advocate Ancient Serif ST | 尙古明体-準繁體。**
<br /><br />
*注：繁体一对多字体中，由于词汇占用一部分字形空间，因此需要移除一部分字形，所显示的字符数目要少一些。（约一万八千字符）*

## 转换工具使用说明
### 1. 运行命令
运行命令`python sourcehantocl.py`
* 选项1：是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？，输入Y/N
* 选项2：标点击择：1.日本 2.简体中文 3.正体中文（居中）
* 选项3：简化字字形选择：1.日本 2.中国大陆
* 选项4：是否移除未使用的字形，输入Y/N
* 选项5：设置字体名称：~1.使用思源原版字体名称~ 2.使用尙古黑体、尙古明体 3.我来命名
* 选项6*：字体的英文名称
* 选项7*：字体的中文名称
### 2. 运行带参数命令
将输入输出文件与上述选项作为参数运行，例如：<br /> 
`python sourcehantocl.py SourceHanSans-Regular.otf AdvocateAncientSans-Regular.otf y 3 2 y 2`<br />
`python sourcehantocl.py SourceHanSans-Regular.otf MyFont-Regular.otf y 3 2 y 3 MyFont 新名称`

## 特别感谢
* [Adobe Fonts](https://github.com/adobe-fonts) [思源黑体](https://github.com/adobe-fonts/source-han-sans) [思源宋体](https://github.com/adobe-fonts/source-han-serif) [思源等宽](https://github.com/adobe-fonts/source-han-mono)
* [otfcc](https://github.com/caryll/otfcc)
* [I.字坊](https://github.com/ichitenfont)的[傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs)及[I.明體](https://github.com/ichitenfont/I.Ming)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC) 
* [《正确实现简转繁字体》](https://ayaka.shn.hk/s2tfont/)
## 关于作者
- **Email：** chunfengfly@outlook.com
