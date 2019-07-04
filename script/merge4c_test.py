#-*-coding: utf-8-*-

from __future__ import print_function
import os, glob, sys
import cv2
import numpy as np
import shutil
#train

# The main method
def main():
# Where to look for training or test samples

    #test
    inputSrcAPath = r'E:/Github/Dataset/face_real/train_set/face_color_thin'
    inputLabelPath = r'E:/Github/Dataset/face_real/train_set/face_label_thin'                 #'F:/edge_detection/test_result/test_mask'
    outputRPath = r'E:/Github/merge4c-output'   #'F:/edge_detection/test_result/test_rgba'
    if  os.path.isdir(outputRPath):
        shutil.rmtree(outputRPath)
    os.makedirs(outputRPath)
    #   OutputW = 256
    #   OutputH = 256

    searchFineA = os.path.join( inputSrcAPath , "*.jpg" )
    searchFineL = os.path.join( inputLabelPath , "*.png" )
    # search files
    filesFineA = glob.glob( searchFineA )
    filesFineA.sort()
    filesFineL = glob.glob( searchFineL )
    filesFineL.sort()
    print(len(filesFineA))
    print(len(filesFineL))
    assert(len(filesFineA) == len(filesFineL))

    # quit if we did not find anything
    if not filesFineA:
        print( "Did not find any files in filesFineA. Please check the dir." ) 
    if not filesFineL:
        print( "Did not find any files in filesFineL. Please check the dir." )
    if not os.path.isdir(outputRPath):
        os.makedirs(outputRPath)

    # a bit verbose
    print("Processing {} annotation files".format(len(filesFineA)))

    # iterate through files
    progress = 0
    for i in range(len(filesFineA)):
        PathNameA = filesFineA[i]
        PathNameL = filesFineL[i]

        ImageA = cv2.imread(PathNameA)
        Mask = cv2.imread(PathNameL, 0)
        Mask = np.expand_dims(Mask, axis=2)

        ImageR = np.concatenate([ImageA, Mask], 2)

        fileNameA = os.path.basename(filesFineA[i])
        fileNameR = os.path.splitext(fileNameA)[0] + ".png"
        cv2.imwrite(os.path.join(outputRPath, fileNameR), ImageR)

        # status
        progress += 1
        print("Progress: {:>3} / {:>3}".format( progress, len(filesFineA)))
        sys.stdout.flush()

# call the main
if __name__ == "__main__":
    main()
