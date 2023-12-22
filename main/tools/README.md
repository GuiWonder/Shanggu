**正體中文** [简体中文](./README-SC.md#小工具使用说明)

## 小工具使用說明
小工具位於`main/tools/`目錄，使用時需要安裝 [FontTools](https://github.com/fonttools/fonttools)。此工具僅適用於本字型及**一部分**其他字型。
#### 1. [多編碼漢字](./main/configs/mulcodechar.dt)（如青-靑 尚-尙 兑-兌 温-溫等）合併為舊字形工具
由於此處理方法常常帶有爭議性，此工具可满足一些需求。  
使用前可根據個人需要修改 [mulcodechar.dt](./main/configs/mulcodechar.dt)。此工具一般可在 2 秒內完成。  
使用方法：執行 `python mulcodechar.py InFont.otf OutFont.otf`  
#### 2. 差集提取工具
此工具可提取本字型與思源不同的字形。  
使用方法：執行 `python finddiffers.py -o OutFont.otf AdvocateAncientSansTC-Regular.otf SourceHanSans-Regular.otf`
