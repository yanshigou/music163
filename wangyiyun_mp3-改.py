# -*- coding: utf-8 -*-
__author__ = "dzt"
__date__ = "2018/12/10 11:49"


import requests
import os, json, base64
from scrapy.selector import Selector
from binascii import hexlify
from Crypto.Cipher import AES
import random
import xlwt
import xlrd

sep = '\n'
sep1 = '*'*50 + '\n'
sep2 = '\n' + '*'*50 + '\n\n'

# url = 'https://www.ximalaya.com/youshengshu/4202564/'
Agent = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
         "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
         "Mozilla/5.0 "
         "(Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
         "Mozilla/5.0 "
         "(Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
         'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
         'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; '
         'MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
         'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); '
         '.NET CLR 2.0.50727; InfoPath.1)',
         'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; '
         'FunWebProducts)',
         'Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
         'Mozilla/5.0 (X11; U; Linux; pt-PT) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.4'
         ]


class Encrypyed():
    '''传入歌曲的ID，加密生成'params'、'encSecKey 返回'''
    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    def create_secret_key(self, size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self, text, key):
        iv = '0102030405060708'
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        result = encryptor.encrypt(text)
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        # print(data)
        return data


class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': random.choice(Agent),
            'Referer': 'http://music.163.com/'}
        self.main_url = 'http://music.163.com/'
        self.session = requests.Session()
        self.session.headers = self.headers
        self.ep = Encrypyed()

    def get_songurls(self, playlist):
        '''进入所选歌单页面，得出歌单里每首歌各自的ID 形式就是“song?id=64006"'''
        url = self.main_url+'playlist?id=%d' % playlist
        re = self.session.get(url)   #直接用session进入网页，懒得构造了
        sel = Selector(text=re.text)   #用scrapy的Selector，懒得用BS4了
        songurls = sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls   #所有歌曲组成的list
        ##['/song?id=64006', '/song?id=63959', '/song?id=25642714', '/song?id=63914', '/song?id=4878122', '/song?id=63650']

    def get_songinfo(self, songurl):
        '''根据songid进入每首歌信息的网址，得到歌曲的信息
        return：'64006'，'陈小春-失恋王'''
        url = self.main_url+songurl
        re = self.session.get(url)
        sel = Selector(text=re.text)
        song_id = url.split('=')[1]
        songname = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer = '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        # songname = singer+'-'+song_name
        return str(song_id), songname, singer

    def get_url(self, ids, br=128000):
        '''self.ep.work输入歌曲ID，解码后返回data，{params 'encSecKey}
        然后post，得出歌曲所在url'''
        text = {'ids': [ids], 'br': br, 'csrf_token': ''}
        data = self.ep.work(text)
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        req = self.session.post(url, data=data)
        song_url = req.json()['data'][0]['url']
        return song_url

    def url_song(self, songurl, dir_path):
        '''根据歌曲url，获取mp3地址'''
        song_id, songname, singer = self.get_songinfo(songurl)  # 根据歌曲url得出ID、歌名、歌手名
        song_url = self.get_url(song_id)                # 根据ID得到歌曲的实质URL
        print(songname)
        print(song_id)
        return songname, song_url, singer, song_id

    def work(self, playlist):
        songurls = self.get_songurls(playlist)         # 输入歌单编号，得到歌单所有歌曲的url
        dir_path = r''
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(u'表1', cell_overwrite_ok=True)
        for songurl in songurls:
            a = songurls.index(songurl)
            # 次song_url为当天失效，所以获取永久url需要另一种方法
            songname, song_url, singer, song_id = self.url_song(songurl, dir_path)
            url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % song_id
            if song_url is None:
                continue
            sheet1.write(a, 0, songname)  # 作品名称
            sheet1.write(a, 1, 12)  # 分类
            sheet1.write(a, 2, url)  # 资源url
            sheet1.write(a, 3, 1)  # 初始年龄
            sheet1.write(a, 4, 99)  # 结束年龄
            sheet1.write(a, 5, 1)  # 语言范围
            sheet1.write(a, 6, '')  # 作品简介
            sheet1.write(a, 7, singer)  # 表演者/主播
            sheet1.write(a, 8, '')  # 作者/作词者
            sheet1.write(a, 9, '')  # 主角
            sheet1.write(a, 10, '')  # 作曲者
            sheet1.write(a, 11, '')  # 主要情节
            sheet1.write(a, 12, '')  # 封面url
            a += 1
        new_imei_file = '%s.xls' % playlist
        f.save(new_imei_file)

if __name__ == '__main__':
    d = wangyiyun()
    d.work(2163777)

