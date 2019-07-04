#-*-coding:utf-8 -*-
import numpy as np
import os
import shutil #批量拷贝数据

def opt_list():
    path1="E:\Github\Dataset\\face_real_merge4c\\test_set/imglist.txt"
    path2="E:\Github\Dataset\\face_real_merge4c\\test_set/lablelist.txt"
    path3="E:\Github\Dataset\\face_real_merge4c\\test_set/face_real_test_pair.txt"

    fp1=open(path1,'r')
    fp2=open(path2,'r')
    fp3=open(path3,'w')

    n=len(fp1.readlines())
    fp1.seek(0) #返回文件头

    for i in  range(n):
        line1=fp1.readline().strip()
        line2=fp2.readline()
        line3=line1+" " +line2
        fp3.writelines(line3)

    fp1.close()
    fp2.close()
    fp3.close()
    print('finish')


def get_imglist(): #get imgnamel list to txt
    list=os.listdir('E:\Github\Dataset\\face_real_merge4c\\test_set\img')
    savefile='E:\Github\Dataset\\face_real_merge4c\\test_set\imglist.txt'
    np.savetxt(savefile,list,fmt='%s')
    print('finish')

def copyimg():
    imgnamelist='E:\Github\share_data\my_temp_dark\imglist.txt'

    orgpath='E:\Github\share_data\merge4c-output-original'
    dstpath='E:\Github\share_data\my_temp_dark_4c\img'

    list=np.loadtxt(imgnamelist,dtype=np.str)
    for ele in list:
        orgimg=orgpath+'/'+ele.split('.')[0]+'.png'
        new_obj_name = dstpath+'/'+ele.split('.')[0]+'.png'

        shutil.copy(orgimg, new_obj_name)
    print('finish')

if __name__ == '__main__':
    print('choose the func')
    opt_list()
    # get_imglist()
    # copyimg()
