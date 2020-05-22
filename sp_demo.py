# -*- coding: utf-8 -*-
#%% Demo for single-pixel imaging using Hadamard patterns as sensing basis
# Loads an object, generates the sensing patterns (Hadamard), 
# does the measurements (with and without noise), and recovers the image.

# %% import stuff
# plot stuff
from matplotlib import pyplot as plt 
# generate hadamard matrices
from scipy.linalg import hadamard    
# working with images stuff
from skimage.transform import resize
from PIL import Image
# doing math stuff
import numpy as np

# %%  Load image & generate object
# load image, convert to grayscale, store as array (matrix)
ground_obj = np.asarray(Image.open("./objects/ghost.png").convert('L')) 
# Choose new size (don't go higher than 128x128 or Hadamard will kill you)
px = 32
# Resize image to smaller size for simulation
test_obj = resize(ground_obj,(px,px))

#%% Generate measurement patterns using a Hadamard matrix. 
## Each row is a 2D pattern (after reshaping)
H = hadamard(px**2)   # Complete Hadamard matrix (+1s and -1s)
Hplus = (H+1)/2       # H+ Hadamard matrix (1s and 0s)
Hminus = (1-H)/2      # H- Hadamard matrix (0s and 1s)

#%% Generate measurements simulating H+ and H- 
## (as if patterns were generated on a DMD)
Mplus = Hplus@test_obj.flatten()    #Project H+ patterns, store intensity
Mminus = Hminus@test_obj.flatten()  #Project H- patterns, store intensity
M = Mplus - Mminus                  #Substract values (H+ - H-)

# Generate measurements with noise
noise_level = 2 #width (std) of the noise distribution (Gaussian)
# Generate noises (random number using a Gaussian distribution)
noise_plus = np.random.normal(np.mean(Mplus),noise_level,Mplus.size)
noise_minus = np.random.normal(np.mean(Mminus),noise_level,Mminus.size)
# Add noise to the true coefficients
Mplus_noise = Mplus + noise_plus        #Project H+
Mminus_noise = Mminus + noise_minus     #Project H-
M_noise = Mplus_noise - Mminus_noise    #Substract values (H+ - H-)

#%% Recover objects
# Inversion from measurements (solve the eq. systems with/without noise)
recovery = np.linalg.solve(H,M)
recovery_noise = np.linalg.solve(H,M_noise)
# Reshape from vector into image           
recovery = recovery.reshape((px,px));
recovery_noise = recovery_noise.reshape((px,px));

#%% Show the results
#Show recovery without noise
plt.figure()
plt.imshow(recovery,cmap='hot')
plt.axis('on')
plt.title('Recovered image without noise')
plt.colorbar()
plt.show()
#Show recovery with noise
plt.figure()
plt.imshow(recovery_noise,cmap='hot')
plt.axis('on')
plt.title('Recovered image with noise')
plt.colorbar()
plt.show()
