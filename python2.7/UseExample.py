#coding=utf-8

from ImageTaskMgr import ImageTaskMgr

# ImageTaskMgr how to use example
# just put the keyword you want to search to the class
# ImageTaskMgr will auto download images
mgr = ImageTaskMgr("saorise ronan")
# for testing chinese character
mgr.search("瑟夏·羅南")
