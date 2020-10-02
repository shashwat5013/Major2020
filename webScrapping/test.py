# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 09:36:24 2020

@author: shash
"""
import requests
from bs4 import BeautifulSoup

url="https://www.instagram.com/anandsingh5615/"
r=requests.get(url)

htmlContent=r.content
#print(htmlContent)

soup=BeautifulSoup(htmlContent,'lxml')
main=soup.find('body')
script=main.find('script')
print(script)








