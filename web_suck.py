from lxml import html
import requests
import urllib
import os, sys
import re


global tree,folder,url,log

url = raw_input("Enter web page to suck: ")
folder = raw_input("Enter folder where to suck: ")
if os.path.isdir(folder) == False:
    os.mkdir( folder, 0755 );
    log = folder+'/stat.log'
    f = open(log, 'wb')
    with open(log, 'a') as file:
        file.write('Folder "' + folder +  '" created\n')
else:
    with open(log, 'a') as file:
        file.write('Such folder exist\n')
    
page = requests.get(url)
tree = html.fromstring(page.text)
 
def get_html(url,folder):
    u = urllib.urlopen(url)
    data = u.read()
    f = open(folder+'/index.html', 'wb')
    f.write(data)
    f.close()

def suck(rules,typeF, typeS):
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
                with open(log, 'a') as file:
                    file.write('Folder "' + path_fObject + '" created.\n')
            with open(log, 'a') as file:
                file.write(path_fObject + all_path[index]+"\n")
            u = urllib.urlopen(str(url) + path_fObject + all_path[index])
            data = u.read()
            f = open(folder + '/'+path_fObject+ all_path[index], 'wb')
            f.write(data)
            f.close()

            #suck images and fonts only from css
            if typeS == "css":
                u = urllib.urlopen(str(url) + path_fObject + all_path[index])
                data = u.read()
                css_comments_removed = re.sub(r'\/\*.*?\*\/', '', data)
                pattern = re.compile(r"url\('?(.*?\.[a-z]{3})")
                matches = pattern.findall(css_comments_removed)  
                
                for i in matches:
                    i = i.replace("'", "")
                    valS = i.split("/")
                    col = len(valS)
                    if valS[0] == "..":
                        full_image = ""
                        for st in range(1, col):
                            full_image = full_image + "/" +valS[st]
                        if os.path.isfile(folder+"/"+full_image) == False:
                            with open(log, 'a') as file:
                                file.write("|--->" + full_image+"\n")
                            ind = len(full_image.split("/")) - 1
                            path_fObject = ""
                            for data in range(0, ind):
                                path_fObject = path_fObject + full_image.split("/")[data] +"/"
                            if os.path.isdir(folder+"/"+path_fObject) == False:
                                os.makedirs(folder+"/"+path_fObject, 0755 );
                                with open(log, 'a') as file:
                                    file.write('Folder "' + path_fObject + '" created.\n')
                            u = urllib.urlopen(str(url) + full_image)
                            data = u.read()
                            f = open(folder + '/'+path_fObject+ full_image.split("/")[ind], 'wb')
                            f.write(data)
                            f.close()
                    else:
                        full_image = i
                        if os.path.isfile(folder+"/"+full_image) == False:
                            with open(log, 'a') as file:
                                file.write("|--->" + full_image+"\n")
                            
                            ind = len(full_image.split("/")) - 1
                            path_fObject = ""
                            for data in range(0, ind):
                                path_fObject = path_fObject + full_image.split("/")[data] +"/"
                            if os.path.isdir(folder+"/"+path_fObject) == False:
                                os.makedirs(folder+"/"+path_fObject, 0755 );                        
                            u = urllib.urlopen(str(url) + full_image)
                            data = u.read()
                            f = open(folder + '/'+path_fObject+ full_image.split("/")[ind], 'wb')
                            f.write(data)
                            f.close()
                        

print "Working, wait..."

get_html(url,folder)
#suck js
suck('//script[contains(@src, "/")][not(contains(@src, "http://"))][not(contains(@src, "//"))]', 'src','js')
#suck css
suck('//link[not(contains(@href, "http://"))][not(contains(@href, "//"))]','href','css')
#suck img
suck('//img[not(contains(@src, "http://"))][not(contains(@src, "//"))]','src', 'img')
print "Done!"
