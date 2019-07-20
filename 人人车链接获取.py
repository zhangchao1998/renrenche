import requests
from lxml import etree
import pymysql
import random
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
url = 'https://www.renrenche.com/cn/ershouche/'
response = requests.get(url=url,headers=headers).content.decode('utf-8')
tree = etree.HTML(response)
all_city = tree.xpath('//div[@class="area-city-letter"]/div/a/@href')
all_city_cn = tree.xpath('//div[@class="area-city-letter"]/div/a/@rrc-event-expand-tag_value')
all_type = tree.xpath('//div[@class="brand-more-content"]/div/p/span[@class="bn"]/a/@href')
all_type_cn = tree.xpath('//div[@class="brand-more-content"]/div/p/span[@class="bn"]/a/text()')
all_city_dict = {}
n = 0
for one_city_cn in all_city_cn:
    all_city_dict[one_city_cn] = all_city[n][1:-1]
    n += 1
db = pymysql.connect('localhost', 'user', 'password', 'proxies')      #连接数据库代理池以获取代理
cursor = db.cursor()
sql = """select proxy,host from can_use where weight >= 0"""      #查询所有权重大于等于零的代理IP
cursor.execute(sql)
all_ip = cursor.fetchall()
can_use = []
for one_ip in all_ip:
    proxies = {'https':'{}:{}'.format(one_ip[0],one_ip[1])}
    try:
        response = requests.get(url='https://www.renrenche.com/',headers=headers,proxies=proxies,timeout=2)      #验证代理IP对该网站的可用性
    except:
        pass
    else:
        can_use.append(one_ip)
print('共获取到{}条可用IP'.format(len(can_use)))
all_number = 0
all_url = []
for k,v in all_city_dict.items():
    url = 'https://www.renrenche.com/index.php?d=api&c=search_cars_info&car_info_city=' + k
    key = True
    one_can_use = random.choice(can_use)
    proxies = {'https':'{}:{}'.format(one_can_use[0],one_can_use[1])}
    n = 1
    while key and n <= 7:
        try:
            response = requests.get(url=url,headers=headers,proxies=proxies).json()
        except:
            if n <= 5:
                one_can_use = random.choice(can_use)
                proxies = {'https': '{}:{}'.format(one_can_use[0], one_can_use[1])}
                n += 1
            else:
                proxies = {}
                n += 1
        else:
            key = False
            for i in response['data']:
                one_url = 'https://www.renrenche.com/' + v + '/' + i['b_pinyin']
                number = i['brand_count']
                pages = number // 40 + 1
                for i in range(1, pages+1):
                    all_url.append(one_url+'/p'+str(i))
                all_number += int(number)
                print(all_number)
with open('数据.txt', 'w', encoding='utf-8') as f:      #将所有已分好页的url地址写入'数据.txt'文件中以便使用
    for one_page in all_url:
        f.write(one_page+'\n')
