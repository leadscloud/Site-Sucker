from lxml import html
import requests
import urllib
import os, sys


global tree,folder

url = raw_input("Введите страничку: ")
folder = raw_input("Введите название папки: ")
if os.path.isdir(folder) == False:
    os.mkdir( folder, 0755 );
    print "Папка создана"
else:
    print "Такая папка уже есть"
    
page = requests.get(url)
tree = html.fromstring(page.text)
 
def get_html(url,folder):
    u = urllib.urlopen(url)
    data = u.read()
    f = open(folder+'/index.html', 'wb')
    f.write(data)
    f.close()

def suck(rules,typeF):
    fObject = tree.xpath(rules)
    if len(fObject) > 0:
       
        for data in fObject:
            
            href = data.attrib[typeF]
            all_path = href.split("/")
            index = len(all_path) - 1
            path_fObject = ""
            for data in range(0, index):
                path_fObject = path_fObject + all_path[data] +"/"

            if os.path.isdir(folder+"/"+path_fObject) == False:
                os.makedirs(folder+"/"+path_fObject, 0755 );

            print path_fObject + all_path[index]   
                       
            u = urllib.urlopen(str(url) + path_fObject + all_path[index])
            data = u.read()
            f = open(folder + '/'+path_fObject+ all_path[index], 'wb')
            f.write(data)
            f.close()

print "Выполняется..."

get_html(url,folder)
#suck js
suck('//script[contains(@src, "/")][not(contains(@src, "http://"))][not(contains(@src, "//"))]', 'src')
#suck css
suck('//link[not(contains(@href, "http://"))][not(contains(@href, "//"))]','href')
#suck img
suck('//img[not(contains(@src, "http://"))][not(contains(@src, "//"))]','src')
print "Выполнено!"
