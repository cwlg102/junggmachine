import os 
import SimpleITK as sitk
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt 
from PIL import Image
# def rt_connecting(rt_arr):
    
def resample(sitk_volume, new_spacing, new_size, default_value=0, is_label=False):
    """1) Create resampler"""
    resample = sitk.ResampleImageFilter() 
    
    """2) Set parameters"""
    #set interpolation method, output direction, default pixel value
    resample.SetInterpolator(sitk.sitkLinear)
    resample.SetOutputDirection(sitk_volume.GetDirection())
    resample.SetDefaultPixelValue(default_value)
    
    #set output spacing
    new_spacing = np.array(new_spacing)
    resample.SetOutputSpacing(new_spacing)
    
    #set output size and origin
    old_size = np.array(sitk_volume.GetSize())
    old_spacing = np.array(sitk_volume.GetSpacing())
    new_size_no_shift = np.int16(np.ceil(old_size*old_spacing/new_spacing))
    old_origin = np.array(sitk_volume.GetOrigin())
    
    shift_amount = np.int16(np.floor((new_size_no_shift - new_size)/2))*new_spacing
    new_origin = old_origin + shift_amount
    
    new_size = [int(s) for s in new_size]
    resample.SetSize(new_size)
    resample.SetOutputOrigin(new_origin)
    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        pass


    """3) execute"""
    new_volume = resample.Execute(sitk_volume)
    return new_volume

def filling_contour(rt_arr):
    rt_arr = np.transpose(rt_arr, (2, 1, 0)).astype("uint8")
    
    for i in range(len(rt_arr)):
        rt_arr[i] = ndimage.binary_closing(rt_arr[i])
    rt_arr = np.transpose(rt_arr, (2, 1, 0)).astype("uint8")
    
    return rt_arr

rt_basepath = r"D:\!JUNG_2nd_data\abdomenCT1_liver_sitk"
rt_savepath = r"D:\!JUNG_2nd_data\abdomenCT1_liver_sitk_res"
rt_dir_list = os.listdir(rt_basepath)

for idx in range(len(rt_dir_list)):
    rt_sitk_path = os.path.join(rt_basepath, rt_dir_list[idx])
    rt_sitk = sitk.ReadImage(rt_sitk_path)
    rt_arr = sitk.GetArrayFromImage(rt_sitk)
    
    rt_arr = filling_contour(rt_arr)
    
    # rt_arr = rt_arr.astype("uint8")   
    # for i in range(len(rt_arr)):
    #     img = Image.fromarray(rt_arr[i])
    #     img.save(os.path.join(r"D:\!JUNG_2nd_data\liver_contour_img_1", "P%03d_%03d.png" %(idx, i)))
    
        
    # #resample 부분
    
    target_spacing = np.array([0.7, 0.7, 1.20],dtype=np.double)
    original_rt_size = rt_sitk.GetSize()
    original_rt_spacing = rt_sitk.GetSpacing()
    
    # z_size setting
    
    new_rt_z_size = original_rt_size[2] * (original_rt_spacing[2] / target_spacing[2])
    new_rt_z_size_int = int(new_rt_z_size)
    zero_one_decimal_num_rt = new_rt_z_size - float(new_rt_z_size_int)
    if zero_one_decimal_num_rt >= 0.5: new_rt_z_size_int += 1
    
    target_rt_size = np.array([512, 512, new_rt_z_size], dtype=np.double)
    
    new_rt_sitk = sitk.GetImageFromArray(rt_arr)
    new_rt_sitk.SetSpacing(rt_sitk.GetSpacing())
    new_rt_sitk.SetOrigin(rt_sitk.GetOrigin())
    
    rt_resampled_sitk = resample(new_rt_sitk, target_spacing, target_rt_size, default_value=0)
    
    sitk.WriteImage(rt_resampled_sitk, os.path.join(rt_savepath, rt_dir_list[idx]))
    
    