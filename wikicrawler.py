#Wikipedia Crawler v3 (inserting results into MySQL)
# @author: Hardik Vasa

#Import Libraries
import time     #For Delay
import requests
import re
from pathlib import Path
import os
from urllib.parse import unquote
starting_page = "https://en.wikipedia.org/wiki/Category:"
seed_page = "https://en.wikipedia.org/wiki/"  #Crawling the English Wikipedia

class siteCrawler():
    currentCate = ["Visualization_(graphic)"]
    def getSubCategoryNames(self, content):
        names = re.findall(r"<a class=\"CategoryTreeLabel.+?>.+</a>", content)
        catename = []
        for item in names:
            catename.append(re.findall(r"href=\"\/wiki\/Category:.+?\"", item)[0].replace("href=\"/wiki/Category:","").replace("\"",""))
        return catename
    
    def getPageUrls(self, text):
        content = re.findall(r"mw-category-generated[\w\W\s\S.]+?<noscript>", text)[0]
        names = re.findall(r"<li><a href=\"/wiki/.+? title=\"", content)
        pagename = []
        for item in names:
            pagename.append(unquote(unquote(item.replace("<li><a href=\"/wiki/","").replace("\" title=\"",""))))
        # <a href="/wiki/Logical_harmony" title="Logical harmony">Logical harmony</a>
        return pagename

    def getPageContent(self, name):
        tmpath = "/".join(self.currentCate) + "/" + name + ".txt"
        if Path(tmpath).exists():
            print("-----------skiped--------"+name)
            return
        r = requests.get(seed_page + name)
        linetext = re.findall(r"<div id=\"content\" class=\"mw-body\" role=\"main\">[\w\W\s\S.]+?<div id=\"mw-navigation\">", r.text)[0]
        linetext = re.sub(r"<style[\w\W\s\S.]+?</style>"," ",linetext)
        linetext = re.sub(r"<script[\w\W\s\S.]+?</script>"," ",linetext)
        data = re.split(r"\.|\!", re.sub(r"<[\w\W\s\S.]+?>"," ", linetext))
        result = []
        for item in data:
            t = re.sub("&nbsp;", "", item)
            t = re.sub(r"[^a-zA-Z0-9]", " ", t)
            t = re.sub(r" [0-9]+ ", " ", t)
            t = re.sub(r"\s+", " ", t).strip()
            t = t.lower()
            result.append(t)
        self.writeContents(name, result)

    def writeContents(self, name, rawtext):
        # return []
        tmpath = "/".join(self.currentCate)
        tmpath = self.mkdirs(tmpath)
        tmname = name.split("/")
        if len(tmname) > 1:
            pth = "/".join(tmname[0:(len(tmname)-1)])
            Path(tmpath + pth).mkdir(parents=True, exist_ok=True)
        with open(tmpath + name + ".txt", "w+") as f:
            for item in rawtext:
                f.write(item+"\n")

    def mkdirs(self, tmpath):
        Path(tmpath).mkdir(parents=True, exist_ok=True)
        return tmpath+"/"

    def run(self, currentCateName):
        print("Category saving-----------------" + currentCateName)
        r = requests.get(starting_page + currentCateName)
        subcate = self.getSubCategoryNames(r.text)
        pageurls = self.getPageUrls(r.text)
        for item in pageurls:
            self.getPageContent(item)
        print("Category finished---------------" + currentCateName)
        for cate in subcate:
            self.currentCate.append(cate)
            self.run(cate)
            self.currentCate.pop()

siteCrawler().run("Visualization_(graphic)")