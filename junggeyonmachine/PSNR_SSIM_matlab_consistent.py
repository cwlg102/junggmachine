import os
import cv2
import numpy as np
import math 
image1_path = r"D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\fakeCT"
image2_path = r"D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\realCT"
image1_list = os.listdir(image1_path)
image2_list = os.listdir(image2_path)

def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

def PSNR(img1, img2, shave_border=0):
    height, width = img1.shape[:2]
    img1 = img1[shave_border:height - shave_border, shave_border:width - shave_border]
    img2 = img2[shave_border:height - shave_border, shave_border:width - shave_border]
    imdff = img1 - img2
    rmse = math.sqrt(np.mean(imdff ** 2))
    if rmse == 0:
        return 100
    return 20 * math.log10(255.0 / rmse)
    
def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')

#img1 = cv2.imread(r"D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\fakeCT_gray\P017MR_slice001_fake.jpg", 0)
#img2 = cv2.imread(r"D:\junggeyon_results\pelvic_unpaired_e250_testrlt\test_latest\realCT\P017CT_slice001.jpg", 0)
#ss = calculate_ssim(img1, img2)
#ps = PSNR(img1, img2)
#print(ss)
#print(ps)

ss_list = []
ps_list = []
for idx in range(len(image1_list)):
    img1 = cv2.imread(image1_path + '/' + image1_list[idx])
    img2 = cv2.imread(image2_path + '/' + image2_list[idx])
    ss = calculate_ssim(img1, img2)
    ps = PSNR(img1, img2)
    ss_list.append(ss)
    ps_list.append(ps)

print(np.mean(ss))
print(np.mean(ps))