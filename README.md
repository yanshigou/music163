## 爬取网易云音乐的音频地址



### wangyiyun_mp3

此可以爬取mp3地址并写入excel文件中（可自定义）





### wangyiyun.py

此为网上查询资料 大神写好的[爬取教程](https://blog.csdn.net/qq_38282706/article/details/80251666)  





####  其他文件均为爬取下来的文件事例



## 发现重大问题！！！ 今天发现昨天爬的歌曲无法播放了

> 每首歌曲的链接  居然每天都在变化



### 这是同一首歌曲的链接 

20181210爬的

```
http://m10.music.126.net/20181210164613/ff07e1a8f567149c25e9a8f72de379be/ymusic/a5e0/56eb/c6f0/06e580cf1f74b27c59cb61451c2b59ef.mp3
```



20181211爬的

```
http://m10.music.126.net/20181211144445/8c19c72e80c6afb79d086f2c714f01c0/ymusic/a5e0/56eb/c6f0/06e580cf1f74b27c59cb61451c2b59ef.mp3
```



不难发现文件夹的名字变化了

这问题可就大了

网易云防的地方也太多了

### 不过又找到了一种解决办法

首先 找到你要下载的歌曲 用网页版打开 复制链接中的歌曲ID 如：
大鱼  动画电影《大鱼海棠》印象曲
```
https://music.163.com/#/song?id=413812448
```
ID就是413812448
然后将ID替换到链接
```
 http://music.163.com/song/media/outer/url?id= .mp3
```
如：
```
http://music.163.com/song/media/outer/url?id=413812448.mp3
```
复制这个链接 就可以直接通过网页打开纯mp3地址了 添加到下载工具中也可下载 还能添加到QQ空间背景音乐中





### 所以更新了爬虫方法，只需要爬下来每首歌的ID就行了  然后拼接到链接当中去就ok了

上传了更改的代码 也传到github上去了
[源码在我的github上](https://github.com/yanshigou/music163) ---> https://github.com/yanshigou/music163