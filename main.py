# --*-- coding : utf-8 --*--
import re
import requests
from bs4 import BeautifulSoup

class mt():
    def __init__(self):
        self.pagenum = []
        self.passkey = input("请输入passkey：")
        self.url = "https://pt.m-team.cc/torrents.php"
        self.catnum = input("请输入cat值：")
        self.cookie = input("请输入cookie：")
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "cookie": "tp=MTBiNzE0OWYzNTYxODUzZTk4MjhjNTU5ZGNjMjgxYjhlYTg4MmQxZQ==; __cfduid=d2045bca789c49cef345964414b1894371612230923"
        }
        self.pattern_id = re.compile(r'(?<=download.php\?id=).*?(?=&amp;https=1)')
        self.pattern_title = re.compile(r'(?<= title=").*?(?="><img alt="torrent thumbnail")')
        self.pattern_space = re.compile(r'[0-9]*\.?[0-9]+<br/>+[G|M|K]B')
        for pagenum in range(23):#此处的23为页码，请根据需求修改
            self.pagenum.append(pagenum)

    def get(self):
        global id, title, space
        id = []
        title = []
        space = []
        for i in self.pagenum:
            i = str(i)
            html = requests.get(self.url,params={'cat':self.catnum,'page':i},headers=self.header)
            soup = BeautifulSoup(html.text,"html.parser")
            soup = str(soup)
            id.append(self.pattern_id.findall(soup))
            title.append(self.pattern_title.findall(soup))
            space.append(self.pattern_space.findall(soup))

    def split(self,li):
        global id,title,space
        pop_index_list = []  # 用来存储需要删除元素的索引
        for ele in li:
            if isinstance(ele, list):
                pop_index_list.insert(0, li.index(ele))
                li.extend(ele)

        for i in pop_index_list:
            li.pop(i)

    def check(self):
        global id,title,space
        select_GB = [i for i in range(len(space)) if "GB" in space[i]]
        select_MB = [i for i in range(len(space)) if "MB" in space[i] and float(str(re.findall('[0-9]*\.?[0-9]+', space[i])[0])) >= 10]
        space = [space[i] for i in range(len(space)) if (i not in select_GB and i not in select_MB)]
        id = [id[i] for i in range(len(id)) if (i not in select_GB and i not in select_MB)]
        title = [title[i] for i in range(len(title)) if (i not in select_GB and i not in select_MB)]

    def txt(self):
        global id,title,space
        print("共有%s条记录"%len(id))
        for i in range(len(id)):
            sh = "wget -P %s.torrent -O %s https://pt.m-team.cc/download.php?id=%s&passkey=%s"%(self.path,title[i].replace(' ','_'),id[i],self.passkey)
            print(sh)

if __name__ == '__main__':
    cls = mt()
    cls.get()
    cls.split(id)
    cls.split(space)
    cls.split(title)
    cls.check()
    cls.txt()
