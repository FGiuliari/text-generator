import requests
import bs4
import json
import re

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
    def getTopStories(self,category,work,words=60,page=1):
        #  print(self.js[category][work]
        st=[]
        payload = {'srt': '4', 'len':words,'p':page,'r':10}
        r=requests.get('https://www.fanfiction.net/'+self.js[category][work],payload)
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        stories=soup.find_all(class_="z-list zhover zpointer ")
        pages=re.findall(r"(?<=&p=)\d+",soup.find_all("center")[0].find_all("a")[-2]['href'])[0]

        for story in stories :
            name=story.a.contents[1]
            link=re.findall(r"^/s/\d+",story.a['href'])[0]
            storyid=re.findall(r"\d+",link)[0]
            chapters=re.findall(r"(?<=Chapters: )\d+",story.div.div.contents[0])[0]
            words=re.findall(r"(?<=Words: )\d+",story.div.div.contents[0])[0]            
            st.append({'name':name,'link':link,'chapters':chapters,'words':words,'id':storyid})
        return st,pages


def main():
    c=crawler();
    s,pag=c.getTopStories("Books","Harry Potter",page=2)
    for i in s:
        print(i)
    print(pag)

if __name__ == '__main__':
    main()
