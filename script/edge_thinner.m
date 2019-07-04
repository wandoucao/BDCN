clear
clc
dbPath='E:\Github\share_data\face_label';
dstPath='E:\Github\share_data\face_label_thin_512';
mkdir(dstPath);
imgList = dir(dbPath);
imgNum = length(imgList);
for id = 3:imgNum
    imgName = imgList(id).name;
    imgFullPath  = fullfile(dbPath, imgName);
    im = imread(imgFullPath);
    [h,w,c]=size(im);
    if(c==3)
        im = rgb2gray(im);
    end
    im(find(im<40))=0;
    im_thin = bwmorph(im,'thin',inf);  %二值图像:形态学细化%
    im_thin(find(im_thin>10))=255;
    dstFullPath = fullfile(dstPath, imgName);
    imwrite(im_thin,dstFullPath);
end
printf("Finished")