# -*- coding: utf-8 -*-
#%% Demo for single-pixel imaging using Hadamard patterns as sensing basis
# Loads an object, generates the sensing patterns (Hadamard), 
# does the measurements (with and without noise), and recovers the image.

#%% Import libraries
from matplotlib import pyplot as plt
import numpy as np
# Generate hadamard matrices
from scipy.linalg import hadamard
# Working with images
from skimage.transform import resize
from PIL import Image

#%% Define useful functions
def noisify(signal: np.ndarray, end_snr: float) -> (np.ndarray, np.ndarray):
    '''
    Add white gaussian noise to a signal so it ends with end_snr 
    signal-to-noise ratio.
    More info at: https://en.wikipedia.org/wiki/Signal-to-noise_ratio#Decibels
    
    Parameters
    ----------
    signal : np.ndarray
        Input signal
    end_snr : float
        Desired SNR.
    Returns
    -------
    noisy_signal : np.ndarray
        Signal with added noise.
    noise : np.ndarray
        Noise added to the original signal.
    '''
    # Calculate signal average (~power)
    signal_avg = np.mean(signal)
    # Convert to dB
    signal_avg_db = 10 * np.log10(signal_avg)
    # Calculate noise power in dB, using objective SNR
    # SNR = P_signal(in dB) - P_noise(in dB)
    noise_avg_db = signal_avg_db - end_snr
    # Convert to noise average (~power)
    noise_avg = 10**(noise_avg_db/10)
    # Build noise with desired power
    noise = np.random.normal(0, np.sqrt(noise_avg), signal.size)
    # Build additive noise (shift to positive-only values)
    noise = noise + np.abs(np.min(noise))
    # Add noise to signal
    noisy_signal = signal + noise
    
    return noisy_signal, noise

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
Hplus = (H + 1) / 2       # H+ Hadamard matrix (1s and 0s)
Hminus = (1 - H) / 2      # H- Hadamard matrix (0s and 1s)

#%% Generate measurements simulating H+ and H- 
#   (as if patterns were generated on a DMD)
Mplus = Hplus @ test_obj.flatten() # Project H+ patterns, store intensity
Mminus = Hminus @ test_obj.flatten() # Project H- patterns, store intensity
M = Mplus - Mminus # Substract values (H+ - H-)

# Generate measurements with noise
noise_level = 2 #width (std) of the noise distribution (Gaussian)
# Generate noises (random number using a Gaussian distribution)
noise_plus = np.random.normal(np.mean(Mplus),noise_level,Mplus.size)
noise_minus = np.random.normal(np.mean(Mminus),noise_level,Mminus.size)
# Generate measurements from a noisy object
desired_SNR = 20 # SNR desired for the object
# Generate noisy object (adding white gaussian noise)
test_obj_noisy, noise = noisify(test_obj.flatten(), desired_SNR)
# Add noise to the true coefficients
Mplus_noisy = Hplus @ test_obj_noisy # Project H+
Mminus_noisy = Hminus @ test_obj_noisy # Project H-
M_noisy = Mplus_noisy - Mminus_noisy # Substract values (H+ - H-)

#%% Recover objects
# Inversion from measurements (solve the eq. systems with/without noise)
recovery = np.linalg.solve(H, M)
recovery_noise = np.linalg.solve(H, M_noisy)
# Reshape from vector into image
recovery = recovery.reshape((px, px))
recovery_noise = recovery_noise.reshape((px, px))

#%% Show the results
#Show recovery without noise
plt.figure()
plt.imshow(recovery, cmap = 'hot')
plt.axis('on')
plt.title('Recovered image without noise')
plt.colorbar()
plt.show()
#Show recovery with noise
plt.figure()
plt.imshow(recovery_noise, cmap = 'hot')
plt.axis('on')
plt.title('Recovered image with noise')
plt.colorbar()
plt.show()
