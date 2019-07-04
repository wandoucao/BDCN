#-*-coding:utf-8 -*-
import numpy as np

path1="E:/Github/Dataset/face_real/train_set/image_overall.txt"
path2="E:/Github/Dataset/face_real/train_set/gt_image_overall.txt"
path3="E:/Github/Dataset/face_real/train_set/face_real_train_pair.txt"

fp1=open(path1,'r')
fp2=open(path2,'r')
fp3=open(path3,'w')

n=len(fp1.readlines())
fp1.seek(0) #返回文件头

for i in  range(n):
    line1=fp1.readline().strip()
    line2=fp2.readline()
    line3=line1+"     " +line2
    fp3.writelines(line3)


fp1.close()
fp2.close()
fp3.close()
print('finish')