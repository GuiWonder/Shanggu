[繁體中文](https://github.com/GuiWonder/SourceHanToClassic#思源中文字体转为传承字形) **简体中文**
# 思源中文字体转为传承字形
* [思源中文字体](https://github.com/adobe-fonts)（使用日版）转为传承字形（旧字形），思源黑体、思源宋体、思源等宽均可用。
## 预览
![image](./pic/aa0001.png)  
![image](./pic/Pic003.jpg)  
与旧报纸对比<br />
![image](./pic/Pic002.png)  
## 关于字体名称：

当前字体命名为“ **尚古 Advocate Ancient Fonts** ”，共 8 套，每套 7 种粗细，字体名称如下：<br />
**Advocate Ancient Sans | 尙古黑体 | 尙古黑體 | 尙古黑體 香港，<br />
Advocate Ancient Serif | 尙古明体 | 尙古明體 | 尙古明體 香港，<br />
Advocate Ancient Mono | 尙古等宽 | 尙古等寬 | 尙古等寬 香港<br />
Advocate Ancient Sans ST | 尙古黑體 轉繁體，<br />
Advocate Ancient Serif ST | 尙古明體 轉繁體。<br />
Advocate Ancient Sans SC | 尙古黑体SC | 尙古黑體SC，<br />
Advocate Ancient Serif SC | 尙古明体SC | 尙古明體 SC，<br />
Advocate Ancient Mono SC | 尙古等宽SC | 尙古等寬SC。<br /><br />**
*注1：SC版为多编码汉字分开编码的版本。*<br />
*注2：“轉繁體”中，由于词汇占用一部分字形空间，因此需要移除一部分字形，所显示的字符数目要少一些。（约一万八千字符）。*

## 下载字体
1. 可从本站 [Releases](https://github.com/GuiWonder/SourceHanToClassic/releases) 页面下载字体。
2. 可从[腾讯微云](https://share.weiyun.com/VEoOc5xK)下载 AdvocateAncient 系列字体。

## 使用工具生成字体
### 1. 运行命令
运行命令`python sourcehantocl.py`
* 选项1：是否合并多个编码的汉字，例如：青-靑 尚-尙 兑-兌 温-溫等？，输入Y/N
* 选项2：标点击择：1.日本 2.简体中文 3.正体中文（居中）
* 选项3：简化字字形选择：1.日本 2.中国大陆
* 选项4：是否移除未使用的字形：1.移除这些字形 2.保留异体选择器中的字形 3.不移除任何字形
* 选项5：设置字体名称：~1.使用思源原版字体名称~ 2.使用尙古黑体、尙古明体 3.我来命名
* 选项6*：字体的英文名称
* 选项7*：字体的中文名称
### 2. 运行带参数命令
将输入输出文件与上述选项作为参数运行，例如：<br /> 
`python sourcehantocl.py SourceHanSans-Regular.otf AdvocateAncientSans-Regular.otf y 3 2 2 2`<br />
`python sourcehantocl.py SourceHanSans-Regular.otf MyFont-Regular.otf y 3 2 2 3 MyFont 新名称`

## 特别感谢
* [Adobe Fonts](https://github.com/adobe-fonts) [思源黑体](https://github.com/adobe-fonts/source-han-sans) [思源宋体](https://github.com/adobe-fonts/source-han-serif) [思源等宽](https://github.com/adobe-fonts/source-han-mono)
* [otfcc](https://github.com/caryll/otfcc)
* [I.字坊](https://github.com/ichitenfont)的[傳承字形標準化文件](https://github.com/ichitenfont/inheritedglyphs)及[I.明體](https://github.com/ichitenfont/I.Ming)
* [Open Chinese Convert](https://github.com/BYVoid/OpenCC) 
* [《正确实现简转繁字体》](https://ayaka.shn.hk/s2tfont/)

## 关于作者
- **Email：** chunfengfly@outlook.com
