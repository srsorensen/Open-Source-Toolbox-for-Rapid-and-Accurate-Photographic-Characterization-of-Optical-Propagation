def remove_outliers_IQR(x, data, blocks, num_neighbors):
    # Removal of outliers using IQR. Change blocks -> Num_Subsets
    data_blocks = np.array_split(data, blocks)
    x_blocks = np.array_split(x, blocks)
    x_blocks_indexes = [x[-1] for x in x_blocks]

    for i in range(len(data_blocks)):
        Q1 = np.percentile(data_blocks[i], 25, interpolation='midpoint')
        Q3 = np.percentile(data_blocks[i], 75, interpolation='midpoint')
        IQR = Q3 - Q1

        upper = Q3 + 1.5 * IQR
        lower = Q1 - 1.5 * IQR

        upper_array = np.where(data_blocks[i] >= upper)[0]
        lower_array = np.where(data_blocks[i] <= lower)[0]

        remove_array = np.concatenate((upper_array, lower_array))
        new_remove_array = []

        for index in remove_array:  # Finding indexes of neighbors to detected outliers
            neighbor_indexes = np.arange(index - num_neighbors, index + num_neighbors + 1, 1)
            neighbor_indexes = [x for x in neighbor_indexes if x > 0 and x < len(data_blocks[i])]
            new_remove_array += neighbor_indexes

        new_remove_array = list(set(new_remove_array))
        data_blocks[i] = np.delete(data_blocks[i], new_remove_array)  # removing outliers and neighbors from data
        x_blocks[i] = np.delete(x_blocks[i], new_remove_array)

    return np.concatenate(x_blocks), np.concatenate(data_blocks), x_blocks_indexes


def split_maximum(data, num_blocks):  # Splits the data up into num_blocks blocks and finds the maximum for each block
    blocks = np.array_split(data, num_blocks)

    maxima = []
    maxima_index = []

    for i in range(len(blocks)):
        index = np.argmax(blocks[i])
        maxima.append(blocks[i][index])
        maxima_index.append((len(blocks[0]) * i) + index)

    return maxima, maxima_index

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit, least_squares
from scipy.signal import find_peaks

from functions import *
import scipy.signal

fontsize = 10
#plt.rcParams['text.usetex'] = True
plt.rcParams['axes.labelsize'] = fontsize
plt.rcParams['legend.fontsize'] = fontsize
plt.rcParams['legend.loc'] = 'upper left'
plt.rcParams['xtick.labelsize'] = fontsize
plt.rcParams['ytick.labelsize'] = fontsize


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.legend_handler


#############################################################
## Setup
fontsize = 8
#plt.rcParams['text.usetex'] = True
plt.rcParams['axes.labelsize'] = fontsize
plt.rcParams['legend.fontsize'] = fontsize
plt.rcParams['legend.loc'] = 'upper left'
plt.rcParams['xtick.labelsize'] = fontsize
plt.rcParams['ytick.labelsize'] = fontsize

LW, MS, MEW = 0.5, 2.5, 0.2
XSMALL, SMALL_SIZE, MEDIUM_SIZE, BIGGER_SIZE = 12, 12, 20, 20
FWIDTH = 2.2  # 2.2
mpl.rcParams['lines.markersize'] = 15
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['axes.linewidth'] = 1  # 1
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rc('xtick.minor', size=5, width=1.5)
mpl.rc('ytick.minor', size=5, width=1.5)
mpl.rc('xtick.major', size=5, width=1.5)
mpl.rc('ytick.major', size=5, width=1.5)
#mpl.rcParams['figure.figsize'] = [FWIDTH, FWIDTH / np.sqrt(2)]
#mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.bbox'] = "tight"
mpl.rcParams['savefig.pad_inches'] = 0.3 * SMALL_SIZE / 72
plt.rc('font', size=MEDIUM_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)
plt.rc('xtick', labelsize=MEDIUM_SIZE)
plt.rc('ytick', labelsize=MEDIUM_SIZE)
plt.rc('legend', fontsize=MEDIUM_SIZE)
plt.rc('figure', titlesize=BIGGER_SIZE)
#############################################################


path = 'Pictures/'

# Load Image
mum_pr_pixel = 0.4876681614349776 # Zoom 7

picture_index = 124
pictures = print_files(path, 'bmp')
print(pictures[picture_index])
original_image = Image.open(path + pictures[picture_index])
original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)  # flip image and manually rotate
original_image_array = np.asarray(original_image)
height, width, num_color = np.shape(original_image_array)
print(width, height)
x_mu_array = np.arange(width) * mum_pr_pixel
y_mu_array = np.arange(height) * mum_pr_pixel
plt.title("Cropped")
plt.xlabel('x [um]')
plt.ylabel('y [um]')
original_intensity_array = get_intensity_array(original_image_array)

plt.imshow(original_intensity_array, cmap="binary", extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])

# -*- coding: utf-8 -*-
"""
Created on Mon May  9 10:03:03 2022

@author: Peter Tønning, Kevin Bach Gravesen, Magnus Linnet Madsen
"""
import numpy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit, least_squares
from scipy.signal import find_peaks

from functions import *
import scipy.signal

# Path the pictures are at
path = 'Pictures/'

# Load Image
picture_index = 124
pictures = print_files(path, 'bmp')
print(pictures[picture_index])
original_image = Image.open(path + pictures[picture_index])
#original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)  # flip image and manually rotate
original_image_array = np.asarray(original_image)

original_intensity_array = get_intensity_array(original_image_array)
plt.imshow(original_intensity_array)



# Size of Image
window_num_pixel_height = np.shape(original_image_array)[0]  # 2048
window_num_pixel_width = np.shape(original_image_array)[1]  # 2448

# Distance Calibration
chip_length_mum = 870 # mu m

# Chip Detection

#find_chip(original_image)

# Detect the pixel of input
input_width_index, input_height_index, output_width_index, output_height_index = insertion_detection(original_image.copy())
print("input_width_index: ", input_width_index, " input_height_index ", input_height_index, " output_width_index: ", output_width_index, "output_height_index: ", output_height_index)


# Change these to cut out the laser from the left and how far you want to go to the right
left_indent = input_width_index - 100
right_indent = output_width_index
top_indent = input_height_index - 100
bottom_indent = input_height_index + 100
cropped_image = original_image.crop((left_indent, top_indent, right_indent, bottom_indent))
cropped_image_array = np.asarray(cropped_image)

distance_input_output_pixel = np.sqrt((input_height_index - output_height_index)**2 + (input_width_index - output_width_index)**2)

# Length Calibration
mum_pr_pixel = chip_length_mum / distance_input_output_pixel
mum_pr_pixel = 0.4876681614349776
print("mum pr pixel: ",mum_pr_pixel)
# Find the waveguide
left_index_guess = 100
separation = 100
number_of_points = 10
angle, angle_params, x_max_index_array, y_max_index_array = find_waveguide_angle(cropped_image_array[:, :, 2], left_index_guess, separation, number_of_points)

# Rotate picture and plot it with the upper and lower limit
print("Angle: ", angle)
left_indent = left_indent
right_indent = right_indent
top_indent = top_indent
bottom_indent = bottom_indent
rotated_image = original_image.rotate(-angle, center=(left_indent, int(angle_params[1]) + top_indent)).crop((left_indent, top_indent, right_indent, bottom_indent))
rotated_image_array = np.asarray(rotated_image)

interval = 10
upper = int(angle_params[1] + interval/2)
lower = int(angle_params[1] - interval/2)
cropped_array = rotated_image_array[lower:upper, :, 2]
shape_cropped_array = np.shape(cropped_array)

x_mu_array = np.arange(np.shape(rotated_image_array)[1]) * mum_pr_pixel
y_mu_array = np.arange(np.shape(rotated_image_array)[0]) * mum_pr_pixel


plt.figure(figsize=(10,6))
plt.imshow(np.flip(get_intensity_array(cropped_image_array.copy())), cmap="turbo", vmin=1.5, vmax=np.max(get_intensity_array(cropped_image_array.copy())), interpolation='spline16', extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
plt.xlabel(r'Propagation length [mm]')
plt.tick_params(left = False, labelleft = False)
plt.tight_layout()
#plt.savefig('Figures/binary_photo.png', transparent=True)
plt.figure()
plt.imshow(get_intensity_array(cropped_image_array.copy()), cmap="jet", vmin=0, vmax=10, interpolation='spline16', extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])

plt.plot(x_mu_array[x_max_index_array], y_mu_array[y_max_index_array],'r.')
plt.plot([x_mu_array[0], x_mu_array[-1]], [angle_params[1]*mum_pr_pixel, (angle_params[0]*len(x_mu_array) + angle_params[1])*mum_pr_pixel],'r-')
#plt.plot(x_mu_array[right_max_width_index], y_mu_array[right_max_height_index], 'r.')
#plt.plot([x_mu_array[left_max_width_index], x_mu_array[right_max_width_index]], [y_mu_array[left_max_height_index], y_mu_array[right_max_height_index]], 'r-')

plt.xlabel('x [um]')
plt.ylabel('y [um]')

# Plot rotated picture
plt.figure()
plt.imshow(get_intensity_array(rotated_image_array), cmap="jet", vmin=4, vmax=5, extent=[x_mu_array[0], x_mu_array[-1], y_mu_array[0], y_mu_array[-1]])
plt.title("Rotated Image")
plt.xlabel('x [um]')
plt.ylabel('y [um]')
plt.show()
upper_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * upper).astype("int")
lower_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * lower).astype("int")

background_delta = 20
background_lower = lower - background_delta
background_upper = upper + background_delta

background_upper_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * background_upper).astype("int")
background_lower_index_array = (np.ones(len(rotated_image_array[0, :, 2])) * background_lower).astype("int")

plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[upper_index_array], 'r-')
plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[lower_index_array], 'r-')

plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[background_upper_index_array], 'r-')
plt.plot(x_mu_array[0:len(rotated_image_array[0, :, 2])], y_mu_array[background_lower_index_array], 'r-')

# Find Saturated Points
unsaturation_percentage_limit = 1
saturated_bool_array = cropped_array != 255
saturated_mean_bool_array = np.mean(saturated_bool_array, axis=0)
peaks_index_array = find_peaks(1 - saturated_mean_bool_array, height=0.05, threshold=None, distance=20, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)[0]
max_array = np.max(cropped_array, axis=0)
saturation_index_list = np.where(max_array != 255)[0]
window_num_pixel_height = np.shape(rotated_image_array)[0]  # 2048
window_num_pixel_ewidth = np.shape(rotated_image_array)[1]  # 2448
length_convolve = 200
saturated_array = max_array != 255
saturated_array_pad = np.pad(saturated_array, (length_convolve, length_convolve), 'constant', constant_values=(0, 1))
saturated_array_pad_convolved = np.convolve(saturated_array_pad, np.ones(length_convolve), 'same') / length_convolve
saturated_array_convolved = saturated_array_pad_convolved[length_convolve:length_convolve + shape_cropped_array[1]]
saturated_list = np.where(saturated_array_convolved >= unsaturation_percentage_limit)

#left_saturation_crop = saturated_list[0][0] + 800
left_saturation_crop = 0
right_saturation_crop = -1
#right_saturation_crop = saturated_list[0][-1]

# Plot Saturation
plt.figure()
plt.plot(x_mu_array, saturated_array, label="Is Saturated")
plt.plot(x_mu_array, saturated_array_convolved, label="Convolved is Saturated")
plt.plot(x_mu_array, saturated_mean_bool_array, "r-", label="Percentage Saturated")
plt.plot(x_mu_array[peaks_index_array], saturated_mean_bool_array[peaks_index_array], "r.")
plt.plot([x_mu_array[left_saturation_crop], x_mu_array[left_saturation_crop]], [0, 1], 'r')
plt.plot([x_mu_array[right_saturation_crop], x_mu_array[right_saturation_crop]], [0, 1], 'r')
plt.plot([x_mu_array[0], x_mu_array[-1]], [unsaturation_percentage_limit, unsaturation_percentage_limit], 'r')
plt.ylabel('Saturation Index')
plt.title("Saturation")
plt.xlabel('x [um]')
plt.legend()

cropped_image_height = np.shape(rotated_image_array)[0]
# Find Background
average_background_list, confidence_background_list, prediction_background_list = find_background(rotated_image_array[:,left_saturation_crop:right_saturation_crop,:], cropped_image_height - upper, cropped_image_height - lower, cropped_image_height - background_upper, cropped_image_height - background_lower)

# Plot Data
x_length_crop_mu_array = x_mu_array[left_saturation_crop:right_saturation_crop] # 7229 um measured on the GDS, 2445 is the pixel width of the sensor (Both numbers inherent of the sensor and lens)
x = x_length_crop_mu_array
pic = rotated_image_array[:, left_saturation_crop:right_saturation_crop, 2]
y = np.mean(rotated_image_array[cropped_image_height - upper: cropped_image_height - lower, left_saturation_crop:right_saturation_crop, 2], axis=0)
y_std = np.std(rotated_image_array[cropped_image_height - lower: cropped_image_height - upper, left_saturation_crop:right_saturation_crop, 2], axis=0)

plt.figure()
y_= np.sum(rotated_image_array[cropped_image_height - upper: cropped_image_height - lower, left_saturation_crop:right_saturation_crop, 2], axis=0)


plt.figure()
#plt.plot(x_length_crop_mu_array, np.max(rotated_image_array[lower:upper, :, 2], axis=0), 'k-', label="Max reading")

plt.plot(x, y, 'b-', label="Raw data")
#plt.plot(x, average_background * np.ones(np.shape(x_length_crop_mu_array)), 'm-', label="Background")
#plt.plot(x, (average_background + 2 * confidence_background) * np.ones(np.shape(x)), 'm', linestyle='dashed', label="2 Sigma Confindece Bound")
#plt.plot(x, (average_background - 2 * confidence_background) * np.ones(np.shape(x)), 'm', linestyle='dashed')
#plt.plot(x, (average_background + 2 * prediction_background) * np.ones(np.shape(x)), 'm', linestyle='dotted', label="2 Sigma Prediction Bound")
#plt.plot(x, (average_background - 2 * prediction_background) * np.ones(np.shape(x)), 'm', linestyle='dotted')
plt.plot(x, average_background_list, 'y-', label="Background")
#plt.plot(x, average_background_list + 2 * confidence_background_list, 'y', linestyle='dashed', label="2 Sigma Confindece Bound")
#plt.plot(x, average_background_list - 2 * confidence_background_list, 'y', linestyle='dashed')
#plt.plot(x, average_background_list + 2 * prediction_background_list, 'y', linestyle='dotted', label="2 Sigma Prediction Bound")
#plt.plot(x, average_background_list - 2 * prediction_background_list, 'y', linestyle='dotted')
plt.legend()
plt.xlabel('x Length [um]')
plt.ylim([0, np.max(y)])
plt.ylabel('Mean of blue intensity')
plt.title(pictures[picture_index])

# Fit Exponential Curve

remove_number = 1

remove_index_array = np.array([])
for peak_index in peaks_index_array:
    remove_index = np.arange(peak_index - remove_number, np.min([peak_index + remove_number + 1, np.size(x_length_crop_mu_array)]), 1)
    remove_index_array = np.concatenate((np.array(remove_index_array), remove_index))

remove_index_array = np.unique(remove_index_array.astype(int))

fit_x = np.delete(x_length_crop_mu_array, np.flip(y > 20))[0:-300]
fit_y = np.flip(np.delete((y - average_background_list), y > 20))[0:-300]
x_iqr, y_iqr, indexes = remove_outliers_IQR(fit_x,fit_y,10,1)
y_max_raw, x_max, = split_maximum(fit_y,100)
x_max = x_max[0:-2]
x_max_raw = fit_x[x_max]
y_max_raw = y_max_raw[0:-2]
y_max_iqr, x_max, = split_maximum(y_iqr,100)
x_max = x_max[0:-5]
x_max_iqr = x_iqr[x_max]
y_max_iqr = y_max_iqr[0:-5]


initial_guess = [ 4.22054755e-06, 6.70214111e-04, -1.25009852e+02]
fit_rescaling = 1
fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(sfg_model_off_set, fit_x/fit_rescaling, fit_y, p0=initial_guess, full_output=True, bounds= ([0,0,-1000],[10e-06, 10e-04, 1000]))
fit = sfg_model_off_set(fit_x/fit_rescaling, fit_parameters[0], fit_parameters[1], fit_parameters[2])
confidence_bounds_fit = sfg_model_off_set_confidence_bound(fit_x/fit_rescaling, fit_parameters, fit_parameters_cov_var_matrix)
#print("Fit Parameters", fit_parameters, "Covariance Matrix", fit_parameters_cov_var_matrix)
residuals_MSE = fit - fit_y
mean_squared_error = np.mean(residuals_MSE**2)

fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(sfg_model_off_set, x_iqr/fit_rescaling, y_iqr, p0=initial_guess, full_output=True, bounds= ([0,0,-1000],[10e-06, 10e-04, 1000]))
fit_iqr = sfg_model_off_set(x_iqr/fit_rescaling, fit_parameters[0], fit_parameters[1], fit_parameters[2])
confidence_bounds_fit_iqr = sfg_model_off_set_confidence_bound(x_iqr/fit_rescaling, fit_parameters, fit_parameters_cov_var_matrix)
#print("Fit Parameters", fit_parameters, "Covariance Matrix", fit_parameters_cov_var_matrix)
residuals_MSE_iqr = fit_iqr - y_iqr
mean_squared_error_iqr = np.mean(residuals_MSE_iqr**2)



avg = moving_average_padding(fit_y, 200)
avg_iqr = moving_average_padding(y_iqr, 200)


residuals = avg - fit
ss_res = np.sum(residuals ** 2)

ss_tot = np.sum((avg - np.mean(avg)) ** 2)
r_squared = 1 - (ss_res / ss_tot)
print('R^2 = ', r_squared)

residuals_iqr = avg_iqr - fit_iqr
ss_res_iqr = np.sum(residuals_iqr ** 2)

ss_tot_iqr = np.sum((avg_iqr - np.mean(avg_iqr)) ** 2)
r_squared_iqr = 1 - (ss_res_iqr / ss_tot_iqr)

fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(sfg_model_off_set, x_max_raw, y_max_raw, p0=initial_guess, full_output=True, bounds= ([0,0,-1000],[10e-06, 10e-04, 1000]))
fit_max_raw = sfg_model_off_set(x_max_raw, fit_parameters[0], fit_parameters[1], fit_parameters[2])
confidence_bounds_fit_max_raw = sfg_model_off_set_confidence_bound(x_max_raw, fit_parameters, fit_parameters_cov_var_matrix)
#print("Fit Parameters", fit_parameters, "Covariance Matrix", fit_parameters_cov_var_matrix)
residuals_max_raw = y_max_raw - fit_max_raw
ss_res_max_raw = np.sum(residuals_max_raw ** 2)

ss_tot_max_raw = np.sum((y_max_raw - np.mean(y_max_raw)) ** 2)
r_squared_max_raw = 1 - (ss_res_max_raw / ss_tot_max_raw)

fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(sfg_model_off_set, x_max_iqr, y_max_iqr, p0=initial_guess, full_output=True, bounds= ([0,0,-1000],[10e-06, 10e-04, 1000]))
fit_max_iqr = sfg_model_off_set(x_max_iqr, fit_parameters[0], fit_parameters[1], fit_parameters[2])
confidence_bounds_fit_max_iqr = sfg_model_off_set_confidence_bound(x_max_iqr, fit_parameters, fit_parameters_cov_var_matrix)
#print("Fit Parameters", fit_parameters, "Covariance Matrix", fit_parameters_cov_var_matrix)
residuals_max_iqr = y_max_iqr - fit_max_iqr
ss_res_max_iqr = np.sum(residuals_max_iqr ** 2)

ss_tot_max_iqr = np.sum((y_max_iqr - np.mean(y_max_iqr)) ** 2)
r_squared_max_iqr = 1 - (ss_res_max_iqr / ss_tot_max_iqr)


plt.figure(figsize=(10,6))
plt.scatter(fit_x*1e-3, fit_y, color='k',linestyle='-', alpha=0.2,s=3)
#plt.scatter(x_max_raw*1e-3,y_max_raw,s=20,color="g",marker="d")
#plt.plot(x_max_raw*1e-3, fit_max_raw, linestyle="--",color="g",label=f"Fit to max values raw: R\u00b2 {r_squared_max_raw:.2f}")
#plt.scatter(x_max_iqr*1e-3,y_max_iqr,s=20,color="#a65628")
#plt.plot(x_max_iqr*1e-3, fit_max_iqr, linestyle="--",color="#a65628",label=f"Fit to max values outlier corrected: R\u00b2 {r_squared_max_iqr:.2f}")
plt.plot(fit_x*1e-3, avg, color='r',linestyle='-',alpha=0.6)
plt.plot(fit_x*1e-3, fit, linestyle="--",color="r",label=f"Fit to raw data: R\u00b2 {r_squared:.2f}")
plt.plot(x_iqr*1e-3, avg_iqr, color='b',linestyle='-',alpha=0.6)
plt.plot(x_iqr*1e-3, fit_iqr, linestyle="--",color="b",label=f"Fit to outlier corrected data: R\u00b2 {r_squared_iqr:.2f}")
#plt.plot(fit_x*1e-3, fit + 2*confidence_bounds_fit, color='k',linestyle='--')
#plt.plot(fit_x*1e-3, fit - 2*confidence_bounds_fit, color='k',linestyle='--')
plt.xlabel(r'Propagation length [mm]',fontsize=24)
plt.ylabel(r'Intensity [a.u.]',fontsize=24)
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.xlim([0, 1000*1e-3])
plt.ylim([0, 3])
plt.tight_layout()
plt.legend(loc='lower right')
plt.show()


print(x_length_crop_mu_array)
print("Picture", pictures[picture_index])
print("Fit Parameters:", fit_parameters)
print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
print(
    f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/m")
print(
    f'alpha_dB = {pr_mum_to_dB_pr_cm(fit_parameters[1])} ({pr_mum_to_dB_pr_cm(fit_parameters[1] + np.sqrt(fit_parameters_cov_var_matrix[1, 1]))} {pr_mum_to_dB_pr_cm(fit_parameters[1] - np.sqrt(fit_parameters_cov_var_matrix[1, 1]))}) dB/cm')

print(f'z_offset = {fit_parameters[2]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum' )
print(f'interaction length = {1134-fit_parameters[2]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum')
print(f'a = {fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum')
print('Mean square error:', mean_squared_error)
print(confidence_bounds_fit)


fit_y_cumsum = np.cumsum(fit_y)

data = np.convolve(fit_y,np.ones(200,dtype=int),'valid')
fit_x_ = fit_x[:len(fit_x)-199]
print('Averaging distance',mum_pr_pixel*50)

fit_parameters, fit_parameters_cov_var_matrix, infodict,mesg, ier,  = curve_fit(sfg_model_off_set, fit_x_, data, p0=[0,0,0], full_output=True)
print("Fit Parameters", fit_parameters)
fit = sfg_model_off_set(fit_x_, fit_parameters[0], fit_parameters[1], fit_parameters[2])



#fig, ax = plt.subplots(figsize=(8, 4))
#ax2 = ax.twinx()

#ax2.plot(fit_x, fit_y,'b-', alpha=0.2)
#ax.plot(fit_x_, data,'k-')
#ax.plot(fit_x_, fit,'r--')

#plt.xlabel(r'Propagation length [µm]')
#ax2.set_ylabel(r'Mean intensity [a.u.]')
#ax.set_ylabel(r'Cumulated intensity [a.u.]')
#ax.set_xlim([0, 1134])
#ax2.set_xlim([0, 1134])
#ax.set_ylim([0, 800])
#ax2.set_ylim([0, 20])

#plt.tight_layout()
#plt.savefig('Figures/cumsum_L_sq.png', transparent=True)
#plt.show()

print("Variance-Covariance Matrix Fit Parameters:", fit_parameters_cov_var_matrix)
print(
    f'a={fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[0, 0])}, b={fit_parameters[1]} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1])}')
print(f"alpha = {fit_parameters[1] * 1e4} +- {np.sqrt(fit_parameters_cov_var_matrix[1, 1]) * 1e4} 1/m")
print(
    f'alpha_dB = {pr_mum_to_dB_pr_cm(fit_parameters[1])} ({pr_mum_to_dB_pr_cm(fit_parameters[1] + np.sqrt(fit_parameters_cov_var_matrix[1, 1]))} {pr_mum_to_dB_pr_cm(fit_parameters[1] - np.sqrt(fit_parameters_cov_var_matrix[1, 1]))}) dB/cm')

print(f'z_offset = {fit_parameters[2]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum' )
print(f'interaction length = {1134-fit_parameters[2]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum')
print(f'a = {fit_parameters[0]} +- {np.sqrt(fit_parameters_cov_var_matrix[2, 2])} mum')

residuals = data - fit
ss_res = np.sum(residuals ** 2)

ss_tot = np.sum((data - np.mean(data)) ** 2)
r_squared = 1 - (ss_res / ss_tot)
print('R^2 = ', r_squared)
