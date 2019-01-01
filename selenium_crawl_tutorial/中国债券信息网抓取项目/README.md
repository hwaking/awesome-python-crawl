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

Step2：执行抓取命令有两种方法<br>
```diff
- 注意：执行此步前请先清空log下的文件!

# 从第1页开始抓取
python data_crawl.py

# 从指定页pagenum开始抓取, pagenum 必须为大于0的整数，且不能超过最大页面数目(当前为603)
python data_crawl.py pagenum

```

## Example

- 抓取过程：抓取过程生成download文件夹，发行文件数据保存于该文件中，同时生产log文件夹，包含日志文件log.txt 以及 已经抓取完成的文件链接用于支持断点续抓取操作，避免重复抓取浪费时间

- 抓取过程截图
![image](https://github.com/Springzhen/python-crawl-demo/blob/master/selenium_crawl_tutorial/%E4%B8%AD%E5%9B%BD%E5%80%BA%E5%88%B8%E4%BF%A1%E6%81%AF%E7%BD%91%E6%8A%93%E5%8F%96%E9%A1%B9%E7%9B%AE/images/%E6%8C%87%E5%AE%9A%E4%BB%8E%E7%AC%AC600%E9%A1%B5%E5%BC%80%E5%A7%8B%E6%8A%93%E5%8F%96%E8%BF%87%E7%A8%8B.png)



## Reference

- [Python3.6+selenium+pytesser3 实现爬虫：含验证码和弹框的页面信息爬取](https://www.jianshu.com/p/125630fe3d6b)
