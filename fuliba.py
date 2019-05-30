import requests
import re
import datetime
import time

def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'UTF-16LE'
        bbs_url=re.findall(r'<p>万能的福利吧/福利吧论坛<a href="http://(.*?)" target="_blank">', response.text,re.I)
        return bbs_url[0]
    else:
        print('Please check the network!')

def checkin(url):
    today = str(datetime.date.today())
    now = str(time.strftime("%H:%M:%S"))
    session = requests.session()
    data = {'fastloginfield':'username',
            'username': '用户名',  #请自行修改
            'password': '密码',    #请自行修改
            'questionid': 0,
            'answer': ''}
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'Accept-Encoding':'gzip, deflate',
               'Accept-Language':'zh-CN,zh;q=0.9',
               'cache-control':'max-age=0',
               'Host':url,
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36'}
    login_url = 'http://'+ url + '/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    session.post(login_url, data=data, headers=headers)
    user_info = session.get('http://' + url + '/forum.php?mobile=no').text
    checkin_url = re.search(r'}function fx_checkin(.*?);', user_info).group(1)[47:-2]
    session.get('http://' + url + '/'+ checkin_url).text
    print('%s %s Check in Success！' % (today, now))
    current_money = re.search(r'<a.*? id="extcreditmenu".*?>(.*?)</a>', user_info).group(1)
    print(current_money)

if __name__ == '__main__':
    base_url = 'http://www.lao4g.com/'
    checkin(get_url(base_url))
