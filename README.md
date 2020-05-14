# single_pixel_demo
Demo for single-pixel imaging using Hadamard patterns as sensing basis
Loads an object, generates the sensing patterns (Hadamard), does the measurements 
(with and without noise), and recovers the image.

Patterns are supposed to be sent with a DMD, so we generate couples of patterns(H+ and H-), 
because Hadamard patterns are conformed of +1/-1 entries. The measurement is done in two steps, with
noise added.

Reconstruction is done by inversion.

Might add some compressive sensing in the future to do subsampling, though there are million examples out there of that
