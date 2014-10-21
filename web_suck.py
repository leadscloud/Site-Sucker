from lxml import html
import requests
import urllib
import os, sys
import re
import lxml.html
from Tkinter import *
global tree,folder,url,log


root = Tk()
root.geometry("400x300")
namel = Label(root, text="SITE SUCKER", font="Arial 18")
namel.pack()
lab = Label(root, text="Please, enter url", font="Arial 14")
lab.pack()
text1=Text(root,height=1,width=20,font='Arial 14',wrap=WORD)
text1.pack()
lab1 = Label(root, text="Plese, enter folder name", font="Arial 14")
lab1.pack()

text2=Text(root,height=1,width=20,font='Arial 14',wrap=WORD)
text2.pack()
def Submit(event):
    if text1.get('1.0', END+'-1c') == "":
        T.delete('1.0', END)  
        T.insert('1.0', "Enter URL!")
    elif text2.get('1.0', END+'-1c') == "":
        T.delete('1.0', END)  
        T.insert('1.0', "Enter Folder!")
    else:
        T.delete('1.0', END)
        url = text1.get('1.0', END+'-1c')
        folder = text2.get('1.0', END+'-1c')

        if (os.path.isdir(folder) == False) and (os.path.isfile(folder+"/stat.log") == False):
            os.mkdir( folder, 0755 )
            log = folder+'/stat.log'
            f = open(log, 'wb')
            with open(log, 'a') as file:
                file.write('WEBPAGE: "' + url +  '"\n')
                file.write('Folder "' + folder +  '" created\n')
            try:
                T.insert('1.0', 'Working...\n\n')
                get_html(str(url),str(folder),log)
                T.insert(END, 'Done!')
            except Exception as e:
                T.insert(END, str(e) +"\nProgram Stop!")
                file.write('ERROR! Program dont finish.\n "' + str(e))
        else:
            T.insert(END, 'Such folder exist!\n')


btn = Button(root,                  
             text="SUCK ME",       
             width=10,height=2,     
             bg="white",fg="black") 
btn.bind("<Button-1>", Submit)

S = Scrollbar(root)
T = Text(root, height=4, width=50,yscrollcommand = S.set)
S.pack(side=LEFT, fill=Y)
T.pack(side=BOTTOM, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
btn.pack()




 
def get_html(url,folder,log):
    root.update()
    connection = urllib.urlopen(url)
    dom =  lxml.html.fromstring(connection.read())


    u = urllib.urlopen(url)
    data = u.read()
    data = data.replace(url, '')
    f = open(folder+ "/index.html", 'wb')
    f.write(data)
    f.close()
    with open(log, 'a') as file:
        file.write("Create page: "+folder+"/index.html\n\n")
    page = requests.get(url)
    tree = html.fromstring(page.text)        
    suck('//script', 'src','js',page,tree,url,folder,log,root)
    suck('//link[(contains(@href, ".css"))]','href','css',page,tree,url,folder,log,root)
    suck('//img','src', 'img',page,tree,url,folder,log,root)
    suck('//div[(contains(@style, "url"))]','url', 'bimg',page,tree,url,folder,log,root)

    
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
                suck('//script', 'src','js',page,tree,url,folder,log,root)
                #suck css
                suck('//link[(contains(@href, ".css"))]','href','css',page,tree,url,folder,log,root)
                #suck img
                suck('//img','src', 'img',page,tree,url,folder,log,root)
                #suck bimg
                suck('//div[(contains(@style, "url"))]','url', 'bimg',page,tree,url,folder,log,root)

def suck(rules,typeF, typeS,page,tree,url,folder,log,root):
    fObject = tree.xpath(rules)
    if len(fObject) > 0:
        for data in fObject:
            root.update()
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
                    css_comments_removed = re.sub('"', '', css_comments_removed)
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
                        

root.mainloop()
