"Site Sucker" ver 0.7 python 2.7
created by Alexey Sysoev, SI Studio

enter url like this http://sistdTest.com/, 
not like this http://sistdTest.com/index.html 
or this http://sistdTest.com/index.php.   

This problem will be solved in next versions.

what program does:
- download main index
- download all css
- download all js
- download all image
- download all fonts
- download images from css

todo:
- donwload all pages

problems:
- dont suck files that strats from "http:"
- folder with fonts may be not in the plase where css is searching it, so you can just copy/past in folder where css need
- when you suck files that start with such url: "/", you try open index file and it dont see url "/" cose it it main folder of your pc. So you can just delete "/" or put files in web server
- program can create empty files, that is type in css but there is no such file on server, so u can just delete it

for all questions, write to info@sistd.com
