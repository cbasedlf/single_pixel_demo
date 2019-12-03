% Demo for single-pixel imaging using Hadamard patterns as sensing basis
% Loads an object, generates the sensing patterns, does the measurements
% (with and without noise), and recovers the image.

close all
clearvars
clc

%% Path
addpath('.\objects');

%% Load object (64x64 pixels)
load('pacman_64px.mat');

%% Generate measurement patterns. Each row (column) is a Hadamard pattern
H = hadamard(64^2); %True Hadamard (+1 and -1 elements)
Hplus = (H+1)/2;    %H+ Hadamard (1s and 0s)
Hminus = (1-H)/2;   %H- Hadamard (0s and 1s)

%% Generate measurements simulating H+ and H- (as if were generated on a DMD)
Mplus = Hplus*obj(:); %Project H+
Mminus = Hminus*obj(:); %Project H-

%Generate measurements corrupted by noise
snr = 35; %signal-to-noise ratio (dB)
MplusNoise = awgn(Mplus,snr,'measured');
MminusNoise = awgn(Mminus,snr,'measured');

%Substract H+ and H- to generate true Hadamard coefficients
M = Mplus - Mminus;
MNoise = MplusNoise - MminusNoise;

%% Recover objects
recovery = H\M; %Inversion from measurements
recovery = reshape(recovery,[64 64]); %Reshape into image

recoveryNoise = H\MNoise; %Inversion from measurements
recoveryNoise = reshape(recoveryNoise,[64 64]); %Reshape into image

%% Show results
figure(1)
subplot(2,3,1)
imagesc(obj);axis square; title('object');
subplot(2,3,2)
imagesc(recovery);axis square; title('recovery (no noise)');
subplot(2,3,3)
imagesc(recoveryNoise);axis square; title('recovery (with noise)');
subplot(2,3,[4 5 6])
plot(M);
hold on
plot(MNoise);
title('measurements'); legend('no noise','with noise');
hold off