import os 
import SimpleITK as sitk
import numpy as np

ct_path = r"D:\!JUNG_2nd_data\abdomenCT1_regi_cc"
mr_path = r"D:\!JUNG_2nd_data\abdomenMr1xT_regi_hist_denoise_2"
ct_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\CT_nii"
mr_savepath = r"D:\!JUNG_2nd_data\cutted_save_fol\MR_nii"

ct_dir_list = os.listdir(ct_path)
mr_dir_list = os.listdir(mr_path)

for idx in range(len(ct_dir_list)):
    ct_sitk = sitk.ReadImage(os.path.join(ct_path, ct_dir_list[idx]))
    mr_sitk = sitk.ReadImage(os.path.join(mr_path, mr_dir_list[idx]))
    
    ct_arr = sitk.GetArrayFromImage(ct_sitk)
    mr_arr = sitk.GetArrayFromImage(mr_sitk)
    
    mr_coord = np.where(mr_arr != 0) # z y x
    mr_z_coord_sort = np.sort(mr_coord[0])
    
    Z1 = mr_z_coord_sort[0]
    Z2 = mr_z_coord_sort[-1]
    Z1 += 30
    Z2 -= 100
    ct_crop_arr = ct_arr[Z1:Z2+1, ...]
    mr_crop_arr = mr_arr[Z1:Z2+1, ...].astype("uint16")
    
    
    
    ct_crop_sitk = sitk.GetImageFromArray(ct_crop_arr)
    mr_crop_sitk = sitk.GetImageFromArray(mr_crop_arr)
    
    ct_crop_sitk.SetSpacing(ct_sitk.GetSpacing())
    ct_crop_sitk.SetOrigin(ct_sitk.GetOrigin())
    mr_crop_sitk.SetSpacing(mr_sitk.GetSpacing())
    mr_crop_sitk.SetOrigin(mr_sitk.GetOrigin())
    
    sitk.WriteImage(ct_crop_sitk, os.path.join(ct_savepath, ct_dir_list[idx]))
    sitk.WriteImage(mr_crop_sitk, os.path.join(mr_savepath, mr_dir_list[idx]))
    
    
    