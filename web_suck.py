from lxml import html
import requests
import urllib
import os, sys
import re
import lxml.html

global tree,folder,url,log

url = raw_input("Enter web page to suck: ")
folder = raw_input("Enter folder where to suck: ")

if os.path.isdir(folder) == False:
    os.mkdir( folder, 0755 )
    log = folder+'/stat.log'
    f = open(log, 'wb')
    with open(log, 'a') as file:
        file.write('Folder "' + folder +  '" created\n')
else:
    with open(log, 'a') as file:
        file.write('Such folder exist\n')
 
def get_html(url,folder):

    connection = urllib.urlopen(url)
    dom =  lxml.html.fromstring(connection.read())
    
    for link in dom.xpath('//a/@href'):
        if link.find('html')!=-1:
            u = urllib.urlopen(url+link)
            if os.path.isfile(folder+"/"+link) == False:
                data = u.read()
                data = data.replace(url, '')
                f = open(folder+ "/" +link, 'wb')
                f.write(data)
                f.close()
                with open(log, 'a') as file:
                    file.write("Create page: "+folder+"/"+link+"\n\n")
                page = requests.get(url+link)
                tree = html.fromstring(page.text)
                #suck js
                suck('//script', 'src','js',page,tree)
                #suck css
                suck('//link[(contains(@href, ".css"))]','href','css',page,tree)
                #suck img
                suck('//img','src', 'img',page,tree)
                #suck bimg
                suck('//div[(contains(@style, "url"))]','url', 'bimg',page,tree)

def suck(rules,typeF, typeS,page,tree):
    fObject = tree.xpath(rules)
    if len(fObject) > 0:
        for data in fObject:
           
            obs = data.attrib
            if (typeF in obs) or (typeS == "bimg"):
                if (typeF in obs):
                    href = data.attrib[typeF]
                if typeS == "bimg":
                    tes = data.attrib['style']
                    css_comments_removed = re.sub(r'\/\*.*?\*\/', '', tes)
                    pattern = re.compile(r"\(.*\)")
                    matches = pattern.findall(css_comments_removed)
                    matches = matches[0].replace('(', '')
                    href = matches.replace(')', '')

                pat = re.compile(r".*\?")
                if href.find('?')!=-1:
                    href = pat.findall(str(href))
                    href = href[0].replace('?','')
  
                all_path = href.split("/")
                typeCode = ""
                if all_path[0] == "http:":
                    typeCode = "WP"
                else:
                    typeCode = "Simple"

                    
                index = len(all_path) - 1
                path_fObject = ""
                for data in range(0, index):
                    path_fObject = path_fObject + all_path[data] +"/"
                    path_fObject = path_fObject.replace(url, '')
                if os.path.isdir(folder+"/"+path_fObject) == False:
                    os.makedirs(folder+"/"+path_fObject, 0755 )
                    with open(log, 'a') as file:
                        file.write('Folder "' + path_fObject + '" created.\n')
                with open(log, 'a') as file:
                    file.write(path_fObject + all_path[index]+"\n")
                if os.path.isfile(folder + '/'+path_fObject+ all_path[index]) == False:
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
                                    os.makedirs(folder+"/"+path_fObject, 0755 )
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
                                    os.makedirs(folder+"/"+path_fObject, 0755 )                       
                                u = urllib.urlopen(str(url) + full_image)
                                data = u.read()
                                f = open(folder + '/'+path_fObject+ full_image.split("/")[ind], 'wb')
                                f.write(data)
                                f.close()
                        
print "Working, wait..."

get_html(url,folder)

print "Done!"
