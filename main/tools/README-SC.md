[正體中文](./#小工具使用說明) **简体中文**

## 小工具使用说明
小工具位于`main/tools/`目录，使用时需要安装 [FontTools](https://github.com/fonttools/fonttools)。此工具仅适用于本字体及**一部分**其他字体。
#### 1. [多编码汉字](./main/configs/mulcodechar.dt)（如青-靑 尚-尙 兑-兌 温-溫等）合并为旧字形工具
由于此处理方法常常带有争议性，此工具可满足一些需求。  
使用前可根据个人需要修改 [mulcodechar.dt](./main/configs/mulcodechar.dt)。此工具一般可在 2 秒内完成。  
使用方法：运行 `python mulcodechar.py InFont.otf OutFont.otf`  
#### 2. 差集提取工具
此工具可提取本字体与思源不同的字形。  
使用方法：运行 `python finddiffers.py -o OutFont.otf AdvocateAncientSansTC-Regular.otf SourceHanSans-Regular.otf`
