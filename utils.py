from datetime import (
    datetime,
    timedelta,
    timezone,
)
import requests
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 把 unix time 转换为格式化字符串
    format = '%Y-%m-%d %H:%M:%S'
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    dt = bj_dt.strftime(format)
    print(dt, *args, **kwargs)
    # a append 追加模式
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def get_location(ip):
    r = requests.get('http://ipinfo.io/' + ip)
    data = r.json()
    IP = data.get('ip', '')
    org = data.get('org', '')
    city = data.get('city', '')
    country = data.get('country', '')
    region = data.get('region', '')

    location = 'IP: {4} \nRegion: {1} \nCountry: {2} \nCity: {3} \nOrg: {0}'
    location = location.format(org, region, country, city, IP)
    return location


def test():
    # wikipedia.org
    ip = '198.35.26.96'
    print(get_location(ip))


if __name__ == '__main__':
    test()
