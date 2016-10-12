#!/usr/bin/env python
# coding=utf-8
#
#Created by gzcug2010@gmail.com
#10-02-2016
#Modefied at 10-08-2016
#
from bs4 import BeautifulSoup
import requests
#use the requests module instead of urllib2

#prevent the IO error that writing result to a file
#error:UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-4: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# A function that help to get the positionID or the detail of jobs
def get_page(url, head, data = None):
    page = requests.post(url = url, headers = head, data = data)
    return page

def get_positionID(url, head):
    for page_no in xrange(1,21):
        page_data = {
            'first':'true',
            'pn':page_no,
            'kd':'运维工程师'
        }
        page = get_page(url, head, data = page_data)
        page_json = page.json()
        
        page_json = page_json['content']['positionResult']['result']
        
        for each in page_json:
            yield each['positionId']

def get_jobsinfo(url, head):
    url2 = "http://www.lagou.com/jobs/"
    with open("result3",'a') as file:
        for positId in get_positionID(url, head):
            url3 = url2 + str(positId).strip('\n') + '.html'
            page = get_page(url3, head)
            #we should pass str to BeautifulSoup constructor, So we need to use the page.text instead of page.
            html = page.text
            soup = BeautifulSoup(html,'lxml')
            txt = soup.select(".job_bt")[0].get_text()
            txt = txt.decode("utf-8")
            file.write(txt)
            file.write('\n')

url = "http://www.lagou.com/jobs/positionAjax.json"
head = {
    'Host':'www.lagou.com',
    'User-Agent':'Mozilla/5.0 (Macitosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
    'Connection':'keep-alive'
}

if __name__ == '__main__':
    get_jobsinfo(url, head)

