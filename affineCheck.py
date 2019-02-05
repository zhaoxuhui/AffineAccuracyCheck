# coding=utf-8
import functionsV1 as fun
import cv2
import numpy as np

if __name__ == '__main__':
    img1 = cv2.imread("img1.jpg")
    img2 = cv2.imread("img2.jpg")
    kp1, des1 = fun.getSurfKps(img1, hessianTh=800)
    kp2, des2 = fun.getSurfKps(img2, hessianTh=800)
    good_kp1, good_kp2 = fun.flannMatch(kp1, des1, kp2, des2)

    match_img = fun.drawMatches(img1, good_kp1, img2, good_kp2)
    cv2.imwrite("match.jpg", match_img)

    affine_mat = fun.findAffine(good_kp1, good_kp2)
    print "Affine matrix:"
    print affine_mat
    T = np.mat(affine_mat[:, 2].reshape(2, 1))
    R = np.mat(affine_mat[:2, :2])
    print "Translation matrix:"
    print T
    print "Rotation matrix:"
    print R

    good_kp2_ = []

    for i in range(good_kp1.__len__()):
        pt1 = np.mat(good_kp1[i]).reshape(2, 1)
        pt2_ = R * pt1 + T
        good_kp2_.append(pt2_)

    for i in range(good_kp2.__len__()):
        pt = (int(good_kp2[i][0]), int(good_kp2[i][1]))
        cv2.circle(img2, pt, 3, [0, 0, 255], 1, cv2.LINE_AA)
        pt_ = (int(good_kp2_[i][0]), int(good_kp2_[i][1]))
        cv2.circle(img2, pt_, 3, [255, 0, 0], 1, cv2.LINE_AA)
    cv2.imwrite("check.jpg", img2)
