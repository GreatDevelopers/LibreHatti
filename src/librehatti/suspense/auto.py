#!/usr/bin/env python
import os
import sys
import django

#if __name__ == '__main__':
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librehatti.settings')
#django.setup()
from django.core.management import execute_from_command_line

sys.path.insert(0,'/home/amisha/python_programs/lh/LibreHatti/src/')
#execute_from_command_line(sys.argv)
#import manage
django.setup()
import librehatti
from librehatti.suspense import urls
from shutil import copyfile

#copyfile("urls.py", "urlsold.py")

#import ipdb
#ipdb.set_trace()
li=[]
new_li=[]
with open('urls.py') as fin:
    fin_content = fin.readlines()

for i in urls.urlpatterns:
    li.append(i.lookup_str.split("views.")[1])

i=0
#import ipdb
#ipdb.set_trace()
for j in range(0, len(fin_content)):
    if (i<len(li) and li[i] in fin_content[j]):
       print((i,j))
       print((li[i]+ "    "+fin_content[j]))
       if (i!=len(li)-1):
          k= fin_content[j].replace("),", ", name= '" + li[i] + "'),")
       else: 
          k= fin_content[j].replace(")", ", name= '" + li[i] + "')")
       new_li.append(k)
       i=i+1
       continue
    else:
       new_li.append(fin_content[j])
       continue

fo = open("urls.py", "w")

line = fo.writelines( new_li )
fo.close()


