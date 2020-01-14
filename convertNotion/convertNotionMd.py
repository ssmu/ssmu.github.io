import re, os, argparse
from glob import glob
from datetime import datetime
from subprocess import check_output

POST_PREFIX=datetime.now().strftime('%Y-%m-%d')
MD_IMG_PAT = "\[.*\]\(.*\.(?:jpg|gif|png)\)"
YAML="""---
layout: post
title: {postname}
date: {date}
img: # Add image post (optional)
tags: []
---
"""

def prepDir(dir_name,postname):
    md_fname = glob(dir_name+'*.md')[0]
    print(glob(dir_name+'*/'))
    img_dir = glob(dir_name+'*/')[0]
    check_output('mv {} ../assets/img/'.format(img_dir),shell=True)
    prepFile(md_fname,postname)

def prepFile(fname, postname="Test"):
    text = readMarkDownFileText(fname)
    md_filename = getPostFileName(postname)
    new_text = getNewText(text)
    new_yaml = YAML.format(postname=postname, date=POST_PREFIX)
    with open("../_posts/"+md_filename, 'w') as f:
        f.write(new_yaml+new_text)
        
def getNewText(text):
    new_text = text
    img_links = re.findall(MD_IMG_PAT,new_text)
    for link in img_links:
        new_text = replaceLink(new_text, link)
    return new_text
    
def replaceLink(text,link):
    new_link = getNewLink(link)
    return text.replace(link,new_link)

def getNewLink(link):
    index = re.search('(?<=\().*(?=\))',link).start()
    return link[:index] + '{{site.baseurl}}/assets/img/' + link[index:]

def readMarkDownFileText(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def getImageFileNames(dir_name):
    return glob('{}*/**'.format(dir_name))

def getPostFileName(title):
    return '{}-{}.markdown'.format(POST_PREFIX, title)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("title")
    args = parser.parse_args()
    prepDir(args.dir, args.title)