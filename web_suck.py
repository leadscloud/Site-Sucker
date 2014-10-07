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

def get_js():
    js = tree.xpath('//script[@type="text/javascript"]')
    if len(js) > 0:
        href_js = js[0].attrib['src']
        href_js_split = href_js.split("/")
        
        if os.path.isdir(folder+"/" + href_js_split[0]) == False:
            os.mkdir(folder+"/"+ href_js_split[0], 0755 );
        for data in js:
            src = data.attrib['src']
            fileNameJs = src.split("/")
            filePathJs = str(url) + "/" + str(data.attrib['src'])
            u = urllib.urlopen(filePathJs)
            data = u.read()
            f = open(folder + '/'+ href_js_split[0]+'/'+ fileNameJs[1], 'wb')
            f.write(data)
            f.close()

def get_css():
    css = tree.xpath('//link[@type="text/css"]')
    if len(css) > 0:
        href_css = css[0].attrib['href']
        href_css_split = href_css.split("/")
        if os.path.isdir(folder+"/"+href_css_split[0]) == False:
            os.mkdir(folder+"/"+href_css_split[0], 0755 );
        for data in css:
            src = data.attrib['href']
            fileNameCss = src.split("/")
            filePathCss = str(url) + "/" + str(data.attrib['href'])
            if fileNameCss[0] == "css": 
                u = urllib.urlopen(filePathCss)
                data = u.read()
                f = open(folder + '/'+href_css_split[0]+'/'+ fileNameCss[1], 'wb')
                f.write(data)
                f.close()

print "Выполняеться..."
get_html(url,folder)
get_js()
get_css()
print "Выполнено!"
