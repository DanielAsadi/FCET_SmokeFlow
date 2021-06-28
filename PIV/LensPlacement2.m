clear
clc
format long

% Known parameters:
Efl1_mm     = 6.35;
dbeam_mm    = 5.5;
Lmirror_mm  = 149.5;
Llens2_mm   = 50.8;
ht_mm       = 400;
hmirror_mm  = 250;


% Efl1_mm     = 19.1;
% dbeam_mm    = 5.5;
% Lmirror_mm  = 149.5;
% Llens2_mm   = 50.8;
% ht_mm       = 800;
% hmirror_mm  = 1000;

%Calculate the laser sheet fan angle.......................................
theta_deg   = 2* atand(dbeam_mm / (2 * Efl1_mm));

% Distance between cylinderical concave and cylinderical convex lenses.....
L1_mm       = ((Llens2_mm - dbeam_mm) * Efl1_mm) / dbeam_mm;

% Distance between cylinderical convex and the laser sheet mirror..........
L2_mm       = (Lmirror_mm - Llens2_mm) * Efl1_mm / dbeam_mm;

% Height of the mirror above the tunnel ceiling............................
Llaser_mm = dbeam_mm * ((hmirror_mm + L1_mm + L2_mm + ht_mm)/Efl1_mm + 1);  %= (Llaser_mm/dbeam_mm - 1) * Efl1_mm - L1_mm - L2_mm - ht_mm;

% Focal length of the cylinderical convex lens such that the laser sheet
% thickness is the lowest at the airfoil. 
Efl2_mm     = L2_mm + hmirror_mm + ht_mm;

% Fan angle for the cylinderical convex lens
theta2_deg = 2 * atand(dbeam_mm / (2 * (L2_mm + hmirror_mm)));