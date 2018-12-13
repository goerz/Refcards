#!/usr/bin/env python
"""Generate a tex file that renders to a Periodic Table of Elements"""
import re
from collections import defaultdict
from textwrap import dedent
from io import StringIO

import numpy as np
import pandas as pd
import click


DATA = pd.read_csv(
    StringIO(
        r'''
atomic number,symbol,name,atomic mass,electron configuration,phase,category,period,group,mass number,radioactive,valence electrons
1,H,Hydrogen,1.00794,1s1,gas,nonmetal,1,IA,1,False,1
2,He,Helium,4.002602,1s2,gas,noble gas,1,VIIIA,4,False,0
3,Li,Lithium,6.941,[He] 2s1,solid,alkali metal,2,IA,7,False,1
4,Be,Beryllium,9.012182,[He] 2s2,solid,alkaline earth metal,2,IIA,9,False,2
5,B,Boron,10.811,[He] 2s2 2p1,solid,metalloid,2,IIIA,11,False,3
6,C,Carbon,12.0107,[He] 2s2 2p2,solid,nonmetal,2,IVA,12,False,4
7,N,Nitrogen,14.0067,[He] 2s2 2p3,gas,nonmetal,2,VA,14,False,5
8,O,Oxygen,15.9994,[He] 2s2 2p4,gas,nonmetal,2,VIA,16,False,6
9,F,Fluorine,18.9984032,[He] 2s2 2p5,gas,halogen,2,VIIA,19,False,7
10,Ne,Neon,20.1797,[He] 2s2 2p6,gas,noble gas,2,VIIIA,20,False,0
11,Na,Sodium,22.98976928,[Ne] 3s1,solid,alkali metal,3,IA,23,False,1
12,Mg,Magne-sium,24.3050,[Ne] 3s2,solid,alkaline earth metal,3,IIA,24,False,2
13,Al,Aluminum,26.9815386,[Ne] 3s2 3p1,solid,post-transition metal,3,IIIA,27,False,3
14,Si,Silicon,28.0855,[Ne] 3s2 3p2,solid,metalloid,3,IVA,28,False,4
15,P,Phosphor-us,30.973762,[Ne] 3s2 3p3,solid,nonmetal,3,VA,31,False,5
16,S,Sulfur,32.065,[Ne] 3s2 3p4,solid,nonmetal,3,VIA,32,False,6
17,Cl,Chlorine,35.453,[Ne] 3s2 3p5,gas,halogen,3,VIIA,35,False,7
18,Ar,Argon,39.948,[Ne] 3s2 3p6,gas,noble gas,3,VIIIA,40,False,0
19,K,Potassium,39.0983,[Ar] 4s1,solid,alkali metal,4,IA,39,False,1
20,Ca,Calcium,40.078,[Ar] 4s2,solid,alkaline earth metal,4,IIA,40,False,2
21,Sc,Scandium,44.955912,[Ar] 3d1 4s2,solid,transition metal,4,IIIB,45,False,3
22,Ti,Titanium,47.867,[Ar] 3d2 4s2,solid,transition metal,4,IVB,48,False,4
23,V,Vanadium,50.9415,[Ar] 3d3 4s2,solid,transition metal,4,VB,51,False,5
24,Cr,Chromium,51.9961,[Ar] 3d5 4s1,solid,transition metal,4,VIB,52,False,6
25,Mn,Manga-nese,54.938045,[Ar] 3d5 4s2,solid,transition metal,4,VIIB,55,False,7
26,Fe,Iron,55.845,[Ar] 3d6 4s2,solid,transition metal,4,VIIIB,56,False,8
27,Co,Cobalt,58.933195,[Ar] 3d7 4s2,solid,transition metal,4,VIIIB,59,False,9
28,Ni,Nickel,58.6934,[Ar] 3d8 4s2,solid,transition metal,4,VIIIB,58,False,10
29,Cu,Copper,63.546,[Ar] 3d10 4s1,solid,transition metal,4,IB,63,False,11
30,Zn,Zinc,65.38,[Ar] 3d10 4s2,solid,transition metal,4,IIB,64,False,12
31,Ga,Gallium,69.723,[Ar] 3d10 4s2 4p1,solid,post-transition metal,4,IIIA,69,False,3
32,Ge,German-ium,72.64,[Ar] 3d10 4s2 4p2,solid,metalloid,4,IVA,74,False,4
33,As,Arsenic,74.92160,[Ar] 3d10 4s2 4p3,solid,metalloid,4,VA,75,False,5
34,Se,Selenium,78.96,[Ar] 3d10 4s2 4p4,solid,nonmetal,4,VIA,80,False,6
35,Br,Bromine,79.904,[Ar] 3d10 4s2 4p5,liquid,halogen,4,VIIA,79,False,7
36,Kr,Krypton,83.798,[Ar] 3d10 4s2 4p6,gas,noble gas,4,VIIIA,84,False,0
37,Rb,Rubidium,85.4678,[Kr] 5s1,solid,alkali metal,5,IA,85,False,1
38,Sr,Strontium,87.62,[Kr] 5s2,solid,alkaline earth metal,5,IIA,88,False,2
39,Y,Yttrium,88.90585,[Kr] 4d1 5s2,solid,transition metal,5,IIIB,89,False,3
40,Zr,Zirconium,91.224,[Kr] 4d2 5s2,solid,transition metal,5,IVB,90,False,4
41,Nb,Niobium,92.90638,[Kr] 4d4 5s1,solid,transition metal,5,VB,93,False,5
42,Mo,Molybde-num,95.96,[Kr] 4d5 5s1,solid,transition metal,5,VIB,98,False,6
43,Tc,Technetium,98,[Kr] 4d5 5s2,solid,transition metal,5,VIIB,98,True,7
44,Ru,Ruthenium,101.07,[Kr] 4d7 5s1,solid,transition metal,5,VIIIB,102,False,8
45,Rh,Rhodium,102.90550,[Kr] 4d8 5s1,solid,transition metal,5,VIIIB,103,False,9
46,Pd,Palladium,106.42,[Kr] 4d10,solid,transition metal,5,VIIIB,106,False,12
47,Ag,Silver,107.8682,[Kr] 4d10 5s1,solid,transition metal,5,IB,107,False,11
48,Cd,Cadmium,112.411,[Kr] 4d10 5s2,solid,transition metal,5,IIB,114,False,12
49,In,Indium,114.818,[Kr] 4d10 5s2 5p1,solid,post-transition metal,5,IIIA,115,False,3
50,Sn,Tin,118.710,[Kr] 4d10 5s2 5p2,solid,post-transition metal,5,IVA,120,False,4
51,Sb,Antimony,121.760,[Kr] 4d10 5s2 5p3,solid,metalloid,5,VA,121,False,5
52,Te,Tellurium,127.60,[Kr] 4d10 5s2 5p4,solid,metalloid,5,VIA,130,False,6
53,I,Iodine,126.90447,[Kr] 4d10 5s2 5p5,solid,halogen,5,VIIA,127,False,7
54,Xe,Xenon,131.293,[Kr] 4d10 5s2 5p6,gas,noble gas,5,VIIIA,132,False,0
55,Cs,Cesium,132.9054519,[Xe] 6s1,solid,alkali metal,6,IA,133,False,1
56,Ba,Barium,137.327,[Xe] 6s2,solid,alkaline earth metal,6,IIA,138,False,2
57,La,Lanthanum,138.90547,[Xe] 5d1 6s2,solid,lanthanide,6,,139,False,2
58,Ce,Cerium,140.116,[Xe] 4f1 5d1 6s2,solid,lanthanide,6,,140,False,2
59,Pr,Praseo-dymium,140.90765,[Xe] 4f3 6s2,solid,lanthanide,6,,141,False,2
60,Nd,Neo-dymium,144.242,[Xe] 4f4 6s2,solid,lanthanide,6,,142,False,2
61,Pm,Prome-thium,145,[Xe] 4f5 6s2,solid,lanthanide,6,,145,True,2
62,Sm,Samarium,150.36,[Xe] 4f6 6s2,solid,lanthanide,6,,152,False,2
63,Eu,Europium,151.964,[Xe] 4f7 6s2,solid,lanthanide,6,,153,False,2
64,Gd,Gadolinium,157.25,[Xe] 4f7 5d1 6s2,solid,lanthanide,6,,158,False,2
65,Tb,Terbium,158.92535,[Xe] 4f9 6s2,solid,lanthanide,6,,159,False,2
66,Dy,Dyspro-sium,162.500,[Xe] 4f10 6s2,solid,lanthanide,6,,164,False,2
67,Ho,Holmium,164.93032,[Xe] 4f11 6s2,solid,lanthanide,6,,165,False,2
68,Er,Erbium,167.259,[Xe] 4f12 6s2,solid,lanthanide,6,,166,False,2
69,Tm,Thulium,168.93421,[Xe] 4f13 6s2,solid,lanthanide,6,,169,False,2
70,Yb,Ytterbium,173.054,[Xe] 4f14 6s2,solid,lanthanide,6,,174,False,2
71,Lu,Lutetium,174.9668,[Xe] 4f14 5d1 6s2,solid,transition metal,6,IIIB,175,False,3
72,Hf,Hafnium,178.49,[Xe] 4f14 5d2 6s2,solid,transition metal,6,IVB,180,False,4
73,Ta,Tantalum,180.94788,[Xe] 4f14 5d3 6s2,solid,transition metal,6,VB,181,False,5
74,W,Tungsten,183.84,[Xe] 4f14 5d4 6s2,solid,transition metal,6,VIB,184,False,6
75,Re,Rhenium,186.207,[Xe] 4f14 5d5 6s2,solid,transition metal,6,VIIB,187,False,7
76,Os,Osmium,190.23,[Xe] 4f14 5d6 6s2,solid,transition metal,6,VIIIB,192,False,8
77,Ir,Iridium,192.217,[Xe] 4f14 5d7 6s2,solid,transition metal,6,VIIIB,193,False,9
78,Pt,Platinum,195.084,[Xe] 4f14 5d9 6s1,solid,transition metal,6,VIIIB,195,False,10
79,Au,Gold,196.966569,[Xe] 4f14 5d10 6s1,solid,transition metal,6,IB,197,False,11
80,Hg,Mercury,200.59,[Xe] 4f14 5d10 6s2,liquid,transition metal,6,IIB,202,False,12
81,Tl,Thallium,204.3833,[Xe] 4f14 5d10 6s2 6p1,solid,post-transition metal,6,IIIA,205,False,3
82,Pb,Lead,207.2,[Xe] 4f14 5d10 6s2 6p2,solid,post-transition metal,6,IVA,208,False,4
83,Bi,Bismuth,208.98040,[Xe] 4f14 5d10 6s2 6p3,solid,post-transition metal,6,VA,209,False,5
84,Po,Polonium,,[Xe] 4f14 5d10 6s2 6p4,solid,metalloid,6,VIA,209,True,6
85,At,Astatine,,[Xe] 4f14 5d10 6s2 6p5,solid,halogen,6,VIIA,210,True,7
86,Rn,Radon,,[Xe] 4f14 5d10 6s2 6p6,gas,noble gas,6,VIIIA,222,True,0
87,Fr,Francium,,[Rn] 7s1,solid,alkali metal,7,IA,223,True,1
88,Ra,Radium,,[Rn] 7s2,solid,alkaline earth metal,7,IIA,226,True,2
89,Ac,Actinium,,[Rn] 6d1 7s2,solid,actinide,7,,227,True,2
90,Th,Thorium,232.03806,[Rn] 6d2 7s2,solid,actinide,7,,232,True,2
91,Pa,Protact-inium,231.03588,[Rn] 5f2 6d1 7s2,solid,actinide,7,,231,True,2
92,U,Uranium,238.02891,[Rn] 5f3 6d1 7s2,solid,actinide,7,,238,True,2
93,Np,Neptunium,,[Rn] 5f4 6d1 7s2,solid,actinide,7,,237,True,2
94,Pu,Plutonium,,[Rn] 5f6 7s2,solid,actinide,7,,244,True,2
95,Am,Americium,,[Rn] 5f7 7s2,solid,actinide,7,,243,True,2
96,Cm,Curium,,[Rn] 5f7 6d1 7s2,solid,actinide,7,,247,True,2
97,Bk,Berkelium,,[Rn] 5f9 7s2,solid,actinide,7,,247,True,2
98,Cf,Californ-ium,,[Rn] 5f10 7s2,solid,actinide,7,,251,True,2
99,Es,Einstein-ium,,[Rn] 5f11 7s2,solid,actinide,7,,252,True,2
100,Fm,Fermium,,[Rn] 5f12 7s2,,actinide,7,,257,True,2
101,Md,Mendelev-ium,,[Rn] 5f13 7s2,,actinide,7,,258,True,2
102,No,Nobelium,,[Rn] 5f14 7s2,,actinide,7,,259,True,2
103,Lr,Lawrenc-ium,,[Rn] 5f14 7s2 7p1,,transition metal,7,IIIB,262,True,3
104,Rf,Ruther-fordium,,[Rn] 5f14 6d2 7s2,,transition metal,7,IVB,261,True,4
105,Db,Dubnium,,[Rn] 5f14 6d3 7s2,,transition metal,7,VB,262,True,5
106,Sg,Seaborg-ium,,[Rn] 5f14 6d4 7s2,,transition metal,7,VIB,266,True,6
107,Bh,Bohrium,,[Rn] 5f14 6d5 7s2,,transition metal,7,VIIB,264,True,7
108,Hs,Hassium,,[Rn] 5f14 6d6 7s2,,transition metal,7,VIIIB,269,True,8
109,Mt,Meitnerium,,[Rn] 5f14 6d7 7s2,,transition metal,7,VIIIB,268,True,9
110,Ds,Darmstadt-ium,,[Rn] 5f14 6d9 7s1,,transition metal,7,VIIIB,,True,10
111,Rg,Roentgen-ium,,[Rn] 5f14 6d10 7s1,,transition metal,7,IB,,True,11
112,Cn,Copernic-ium,,[Rn] 5f14 6d10 7s2,,transition metal,7,IIB,,True,12
113,Nh,Nihonium,,[Rn] 5f14 6d10 7s2 7p1,,unknown,7,IIIA,,True,3
114,Fl,Flerovium,,[Rn] 5f14 6d10 7s2 7p2,,unknown,7,IVA,,True,4
115,Mc,Moscov-ium,,[Rn] 5f14 6d10 7s2 7p3,,unknown,7,VA,,True,5
116,Lv,Livermor-ium,,[Rn] 5f14 6d10 7s2 7p4,,unknown,7,VIA,,True,6
117,Ts,Tennessine,,[Rn] 5f14 6d10 7s2 7p5,,unknown,7,VIIA,,True,7
118,Og,Oganesson,,[Rn] 5f14 6d10 7s2 7p6,,unknown,7,VIIIA,,True,0
'''
    ),
    index_col=0,
    dtype=str,
)

SPIN_DATA = pd.read_csv(
    StringIO(
        r'''
%==============================================================
% EasySpin nuclear isotope database
% http://easyspin.org/documentation/isotopetable.html
%==============================================================
% Contains all naturally occurring nuclei plus selected
% radioactive ones, which are marked by * in column 3.
% Line syntax:
%  Column 1: #protons
%  Column 2: #nucleons
%  Column 3: radioactive *, stable -
%  Column 4: symbol
%  Column 5: name
%  Column 6: spin quantum number
%  Column 7: nuclear g factor gn
%  Column 8: natural abundance, in percent
%  Column 9: electric quadrupole moment, in barn (10^-28 m^2)
%            NaN indicates 'not measured'
%
% Nuclear magnetic moments are taken from
%   N.Stone
%   Table of Nuclear Magnetic Dipole and Electric Quadrupole Moments
%   International Atomic Energy Agency, INDC(NDS)-0658, February 2014
%     (https://www-nds.iaea.org/publications/indc/indc-nds-0658.pdf)
%  (Typo for Rh-103: Moment is factor of 10 too large)
% 237Np, 239Pu, 243Am data from
%   N.E.Holden
%   Table of the Isotopes
%   CRC Handbook of Physics and Chemistry, section 11-2
%     (http://www.hbcponline.com//articles/11_02_92.pdf)
%
% Nuclear quadrupole moments are taken from
%   N.Stone
%   Table of Nuclear Quadrupole Moments
%   International Atomic Energy Agency, INDC(NDS)-650, December 2013
%     (https://www-nds.iaea.org/publications/indc/indc-nds-0650.pdf)
%  (Typo for Ac-227: Sign should be +)
% See also
%   P.Pyykk�
%   Year-2008 Nuclear Quadrupole Moments
%   Mol.Phys. 106(16-18), 1965-1974 (2008)
%     (http://dx.doi.org/10.1080/00268970802018367)
%   N.E.Holden
%   Table of the Isotopes
%   CRC Handbook of Physics and Chemistry, section 11-2
%     (http://www.hbcponline.com//articles/11_02_92.pdf)
%--------------------------------------------------------------
% first period
%--------------------------------------------------------------
 1   1 - H   hydrogen       0.5 +5.58569468 99.9885    0
 1   2 - H   hydrogen       1.0 +0.8574382   0.0115   +0.00286
 1   3 * H   hydrogen       0.5 +5.95799369  0.0       0
 2   3 - He  helium         0.5 -4.25499544  0.000137  0
 2   4 - He  helium         0.0  0.0        99.999863  0
%--------------------------------------------------------------
% second period
%--------------------------------------------------------------
 3   6 - Li  lithium        1.0 +0.8220473   7.59     -0.000806
 3   7 - Li  lithium        1.5 +2.170951   92.41     -0.0400
 4   9 - Be  beryllium      1.5 -0.78495   100.0      +0.0529
 5  10 - B   boron          3.0 +0.600215   19.9      +0.0845
 5  11 - B   boron          1.5 +1.7924326  80.1      +0.04059
 6  12 - C   carbon         0.0  0.0        98.93      0
 6  13 - C   carbon         0.5 +1.4048236   1.07      0
 6  14 * C   carbon         0.0  0.0         0.0       0
 7  14 - N   nitrogen       1.0 +0.40376100 99.632    +0.02044
 7  15 - N   nitrogen       0.5 -0.56637768  0.368     0
 8  16 - O   oxygen         0.0  0.0        99.757     0
 8  17 - O   oxygen         2.5 -0.757516    0.038    -0.0256
 8  18 * O   oxygen         0.0  0.0         0.205     0
 9  19 - F   fluorine       0.5 +5.257736  100.0       0
10  20 - Ne  neon           0.0  0.0        90.48      0
10  21 - Ne  neon           1.5 -0.441198    0.27     +0.102
10  22 - Ne  neon           0.0  0.0         9.25      0
%--------------------------------------------------------------
% third period
%--------------------------------------------------------------
11  22 * Na  sodium         3.0 +0.582       0.0      +0.180
11  23 - Na  sodium         1.5 +1.478348  100.0      +0.104
12  24 - Mg  magnesium      0.0  0.0        78.99      0
12  25 - Mg  magnesium      2.5 -0.34218    10.00     +0.199
12  26 - Mg  magnesium      0.0  0.0        11.01      0
13  27 - Al  aluminium      2.5 +1.4566028 100.0      +0.1466
14  28 - Si  silicon        0.0  0.0        92.2297    0
14  29 - Si  silicon        0.5 -1.11058     4.6832    0
14  30 - Si  silicon        0.0  0.0         3.0872    0
15  31 - P   phosphorus     0.5 +2.26320   100.0       0
16  32 - S   sulfur         0.0  0.0        94.93      0
16  33 - S   sulfur         1.5 +0.429214    0.76     -0.0678
16  34 - S   sulfur         0.0  0.0         4.29      0
16  36 - S   sulfur         0.0  0.0         0.02      0
17  35 - Cl  chlorine       1.5 +0.5479162  75.78     -0.0817
17  36 * Cl  chlorine       2.0 +0.642735    0.0      -0.0178
17  37 - Cl  chlorine       1.5 +0.4560824  24.22     -0.0644
18  36 - Ar  argon          0.0  0.0         0.3365    0
18  38 - Ar  argon          0.0  0.0         0.0632    0
18  39 * Ar  argon          3.5 -0.4537      0.0      -0.12
18  40 - Ar  argon          0.0  0.0        99.6003    0
%--------------------------------------------------------------
% fourth period, first row transition metals
%--------------------------------------------------------------
19  39 - K   potassium      1.5 +0.26098    93.2581   +0.0585
19  40 - K   potassium      4.0 -0.324525    0.0117   -0.073
19  41 - K   potassium      1.5 +0.1432467   6.7302   +0.0711
20  40 - Ca  calcium        0.0  0.0         96.941    0
20  41 * Ca  calcium        3.5 -0.4556517   0.0      -0.0665
20  42 - Ca  calcium        0.0  0.0         0.647     0
20  43 - Ca  calcium        3.5 -0.37637     0.135    -0.0408
20  44 - Ca  calcium        0.0  0.0         2.086     0
20  46 - Ca  calcium        0.0  0.0         0.004     0
20  48 - Ca  calcium        0.0  0.0         0.187     0
21  45 - Sc  scandium       3.5 +1.35899   100.0      -0.220
22  46 - Ti  titanium       0.0  0.0         8.25      0
22  47 - Ti  titanium       2.5 -0.31539     7.44     +0.302
22  48 - Ti  titanium       0.0  0.0        73.72      0
22  49 - Ti  titanium       3.5 -0.315477    5.41     +0.247
22  50 - Ti  titanium       0.0  0.0         5.18      0
23  50 - V   vanadium       6.0 +0.5576148   0.25     +0.21
23  51 - V   vanadium       3.5 +1.47106    99.75     -0.043
24  50 - Cr  chromium       0.0  0.0         4.345     0
24  52 - Cr  chromium       0.0  0.0        83.789     0
24  53 - Cr  chromium       1.5 -0.31636     9.501    -0.15
24  54 - Cr  chromium       0.0  0.0         2.365     0
25  53 * Mn  manganese      3.5 +1.439       0.0      +0.17
25  55 - Mn  manganese      2.5 +1.3813    100.0      +0.330
26  54 - Fe  iron           0.0  0.0         5.845     0
26  56 - Fe  iron           0.0  0.0        91.754     0
26  57 - Fe  iron           0.5 +0.1809      2.119     0
26  58 - Fe  iron           0.0  0.0         0.282     0
27  59 - Co  cobalt         3.5 +1.322     100.0      +0.42
27  60 * Co  cobalt         5.0 +0.7598      0.0      +0.46
28  58 - Ni  nickel         0.0  0.0        68.0769    0
28  60 - Ni  nickel         0.0  0.0        26.2231    0
28  61 - Ni  nickel         1.5 -0.50001     1.1399   +0.162
28  62 - Ni  nickel         0.0  0.0         3.6345    0
28  64 - Ni  nickel         0.0  0.0         0.9256    0
29  63 - Cu  copper         1.5 +1.4824     69.17     -0.220
29  65 - Cu  copper         1.5 +1.5878     30.83     -0.204
30  64 - Zn  zinc           0.0  0.0        48.63      0
30  66 - Zn  zinc           0.0  0.0        27.90      0
30  67 - Zn  zinc           2.5 +0.350192    4.10     +0.150
30  68 - Zn  zinc           0.0  0.0        18.75      0
30  70 - Zn  zinc           0.0  0.0         0.62      0
31  69 - Ga  gallium        1.5 +1.34439    60.108    +0.171
31  71 - Ga  gallium        1.5 +1.70818    39.892    +0.107
32  70 - Ge  germanium      0.0  0.0        20.84      0
32  72 - Ge  germanium      0.0  0.0        27.54      0
32  73 - Ge  germanium      4.5 -0.1954373   7.73     -0.19
32  74 - Ge  germanium      0.0  0.0        36.28      0
32  76 - Ge  germanium      0.0  0.0         7.61      0
33  75 - As  arsenic        1.5 +0.95965   100.0      +0.314
34  74 - Se  selenium       0.0  0.0         0.89      0
34  76 - Se  selenium       0.0  0.0         9.37      0
34  77 - Se  selenium       0.5 +1.07008     7.63      0
34  78 - Se  selenium       0.0  0.0        23.77      0
34  79 * Se  selenium       3.5 -0.29        0.0      +0.8
34  80 - Se  selenium       0.0  0.0        49.61      0
34  82 - Se  selenium       0.0  0.0         8.73      0
35  79 - Br  bromine        1.5 +1.404267   50.69     +0.313
35  81 - Br  bromine        1.5 +1.513708   49.31     +0.262
36  78 - Kr  krypton        0.0  0.0         0.35      0
36  80 - Kr  krypton        0.0  0.0         2.28      0
36  82 - Kr  krypton        0.0  0.0        11.58      0
36  83 - Kr  krypton        4.5 -0.215704   11.49     +0.259
36  84 - Kr  krypton        0.0  0.0        57.00      0
36  85 * Kr  krypton        4.5 -0.2233      0.0      +0.443
36  86 - Kr  krypton        0.0  0.0        17.30      0
%--------------------------------------------------------------
% fifth period, second row transition metals
%--------------------------------------------------------------
37  85 - Rb  rubidium       2.5 +0.541192   72.17     +0.276
37  87 - Rb  rubidium       1.5 +1.83421    27.83     +0.1335
38  84 - Sr  strontium      0.0  0.0         0.56      0
38  86 - Sr  strontium      0.0  0.0         9.86      0
38  87 - Sr  strontium      4.5 -0.24284     7.00     +0.305
38  88 - Sr  strontium      0.0  0.0        82.58      0
39  89 - Y   yttrium        0.5 -0.2748308 100.0       0
40  90 - Zr  zirconium      0.0  0.0        51.45      0
40  91 - Zr  zirconium      2.5 -0.521448   11.22     -0.176
40  92 - Zr  zirconium      0.0  0.0        17.15      0
40  94 - Zr  zirconium      0.0  0.0        17.38      0
40  96 - Zr  zirconium      0.0  0.0         2.80      0
41  93 - Nb  niobium        4.5 +1.3712    100.0      -0.32
42  92 - Mo  molybdenum     0.0  0.0        14.84      0
42  94 - Mo  molybdenum     0.0  0.0         9.25      0
42  95 - Mo  molybdenum     2.5 -0.3657     15.92     -0.022
42  96 - Mo  molybdenum     0.0  0.0        16.68      0
42  97 - Mo  molybdenum     2.5 -0.3734      9.55     +0.255
42  98 - Mo  molybdenum     0.0  0.0        24.13      0
42 100 - Mo  molybdenum     0.0  0.0         9.63      0
43  99 * Tc  technetium     4.5 +1.2632      0.0      -0.129
44  96 - Ru  ruthenium      0.0  0.0         5.54      0
44  98 - Ru  ruthenium      0.0  0.0         1.87      0
44  99 - Ru  ruthenium      2.5 -0.256      12.76     +0.079
44 100 - Ru  ruthenium      0.0  0.0        12.60      0
44 101 - Ru  ruthenium      2.5 -0.288      17.06     +0.46
44 102 - Ru  ruthenium      0.0  0.0        31.55      0
44 104 - Ru  ruthenium      0.0  0.0        18.62      0
45 103 - Rh  rhodium        0.5 -0.1768    100.0       0
46 102 - Pd  palladium      0.0  0.0         1.02      0
46 104 - Pd  palladium      0.0  0.0        11.14      0
46 105 - Pd  palladium      2.5 -0.257      22.33     +0.660
46 106 - Pd  palladium      0.0  0.0        27.33      0
46 108 - Pd  palladium      0.0  0.0        26.46      0
46 110 - Pd  palladium      0.0  0.0        11.72      0
47 107 - Ag  silver         0.5 -0.22714    51.839     0
47 109 - Ag  silver         0.5 -0.26112    48.161     0
48 106 - Cd  cadmium        0.0  0.0         1.25      0
48 108 - Cd  cadmium        0.0  0.0         0.89      0
48 110 - Cd  cadmium        0.0  0.0        12.49      0
48 111 - Cd  cadmium        0.5 -1.18977    12.80      0
48 112 - Cd  cadmium        0.0  0.0        24.13      0
48 113 - Cd  cadmium        0.5 -1.244602   12.22      0
48 114 - Cd  cadmium        0.0  0.0        28.73      0
48 116 - Cd  cadmium        0.0  0.0         7.49      0
49 113 - In  indium         4.5 +1.2286      4.29     +0.759
49 115 - In  indium         4.5 +1.2313     95.71     +0.770
50 112 - Sn  tin            0.0  0.0         0.97      0
50 114 - Sn  tin            0.0  0.0         0.66      0
50 115 - Sn  tin            0.5 -1.8377      0.34      0
50 116 - Sn  tin            0.0  0.0        14.54      0
50 117 - Sn  tin            0.5 -2.00208     7.68      0
50 118 - Sn  tin            0.0  0.0        24.22      0
50 119 - Sn  tin            0.5 -2.09456     8.59      0
50 120 - Sn  tin            0.0  0.0        32.58      0
50 122 - Sn  tin            0.0  0.0         4.63      0
50 124 - Sn  tin            0.0  0.0         5.79      0
51 121 - Sb  antimony       2.5 +1.3454     57.21     -0.543
51 123 - Sb  antimony       3.5 +0.72851    42.79     -0.692
51 125 * Sb  antimony       3.5 +0.751       0.0       NaN
52 120 - Te  tellurium      0.0  0.0         0.09      0
52 122 - Te  tellurium      0.0  0.0         2.55      0
52 123 - Te  tellurium      0.5 -1.473896    0.89      0
52 124 - Te  tellurium      0.0  0.0         4.74      0
52 125 - Te  tellurium      0.5 -1.7770102   7.07      0
52 126 - Te  tellurium      0.0  0.0        18.84      0
52 128 - Te  tellurium      0.0  0.0        31.74      0
52 130 - Te  tellurium      0.0  0.0        34.08      0
53 127 - I   iodine         2.5 +1.12531   100.0      -0.696
53 129 * I   iodine         3.5 +0.74886     0.0      -0.488
54 124 - Xe  xenon          0.0  0.0         0.09      0
54 126 - Xe  xenon          0.0  0.0         0.09      0
54 128 - Xe  xenon          0.0  0.0         1.92      0
54 129 - Xe  xenon          0.5 -1.55595    26.44      0
54 130 - Xe  xenon          0.0  0.0         4.08      0
54 131 - Xe  xenon          1.5 +0.461      21.18     -0.114
54 132 - Xe  xenon          0.0  0.0        26.89      0
54 134 - Xe  xenon          0.0  0.0        10.44      0
54 136 - Xe  xenon          0.0  0.0         8.87      0
%--------------------------------------------------------------
% sixth period, third row transition metals, rare earths
%--------------------------------------------------------------
55 133 - Cs  caesium        3.5 +0.7377214 100.0      -0.00343
55 134 * Cs  caesium        4.0 +0.74843     0.0      +0.37
55 135 * Cs  caesium        3.5 +0.78069     0.0      +0.048
55 137 * Cs  caesium        3.5 +0.81466     0.0      +0.048
56 130 - Ba  barium         0.0  0.0         0.106     0
56 132 - Ba  barium         0.0  0.0         0.101     0
56 133 * Ba  barium         0.5 -1.5433      0.0       0
56 134 - Ba  barium         0.0  0.0         2.417     0
56 135 - Ba  barium         1.5 +0.55863     6.592    +0.160
56 136 - Ba  barium         0.0  0.0         7.854     0
56 137 - Ba  barium         1.5 +0.62491    11.232    +0.245
56 138 - Ba  barium         0.0  0.0        71.698     0
57 137 * La  lanthanum      3.5 +0.7714      0.0      +0.21
57 138 - La  lanthanum      5.0 +0.742729    0.090    +0.39
57 139 - La  lanthanum      3.5 +0.795156   99.910    +0.200
58 136 - Ce  cerium         0.0  0.0         0.185     0
58 138 - Ce  cerium         0.0  0.0         0.251     0
58 140 - Ce  cerium         0.0  0.0        88.450     0
58 142 - Ce  cerium         0.0  0.0        11.114     0
59 141 - Pr  praesodymium   2.5 +1.7102    100.0      -0.077
60 142 - Nd  neodymium      0.0  0.0        27.2       0
60 143 - Nd  neodymium      3.5 -0.3043     12.2      -0.61
60 144 - Nd  neodymium      0.0  0.0        23.8       0
60 145 - Nd  neodymium      3.5 -0.187       8.3      -0.314
60 146 - Nd  neodymium      0.0  0.0        17.2       0
60 148 - Nd  neodymium      0.0  0.0         5.7       0
60 150 - Nd  neodymium      0.0  0.0         5.6       0
61 147 * Pm  promethium     3.5 +0.737       0.0      +0.74
62 144 - Sm  samarium       0.0  0.0         3.07      0
62 147 - Sm  samarium       3.5 -0.232      14.99     -0.26
62 148 - Sm  samarium       0.0  0.0        11.24      0
62 149 - Sm  samarium       3.5 -0.1908     13.82     +0.078
62 150 - Sm  samarium       0.0  0.0         7.38      0
62 151 * Sm  samarium       2.5 +0.1444      0.0      +0.71
62 152 - Sm  samarium       0.0  0.0        26.75      0
62 154 - Sm  samarium       0.0  0.0        22.75      0
63 151 - Eu  europium       2.5 +1.3887     47.81     +0.903
63 152 * Eu  europium       3.0 -0.6467      0.0      +2.72
63 153 - Eu  europium       2.5 +0.6134     52.19     +2.41
63 154 * Eu  europium       3.0 -0.6683      0.0      +2.85
63 155 * Eu  europium       2.5 +0.608       0.0      +2.5
64 152 - Gd  gadolinium     0.0  0.0         0.20      0
64 154 - Gd  gadolinium     0.0  0.0         2.18      0
64 155 - Gd  gadolinium     1.5 -0.1715     14.80     +1.27
64 156 - Gd  gadolinium     0.0  0.0        20.47      0
64 157 - Gd  gadolinium     1.5 -0.2265     15.65     +1.35
64 158 - Gd  gadolinium     0.0  0.0        24.84      0
64 160 - Gd  gadolinium     0.0  0.0        21.86      0
65 157 * Tb  terbium        1.5 +1.34        0.0      +1.40
65 159 - Tb  terbium        1.5 +1.343     100.0      +1.432
65 160 * Tb  terbium        3.0 +0.5967      0.0      +3.85
66 156 - Dy  dysprosium     0.0  0.0         0.06      0
66 158 - Dy  dysprosium     0.0  0.0         0.10      0
66 160 - Dy  dysprosium     0.0  0.0         2.34      0
66 161 - Dy  dysprosium     2.5 -0.192      18.91     +2.51
66 162 - Dy  dysprosium     0.0  0.0        25.51      0
66 163 - Dy  dysprosium     2.5 +0.269      24.90     +2.65
66 164 - Dy  dysprosium     0.0  0.0        28.18      0
67 165 - Ho  holmium        3.5 +1.668     100.0      +3.58
68 162 - Er  erbium         0.0  0.0         0.14      0
68 164 - Er  erbium         0.0  0.0         1.61      0
68 166 - Er  erbium         0.0  0.0        33.61      0
68 167 - Er  erbium         3.5 -0.1611     22.93     +3.57
68 168 - Er  erbium         0.0  0.0        26.78      0
68 170 - Er  erbium         0.0  0.0        14.93      0
69 169 - Tm  thulium        0.5 -0.462     100.0       0
69 171 * Tm  thulium        0.5 -0.456       0.0       0
70 168 - Yb  ytterbium      0.0  0.0         0.13      0
70 170 - Yb  ytterbium      0.0  0.0         3.04      0
70 171 - Yb  ytterbium      0.5 +0.98734    14.28      0
70 172 - Yb  ytterbium      0.0  0.0        21.83      0
70 173 - Yb  ytterbium      2.5 -0.2592     16.13     +2.80
70 174 - Yb  ytterbium      0.0  0.0        31.83      0
70 176 - Yb  ytterbium      0.0  0.0        12.76      0
71 173 * Lu  lutetium       3.5 +0.6517      0.0      +3.53
71 174 * Lu  lutetium       1.0 +1.988       0.0      +0.773
71 175 - Lu  lutetium       3.5 +0.6378     97.41     +3.49
71 176 - Lu  lutetium       7.0 +0.4517      2.59     +4.92
72 174 - Hf  hafnium        0.0  0.0         0.16      0
72 176 - Hf  hafnium        0.0  0.0         5.26      0
72 177 - Hf  hafnium        3.5 +0.2267     18.60     +3.37
72 178 - Hf  hafnium        0.0  0.0        27.28      0
72 179 - Hf  hafnium        4.5 -0.1424     13.62     +3.79
72 180 - Hf  hafnium        0.0  0.0        35.08      0
73 180 - Ta  tantalum       9.0  0.5361      0.012    +4.80
73 181 - Ta  tantalum       3.5 +0.67729    99.988    +3.17
74 180 - W   tungsten       0.0  0.0         0.12      0
74 182 - W   tungsten       0.0  0.0        26.50      0
74 183 - W   tungsten       0.5 +0.2355695  14.31      0
74 184 - W   tungsten       0.0  0.0        30.64      0
74 186 - W   tungsten       0.0  0.0        28.43      0
75 185 - Re  rhenium        2.5 +1.2748     37.40     +2.18
75 187 - Re  rhenium        2.5 +1.2879     62.60     +2.07
76 184 - Os  osmium         0.0  0.0         0.02      0
76 186 - Os  osmium         0.0  0.0         1.59      0
76 187 - Os  osmium         0.5 +0.1293038   1.96      0
76 188 - Os  osmium         0.0  0.0        13.24      0
76 189 - Os  osmium         1.5 +0.439956   16.15     +0.86
76 190 - Os  osmium         0.0  0.0        26.26      0
76 192 - Os  osmium         0.0  0.0        40.78      0
77 191 - Ir  iridium        1.5 +0.1005     37.3      +0.816
77 193 - Ir  iridium        1.5 +0.1091     62.7      +0.751
78 190 - Pt  platinum       0.0  0.0         0.014     0
78 192 - Pt  platinum       0.0  0.0         0.784     0
78 194 - Pt  platinum       0.0  0.0        32.967     0
78 195 - Pt  platinum       0.5 +1.2190     33.832     0
78 196 - Pt  platinum       0.0  0.0        25.242     0
78 198 - Pt  platinum       0.0  0.0         7.163     0
79 197 - Au  gold           1.5 +0.097164  100.0      +0.547
80 196 - Hg  mercury        0.0  0.0         0.15      0
80 198 - Hg  mercury        0.0  0.0         9.97      0
80 199 - Hg  mercury        0.5 +1.011771   16.87      0
80 200 - Hg  mercury        0.0  0.0        23.10      0
80 201 - Hg  mercury        1.5 -0.373484   13.18     +0.387
80 202 - Hg  mercury        0.0  0.0        29.86      0
80 204 - Hg  mercury        0.0  0.0         6.87      0
81 203 - Tl  thallium       0.5 +3.24451574 29.524     0
81 204 * Tl  thallium       2.0 +0.045       0.0       NaN
81 205 - Tl  thallium       0.5 +3.2764292  70.476     0
82 204 - Pb  lead           0.0  0.0         1.4       0
82 206 - Pb  lead           0.0  0.0        24.1       0
82 207 - Pb  lead           0.5 +1.18512    22.1       0
82 208 - Pb  lead           0.0  0.0        52.4       0
83 207 * Bi  bismuth        4.5 +0.9092      0.0      -0.76
83 209 - Bi  bismuth        4.5 +0.9134    100.0      -0.516
84 209 * Po  polonium       0.5 +1.5         0.0       0
85   0 * At  astatine      -1.0  0.0         0.0       0
86   0 * Rn  radon         -1.0  0.0         0.0       0
%--------------------------------------------------------------
% seventh period, rare earths
%--------------------------------------------------------------
87   0 * Fr  francium      -1.0  0.0         0.0       0
88   0 * Ra  radium        -1.0  0.0         0.0       0
89 227 * Ac  actinium       1.5 +0.73        0.0      +1.7
90 229 * Th  thorium        2.5 +0.18        0.0      +4.3
90 232 - Th  thorium        0.0  0.0       100.0       0
91   0 - Pa  protactinium  -1.0  0.0       100.0       0
92 234 * U   uranium        0.0  0.0         0.0055    0
92 235 * U   uranium        3.5 -0.109       0.7200   +4.936
92 238 * U   uranium        0.0  0.0        99.2745    0
93 237 * Np  neptunium      2.5 +1.256       0.0      +3.87
94 239 * Pu  plutonium      0.5 +0.406       0.0       0
95 243 * Am  americium      2.5 +0.6         0.0      +2.86
96   0 * Cm  curium        -1.0  0.0         0.0       0
97   0 * Bk  berkelium     -1.0  0.0         0.0       0
98   0 * Cf  californium   -1.0  0.0         0.0       0
99   0 * Es  einsteinium   -1.0  0.0         0.0       0
100  0 * Fm  fermium       -1.0  0.0         0.0       0
101  0 * Md  mendelevium   -1.0  0.0         0.0       0
102  0 * No  nobelium      -1.0  0.0         0.0       0
103  0 * Lr  lawrencium    -1.0  0.0         0.0       0
104  0 * Rf  rutherfordium -1.0  0.0         0.0       0
105  0 * Db  dubnium       -1.0  0.0         0.0       0
106  0 * Sg  seaborgium    -1.0  0.0         0.0       0
107  0 * Bh  bohrium       -1.0  0.0         0.0       0
108  0 * Hs  hassium       -1.0  0.0         0.0       0
109  0 * Mt  meitnerium    -1.0  0.0         0.0       0
110  0 * Ds  darmstadtium  -1.0  0.0         0.0       0
111  0 * Rg  roentgenium   -1.0  0.0         0.0       0
112  0 * Cn  copernicium   -1.0  0.0         0.0       0
113  0 * Nh  nihonium      -1.0  0.0         0.0       0
114  0 * Fl  flerovium     -1.0  0.0         0.0       0
115  0 * Mc  moscovium     -1.0  0.0         0.0       0
116  0 * Lv  livermorium   -1.0  0.0         0.0       0
117  0 * Ts  tennessine    -1.0  0.0         0.0       0
118  0 * Og  oganesson     -1.0  0.0         0.0       0
'''
    ),
    delim_whitespace=True,
    comment='%',
    names=[
        'protons',
        'nucleons',
        'radioactive',
        'symbol',
        'name',
        'spin',
        'g',
        'abundance',
        'quadrupole moment',
    ],
).set_index(['protons', 'nucleons'])


def get_nuclear_spin(atomic_number, data, spin_data):
    atomic_number = int(atomic_number)
    try:
        mass_number = int(data.loc[atomic_number]['mass number'])
    except ValueError:
        return ''
    isotope_data = spin_data.loc[atomic_number]

    spin = None
    found_mass_number = None

    if mass_number in isotope_data.index:
        found_mass_number = mass_number
        spin = isotope_data.loc[mass_number]['spin']
        if spin == 0:
            spin = None
            found_mass_number = None
    prefix = ''

    if found_mass_number is None:
        isotope_data = isotope_data.sort_values('abundance', ascending=False)
        for A in isotope_data.index:
            if isotope_data.loc[A]['spin'] != 0:
                found_mass_number = A
                spin = isotope_data.loc[found_mass_number]['spin']
                break
        if spin is None:
            found_mass_number = isotope_data.index[0]
            spin = isotope_data.loc[found_mass_number]['spin']

    prefix = '~~I='
    if found_mass_number != mass_number:
        prefix = r'%d:\,I=' % found_mass_number
    if int(spin) < 0:
        return ''
    if int(spin * 2) % 2 == 1:
        return "%s%d/2" % (prefix, int(spin * 2))
    else:
        return "%s%d" % (prefix, spin)


DATA['nuclear spin'] = pd.Series(
    [get_nuclear_spin(Z, DATA, SPIN_DATA) for Z in DATA.index],
    index=DATA.index,
)


GROUPS = [
    ('IA', 'Alkali metals'),
    ('IIA', 'Alkaline earths'),
    ('IB', 'Coinage metals'),
    ('IIIA', 'Boron group'),
    ('IVA', 'Carbon group'),
    ('VA', 'Pnictogens'),
    ('VIA', 'Chalcogens'),
    ('VIIA', 'Halogens'),
    ('VIIIA', 'Noble gases'),
]


CATEGORIES = [
    'nonmetal',
    'alkali metal',
    'alkaline earth metal',
    'lanthanide',
    'actinide',
    'transition metal',
    'post-transition metal',
    'metalloid',
    'halogen',
    'noble gas',
]


HEADER = r'''
\usepackage[T1]{fontenc}
\usepackage[scaled=0.8]{helvet}
\usepackage[misc]{ifsym}
\usepackage{amsmath}
\usepackage{braket}
\usepackage{ccicons}
\renewcommand*\familydefault{\sfdefault}
\usepackage{multicol}
\usepackage{pdfpages}
\usepackage{tikz}
\usepackage{ifthen}
\usepackage[
    hidelinks,
    pdftitle={Periodic Table},
    pdfauthor={Michael Goerz},
]{hyperref}

\newcommand\colorsquare[1]{\textcolor{#1}{\rule{3mm}{3mm}}}

\newcommand{\smallPeriodBox}[3][large]{% large/small, anchor, period
  \draw ($(#2) + (0.8,0)$) rectangle ++($(0.6cm, -1.2) - #3*(0,0.2)$);
  \ifthenelse{#3<2}{\node at ($(#2) + (1.1,-0.1)$) {\tiny Period};}{}
  \node at ($(#2) + (1.1,-0.6)$) {\Large #3};
  \draw            ($(#2) + (0.8,-1.2)$) -- ++(0.6cm,0);
  \node at         ($(#2) + (1.1,-1.3)$) {\tiny K: 1};
  \ifthenelse{#3>1}{%
    \draw[very thin] ($(#2) + (0.8,-1.4)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-1.5)$) {\tiny L: 2};
  }{}%
  \ifthenelse{#3>2}{%
    \draw[very thin] ($(#2) + (0.8,-1.6)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-1.7)$) {\tiny M: 3};
  }{}%
  \ifthenelse{#3>3}{%
    \draw[very thin] ($(#2) + (0.8,-1.8)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-1.9)$) {\tiny N: 4};
  }{}%
  \ifthenelse{#3>4}{%
    \draw[very thin] ($(#2) + (0.8,-2.0)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-2.1)$) {\tiny O: 5};
  }{}%
  \ifthenelse{#3>5}{%
    \draw[very thin] ($(#2) + (0.8,-2.2)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-2.3)$) {\tiny P: 6};
  }{}%
  \ifthenelse{#3>6}{%
    \draw[very thin] ($(#2) + (0.8,-2.4)$) -- ++(0.6cm,0);
    \node at         ($(#2) + (1.1,-2.5)$) {\tiny Q: 7};
  }{}%
}
\newcommand{\periodBox}[3][large]{% large/small, anchor, period
  \draw ($(#2) + (0.8,0)$) rectangle ++($(0.8cm, -1.2) - #3*(0,0.2)$);
  \node at ($(#2) + (1.2,-0.6)$) {\Large #3};
  \draw            ($(#2) + (0.8,-1.2)$) -- ++(0.8cm,0);
  \node at         ($(#2) + (1.0,-1.3)$) {\tiny K};
  \node at         ($(#2) + (1.28,-1.3)$) {\tiny n=};
  \node at         ($(#2) + (1.4,-1.3)$) {\tiny 1};
  \ifthenelse{#3>1}{%
    \draw[very thin] ($(#2) + (0.8,-1.4)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-1.5)$) {\tiny L};
    \node at         ($(#2) + (1.4,-1.5)$) {\tiny 2};
  }{}%
  \ifthenelse{#3>2}{%
    \draw[very thin] ($(#2) + (0.8,-1.6)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-1.7)$) {\tiny M};
    \node at         ($(#2) + (1.4,-1.7)$) {\tiny 3};
  }{}%
  \ifthenelse{#3>3}{%
    \draw[very thin] ($(#2) + (0.8,-1.8)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-1.9)$) {\tiny N};
    \node at         ($(#2) + (1.4,-1.9)$) {\tiny 4};
  }{}%
  \ifthenelse{#3>4}{%
    \draw[very thin] ($(#2) + (0.8,-2.0)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-2.1)$) {\tiny O};
    \node at         ($(#2) + (1.4,-2.1)$) {\tiny 5};
  }{}%
  \ifthenelse{#3>5}{%
    \draw[very thin] ($(#2) + (0.8,-2.2)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-2.3)$) {\tiny P};
    \node at         ($(#2) + (1.4,-2.3)$) {\tiny 6};
  }{}%
  \ifthenelse{#3>6}{%
    \draw[very thin] ($(#2) + (0.8,-2.4)$) -- ++(0.8cm,0);
    \node at         ($(#2) + (1.0,-2.5)$) {\tiny Q};
    \node at         ($(#2) + (1.4,-2.5)$) {\tiny 7};
  }{}%
}
\newcommand{\Gaseous}{\tikz{\draw (0,0) circle (2pt);}}
\newcommand{\Liquid}{\tikz{\draw[very thin] (0,0) circle (2pt);%
                     \draw[fill=black] (1.9pt,0pt) arc (0:-180:1.9pt);}}
\newcommand{\valenceCell}[3]{% anchor, x, y
  \draw[fill=blue!20, line width=0.2pt]%
  ($(#1) - (0.2cm,1.2cm) + #2*(0.2cm,0) - #3*(0,0.2cm) +(0.1pt,0.2pt)$)%
  rectangle ++($(2mm,2mm) - (0.3pt, 0.3pt)$);%
}

\begin{document}
\usetikzlibrary{calc}

\linespread{0.35}
\setlength{\parindent}{0pt}

\topskip0pt
\vspace*{\fill}

\begin{tikzpicture}[
electron grid/.style={step=0.2cm, very thin},
electron matrix/.style={below right,inner sep=0pt,column sep={2mm,between origins}, row sep={2mm,between origins}},
el/.style={font=\tiny},
valence el/.style={fill=blue!40, inner sep=0, font=\tiny},
alkali metal/.style={fill=orange!40},
alkaline earth metal/.style={fill=orange!20},
lanthanide/.style={fill=green!10},
actinide/.style={fill=green!30},
transition metal/.style={fill=red!10},
post-transition metal/.style={fill=red!40},
metalloid/.style={fill=red!20},
nonmetal/.style={fill=yellow!50},
halogen/.style={fill=yellow!20},
noble gas/.style={fill=blue!10},
unknown/.style={fill=white},
]

  %\draw[step=10mm, color=black, very thin] (0,0) grid (27,18.5);
  %\draw[step=5mm, color=gray, very thin] (0,0) grid (27,18.5);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

FOOTER = r'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\smallPeriodBox{He}{1}
\smallPeriodBox{Ne}{2}
\smallPeriodBox{Ar}{3}
\smallPeriodBox{Kr}{4}
\smallPeriodBox{Xe}{5}
\smallPeriodBox{Rn}{6}
\smallPeriodBox{Og}{7}

\end{tikzpicture}

%%\begin{multicols}{3}
%%\scriptsize
%%electronic quantum numbers: $\ket{n,l,m_l,m_s}$ or $\ket{n,l,j,m_j}$ ($j=l\pm 1/2$)
%%
%%parity $\sum_i l_i$
%%
%%LS Coupling: $\vec{L} = \sum_i \vec{l}_i$, $\vec{S} = \sum_i \vec{s}_i$, $\vec{J} = \vec{L} + \vec{S}$.
%%
%%atomic quantum numbers: $\ket{S, m_s, L, m_L}$ (uncoupled), $\ket{J,M_J,S,L}$
%%(spin-orbit-coupled)
%%% https://www.nist.gov/pml/atomic-spectroscopy-compendium-basic-ideas-notation-data-and-formulas
%%
%%configuration \\
%%$\rightarrow$ terms (L, S, orbit-orbit interaction) \\\\
%%$\rightarrow$ fine structure levels (J, spin-orbit interaction)\\\\
%%$\rightarrow$ states ($m_J$, Zeeman effect in magnetic field)
%%% http://mackenzie.chem.ox.ac.uk/teaching/Atomic%20Spectroscopy.pdf
%%
%%LS-couping/Russel-Saunders/Spin-Orbit coupling term symbol:\\\\
%%$^{2S+1}L_J$, e.g. $^2\text{P}_{3/2}$.
%%
%%selection rules
%%
%%hyperfine states: F = I + S, Zeeman splitting $m_F$
%%
%%\end{multicols}

\vspace*{\fill}

\end{document}
'''


def pictogram(atomic_number):
    """return a pictogram for the given element"""
    if DATA['radioactive'][atomic_number] == 'True':
        return r'\Radiation'
    if DATA['phase'][atomic_number] == 'gas':
        return r'\Gaseous'
    if DATA['phase'][atomic_number] == 'liquid':
        return r'\Liquid'
    return ''


def electron_configuration(atomic_number):
    """Return list of tuples (n, l, electrons)"""
    ec_strings = DATA['electron configuration'][atomic_number].split()
    nobels = {
        '[He]': 2,
        '[Ne]': 10,
        '[Ar]': 18,
        '[Kr]': 36,
        '[Xe]': 54,
        '[Rn]': 86,
    }
    l_mapping = {'s': 1, 'p': 2, 'd': 3, 'f': 4}
    result = []
    for s in ec_strings:
        if s in nobels:
            result = electron_configuration(nobels[s])
        else:
            n = int(s[0:1])
            l = l_mapping[s[1:2]]
            electrons = int(s[2:])
            result.append((n, l, electrons))
    return result


def electron_matrix(atomic_number):
    """Return a list of lines renedering the electron configuration matrix for
    the given element"""
    result = []
    configuration = electron_configuration(atomic_number)
    symbol = DATA['symbol'][atomic_number]
    n_valence = int(DATA['valence electrons'][atomic_number])
    reverse_configuration = reversed(configuration)
    while n_valence > 0:
        n, l, electrons = next(reverse_configuration)
        n_valence -= electrons
        result.append(
            r'\valenceCell{{{symbol}}}{{{l}}}{{{n}}}'.format(
                symbol=symbol, l=l, n=n
            )
        )
    result.append(
        r'\matrix[electron matrix] at ($(%s) + (0.01,-1.225cm)$){' % symbol
    )
    shells = defaultdict(list)
    for (n, l, electrons) in configuration:
        shells[n].append((l, electrons))
    for n in sorted(shells):
        shell_electrons = ['', '', '', '']
        for l, electrons in shells[n]:
            shell_electrons[l - 1] = (r'\node[el]{%2d};' % electrons).replace(
                " ", '~'
            )
        result.append(r'  %s & %s & %s & %s \\' % tuple(shell_electrons))
    result.append(r'};')
    return result


def x_y_position(atomic_number, lanthanide=False, actinide=False):
    """Return the x and y coordinate of the top left corner of the box
    indicating the element specified by `atomic_number`"""
    group_col = {
        'IA': 1,
        'IIA': 2,
        'IIIB': 3,
        'IVB': 4,
        'VB': 5,
        'VIB': 6,
        'VIIB': 7,
        'VIIIB': 8,  # 9, 10
        'IB': 11,
        'IIB': 12,
        'IIIA': 13,
        'IVA': 14,
        'VA': 15,
        'VIA': 16,
        'VIIA': 17,
        'VIIIA': 18,
    }
    y_period = {1: 16.0, 2: 14.6, 3: 13.0, 4: 11.2, 5: 9.2, 6: 7.0, 7: 4.6}
    period = int(DATA['period'][atomic_number])
    y = y_period[period]
    x_offset = 0.0
    if lanthanide:
        col = 3 + atomic_number - 57
        #  y -= 5.6
    elif actinide:
        col = 3 + atomic_number - 89
        #  y -= 5.6
    else:
        if atomic_number in [57, 89]:
            group = 'IIIB'
        else:
            group = DATA['group'][atomic_number]
        col = group_col[group]
        if col > 3:  # make space of lanthanides/actanides
            col += 14
            x_offset = 0.2
        if atomic_number in [27, 45, 77, 109]:  # VIIIB 2nd col
            col += 1
        elif atomic_number in [28, 46, 78, 110]:  # VIIIB 3rd col
            col += 2
    x = 0.8 * (col - 1) + x_offset
    return "%.2f" % x, "%.2f" % y


def mass_number(atomic_number):
    """Return a string with the mass number of the most common isotope for the
    given atomic_number)"""
    if DATA['mass number'].isnull()[atomic_number]:
        return ''
    else:
        val = int(DATA['mass number'][atomic_number])
        return ("%3d" % val).replace(' ', '~')


def atomic_mass(atomic_number):
    """Return a string the the relative atomic mass (averaged over all
    isotopes) for the given atomic_number"""
    if DATA['atomic mass'].isnull()[atomic_number]:
        return ''
    else:
        val = float(DATA['atomic mass'][atomic_number])
        if val < 10:
            return "%.4f" % val
        elif val < 100:
            return "%.3f" % val
        else:
            return "%.2f" % val


def render_element(atomic_number, lanthanide=False, actinide=False):
    """Render the given element"""
    lines = []
    x, y = x_y_position(
        atomic_number, lanthanide=lanthanide, actinide=actinide
    )
    fmt_data = dict(
        pictogram=pictogram(atomic_number),
        coord="(%s,%s)" % (x, y),
        symbol=DATA['symbol'][atomic_number],
        name=DATA['name'][atomic_number],
        nuclear_spin=DATA['nuclear spin'].replace(np.nan, '')[atomic_number],
        category=DATA['category'][atomic_number],
        mass=atomic_mass(atomic_number),
        atomic_number=("%3d" % atomic_number).replace(' ', '~'),
        mass_number=mass_number(atomic_number),
        period=int(DATA['period'][atomic_number]),
    )

    element_lines = [
        r'%%%% {name}',
        r'\node ({symbol}) at {coord} {{}};%',
        r'\draw[{category}] ({symbol}) rectangle ($({symbol}) + (0.8,-1.2cm)$);%',
        r'\node at ($({symbol}) + (0.40cm,-0.47cm)$)%',
        r'{{{{\tiny$_{{\text{{{atomic_number}}}}}^{{^{{\text{{{mass_number}}}}}}}$}}\text{{{symbol}}}}};',
        r'\node[text width=0.7 cm, text centered] at ($({symbol}) + (0.40cm,-0.78cm)$) {{\tiny {nuclear_spin}}};',
        r'\node at ($({symbol}) + (0.65cm,-0.22cm)$) {{\tiny {pictogram}}};',
        r'\node[text width=0.7 cm, text centered] at ($({symbol}) + (0.40cm,-1.00cm)$)%',
        r'{{\tiny {name}}};',
        r'\node at ($({symbol}) + (0.30cm,-0.15cm)$) {{\tiny {mass}}};',
        r'\draw[electron grid] ($({symbol}) - (0,1.2) - {period}*(0,0.2) $)%',
        r'                   grid ++($(0.8,0.0) + {period}*(0,0.2)$);%',
        r'\draw                ($({symbol}) - (0,1.2) - {period}*(0,0.2) $) % box around grid',
        r'              rectangle ++($(0.8,0.0) + {period}*(0,0.2)$);%',
        r'% make non-existing electron boxes black',
        r'\draw[fill=black, line width=0pt]% non-existing electron box',
        r'     ($({symbol}) + (0.2cm,-1.4cm)$) rectangle ++ (0.6cm,0.2cm);%',
        r'\ifthenelse{{{period}>1}}{{%',
        r'  \draw[fill=black, line width=0pt]% non-existing electron box',
        r'       ($({symbol}) + (0.4cm,-1.6cm)$) rectangle ++ (0.4cm,0.2cm);%',
        r'}}{{}}%',
        r'\ifthenelse{{{period}>2}}{{%',
        r'  \draw[fill=black, line width=0pt]% non-existing electron box',
        r'       ($({symbol}) + (0.6cm,-1.8cm)$) rectangle ++ (0.2cm,0.2cm);%',
        r'}}{{}}%',
    ]

    for line in element_lines:
        lines.append(line.format(**fmt_data))

    lines.extend(electron_matrix(atomic_number))

    lines.append("%%%%%\n")

    return "\n".join(lines) + "\n"


def box_legend():
    """Return array of lines that render a legend for the element boxes"""
    result = [r'\begin{scope}[shift={(-17.5, 0)}]']
    result.append(render_element(35))
    x0, y0 = x_y_position(35)
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[right, align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0) + 4 * 0.2),
            y1=float(y0),
            dx=0.2,
            dy=-0.4,
            text=dedent(
                r'''
            state of matter:\\
            \begin{tabular}{rl}
            {\rule{0pt}{6pt}{\Huge\Gaseous}} & gaseous \\
            {\rule{0pt}{6pt}{\Huge\Liquid}} & liquid \\
            {\rule{0pt}{6pt}{\tiny\Radiation}} & radioactive
            \end{tabular}
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[right, align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0) + 4 * 0.2),
            y1=float(y0),
            dx=-3.3,
            dy=-1.7,
            text=dedent(
                r'''
            electron configuration:\\
            $[$Ar$]$  3d\textsuperscript{10} 4s\textsuperscript{2} 4p\textsuperscript{5}\\
            valence electrons in blue
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[right, align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0) + 4 * 0.2),
            y1=float(y0),
            dx=0.2,
            dy=-1.5,
            text=dedent(
                r'''
            I=3/2: nuclear spin of most common isotope.\\
            When $\text{I}\!=\!\text{0}$ for most common isotope , shows \\
            "\textit{Z}:\,I=\textit{I}" for most common isotope with $\text{I}\!\neq\!\text{0}$.\\
            E.g. for $^{\text{24}}_{\text{12}}$Mg: I=0, but for $^{\text{25}}_{\text{12}}$Mg: I=5/2.
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0)),
            y1=float(y0),
            dx=0.8,
            dy=0.5,
            text=dedent(
                r'''
            79.904: atomic weight\\
            aka. ``relative atomic mass''\\
            (average over isotopes)
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[right, align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0)),
            y1=float(y0),
            dx=-2.5,
            dy=-0.2,
            text=dedent(
                r'''
            79: mass number (A):\\
            number of nucleons\\
            (most common isotope)
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[right, align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0)),
            y1=float(y0),
            dx=-2.5,
            dy=-0.9,
            text=dedent(
                r'''
            35: atomic number (Z):\\
            number of protons\\
            ($=$ number of electrons)
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0) + 2.8 * 0.2),
            y1=float(y0) - 1.2 - 4 * 0.2,
            dx=-1.75,
            dy=-0.5,
            text=dedent(
                r'''
            Madelung ordering rule: (n+l, n)\\
            $\Rightarrow$ 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, \\ \hspace{3mm} 5p, 6s, 4f, 5d, 6p, 7s, 5f, 6d, 7p, \dots
            '''
            ),
        )
    )
    result.append(
        r'\path({x1}, {y1}) -- +({dx}, {dy}) node[align=left, font=\scriptsize]{{{text}}};'.format(
            x1=(float(x0) + 2.8 * 0.2),
            y1=float(y0) - 1.2 - 4 * 0.2,
            dx=2.2,
            dy=-0.5,
            text=dedent(
                r'''
                Nuclear spin rules: based on Z, N=A-Z\\
                even/even: I=0; odd/odd: integer I; \\
                even/odd or odd/even: half-integer I
                '''
            ),
        )
    )
    result.append(r'\end{scope}')
    return "\n".join(result) + "\n"


def tex_group_label(label):
    """Format group label for tex"""
    if label.endswith('A') or label.endswith('B'):
        return label[:-1] + r'\,' + label[-1]
    else:
        return label


def render_group_label(x_anchor, y_anchor, name):
    x = float(x_anchor) + 0.4
    y = float(y_anchor) + 0.15
    name = tex_group_label(name)
    return r'\node[above, align=center] at (%s, %s) {\large %s};' % (
        x,
        y,
        name,
    )


def render_group_labels():
    """Return array of lines the render the names of the groups"""
    result = []
    anchors = [  # group name to atomic number of lightest element in group
        ('IA', 1),
        ('IIA', 4),
        ('IIIB', 21),
        ('IVB', 22),
        ('VB', 23),
        ('VIB', 24),
        ('VIIB', 25),
        ('---', 26),
        ('VIIIB', 27),
        ('---', 28),
        ('IB', 29),
        ('IIB', 30),
        ('IIIA', 5),
        ('IVA', 6),
        ('VA', 7),
        ('VIA', 8),
        ('VIIA', 9),
        ('VIIIA', 2),
    ]
    for groupname, anchor_atomic_number in anchors:
        x_anchor, y_anchor = x_y_position(anchor_atomic_number)
        result.append(render_group_label(x_anchor, y_anchor, groupname))
    return "\n".join(result) + "\n"


def render_title_box():
    """Return code to render title box"""
    COMPACT = False
    # If we add more information ad the bottom of the page, we'll want to
    # switch to the "copact" title
    if COMPACT:
        result = [r'\node[align=left, anchor=north] at (6.75, 16.6) {', ]
        result.append(r"{\Large \bf Periodic Table of Elements}\\~\vspace{3pt}\\" + "\n")
        result.append(r"{\footnotesize\ccLogo~2018 by Michael Goerz (\url{https://michaelgoerz.net})}\\" + "\n")
        result.append(r'{\footnotesize\ccAttribution~This work is licensed under a Creative Commons}\\' + "\n")
        result.append(r'{\footnotesize\ccNonCommercial~\href{https://creativecommons.org/licenses/by-nc/4.0/}{"Attribution-NonCommercial 4.0 International"} license.}' + "\n")
        result.append('};')
    else:
        result = [r'\node[align=left, anchor=west] at (0.0, 17.6) {', ]
        result.append(r"{\Large \bf Periodic Table of Elements}" + "\n")
        result.append('};')
        result.append(r'\node[align=left, anchor=west] at (0.0, 0.75) {')
        result.append(r"{\footnotesize\ccLogo\ccAttribution\ccNonCommercial~2018 by Michael Goerz (\url{https://michaelgoerz.net})}." + "\n")
        result.append(r'{\footnotesize~This work is licensed under a Creative Commons}' + "\n")
        result.append(r'{\footnotesize \href{https://creativecommons.org/licenses/by-nc/4.0/}{"Attribution-NonCommercial 4.0 International"} license.}' + "\n")
        result.append('};')
    return "\n".join(result) + "\n"


def render_group_table():
    """Return code to render table of groups"""
    result = [r'\node[align=left, anchor=north] at (14, 16.5) {']
    result.append("{\\bf groups (CAS):}\\\\~\\\\\n")
    result.append(r'\begin{tabular}{ll}')
    for group, label in GROUPS:
        result.append("%s & %s\\\\" % (tex_group_label(group), label))
    result.append(r'\end{tabular}\\')
    result.append(r'A: main groups\\')
    result.append(r'B: transition elements\vspace*{5pt}\\')
    result.append(r'UIPAC: number groups 1--18')
    result.append('};')
    return "\n".join(result) + "\n"


def get_category_color(category_name):
    """Return the latex color for the given category name (e.g. 'alkali
    metal')"""
    color_rx = re.compile(r'fill=([\w\d!]+)')
    for line in HEADER.split("\n"):
        if line.startswith(category_name):
            return color_rx.search(line).group(1)
    raise ValueError("Cannot determine color for %s" % category_name)


def render_category_table():
    """Return code to render table of categoriess"""
    result = [r'\node[align=left, anchor=north] at (18, 16.5) {']
    result.append("{\\bf categories:}\\\\~\\\\\n")
    result.append(r'\begin{tabular}{ll}')
    for category_name in CATEGORIES:
        color = get_category_color(category_name)
        result.append("\\colorsquare{%s} & %s\\\\" % (color, category_name))
    result.append(r'\end{tabular}')
    result.append('};')
    return "\n".join(result) + "\n"


def render_quantum_numbers_grid():
    """Return to to render the grid of quantum numbers"""
    result = []

    ## spdf
    x1, y1 = x_y_position(87)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 8 * 0.2
    x2, y2 = x_y_position(103, actinide=True)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 7 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) grid (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    for col in range(17):
        result.append(
            r'\node[el] at (%s, %s){s};' % (x1 + col * 0.8 + 0.1, y1 + 0.1)
        )
        result.append(
            r'\node[el] at (%s, %s){p};' % (x1 + col * 0.8 + 0.3, y1 + 0.075)
        )
        result.append(
            r'\node[el] at (%s, %s){d};' % (x1 + col * 0.8 + 0.5, y1 + 0.1)
        )
        result.append(
            r'\node[el] at (%s, %s){f};' % (x1 + col * 0.8 + 0.7, y1 + 0.1)
        )
    # spdf
    x1, y1 = x_y_position(104)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 8 * 0.2
    x2, y2 = x_y_position(118)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 7 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) grid (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    for col in range(15):
        result.append(
            r'\node[el] at (%s, %s){s};' % (x1 + col * 0.8 + 0.1, y1 + 0.1)
        )
        result.append(
            r'\node[el] at (%s, %s){p};' % (x1 + col * 0.8 + 0.3, y1 + 0.075)
        )
        result.append(
            r'\node[el] at (%s, %s){d};' % (x1 + col * 0.8 + 0.5, y1 + 0.1)
        )
        result.append(
            r'\node[el] at (%s, %s){f};' % (x1 + col * 0.8 + 0.7, y1 + 0.1)
        )

    ## s-block
    x1, y1 = x_y_position(87)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 9 * 0.2
    x2, y2 = x_y_position(88)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 8 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){0 (s-block)};' % (0.5 * (x2 + x1), y1 + 0.1)
    )
    # s
    x1, y1 = x_y_position(87)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(87)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){+1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )
    x1, y1 = x_y_position(88)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(88)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){-1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )

    ## d-block
    x1, y1 = x_y_position(89, actinide=True)
    x2, y2 = x1, y1
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 9 * 0.2
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 8 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){2};' % (x1 + 0.5 * (x2 - x1), y1 + 0.1)
    )
    # s
    y1 += -0.4
    y2 += -0.4
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){+1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )

    ## f-block
    x1, y1 = x_y_position(90, actinide=True)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 9 * 0.2
    x2, y2 = x_y_position(103, actinide=True)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 8 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){3 (f-block)};'
        % (x1 + 0.5 * (x2 - x1), y1 + 0.1)
    )
    # s
    x1, y1 = x_y_position(90, actinide=True)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(96, actinide=True)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){+1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )
    x1, y1 = x_y_position(97, actinide=True)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(103, actinide=True)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){-1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )

    ## d-block
    x1, y1 = x_y_position(104)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 9 * 0.2
    x2, y2 = x_y_position(112)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 8 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){2 (d-block)};'
        % (x1 + 0.5 * (x2 - x1), y1 + 0.1)
    )
    # s
    x1, y1 = x_y_position(104)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(107)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){+1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )
    x1, y1 = x_y_position(108)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(112)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){-1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )

    ## p-block
    x1, y1 = x_y_position(113)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 9 * 0.2
    x2, y2 = x_y_position(118)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 8 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){1 (p-block)};'
        % (x1 + 0.5 * (x2 - x1), y1 + 0.1)
    )
    # s
    x1, y1 = x_y_position(113)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(115)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){+1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )
    x1, y1 = x_y_position(116)
    x1 = float(x1)
    y1 = float(y1) - 1.2 - 11 * 0.2
    x2, y2 = x_y_position(118)
    x2 = float(x2) + 0.8
    y2 = float(y2) - 1.2 - 10 * 0.2
    result.append(
        r'\draw[electron grid] (%s, %s) rectangle (%s, %s);' % (x1, y1, x2, y2)
    )
    result.append(
        r'\node[el] at (%s, %s){-1/2};' % (0.5 * (x2 + x1), y1 + 0.1)
    )

    ## m
    m_labels = [
        '0', '0', '+2', '+3', '+2', '+1', '0', '-1', '-2', '-3', '+3', '+2',
        '+1', '0', '-1', '-2', '-3', '+1', '0', '-1', '-2', '+2', '+1', '0',
        '-1', '-2', '+1', '0', '-1', '+1', '0', '-1'
    ]
    for i, m_label in enumerate(m_labels):
        x1, y1 = x_y_position(87 + i, actinide=(3 <= i <= 16))
        x1 = float(x1)
        y1 = float(y1) - 1.2 - 10 * 0.2
        x2 = x1 + 0.8
        y2 = y1 + 0.2
        result.append(
            r'\draw[electron grid] (%s, %s) rectangle (%s, %s);'
            % (x1, y1, x2, y2)
        )
        result.append(
            r'\node[el] at (%s, %s){%s};'
            % (0.5 * (x2 + x1), y1 + 0.1, m_label)
        )

    ## labels
    x0, y0 = x_y_position(118)
    x0 = float(x0) + 4 * 0.2
    y0 = float(y0) - 1.2 - 8 * 0.2 - 0.1
    result.append(
        r'\node[right, el] at (%s, %s){%s};' % (x0, y0 + 0.2, '$l$ / $n$')
    )
    # result.append(r'\node[right, el] at (%s, %s){%s};' % (x0, y0-0.0, ''))
    result.append(
        r'\node[right, el] at (%s, %s){%s};' % (x0, y0 - 0.2, '$m_l$')
    )
    result.append(
        r'\node[right, el] at (%s, %s){%s};' % (x0, y0 - 0.4, '$m_s$')
    )

    return "\n".join(result) + "\n"


@click.command()
@click.help_option('--help', '-h')
@click.option(
    '--paperwidth',
    type=float,
    help="The width of the page in mm. "
    "Defaults to 297 for --a4 and to 279 for --letter.",
)
@click.option(
    '--paperheight',
    type=float,
    help="The height of the page in mm. "
    "Defaults to 210 for --a4 to 215 for --letter.",
)
@click.option(
    '--left',
    type=float,
    help="The left page margin in mm. "
    "Defaults to 15 for --a4 and to 6 for --letter.",
)
@click.option(
    '--right',
    type=float,
    help="The right page margin in mm. " "Defaults to the value of --left",
)
@click.option(
    '--top',
    type=float,
    help="The top page margin in mm. "
    "Defaults to 6 for --a4 and to 8 for --letter.",
)
@click.option(
    '--bottom',
    type=float,
    help="The width of the page" "Defaults to the value of --top",
)
@click.option(
    '--a4',
    'paperformat',
    flag_value='a4',
    default=True,
    help="Use layout options for A4 paper (default)",
)
@click.option(
    '--letter',
    'paperformat',
    flag_value='letter',
    help="User layout options for letter-sized paper",
)
@click.argument('outfile')
def render_periodic_table(
    paperwidth, paperheight, left, right, top, bottom, paperformat, outfile
):
    """Write LaTeX for a periodic table to the given OUTFILE"""
    if paperformat == 'a4':
        paperwidth = 297.0 if paperwidth is None else paperwidth
        paperheight = 210.0 if paperheight is None else paperheight
        left = 15.0 if left is None else left
        right = left if right is None else right
        top = 6.0 if top is None else top
        bottom = top if bottom is None else bottom
    elif paperformat == 'letter':
        paperwidth = 279.0 if paperwidth is None else paperwidth
        paperheight = 215.0 if paperheight is None else paperheight
        left = 6.0 if left is None else left
        right = left if right is None else right
        top = 8.0 if top is None else top
        bottom = top if bottom is None else bottom
    else:
        raise ValueError("Invalid paperformat: %s" % paperformat)
    with open(outfile, 'w') as out_fh:
        out_fh.write(r'\documentclass{article}' + "\n")
        out_fh.write(
            r'\usepackage[paperwidth=%.1fmm,paperheight=%.1fmm,left=%.1fmm,'
            r'right=%.1fmm,top=%.1fmm,bottom=%.1fmm]{geometry}'
            % (paperwidth, paperheight, left, right, top, bottom)
        )
        out_fh.write("\n")
        out_fh.write(HEADER)
        for atomic_number in range(1, 119):
            if atomic_number in range(57, 72):
                out_fh.write(render_element(atomic_number, lanthanide=True))
            elif atomic_number in range(89, 104):
                out_fh.write(render_element(atomic_number, actinide=True))
            else:
                out_fh.write(render_element(atomic_number))
            out_fh.write("\n")
        out_fh.write(render_title_box())
        out_fh.write(render_group_table())
        out_fh.write(render_quantum_numbers_grid())
        out_fh.write(render_category_table())
        out_fh.write(render_group_labels())
        out_fh.write(box_legend())
        out_fh.write(FOOTER)


if __name__ == "__main__":
    render_periodic_table()
