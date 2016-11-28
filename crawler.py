import requests
import bs4
import json

class crawler():
    category={'Anime':'anime','Books':'book','Cartoons':'cartoon','Games':'game','Misc':'misc','Plays':'play','Movies':'movie','TV':'tv'}  
    js={'category':category}
    def __init__(self):        
        try:
            f = open ("config.json", "r")
            self.js=json.loads(f.read())
            f.close()
        except:
            self.update()        
        
    #open("config.txt",'w').write(json.dumps(js,sort_keys=True, indent=4 * ' '))
    def update(self):
        for i in self.category:
            app={}
            n=0
            r = requests.get('https://www.fanfiction.net/'+self.category[i])
            soup = bs4.BeautifulSoup(r.content, 'lxml')
            s=soup.find(id='list_output')
            s=s.find_all('a')
            if i=='Movies':
                del s[1532]
            for j in s:
                app[str(j.string)]=j['href']
                n+=1
            self.js[str(i)]=app
        
        file=open("config.json",'w')
        file.write(json.dumps(self.js,sort_keys=True, indent=4 * ' '))
        file.close()
        print("updated config file")
        
    def getStory(self,id):
        r = requests.get('https://www.fanfiction.net/'+id)
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        s=soup.find(id="storytext")
        s=s.find_all('p')
        txt=""
        for i in s:
            if i.string!=None:
                a=i.string.replace('\n', ' ')
                txt+=a+"\n"
            
        return txt
