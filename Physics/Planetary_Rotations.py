import numpy as np
import math
from functools import reduce

"""This script gets the rotation of various celestial bodies as defined in the 
"Report of the IAU Working Group on Cartographic Coordinates and Rotational Elements: 2015" """

def get_rotation(body, t):
    SE = 0 # Just Placeholder, need to find Julian date for standard epoch
    d = (t-SE)/86400 # days since standard epoch
    T = d/36525
    if body == "Sun":
        a_0 = 286.13
        d_0 = 63.87
        W = 84.176 +(14.1844000*d)
    if body == "Mercury":
        a_0 = 281.0103 - (0.0328*T)
        d_0 = 61.4155 - (0.0049*T)
        M1 = math.radians(1747910857+(4.092335*d))
        M2 = math.radians(349.5821714+(8.184670*d))
        M3 = math.radians(164.3732571+(12.277005*d))
        M4 = math.radians(339.1643429+(16.369340*d))
        M5 = math.radians(153.9554286+20.461675*d)
        W = 84.176 + (14.1844000*d) + (0.01067257*math.sin(M1)) - (0.00112309*math.sin(M2)) - (0.00011040*math.sin(M3)) -(0.00002539*math.sin(M4)) - (0.00000571*math.sin(M5))
    if body == "Venus":
        a_0 = 272.76
        d_0 = 67.16
        W = 160.20-(1.4813688*d)
    if body == "Mars":
        a_0 = 317.269202 - (0.10927547*T) + (0.000068*math.sin(math.radians(198.991226+(19139.4819985*T))))+(0.000238*math.sin(math.radians(226.29679+(38280.8511281*T))))+(0.000052*math.sin(math.radians(249.663391+(57420.7251593*T))))+(0.000009*math.sin(math.radians(266.183510+(76560.6367950*T))))+(0.0419057*math.sin(math.radians(79.398797+(0.5042615*T))))
        d_0 = 54.432516 - (0.05827105*T) + 0.000051*math.cos(math.radians(122.433576+19139.9407476*T)) + 0.000141*math.cos(math.radians(43.058401+38280.8753272*T))+0.000031*math.cos(math.radians(57.663379+57420.7517205*T))+(0.000005*math.cos(math.radians(79.476401+76560.6495004*T)))+ (1.591274*math.cos(166.325722+0.5042615*T))
        W = (176.049863 + 350.891982443297*d) + (0.000145*math.sin(129.071773+19140.0328244*T))+ (0.000157*math.sin(math.radians(36.352167+38281.0473591*T))) + (0.000040*math.sin(math.radians(56.668646+57420.9295360*T))) + (0.000001*math.sin(math.radians(67.364003+76560.2552215*T)))+ (0.000001*math.sin(math.radians(104.792680+95700.4387578*T))) + (0.584542*math.sin(math.radians(95.391654+0.5042615*T)))
    if body == "Jupiter":
        Ja = math.radians(99.360714+4850.4046*T)
        Jb = math.radians(175.895369+1191.9605*T)
        Jc = math.radians(300.323162+262.5475*T)
        Jd = math.radians(114.012305 + 6070.2476*T)
        Je = math.radians(49.511251+64.3000*T)
        a_0 = (268.056595 - 0.006499*T) + (0.000117*math.sin(Ja)) + (0.000938*math.sin(Jb))+ (0.001432*math.sin(Jc)) + (0.000030*math.sin(Jd)) + (0.002150*math.sin(Je))
        d_0 = (64.495303 + 0.002413*T) + (0.000050*math.cos(Ja)) + (0.000404*math.cos(Jb)) + (0.000617*math.cos(Jc)) - (0.000013*math.cos(Jd)) + (0.000926*math.cos(Je))
        W = 284.95 + 870.5360000*d
    if body == "Saturn":
        a_0 = 40.589 - 0.036*T
        d_0 = 83.537 - 0.004*T
        W = 38.90 + 910.7939024*d
    if body == "Uranus":
        a_0 = 257.311
        d_0 = -15.175
        W = 203.81 - 501.1600928*d
    if body == "Neptune":
        N = 357.85 + 52.316*T
        a_0 = 299.36 + 0.70*math.sin(N)
        d_0 = 43.46 - 0.51*math.cos(N)
        W = 249.978 + 541.1397757*d - 0.48*math.sin(N)
    if body == "Moon":
        pass
    if body == "Phobos":
        M1 = math.radians(190.72646643 + (15917.10818695*T))
        M2 = math.radians(21.46892470 + (31834.27934054*T))
        M3 = math.radians(332.86082793 + (19139.89694742*T))
        M4 = math.radians(394.93256437 + (38280.79631835*T))
        a_0 = (317.67071657 - 0.10844326*T)- (1.78428399*math.sin(M1)) + (0.02212824*math.sin(M2)) - (0.01028251*math.sin(M3)) - (0.00475595*math.sin(M4))
        d_0 = 52.88627266 - 0.06134706*T - 1.07516537*math.cos(M1) + 0.00668626*math.cos(M2) - 0.00648740*math.cos(M3) + 0.00281576*math.cos(M4)
        W = 34.9964842535 + 1128.84475928*d + (12.72192797*T**2) + 1.42421769*math.sin(M1) - 0.02273783*math.sin(M2) + 0.00410711*math.sin(M3) + 0.00631964*math.sin(M4)+ 1.143*math.sin(M5)

    if body == "Deimos":

        M6 = math.radians(121.46893664 + (660.22803474*T))
        M7 = math.radians(231.05028581 + (660.99123540*T))
        M8 = math.radians(251.37314025 + (1320.50145245*T))
        M9 = math.radians(217.98635955 + (38279.96125550*T))
        M10 = math.radians(196.19729402 + (19139.83628608*T))
        a_0 = (316.65705808 - 0.10518014*T) + 3.09217726*math.sin(M6) + 0.22980637*math.sin(M7) + (0.06418655*math.sin(M8)) + 0.02533537*math.sin(M9) + (0.00778695*math.sin(M10))
        d_0 = (53.50992033 - (0.05979094*T)) + (1.83936004*math.cos(M6)) + (0.14325320*math.cos(M7)) + (0.01911409*math.cos(M8)) - (0.01482590*math.cos(M9)) + (0.00192430*math.cos(M10))
        W = (79.39932954 + 285.16188899*d) - (2.73954829*math.sin(M6)) -(0.39968606*math.sin(M7)) - (0.06563259*math.sin(M8)) - (0.02912940*math.sin(M9))+ (0.01699160*math.sin(M10))

    if body == "Metis":
        a_0 = 268.05 - 0.009*T
        d_0 = 64.49 + 0.003*T
        W = 346.09 + 1221.2547301*d

    if body == "Adrastea":
        a_0 =  (268.05 - (0.009*T))
        d_0 =  64.49 + 0.003*T
        W =  33.29 + 1206.9986602*d

    if body == "Amalthea":
        J1 = math.radians(73.32 + 91472.9*T)
        a_0 = 268.05 - 0.009*T - (0.84*math.sin(J1)) + (0.01*math.sin(2*J1))
        d_0 = 64.49 + 0.003*T - (0.36*math.cos(J1))
        W = 231.67 + 722.6314560*d + 0.76*math.sin(J1) - (0.01*math.sin(2*J1))
    if body == "Thebe":
        J2 = math.radians(24.62 + 45137.2*T)

        a_0 = 268.05 - 0.009*T - 2.11*math.sin(J2) + 0.04*math.sin(2*J2)
        d_0 = 64.49 + 0.003*T - 0.91*math.cos(J2) + 0.01*math.cos(2*J2)
        W = 8.56 + 533.7004100*d + 1.91*math.sin(J2) - 0.04*math.sin(2*J2)
    if body == "Io":
        J3 = math.radians(283.90 + 4850.7*T)
        J4 = math.radians(355.80 + 1191.3*T)

        a_0 = 268.05 - 0.009*T + 0.094*math.sin(J3) + 0.024*math.sin(J4)
        d_0 = 64.50 + 0.003*T + 0.040*math.cos(J3) + 0.011*math.cos(J4)
        W = 200.39 + 203.4889538*d - 0.085*math.sin(J3) - 0.022*math.sin(J4)
    if body == "Europa":
        J4 = math.radians(355.80 + 1191.3*T)
        J5 = math.radians(119.90 + 262.1*T)
        J6 = math.radians(229.80 + 64.3*T)
        J7 = math.radians(352.25 + 2382.6*T)

        a_0 =  268.08 - 0.009*T + 1.086*math.sin(J4) + 0.060*math.sin(J5) + 0.015*math.sin(J6) + 0.009*math.sin(J7)
        d_0 = 64.51 + 0.003*T + 0.468*math.cos(J4) + 0.026*math.cos(J5) + 0.007*math.cos(J6) + 0.002*math.cos(J7)
        W = 36.022 + 101.3747235*d - 0.980*math.sin(J4) - 0.054*math.sin(J5)- 0.014*math.sin(J6) - 0.008*math.sin(J7)
    if body == "Ganymede":
        J4 = math.radians(355.80 + 1191.3*T)
        J5 = math.radians(119.90 + 262.1*T)
        J6 = math.radians(229.80 + 64.3*T)
        a_0 = 268.20 - 0.009*T - 0.037*math.sin(J4) + 0.431*math.sin(J5) + 0.091*math.sin(J6)
        d_0 =  64.57 + 0.003*T - 0.016*math.cos(J4) + 0.186*math.cos(J5) + 0.039*math.cos(J6)
        W = 44.064 + 50.3176081*d + 0.033*math.sin(J4) - 0.389*math.sin(J5) - 0.082*math.sin(J6)
    if body == "Callisto":
        J5 = math.radians(119.90 + 262.1*T)
        J6 = math.radians(229.80 + 64.3*T)
        J8 = math.radians(113.35 + 6070.0*T)

        a_0 =  268.72 - 0.009*T - 0.068*math.sin(J5) + 0.590*math.sin(J6) +0.010*math.sin(J8)
        d_0 =  64.83 + 0.003*T - 0.029*math.cos(J5) + 0.254*math.cos(J6) - 0.004*math.cos(J8)
        W =  259.51 + 21.5710715*d + 0.061*math.sin(J5) - 0.533*math.sin(J6) - 0.009*math.sin(J8)

    if body == "Pan":
        a_0 =  40.6 - 0.036*T
        d_0 = 83.5 - 0.004*T
        W =  48.8 + 626.0440000*d
    if body == "Atlas":
        a_0 =  40.58 - 0.036*T
        d_0 =  83.53 - 0.004*T
        W =  137.88 + 598.3060000*d
    if body == "Prometheus":
        a_0 = 40.58 - 0.036*T
        d_0 = 83.53 - 0.004*T
        W =  296.14 + 587.289000*d
    if body == "Pandora":
        a_0 = 40.58 - 0.036*T
        d_0 = 83.53 - 0.004*T
        W =  162.92 + 572.7891000*d
    if body == "Epimetheus":
        S1 = math.radians(353.32 + 75706.7*T)
        a_0 =  40.58 - 0.036*T - 3.153*math.sin(S1) + 0.086*math.sin(2*S1)
        d_0 = 83.52 - 0.004*T - 0.356*math.cos(S1) + 0.005*math.cos(2*S1)
        W =  293.87 + 518.4907239*d + 3.133*math.sin(S1) - 0.086*math.sin(2*S1)
    if body == "Janus":
        S2 = math.radians(28.72 + 75706.7*T)
        a_0 = 40.58 - 0.036*T - 1.623*math.sin(S2) + 0.023*math.sin(2*S2)
        d_0 = 83.52 - 0.004*T - 0.183*math.cos(S2) + 0.001*math.cos(2*S2)
        W =  58.83 + 518.2359876*d + 1.613*math.sin(S2) - 0.023*math.sin(2*S2)
    if body == "Mimas":
        S3 = math.radians(177.40 - 36505.5*T)
        S5 = math.radians(316.45 + 506.2*T)
        a_0 = 40.66 - 0.036*T + 13.56*math.sin(S3)
        d_0 = 83.52 - 0.004*T - 1.53*math.cos(S3)
        W = 333.46 + 381.9945550*d - 13.48*math.sin(S3) - 44.85*math.sin(S5)
    if body == "Enceladus":
        a_0 = 40.66 - 0.036*T
        d_0 = 83.52 - 0.004*T
        W = 6.32 + 262.7318996*d
    if body == "Tethys":
        S1 = math.radians(353.32 + 75706.7*T)
        S2 = math.radians(28.72 + 75706.7*T)
        S3 = math.radians(177.40 - 36505.5*T)
        S4 = math.radians(300.00 - 7225.9*T)
        S5 = math.radians(316.45 + 506.2*T)
        S6 = math.radians(345.20 - 1016.3*T)

        a_0 =  40.66 - 0.036*T + 9.66*math.sin(S4)
        d_0 = 83.52 - 0.004*T - 1.09*math.cos(S4)
        W = 8.95 + 190.6979085*d - 9.60*math.sin(S4) + 2.23*math.sin(S5)
    if body == "Telesto":
        a_0 =  50.51 - 0.036*T
        d_0 =  84.06 - 0.004*T
        W = 56.88 + 190.6979332*d
    if body == "Calypso":
        a_0 = 6.41 - 0.036*T
        d_0 = 85.04 - 0.004*T
        W = 153.51 + 190.6742373*d
    if body == "Dione":
        a_0 = 40.66 - 0.036*T
        d_0 = 83.52 - 0.004*T
        W = 357.6 + 131.5349316*d
    if body == "Helene":
        a_0 = 40.85 - 0.036*T
        d_0 = 83.34 - 0.004*T
        W = 245.12 + 131.6174056*d
    if body == "Rhea":
        S1 = math.radians(353.32 + 75706.7*T)
        S2 = math.radians(28.72 + 75706.7*T)
        S3 = math.radians(177.40 - 36505.5*T)
        S4 = math.radians(300.00 - 7225.9*T)
        S5 = math.radians(316.45 + 506.2*T)
        S6 = math.radians(345.20 - 1016.3*T)

        a_0 = 40.38 - 0.036*T + 3.10*math.sin(S6)
        d_0 = 83.55 - 0.004*T - 0.35*math.cos(S6)
        W = 235.16 + 79.6900478*d - 3.08*math.sin(S6)
    if body == "Titan":
        a_0 = 39.4827
        d_0 = 83.4279
        W = 186.5855 + 22.5769768*d
    if body == "Iapetus":
        a_0 = 318.16 - 3.949*T
        d_0 = 75.03 - 1.143*T
        W = 355.2 + 4.5379572*d
    if body == "Phoebe":
        a_0 = 356.90
        d_0 = 77.80
        W = 178.58 + 931.639*d
    if body == "Cordelia":
        U1 = math.radians(115.75 + 54991.87*T)
        a_0 =  257.31 - 0.15*math.sin(U1)
        d_0 = - 15.18 + 0.14*math.cos(U1)
        W = 127.69 - 1074.5205730*d - 0.04*math.sin(U1)
    if body == "Ophelia":
        U2 = math.radians(141.69 + 41887.66*T)
        a_0 = 257.31 - 0.09*math.sin(U2)
        d_0 = - 15.18 + 0.09*math.cos(U2)
        W = 130.35 - 956.4068150*d - 0.03*math.sin(U2)
    if body == "Bianca":
        U3 = math.radians(135.03 + 29927.35*T)
        a_0 = 257.31 - 0.16*math.sin(U3)
        d_0 = - 15.18 + 0.16*math.cos(U3)
        W = 105.46 - 828.3914760*d - 0.04*math.sin(U3)
    if body == "Cressida":
        U4 = math.radians(61.77 + 25733.59*T)
        a_0 = 257.31 - 0.04*math.sin(U4)
        d_0 = - 15.18 + 0.04*math.cos(U4)
        W = 59.16 - 776.5816320*d - 0.01*math.sin(U4)
    if body == "Desdemona":
        U5 = math.radians(249.32 + 24471.46*T)
        a_0 = 257.31 - 0.17*math.sin(U5)
        d_0 = -15.18 + 0.16*math.cos(U5)
        W =  95.08 - 760.0531690*d - 0.04*math.sin(U5)
    if body == "Juliet":
        U6 = math.radians(43.86 + 22278.41*T)
        a_0 = 257.31 - 0.06*math.sin(U6)
        d_0 = -15.18 + 0.06*math.cos(U6)
        W = 302.56 - 730.1253660*d - 0.02*math.sin(U6)
    if body == "Portia":
        U7 = math.radians(77.66 + 20289.42*T)
        a_0 = 257.31 - 0.09*math.sin(U7)
        d_0 = -15.18 + 0.09*math.cos(U7)
        W = 25.03 - 701.4865870*d - 0.02*math.sin(U7)
    if body == "Rosalind":
        U8 = math.radians(157.36 + 16652.76*T)
        a_0 = 257.31 - 0.29*math.sin(U8)
        d_0 = - 15.18 + 0.28*math.cos(U8)
        W = 314.90 - 644.6311260*d - 0.08*math.sin(U8)
    if body == "Belinda":
        U9 = math.radians(101.81 + 12872.63*T)
        a_0 = 257.31 - 0.03*math.sin(U9)
        d_0 = -15.18 + 0.03*math.cos(U9)
    if body == "Puck":
        U10 = math.radians(138.64 + 8061.81*T)
        a_0 = 257.31 - 0.33*math.sin(U10)
        d_0 = -15.18 + 0.31*math.cos(U10)
        W =  91.24 - 472.5450690*d - 0.09*math.sin(U10)
    if body == "Miranda":
        U11 = math.radians(102.23 - 2024.22*T)
        U12 = math.radians(316.41 + 2863.96*T)
        a_0 = 257.43 + 4.41*math.sin(U11) - 0.04*math.sin(2*U11)
        d_0 = - 15.08 + 4.25*math.cos(U11) - 0.02*math.cos(2*U11)
        W = 30.70 - 254.6906892*d - 1.27*math.sin(U12) + 0.15*math.sin(2*U12) + 1.15*math.sin(U11) - 0.09*math.sin(2*U11)
    if body == "Ariel":
        U12 = math.radians(316.41 + 2863.96*T)
        U13 = math.radians(304.01 - 51.94*T)
        a_0 = 257.43 + 0.29*math.sin(U13)
        d_0 = - 15.10 + 0.28*math.cos(U13)
        W =  156.22 - 142.8356681*d + 0.05*math.sin(U12) + 0.08*math.sin(U13)
    if body == "Umbriel":
        U12 = math.radians(316.41 + 2863.96*T)
        U14 = math.radians(308.71 - 93.17*T)
        a_0 =  257.43 + 0.21*math.sin(U14)
        d_0 =  -15.10 + 0.2*math.cos(U14)
        W =  108.05 - 86.8688923*d - 0.09*math.sin(U12) + 0.06*math.sin(U14)
    if body == "Titania":
        U15 = math.radians(340.82 - 75.32*T)
        a_0 = 257.43 + 0.29*math.sin(U15)
        d_0 = -15.10 + 0.28*math.cos(U15)
        W = 77.74 - 41.3514316*d + 0.08*math.sin(U15)
    if body == "Oberon":
        U16 = math.radians(259.14 - 504.81*T)
        a_0 = 257.43 + 0.16*math.sin(U16)
        d_0 = - 15.10 + 0.16*math.cos(U16)
        W =  6.77 - 26.7394932*d + 0.04*math.sin(U16)
    if body == "Naiad":
        N = math.radians(357.85 + 52.316*T)
        N1 = math.radians(323.92 + 62606.6*T)
        a_0 = 299.36 + 0.70*math.sin(N) - 6.49*math.sin(N1) + 0.25*math.sin(2*N1)
        d_0 = 43.36 - 0.51*math.cos(N) - 4.75*math.cos(N1) + 0.09*math.cos(2*N1)
        W =  254.06 + 1222.8441209*d - 0.48*math.sin(N) + 4.40*math.sin(N1) - 0.27*math.sin(2*N1)
    if body == "Thalassa":
        N = math.radians(357.85 + 52.316*T)
        N2 =math.radians(220.51 + 55064.2*T)
        a_0 = 299.36 + 0.70*math.sin(N) - 0.28*math.sin(N2)
        d_0 = 43.45 - 0.51*math.cos(N) - 0.21*math.cos(N2)
        W =  102.06 + 1155.7555612*d - 0.48*math.sin(N) + 0.19*math.sin(N2)
    if body == "Despina":
        N = math.radians(357.85 + 52.316*T)
        N3 =math.radians(354.27 + 46564.5*T)
        a_0 = 299.36 + 0.70*math.sin(N) - 0.09*math.sin(N3)
        d_0 =  43.45 - 0.51*math.cos(N) - 0.07*math.cos(N3)
        W =  306.51 + 1075.7341562*d - 0.49*math.sin(N) + 0.06*math.sin(N3)
    if body == "Galatea":
        N = math.radians(357.85 + 52.316*T)
        N4 =math.radians(75.31 + 26109.4*T)
        a_0 = 299.36 + 0.70*math.sin(N) - 0.07*math.sin(N4)
        d_0 = 43.43 - 0.51*math.cos(N) -0.05*math.cos(N4)
        W =  258.09 + 839.6597686*d - 0.48*math.sin(N) + 0.05*math.sin(N4)
    if body == "Larissa":
        N = math.radians(357.85 + 52.316*T)
        N5 =math.radians(35.36 + 14325.4*T)
        a_0 = 299.36 + 0.70*math.sin(N) - 0.27*math.sin(N5)
        d_0 = 43.41 - 0.51*math.cos(N) - 0.20*math.cos(N5)
        W = 179.41 + 649.0534470*d - 0.48*math.sin(N) + 0.19*math.sin(N5)
    if body == "Proteus":
        N = math.radians(357.85 + 52.316*T)
        N6 =math.radians(142.61 + 2824.6*T)
        a_0 = 299.27 + 0.70*math.sin(N) - 0.05*math.sin(N6)
        d_0 = 42.91 - 0.51*math.cos(N) - 0.04*math.cos(N6)
        W = 93.38 + 320.7654228*d - 0.48*math.sin(N) + 0.04*math.sin(N6)
    if body == "Triton":
        N7 = math.radians(177.85 + 52.316*T)
        a_0 = 299.36 - 32.35*math.sin(N7) - 6.28*math.sin(2*N7) - 2.08*math.sin(3*N7) - 0.74*math.sin(4*N7) - 0.28*math.sin(5*N7) - 0.11*math.sin(6*N7) - 0.07*math.sin(7*N7) - 0.02*math.sin(8*N7) - 0.01*math.sin(9*N7)
        d_0 =  41.17 + 22.55*math.cos(N7) + 2.10*math.cos(2*N7) + 0.55*math.cos(3*N7) + 0.16*math.cos(4*N7) + 0.05*math.cos(5*N7) + 0.02*math.cos(6*N7) + 0.01*math.cos(7*N7)
        W =  296.53 - 61.2572637*d + 22.25*math.sin(N7) + 6.73*math.sin(2*N7) + 2.05*math.sin(3*N7) + 0.74*math.sin(4*N7) + 0.28*math.sin(5*N7) + 0.11*math.sin(6*N7) + 0.05*math.sin(7*N7) + 0.02*math.sin(8*N7) + 0.01*math.sin(9*N7)
    if body == "Ceres":
        a_0 = 291.418
        d_0 = 66.764
        W = 170.650 + 952.1532*d
    if body == "Pallas":
        a_0 = 33
        d_0 = -3
        W = 38 + 1105.8036*d
    if body == "Vesta":
        a_0 = 309.031
        d_0 = 42.235
        W = 285.39 + 1617.3329428*d
    if body == "Lutetia":
        a_0 = 52
        d_0 = 12
        W = 94 + + 1057.7515*d
    if body == "Europa":
        a_0 = 257
        d_0 = 12
        W = 55 + 1534.6472187*d
    if body == "Ida":
        a_0 = 168.76
        d_0 = -87.12
        W = 274.05 + 1864.6280070*d
    if body == "Eros":
        a_0 = 11.35
        d_0 = 17.22
        W = 326.07+1639.38864745*d
    if body == "Davida":
        a_0 = 297
        d_0 = 5
        W = 268.1 + 1684.4193549*d
    if body == "Gaspra":
        a_0 = 9.47
        d_0 = 26.70
        W = 268.1 + 1684.4193549*d
    if body == "Steins":
        a_0 = 91
        d_0 = -62
        W = 321.76 + 1428.09917*d
    if body == "Itokawa":
        a_0 = 90.53
        d_0 = -66.3
        W = 712.143*d
    if body == "Pluto":
        a_0 = 132.993
        d_0 = -6.163
        W = 302.695 + 56.3625225*d
    if body == "Charon":
        a_0 = 132.993
        d_0 = -6.163
        W = 122.695 + 56.3625225*d
    if body == "Tempel 1":
        a_0 = 255
        d_0 = 64.5
        W = 109.7
        Wdot = 211.849 #deg/day?
    if body == "19P" or body == "Borrelly" or body == "19P/Borrelly":
        a_0 = 218.5
        d_0 = -12.5
        Wdot = 324.3/d #deg/day?
    if body == "67P" or body == "Churtumov-Gerasimenko":
        a_0 = 69.54
        d_0 = 64.11
        W = 114.69+ 696.543884683/d


    R1d_0 = np.array(((1,0,0),(0, math.cos(math.radians(90-d_0)), -math.sin(math.radians(90-d_0))),(0,math.sin(math.radians(90-d_0)),math.cos(math.radians(90-d_0)))))
    R3a_0 = np.array(((math.cos(math.radians(90+a_0)),-math.sin(math.radians(90+a_0)),0),(math.sin(math.radians(90+a_0)), math.cos(math.radians(90+a_0)),0),(0,0,1)))
    R3W = np.array(((math.cos(math.radians(W)),-math.sin(math.radians(W)),0),(math.sin(math.radians(W)), math.cos(math.radians(W)),0),(0,0,1)))
    R1d_0T = np.linalg.inv(R1d_0)
    R3a_0T = np.linalg.inv(R3a_0)
    R3W_0T = np.linalg.inv(R3W)

    R1T = reduce(np.dot, [R3W_0T, R1d_0T, R3a_0T])
    return R1T

print(get_rotation("Despina", 800000000))



