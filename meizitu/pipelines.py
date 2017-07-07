
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
#from scrapy.http import Request
from meizitu import settings
import os
import urllib

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item:
            images = []

            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)   #.name .画面太美

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                us = image_url.split('/')[3:]    # 删除地址中的斜杠，取第三个到最后，0 1 2 3 ：
                image_file_name = '_'.join(us)   # 用_加在us的切片里面，如 image_file_name = "upload_2017a_05_13.jpg"
                file_path = '%s/%s' % (dir_path, image_file_name)  #./upload_2017a_05_13.jpg
                images.append(file_path)

                if os.path.exists(file_path):
                    continue
                # 进行图片文件写入,wb模式打开文件,然后requests.get获取图片流,

                with open(file_path, 'wb') as handle:   # with open as 免去handle.close()
                    response = requests.get(image_url, headers=headers)
                    for block in response.iter_content(1024):

                        if not block:
                            break
                        handle.write(block)
            item['images'] = images
        return item




'''
# -*- coding: utf-8 -*-

# 图片下载部分（自动增量）
import requests
from meizitu import settings
import os


# 图片下载类
class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item:  # 如果‘图片地址’在项目中
            images = []  # 定义图片空集

            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)

            # 建立目录名字和项目名称一致
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # 根据item字典进行查询
            for image_url in item['image_urls']:
                us = image_url.split('/')[3:]
                image_file_name = '_'.join(us)
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)

                # 如果这个文件存在则跳过
                if os.path.exists(file_path):
                    continue
                    # 进行图片文件写入,wb模式打开文件,然后requests.get获取图片流,
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        # 获取的流如果有不存在的,则使用break结束,如果没有一次结束则进行写入
                        if not block:
                            break

                        handle.write(block)

            item['images'] = images
            # 即使注释了也一样效果,不知道为何
        return item
'''