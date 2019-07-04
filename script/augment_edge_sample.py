# -*- coding: utf-8 -*-
from PIL import Image
import os
import numpy as np
import sys
import string
from PIL import ImageEnhance
#import ImageEnhance
import random
import argparse
import shutil
from pylab import *
from numpy import *

import glob

def make_parser():
	parser = argparse.ArgumentParser(description='Process Images.',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	add_arg = parser.add_argument
	add_arg('--src_color',			default=False, type=str,			help='File pattern to load for training.')
	add_arg('--src_mask',			default=False, type=str,			help='File pattern to load for training mask.')
	add_arg('--src_label',			default=False, type=str,			help='File pattern to load for training label.')
	add_arg('--dst_color',			default=False, type=str,			help='Path  to save color images.')
	add_arg('--dst_mask',			default=False, type=str,			help='Path  to save mask images.')
	add_arg('--dst_label',			default=False, type=str,			help='Path  to save label images.')
	add_arg('--resize',				default=0, type=int,				help='images size.')
	add_arg('--augment',			default=0, type=int,				help='images size.')
	return parser
	
def histeq(im,nbr_bins = 256):
    """对一幅灰度图像进行直方图均衡化"""
    #计算图像的直方图
    #在numpy中，也提供了一个计算直方图的函数histogram(),第一个返回的是直方图的统计量，第二个为每个bins的中间值
    imhist,bins = histogram(im.flatten(),nbr_bins,normed= True)
    cdf = imhist.cumsum()   #
    cdf = 255.0 * cdf / cdf[-1]
    #使用累积分布函数的线性插值，计算新的像素值
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf
	
'''
def get_imlist(path):
	return [f for f in os.listdir(path) if (f.endswith('.bmp') or f.endswith('.jpg'))]
'''
#import pdb
def get_imlist(path, szExt):
	print(type(path))
	return [f for f in os.listdir(path) if (f.endswith(szExt) or f.endswith('.JPG') or f.endswith('.png'))]
#args=sys.argv

def resize_img():
	print("begin")
	parser = make_parser()
	args = parser.parse_args()
	args.src_color = r'E:\\Github\\Dataset_original\\face_real\\train_set\\face_color_thin/'              #'F:/edge_detection/sample/train_set/face_real/face_color_thin_dark/'
	args.src_mask = r'' #'F:/edge_detection/sample/train_set/face_real/face_mask_thin_dark/'
	args.src_label =r'E:\\Github\\Dataset_original\\face_real\\train_set\\face_label_thin/'  				  #'F:/edge_detection/sample/train_set/face_real/face_label_thin_dark/'

	args.dst_color = r'E:\\Github\\Dataset\\face_real\\train_set\\face_color_thin/'        		# r'F:/edge_detection/sample/train_set/face_real/face_color_thin_dark_512/'
	args.dst_mask =  r'' 	#r'F:/edge_detection/sample/train_set/face_real/face_mask_thin_dark_512/'
	args.dst_label =r'E:\\Github\\Dataset\\face_real\\train_set\\face_label_thin/'  		#r'F:/edge_detection/sample/train_set/face_real/face_label_thin_dark_512/'
	args.augment = 1
	args.resize = 512
	g_bMirror = 1
	g_lBright = 1
	g_lContrast = 1
	g_lNoise  = 1
	g_bHisteq = 0
	if os.path.isdir(args.dst_color):
		shutil.rmtree(args.dst_color)
	os.makedirs(args.dst_color)
	if os.path.isdir(args.dst_mask):
		shutil.rmtree(args.dst_mask)
	os.makedirs(args.dst_mask)
	if  os.path.isdir(args.dst_label):
		shutil.rmtree(args.dst_label)
	os.makedirs(args.dst_label)
	
	print("color={}; mask={}, label={}; dst_color={}; dst_mask={};  dst_label={}; ".format(args.src_color, args.src_mask, args.src_label, args.dst_color, args.dst_mask, args.dst_label))
	img_list = get_imlist(args.src_color, '.jpg')
	img_num = len(img_list)
	total_num =0
	resize = args.resize
	b_augment = args.augment
	if(len(img_list)==0):
		print("error: no image file found!")
		return -1
	for in_idx, in_ in enumerate(img_list):
		print("process #id {}, #total {}, #name {},".format(in_idx, img_num, in_,))
		in_color=(Image.open(args.src_color+in_))	
		(imgHeight, imgWidth)=in_color.size
		if(imgHeight>imgWidth):
			dstWidth = resize
			scale=(float)(dstWidth)/(float)(imgWidth)
			dstHeight=int(scale*imgHeight)
		else:
			dstHeight = resize
			scale=(float)(dstHeight)/(float)(imgHeight)
			dstWidth=(int)(scale*imgWidth)
		xMin=int(random.uniform(0, (dstHeight-resize)/2))
		yMin=int(random.uniform(0, (dstWidth-resize)/2))
		xMax=xMin+resize
		yMax=yMin+resize
		box=(xMin,yMin,xMax,yMax)
		#print box
		dstHeight = resize
		dstWidth = resize

		#resize color
		out_color = (in_color.resize((dstHeight,dstWidth),Image.BILINEAR))	 #改为双线性
		outpath_color = args.dst_color
		#out_crop_color=out_color.crop(box)
		out_crop_color = out_color
		out_crop_color.save(outpath_color + in_)
		
		#resize label
		in_label_name = os.path.splitext(in_)[0]+'.png'
		#in_label_name = in_
		in_label = (Image.open(args.src_label+in_label_name))
		out_label = (in_label.resize((dstHeight,dstWidth),Image.BILINEAR))	  	 #改为双线性
		#out_crop_label = out_label.crop(box)	
		#arr_label = np.array(out_label)
		#mask1=(arr_label>80)#skin
		#arr_label[mask1]=255;
		#out_label=Image.fromarray(arr_label)
		out_crop_label = out_label
		label_outpath = args.dst_label
		out_crop_label.save(label_outpath+in_label_name)

		#resize mask
		in_mask_name = os.path.splitext(in_)[0]+'.png'
		in_mask = (Image.open(args.src_mask + in_mask_name))
		out_mask = (in_mask.resize((dstHeight, dstWidth)))	
		out_crop_mask = out_mask
		mask_outpath = args.dst_mask
		out_crop_mask.save(mask_outpath+in_mask_name)

		#augment
		total_num = total_num+1	
		if(b_augment==1):
			[pre,sub]=os.path.splitext(in_)
			for i in range(g_lBright) :
				xMin=int(random.uniform(0, (dstHeight-resize)/2))
				yMin=int(random.uniform(0, (dstWidth-resize)/2))
				xMax=xMin+resize
				yMax=yMin+resize
				box=(xMin,yMin,xMax,yMax)
				#out_crop_color=out_color.crop(box)
				#out_crop_label = out_label.crop(box)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_mask = out_mask
				imgBright = ImageEnhance.Brightness(out_crop_color)
				out_crop_color = imgBright.enhance(random.uniform(0.2, 2))
				out_crop_color.save("{}bright{}_{}".format(outpath_color, i, in_))
				out_crop_label.save("{}bright{}_{}".format(label_outpath, i, in_label_name))
				out_crop_mask.save("{}bright{}_{}".format(mask_outpath, i, in_mask_name))
				total_num = total_num+1	
			for i in range(g_lContrast):
				xMin=int(random.uniform(0, (dstHeight-resize)/2))
				yMin=int(random.uniform(0, (dstWidth-resize)/2))
				xMax=xMin+resize
				yMax=yMin+resize
				box=(xMin,yMin,xMax,yMax)
				#out_crop_color=out_color.crop(box)
				#out_crop_label = out_label.crop(box)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_mask = out_mask
				imgContrast = ImageEnhance.Contrast(out_crop_color)
				out_crop_color = imgContrast.enhance(random.uniform(0.2, 2))
				out_crop_color.save("{}contrast{}_{}".format(outpath_color, i, in_))
				out_crop_label.save("{}contrast{}_{}".format(label_outpath, i, in_label_name))
				out_crop_mask.save("{}contrast{}_{}".format(mask_outpath, i, in_mask_name))
				total_num = total_num+1
			for i in range(g_lNoise):
				xMin=int(random.uniform(0, (dstHeight-resize)/2))
				yMin=int(random.uniform(0, (dstWidth-resize)/2))
				xMax=xMin+resize
				yMax=yMin+resize
				box=(xMin,yMin,xMax,yMax)
				#out_crop_color=out_color.crop(box)
				#out_crop_label = out_label.crop(box)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_mask = out_mask
				out_crop_color = np.array(out_crop_color)
				rn = int(32*random.uniform(0.5, 1) )
				out_crop_color = out_crop_color +  np.random.randint(-rn, rn, size=out_crop_color.shape)                
				out_crop_color[(out_crop_color>255).nonzero()] = 255
				out_crop_color[(out_crop_color<0).nonzero()] = 0
				out_crop_color = Image.fromarray(out_crop_color.astype(np.uint8))
				out_crop_color.save("{}noise{}_{}".format(outpath_color, i, in_))
				out_crop_label.save("{}noise{}_{}".format(label_outpath, i, in_label_name))    
				out_crop_mask.save("{}noise{}_{}".format(mask_outpath, i, in_mask_name))
				total_num = total_num+1
			if 1 == g_bMirror:
				xMin=int(random.uniform(0, (dstHeight-resize)/2))
				yMin=int(random.uniform(0, (dstWidth-resize)/2))
				xMax=xMin+resize
				yMax=yMin+resize
				box=(xMin,yMin,xMax,yMax)
				#out_crop_color=out_color.crop(box)
				#out_crop_label = out_label.crop(box)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_mask = out_mask
				out_crop_color=out_crop_color.transpose(Image.FLIP_LEFT_RIGHT)
				out_crop_color.save(outpath_color+'mirror_'+in_)       
				out_label_mirror=out_crop_label.transpose(Image.FLIP_LEFT_RIGHT)
				out_label_mirror.save(label_outpath+'mirror_'+in_label_name)    
				out_mask_mirror = out_crop_mask.transpose(Image.FLIP_LEFT_RIGHT)
				out_mask_mirror.save(mask_outpath+'mirror_'+in_mask_name)  
				total_num = total_num+1
			if 1 == g_bHisteq:
				xMin=int(random.uniform(0, (dstHeight-resize)/2))
				yMin=int(random.uniform(0, (dstWidth-resize)/2))
				xMax=xMin+resize
				yMax=yMin+resize
				box=(xMin,yMin,xMax,yMax)
				#out_crop_color=out_color.crop(box)
				#out_crop_label = out_label.crop(box)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_mask = out_mask
				'''
				out_color_yuv = out_color.convert('YCbCr')
				y,u,v = out_color_yuv.split()
				#print y.mode
				yh,cdf = histeq(array(y));
				yh = (Image.fromarray(yh)).convert('L')
				out_crop_color = Image.merge("YCbCr",[yh,u,v])
				'''
				
				r,g,b = out_color.split()
				r,cdf = histeq(array(r))
				g,cdf = histeq(array(g))
				b,cdf = histeq(array(b))
				b = Image.fromarray(b).convert('L')
				g = Image.fromarray(g).convert('L')
				r = Image.fromarray(r).convert('L')
				out_crop_color = Image.merge("RGB",[r,g,b])
				
				out_crop_color.save(outpath_color+'histeq_'+in_)       
				out_crop_label.save(label_outpath+'histeq_'+in_label_name)    	
				out_crop_mask.save(mask_outpath+'histeq_'+in_mask_name)    			
				total_num = total_num+1
			'''
			#flag = random.randint(1,2)
			flag = 1
			if(flag==1):
				roll = random.randint(1,45)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_color=out_crop_color.rotate(roll)
				out_crop_label=out_crop_label.rotate(roll)
				out_crop_color.save(outpath_color+'rotate'+str(roll)+in_)       
				out_crop_label.save(label_outpath+'rotate'+str(roll)+in_label_name)    				
				total_num = total_num+1
			flag = 2
			if(flag==2):
				roll = random.randint(315,359)
				out_crop_color = out_color
				out_crop_label = out_label
				out_crop_color=out_crop_color.rotate(roll)
				out_crop_label=out_crop_label.rotate(roll)
				out_crop_color.save(outpath_color+'rotate'+str(roll)+in_)       
				out_crop_label.save(label_outpath+'rotate'+str(roll)+in_label_name)    				
				total_num = total_num+1
			'''
	print("#total_num={}  finsish !;".format(total_num))

		   
if __name__=="__main__":
	resize_img()

