from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
import json
import sys


class HTML2JSON:

    def __init__(self, url, num, file_name):
        self.file = file_name
        self.num = num
        self.driver = webdriver.Chrome('D:/programs/chromedriver.exe')
        self.driver.get(url)
        # [ATTENTION]必须缩放图片，使所有元素都位于在浏览器窗口范围内，才是clickable
        self.driver.find_element_by_class_name('zoom-in').click()
        WebDriverWait(self.driver, timeout=3).until(
            EC.presence_of_element_located((By.ID, 'layer-0'))  # 等待直到指定元素出现
        )
        self.url = url

    def delete_element_by_id(self, element_id):
        '''
        有的元素因为重叠而无法点击，需删除位于其上方的元素
        '''
        element = self.driver.find_element_by_id('layer-' + str(element_id))
        self.driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

    def run(self):
        success_time = 0
        done = []
        undone = list(range(self.num))
        # 循环遍历，直到所有元素被点击
        start = time.time()
        while True:
            temp = []
            print('---开始遍历---')
            for i in undone:
                layer_id = 'layer-' + str(i)
                try:
                    self.driver.find_element_by_id(layer_id).click()
                except:
                    temp.append(i)
                else:
                    success_time += 1
                    done.append(i)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    class_name = soup.find('div', id=layer_id)['class'][1]
                    object_id = class_name[6:]
                    aside = soup.find('aside', id='inspector')
                    yield aside, object_id
            print('Done:', done)
            for i in done:
                self.delete_element_by_id(i)
            done = []
            if not temp: break  # 没有发生异常，退出循环
            print('Undone:', temp)
            undone = temp
        print('total times of success: ', success_time)
        print('total time: %.2f' % (time.time() - start))
        self.driver.quit()

    def download(self):
        for aside, object_id in self.run():
            item = dict()
            name = aside.find('h2').text
            item['object_id'] = object_id
            item['name'] = name
            for section in aside.find_all('section')[:-1]:  # 省略最后的“代码模板”
                s_name = section.find('h3').text
                item[s_name] = dict()
                for div in section.find_all('div', class_=re.compile(r'item.*')):
                    try:
                        attribute_name = div['data-label'][:-1]   # "位置:" > "位置"
                    except:
                        pass
                    else:
                        if attribute_name in ['颜色', '不透明度', '字体', '大小', '粗细', '圆角']:
                            item[s_name][attribute_name] = div.find('input')['value']
                        elif attribute_name == '渐变':
                            item[s_name][attribute_name] = [i['value'] for i in div.find_all('input')]
                        else:
                            item[s_name][attribute_name] = dict()
                            for label in div.find_all('label'):
                                try:
                                    label_name = label['data-label']
                                except:
                                    print(aside)
                                    raise
                                value = label.find('input')['value']
                                item[s_name][attribute_name][label_name] = value
            temp = json.dumps(item, ensure_ascii=False)
            print(temp)
            with open(self.file, 'a', encoding='utf8') as f:
                f.write(temp + '\n')
            

if __name__ == '__main__':
    file_name = sys.argv[1]
    start_urls = [
        ('D:/coding/肠道功能检测模版/index.html', 56),
        ('file:///D:/coding/%E8%82%A0%E9%81%93%E5%8A%9F%E8%83%BD%E6%A3%80%E6%B5%8B%E6%A8%A1%E7%89%88/index.html#artboard1', 172),
        ('file:///D:/coding/%E8%82%A0%E9%81%93%E5%8A%9F%E8%83%BD%E6%A3%80%E6%B5%8B%E6%A8%A1%E7%89%88/index.html#artboard2', 23)
    ]
    for i in start_urls:
        HTML2JSON(i[0], i[1], file_name).download()

        

