clear
clc
format long

% known parameters:

Efl1_mm     = 12.7;
dbeam_mm    = 5;
Lmirror_mm  = 149.23;
Llens2_mm   = 50.8;
ht_mm       = 400;
Llaser_mm   = 450; % Laser sheet width in the streamwise direction

%Calculate the laser sheet fan angle.......................................
theta_deg   = 2* atand(dbeam_mm / (2 * Efl1_mm));

% Distance between cylinderical concave and cylinderical convex lenses.....
L1_mm       = ((Llens2_mm - dbeam_mm) * Efl1_mm) / dbeam_mm;

% Distance between cylinderical convex and the laser sheet mirror..........
L2_mm       = (Lmirror_mm - Llens2_mm) * Efl1_mm / dbeam_mm;

% Height of the mirror above the tunnel ceiling............................
hmirror_mm  = (Llaser_mm/dbeam_mm - 1) * Efl1_mm - L1_mm - L2_mm - ht_mm;

% Focal length of the cylinderical convex lens such that the laser sheet
% thickness is the lowest at the airfoil. 
Efl2_mm     = L2_mm + hmirror_mm + ht_mm;

% Fan angle for the cylinderical convex lens
theta2_deg = 2 * atand(dbeam_mm / (2 * (L2_mm + hmirror_mm)));