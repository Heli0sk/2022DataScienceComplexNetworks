import csv
import requests
import json
from tqdm import tqdm
from pyquery import PyQuery as pq
import numpy as np
import time


header = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/80.0.3987.132 Safari/537.36'
}


# 爬取站点名称
def get_station(city_pinyin):
    url_station = 'https://{}.8684.cn/so.php?q=&k=p'.format(city_pinyin)
    doc = pq(url=url_station, encoding='utf-8', headers=header)
    class_ = doc('.list.clearfix')
    a = class_('a').items()

    filename = 'data/station_' + city_pinyin + '.txt'
    with open(filename, 'w', encoding='utf8') as f:
        for item in a:
            f.write(item.text())
            f.write('\n')


# 爬取线路名称
def get_line(city_pinyin):
    url_line = 'https://{}.8684.cn/line'.format(city_pinyin)
    page = np.arange(1, 9)

    filename = 'data/line_' + city_pinyin + '.txt'
    with open(filename, 'w', encoding='utf8') as f:
        l = []
        for p in tqdm(page):
            p = str(p)
            url = url_line + p
            status = requests.get(url=url).status_code
            # 检验状态
            if status == 200:
                doc = pq(url=url, encoding='utf-8', headers=header)
                class_ = doc('.list.clearfix')
                a = class_('a').items()
                for item in a:
                    s = item.text()
                    # s = s.replace('[', '')
                    # s = s.replace(']', '')
                    f.write(s)
                    f.write('\n')
                    l.append(s)


# 读文件
def get_list_from_file(filename):
    l = []
    with open(filename, encoding='utf8') as f:
        for txt in f.readlines():
            txt = txt.replace('\n', '')
            l.append(txt)
    return l


# 获取线路详细信息
def get_info(city_pinyin, city_hanzi):
    key = '6aeefcc858dc1b239e73d7ab86566edf'
    city = city_hanzi
    filename = 'data/line_' + city_pinyin
    # 读取公交线路列表
    line_list = get_list_from_file(filename + '.txt')

    # 关闭多余连接
    s = requests.session()
    s.keep_alive = False

    # 爬取详细信息
    with open(filename + '.csv', 'w', encoding='gbk', newline='') as f:
        w = csv.writer(f)
        w.writerow(['line', 'line_name', 'line_path', 'station_location', 'station_name'])
        for keyword in tqdm(line_list):
            if keyword[0:4] == '青岛地铁':
                keyword = keyword[4:]
            url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&' \
                  'key={}&output=json&city={}&offset=1&keywords={}%E8%B7%AF&platform=JS'.format(key, '青岛', keyword)
            # print(url)

            txt = requests.get(url=url, headers=header)
            js = json.loads(txt.text)
            # print(keyword)
            # print(json.dumps(js, indent=2, ensure_ascii=False))
            if js['buslines']:
                line_name = js['buslines'][0]['name']
                line_path = js['buslines'][0]['polyline']

                station_location = []
                station_name = []
                for j in js['buslines'][0]['busstops']:
                    station_location.append(j['location'])
                    station_name.append(j['name'])
                # print(station_location)
                # print(station_name)
                w.writerow([keyword, line_name, line_path, station_location, station_name])
            else:
                print("No Such Route: ", keyword)


# 启动！
def rebot_start(city_pinyin, city_hanzi):
    print('Get {}\'s data...'.format(city_pinyin))
    # get_station(city_pinyin)
    # get_line(city_pinyin)
    get_info(city_pinyin, city_hanzi)
    print('Done!\n')


if __name__ == '__main__':
    rebot_start('qingdao', '青岛市')
    # citys = (('qingdao', '青岛市'), ('jinan', '济南市'))
    # for city in citys:
    #     rebot_start(city[0], city[1])
