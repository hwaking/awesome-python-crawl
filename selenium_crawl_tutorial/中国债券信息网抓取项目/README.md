## Selenium Crawl

模拟浏览器登陆获取js动态加载的页面数据，该方法可以模拟用户一切操作过程，简单实用，该项目代码为[中国债券信息网](https://www.chinabond.com.cn/Channel/21000)企业债板块发行文件内容的下载代码。


## Requirements
- Python >= 3.6
- Selenium >= 3.4.3
- [Chromedriver](Windows10*64)(https://chromedriver.storage.googleapis.com/index.html)
- Chrome >= 64.0.3282.186
- tqdm


## Usage

Step1: 克隆项目到本地路径，并切换路径进入项目并安装第三方包
```
git clone git@github.com:Springzhen/python-crawl-demo.git
cd ./selenium_crawl_tutorial

```

Step2：执行抓取命令有两种方法
```
# 从第1页开始抓取
python data_crawl.py

# 从指定页pagenum开始抓取, pagenum 必须为大于0的整数，且不能超过最大页面数目(当前为603)
python data_crawl.py pagenum

```

## Example

- 抓取过程：抓取过程生成download文件夹，发行文件数据保存于该文件中，同时生产log文件夹，包含日志文件log.txt 以及 已经抓取完成的文件链接用于支持断点续抓取操作，避免重复抓取浪费时间

- 抓取过程截图




## Reference

- [Python3.6+selenium+pytesser3 实现爬虫：含验证码和弹框的页面信息爬取](https://www.jianshu.com/p/125630fe3d6b)
