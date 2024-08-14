"""This module defines constants that are used throughout the project"""
import os
import string
from enum import Enum

# Colors
BLACK             : str = '#000000'
RED               : str = '#FF0000'
WHITE             : str = '#FFFFFF'
SKY_BLUE          : str = '#61ADFF'
MED_LIGHT_GRAY    : str = '#999999'
LIGHT_THEME_DGRAY : str = '#888888'
LIGHT_THEME_LGRAY : str = '#AAAAAA'
MED_GRAY          : str = '#777777'
MED_DARK_GRAY     : str = '#555555'
LIGHT_GRAY        : str = '#DDDDDD'
CONCRETE          : str = '#E1E1E1'
MILK_WHITE        : str = '#F0F0F0'

# Fonts
FONT_A: tuple = ('CorsicaMX-Regular', 18, 'normal')
FONT_B: tuple = ('CorsicaMX-Book',    14, 'normal')
FONT_C: tuple = ('CorsicaMX-Book',    12, 'normal')
FONT_D: tuple = ('CorsicaMX-Regular', 17, 'normal')
FONT_E: tuple = ('CorsicaMX-Normal',  12, 'normal')
FONT_F: tuple = ('CorsicaMX-Book',    10, 'normal')
FONT_G: tuple = ('CorsicaMX-Book',    11, 'normal')
FONT_H: tuple = ('CorsicaMX-Regular', 14, 'normal')
FONT_I: tuple = ('CorsicaMX-Regular', 16, 'normal')

# Paths
WORK_DIR        : str = os.path.join(os.getcwd(),               "password_manager")
LANGUAGES_DIR   : str = os.path.join(WORK_DIR,               "lang")
ICONS_DIR       : str = os.path.join(WORK_DIR,               "icons")
DATA_PATH       : str = os.path.join(os.getenv('LOCALAPPDATA'), "PM Master")
BACKUPS_PATH    : str = os.path.join(DATA_PATH,              "backups")
IMPORTED_PATH   : str = os.path.join(BACKUPS_PATH,           "Imported")
SETTINGS_FILE   : str = os.path.join(DATA_PATH,              "settings.json")
DICTIONARY_PATH : str = os.path.join(WORK_DIR,               "security/dictionary.json")

DATA : str = 'pmd.dat'

# Datetime format
WORD_FORMAT : str = '%b %d, %Y - %H.%M.%S'
DIGIT_FORMAT: str = '%d/%m/%y - %H:%M:%S'

# Tkinter events
MOTION     : str = '6'
MOUSE_ENTER: str = '7'
MOUSE_LEAVE: str = '8'
FOCUS_IN   : str = '9'
FOCUS_OUT  : str = '10'

SCROLL_DELTA: int = 120

NUM_BACKUPS: int = 3
DEFAULT_AUTOCLOSE_MINS: int = 5
VALID_CHARS = string.ascii_letters + string.punctuation + string.digits
DELIMITERS: tuple = ("-", "_", "*", "^", "&", "@", "#", ".", "/", "+", "=", ";", ":", "|", "$")
# Define custom acceptable email pattern
EMAIL_PATTERN = r"(?i)^(?P<EMAIL>(?=.{5,254}$)(?P<LOCAL>(?=.{1,64}$)(?P<FIRST_CHAR>\w)" \
    r"(?P<BODY>[\w.!#$%^&*-+='`{|}~_?\/]*?)(?P<LAST_CHAR>\w)?)@(?P<DOMAIN>(?=.{1,249}$)" \
        r"(?P<FIRST_DOMAIN_CHAR>\w)(?P<DOMAIN_BODY>[\w-]*?)(?P<LAST_DOMAIN_CHAR>\w)?)\." \
            r"(?P<TOPLEVEL>[a-z]{2,63})$)"


# Default themes
LIGHT_THEME: tuple = (LIGHT_THEME_LGRAY, BLACK, LIGHT_THEME_DGRAY, BLACK, WHITE)
DARK_THEME: tuple = (MED_GRAY, BLACK, MED_DARK_GRAY, WHITE, LIGHT_GRAY)


class Overwrite(Enum):
    """Defines overwrite options"""
    NO_NEED = 0
    YES = 1
    NO = 2


SETTINGS: dict = {
    "language": "english"
}


MASTER_PASS_LST: tuple = (
    "fSD7^&=+?\"8iLL@Kuw~DqcKud?g8Gg~7wRLd`SMO~z\"ZP:W9?tK#0nEJ.{Hm'4>V'?yNwWqVKZGI=DQlND(5A",
    "YZ0cg7E6,DN99H6oAFYBAjIyUL2:75i0J49d*:8=74b2bQA2830i9U4WY*y\\HqOo,FdFEoEp56F17+67hrVV25z8",
    "iTK&hP?uk%HOqR]j7Ry=XXWs)'vbmu^LiUY/jjAZ^}s,BGJjIw1EQ\"O8axppAbADHIC9XdyYvPzvm(CXn7yKSrQ",
    "i8(W`9VTL=-FVaGx>kTP~W/6E8kIJcr3J+mE3qaSCY(}Q25xgG3p8k1P!M3Lvsnxyz;qd5X8@,4B>,5H4m_H4Jv$_[",
    "BdW5(5Iy<g9_|`V=8vF5XQ76M]a6Ufg0S~}hUmg)!?<&L^cxd!r$,%UC;\\fP#V%~p\",(}dR2P'Bo}FNhc%Hg\"",
    "JpNi,O@4&V4m\"cMx@6Fp'm;3A?2V7j7<N1v8c7d<#9y4B0x471B42eP1EY#28kM1J2V__5Ob;c+9h",
    "rHHh/Bli)MSxAugpQkxG5aTVDJdhwghs0N\\{p6fo$[QK2xOOQo8UbVLVkXvGCn7BiyhmEfJxSi0Cf@F",
    "P43bzU3[t5O&9Bb[7$9F113\"2J2Z5g4eY7GoHhT37zht5@s66;Dv{X7.731)[]798~*x7PiFWG6.D9?",
    "2\\]<+59^Q#8a11(O8`4/4'G@7;Fpyf0z36s0(,%C9\\~R\"@]2Y~?&P4ULX/!$62i}p8w6j58c",
    "30]5Jf703tR8{Ro9D(emE@p5JG{8^5wBS213:65fGK!Z?\\an28O+)LNH|YI:i62c3gm24,H<0",
    "Wc2S%5#]~j{#x+n)>z3P7OS@yi5kktc+<mB76udQXBg>wD2Rw.13@%.f(V\\O`EsU63WttLYdAkI!;WP",
    "%=Yhhq9prq9`^7Ow=,n38_9=vXb/')8!6-~0y1t(9[MA;61d#>9X24Ssm?1;%16z4$N.?p0pV2V#3p[(5!};+2|{H",
    "w05nlceMnvKBR4bmtLYB2rivAsJs~D\\exr7p\"WKQkV]]y!d#QG_QvvcT&caS8nSChTQjkVJUixEiX;bzoYWmk",
    "i4Ng57R{Y3fcH708L/4|LgEi4-6S7Jtq35#.c2Ycbd\\w2T9,0he{vYT82145721OW7l3}fv",
    "723py%81Z219N2i0,4GNB55A9\\]4#y]J&G^7/&d/54[9#$:\\'^%`R>2w?-3g=83,?o01957=985|29!X6^h51@",
    "Ocf9EK503U?5vCRKLo5RKTmLdBNTbTG1GRhGggNxi3W$Zh4nl0EJa4(qpdo/FQK7WBE%mLhzuI8HHE",
    "-U93n0Yhxl5D1683UZwo9364t06DF2v8K-6c5D1h82E2kV222RxzOw50n0N81j37IXo93893d13(CbSzUXXeV6",
    "U\\aDg0.)244&ntBxT2$H6\\A,3X$wLy<EO2K79$RK3<J7s4j?e21jO7w0S17w1ONq9^iXuJG3NLJa67vp",
    "YU1&Qd21O}$gqoYxFSyjp*vtL0dPF}TOa0t1YQywhLVzX5z.X5qsPtk54T.Y1NlQw[b0DW}NI3jc9xz8gnC4+O",
    "6./=0h}g4P89=-y5!=i2}9n1c93_-6lH,4)^]\\5]$x\"7/35I['dw241zb7\"52N1$7(BlTZ08(5?[\"j;83",
    "x4)5bIG4sp5ZojT9/?C*(D8AVlpgM+{\\DbQ6L_63XKcH80t~L[{NN/00Y489-16OB+RAE6q",
    "5^/#G9U2[28.Iw37:<+z!5)k\"7q9;j<-H/F[7>7G\"2'5623138oY.)0m+~(e&jRA/c8:n}\\2`qq73;",
    "~A02[|2erb2Y<4Sprggp0[1MR^8cpw1=y#B8v73)J8$1t`g;E3504^a*=XG4O9kk3q;T3d42b0,w7GjZ57HM1fJ|Wb",
    "?XBS990rk2?72OS[x2O3341`9Y5az,xO#Msf3P>T6!{FW6\\ZEWNJGiAF0Ll.3e8IdVFU18",
    "y63oa>X`0cjU3=t3X,)01|Q*w3954-=]S715l?vONN*Yvz_McexPY7507k(;6dF092<7W3dAl78U911W`90FP",
    "wHc5?2X7EzC5Rg5376BF~L565QX1j1XD1<Zf94%tci@cl5IX13>91i7dU11nW3S61-2\\ot_11V=/N3{",
    "2dTJ4L97S&es45Z0e|5@sWM8C2F]C<\\kA,8805D)x5+52sOPA`9F`uramT2HJ_uM8t2ya5dQ<k0(EAQY91",
    "g8b81X-N+G&-3ve&9Q[Dbn@-izjJVzypJfq+gc5*kgc>3mr^(]+jv#46C~qYAhToOD&Z$6",
    "gPjb2~yigAwmhM(Iywps3U2Vkeb8yn&A}nPYJ#Mo3tShusUG*|<lKTiDqqn4SMq2GoPW52c3i9VsZgaoik4nE/p",
    "RzMIXBftjdlGIoYOS\\&'sCXMfp:fudrOtY6[cYJtsvh;ZFtnfuWP:+ImRVGi9ZAl5lQTmfAFZYkw\")Cl",
    "04XMF%a#n^mSQ@FpKy9lST$<4(`^i0q0f6nF30=334m$G1/Sg1YE~86z6Wrrhnsr0mP435$",
    "T3#eA@g0.QAb?9;!Ipz?1CX1mZRwu,^A.?2Tb0:&38f97sp%|h{^rU>IOtjOpf\\${-0M9aZq6r7}s[1404A*8,q(+",
    "\"oZK!fPZ2V\\Umsn\".{GccE`gZtt+o6OkZdmZ}LErQ-&MXttvH?Z7Sz$S+\\:/pie;\"o?Tv/",
    "sIA7*~<%a1@58r-0p5<A:A?8}A9QG9@s)2(5|O60P=XEx4BcC<L}3TW8Q6Hx%NX4!fn[(6L;23P_M*rR]'F>",
    "CgG<\"d:2/PG%aAo/([r)MF{Okf<!'{8+WQ(Kd.vN5,)P1RnR287*TzE%uG.nu9As#R\\ac+SK&T0/5f",
    "Gxdv2z990d1N89KK{59701B?8Ua!49tw356}pk3m24z2t2q57t29k1wMn29Ph>6rP2u088ZW",
    "ysKi,(mJAyMM<3HLK&YOl@X236VM.~(6>xtHTpWFXu69JFbPza4JY8^G96H&SNimLKnXf<%S,Ff=",
    "944=18<~>48(_K$L180+k'os[oN782U*1T7E7:K<l~^'7DSv08,X;4)I`2L1'kY4~5ZuGI0D097022[05Fm_7K4",
    "h9186417<,517)3#009?2I8}76/?B6}41'.)1#44)3?9\\<`JU97#6-0(3r86U%)>5H0O!0^>",
    "1Z1573sF9JOzPN12HbECel0727GVwH71lzvse83ra9ZKMQYgQrs9yS76K5pVvfF,3/fdA41R{L0Uvex8G8",
    "M8IcggdA]mEf'U6MW4\\R`j&1Y8G*^Q%btyB4_S0\"q#fL.]ZOleQDDKzt29vUvqB3^gitATIe$3qso/0R-RK4O|c-U3",
    "P68572{-94:53(S33]0H6%/22-vq(8$E8955tILm697O2=5`._`[;)%?86<97o718<2:Y(70",
    "jVc$QZlHcFkE/+l).kTN#gqdjK)}\\b)>nSFDF#Nt4VgDp'<o~*ntc$c!<*'ms-/F<MNy4p,]\".A=t$\\C4A:`jc^Cq}",
    "Dczr(|MK(Uh8kGy@nto5&xPuAQ\"!oz<)rb('6fHf7|UPj=xp7Wk6qxUIpDE1ZH6[1Dtn)CS4K5",
    "s1qs8136&VE38g91;A;h21w9R;0A%L5*Wm9623`g153l7qV3nP1e4M09160G663xrQR01Tt",
    "2}Ta.704}1m1.iBY10:3)0~P6V|#3<{[868!3c3`M26/UH87~)0,DU6*0L5k8444]~480=b-1E83192:61,4h4/12f",
    "0%ue)7\"TiiNgO79Kwl:u:z#5nO(Sf)3IcApA30t-x6:o@qkNdx>?Y3#ZwH0r58*ABt5$O=Kd;8mF+NHy:",
    "_b&b]<82;`KO5'MAa$o\\IIv!px70r22?N*#5,FM_H8Sr8@;pXWi57-NC3\"0%d7<M57O9z1Sz67sB2'2bt2HIq",
    "m=5{31e`0zbq@x;GLl9j056f{K9$^q1Ag4&MPu1IrSWr]if<LU|}caO?7naSu3B6<{`6ePa]_1/=)3s72Z%%$|3fZT",
    "dm}5L.D8y!\"tMPG^0HrR6(0KH$$EV$u;G?0h.-cSQC;LJ6r6huT2$ms;g2v;[t1.E9q(4#(]ur1~GTJxfLm6h"
)


PASS_LST: tuple = (
    "3x4XVqPY0483Ue73gPvXBz4Q5Z+,da9p8AlF\"lH4XUgIy87)w6ldf2aKg6GbP82qjbXq]1!J3Q%Vj9Gn3r~YDZ0cmC",
    "43h-4360Y3659]=-03=`71$29L2[P9D+<H0&*cN455443B783,8%ef8|H9'Z8C\\|5@j8Wc{40",
    "M94=HBiKV?pl64H8z^k5D#S'VtRc+U6!\\B`wW?L^P0mp70~P)zzlf6zCT!Y1ZbG8VGbHvwCs'M9{}d",
    "!$Ba;(m7O\\(Aq3#ter/>rnN02Rs`o%qq6gPNLBy),.w%DcBjHOa^qmR==Q=Ybb;EVP/&+|)X4eWM#2w]",
    "B{`[o5bH5_<B%h233603W4<U)'|5\\876Nh03}6z08z7c-R0p4\\hs*2`8.`pG(16Q4G\\X856Lh0wW5^ShQ8jyBq",
    "8?8I&||,,486[k7<wb`<+2713&6(_*97125=_^56+3%9096k?1'3c9_.rqX4?b96^c>>3821",
    "S5$7f183G93>MC`}7-479j=5z\\HmS09mZ813n1C,j65P>]EH79e8kay708u6X7Z68333\\@0d8s283",
    ":2Yu7S0Pj|edkU*$$X88lX`d2TbsGEAb7[6-PVN2<Mv$H5g2mwU|2)bN_w>(e#)J&PF.43a3btc$ya6JcC^",
    "F\"75I=4rl}:YWOckpK)9TZ0Q1c3G11sDj;yX587wOi!19zK.556Ri}qG3t:*qhDhy\\3|T9Q0T`",
    "YwQ2Rd549,208G97X3cWb}9Mdu6BkT0N7a1P2iYG09kP$7L1SVLcs57an3Z!R8uv66K3G4E@0tS428[tH",
    "vya4$DQrAU5ZrtQYxU3Rv8LiMg/}Sq6n.A0vDH1xos0B:3yfWyPMi0<V0yXR2mOoi22bd%",
    "Y31860I1eGkG24Z_+8FA39=,2Lk6J3EaTc8265(lBVS3r0<l3SnUj5Gr_X28^@464i19696*m`99G979{0\\8%g1",
    "7V1[ICufU816=l42U0^',8p4Pa02lN>7sCM0q4XV4%UXl\\9Sud+<6]:D]6f21F?0/5%r\"{!!",
    "6$889x224p|8W1eJRUR3mB/7A98Ft7NWJX06)9w6F95i3brw281w9<2su87niHuNt5n1CxHGI0SY9HB2k7Kov)81k5",
    "8R\"|0x73-75U68\"%c$Z29^06is3l(4._/0!\\=w,Z7n(u5Fr.4@S3HG$N6(~rT@1U7G=z752M%^P6|4%",
    "qse9KLEL/$753sL4OPa5gOd'09cC2q9Rq!YAb-r:Oy1ps5z6f>1^{q8[Qfw,4w3iWX14h9sUk5d",
    "t%UW7\\+9w+U6|;7t8bqro|+L5.69`TKt`@'f]R7Y$Cy20lH:B3._wY|884hsoZLK4;-x\\N|3JDl~(pv0T0/Sg-&N",
    "@CfuUCE[J3MBv5(7nTrrScu<kq2Ge)MHN3bd/NZW7iR;FfhdGGEAG2Y+wOcjp*R!dchj!|Iy3B05Xktu}yxm",
    "98WK7h)i0IRis246147b713684X6tDM6s5yPPZwbzuqAI9r~9oCV9241z2Z526Xq1K88Q99ljf50G@YOb7B507417",
    "3y$82qeO\"TpHnj6dyrX2E=v1NRfqTMx_u5B4B619n61V(bLsShydMnILB=i785QA631kn2923j)vh9X>Yq?8o",
    "W>GULUqBfzJXrU2SrWrI-4(yCUw6G7JJ)DxRnlbflChM1HJU7dbq'0hlqGnkuY0}XqLgpH~dHR9f6w",
    "!l5J2i)f.97>:K19JR3'wOR{jx,7`2[2t08\\_$\"[OX56&4}G1MhXF6q*2{08429,39m0484EPg4\"7G6@",
    "V6k4D436P34A2694yE2D9pg4i$Iu3v*371z1~45OSzuaN5vjgk4^2Ypj6~StOX9A8WyZH7c|u;FH7<7OnH",
    "&=9\\}l173xG59H9h20%43FINj-52`=`49}564^)28_S211F(z-62e2D11g5s35.R7=ZU83L{p|80(u61}1r@.{",
    "Tf`cUn\\/\\w{pEwVS+Bf4kLx5Eb[^,Wy$Jy~4OJ..kHY\\%&VF$HF:6i',}}1fFI`4ru:3H?Fot'/jGIr.+`|;<^",
    "s3QU:!q9z!ux5>0x|^279;9/|DJl;N2Ky36U'p6Q9!5\"^S&\"F<VJ2}2e67x8uM31by8o4Bf4",
    "618v;zN3ByqZVIoff^f3VPBNURCx)PY440n6xlBO39yqE?\\sF\\xZT7ieMZfI9r2bN6toszDQ",
    "zK7RYrJQeP3w092a3\\14616F124_2nm~Dt1nE:139v1yk}>~]w1Sn]IOt-g8ML5se=t,+$?\\",
    "XYucpcrij!NMsJxh%hZmU\\aW^f;2b&m3GZ;3rT5H1PaQ`F91yo%xS|(^xJK9lum)ZgRA@O3npMj$lR_w",
    "6s=VR;'H=CU56&:!9j1!%+!@&I8c\".wSZSX^EMw^i3lp;|)FkfU;%whvc7]/+F;eEGyE(0Vvw39[$25)D'3q",
    "31J373r1k6qI146[6r7aWE85x-UC785b^neST8Hj48Sf802p58Gf^94cJ17aTJAK5h210F37v7h47xq",
    "7qAm\\5g7/s@OWJ!{dr7hB2bjKXJ)rhZBvtQCi%2npp7P.u%!{P#203m`[j8DSr&^YDrHT)3\\%x<P",
    "r^I3Jt%(X3M715828k18FLT813783SM0{470o8$087`9P69I1C82q{w6TfTUT6ioj7WZU76Gl342I1EX61:Z7GZ8Qc",
    "ChnUKBbaNjJXso)BmxWrVzuanyhdtSVLjoT9DoFdy2CVPs1aUI4e_Imcc:7sfKZAPczQ}aXQG1HQTjT5SI",
    "x5hEPnDcO8kzGGM5Sbzqh\"hMEF7BYR867zMbDGsjgO[BjA1pTRIJIlUFh1IUHeCwZXp9ywAdRVNZMGA(mB}psrbE",
    "%!|52740x}73`5&=7%5j54*>'\"q'vg];1J(?|\\1nV>5,c=ms{8Oc5]V0&39.963*70857^92Rb7f;[LR4/.",
    ",2592ONyt823~]9,45&.-\"DuCw{0yP1!\"4(b7]ql,y4@87@+]G0oN>J,4%$Dd;>407;v2A39'",
    "_(p\"cdsx4M6|&1a7Yw<3sh65A1c~8LdU3c1!3u1.3<NWZol4NBBGMj6hHb.YP'zGMQn*4QnfEi6Y?kVU6K7KT2\"=",
    "V4B^%7N4`3=KcR08Wg8*9B|4c);834c<80l6Z36i6vSY/7|557C0SOka9656'V%_5(Vsr#A`?-42M23a+4",
    "9)1B9D77(8;79361vy:rEQ\"/)2;|_,D,ou[(83(6$(Y26*?638(]D95\\6|}9919T96PEy65",
    "DA7&{9j?]^|U=-9l04-DJ2C+U}pv$]Cm93B*g9P>5Y=6Rr_8+w]os(A|16%2d#15-dCs>y",
    "7{IEWT16bu9l%66>eS\\nr1>P*%+%S!''[1j!wT|`'KyR[3ln[[P^)P!9q4!nq41x{(V1H^:5R!'5$60N55K",
    "wn?}<?OhxKSko7J@kVOk3DT$2z6kr-kxv,IJhG9\"FDJmEX6`i8?u60v%xRCd39f'i3xB}iGzPKiB=vYSQWu",
    "~kV=y`P7.&7YN3(/]^~pVh6If$qW@jt0w_Y}/$vSw%Znf%OuY]6:$(gYVsB10sr|F0)}}&t{\"2PP#b/-lzr_",
    "u9mQ95zWw427690I75106+4;&L\\6*1.NT94613U=536%\\;06E9EiaURjrW5q1KH/!2:\"\\12I/12R18^",
    "9QFHUg7P!c8j1Zqa\\FI7_m5O?J{A17=xLCSy08j4AODt&3hc[4@lD>0ZO_)0/wzq]i7gFUrm_[qVTrT2i>scj[cO",
    "\"(D8~2}#,'\"=n*8/6152435;!x2|76!dIXj68#0?7K86`b17<9428;1D}m\\0C(>}y215528f|9/{]883|7@",
    "9g99$4y$EYi3r,6f245n3D31a171I4nMW^378wpd8GK2Dlw/`618z6m521\\5;XdR99c&URH7GhC$6539:Kfeu9",
    "Q)gK8Z9wow{bInw]~^C+~%~Kg\\WP&_Wi8rQJ)u%UW@Jgcic/QG!!54M_/DclTXMY]gqZmekQTO",
    "5Fs?}DVn79aiD<RXEtHNgXAD=pM+:3r)<A`,~/vA.cS\"%KQM%ZQ$|,d9i+5dRreQn_GHoFbgaSX/",
    "ndL0edSmypmcHu4RKbrJLUGZWi8ZsyXQ/PhM?PAKK$<yzH%MQqvbzEflGQGfpUdWJpO:uB~QyzSqBPBGWETEZwUtT",
    "f)-z1v<V=f#E;&9c]&F5x$~YByPWI$3@H,8?0&}xWVdyY5/+3I]j]{#_OLR%cHwA276;h\"p^sIpyFXC+5M<84w",
    "Fwz19(96Jp0rdOSZ60w}R9M9'$9nBz!UKpUiqz58ZK6`SjPvO73tbkzuBcGH0.HDCCZo7PZyEmL'wZRcr8",
    "1]F66>99V24[ENB\"85i49|/5IOk06E482\"L9Jmg2082B77)=!CKg929_`Dt53;/h^2fq7)",
    "$17c,].0??)5621_8l17tSWAhH}58+38]IS=f=34#nlMlR066Y4AR8uM:E9095s56V646+70/849~9^s",
    ")iw#Dd02hTxEE)Ds9G@FlalC5R3Q*zi81[9M3vMk7uRsMRyJ87asiZs8^I7m773L+0m|0W}u9^}x",
    "^P%5sgm}Q(UGH{`;Mi;qb^l_gakZ/\\;H\\S\\.GNg}\"MT]ZK[,5blC\\mmxXaAFUx?s.ILVzUrJ@$cBpAjePL",
    "?0`1b:1n19R+418T683:\\,5u5C)8y-1;i6)%^6+KL.#]>\"6>u9^5}=c(X\",082R1xbz5^473;2,\\v^",
    "h^Qq!A^uyoe}pZx:m3XTIzYsO9jn@CPebx?Od`M0H%;uos!Fy-$>WX-mLe^b|rv}7InZEf%Zv@kTm",
    "ynFKg5cCDZfSi9^QTPBR6wtrwK.K00i7pO2Vp6Z1556+b5784)UB2FZbCFxj(aYR278jEM011`@",
    "R=Z<C{4eEm3$P25XNyJ39iz$GyoPVS8uIe9jE0^mCeF[_'7o*9Zjnu49vg!f}t/U5mqhv/w/gsL76BR",
    "8Up4OL1YRBEI0q3Uh3kPXd4Qos7Vzuvr899n9gCT7Q8Tkr90EhTfN5Dg^Av;jpZVCwTEWUF}mFRKCju0lthyegBa",
    ":5MH:VzX?f0UNSPz!2mS1kp'os3)UuuA*ofXE%|MzC|fpkT.Ppkk\\~YnfT>7NPw5Z|}HJM1AJg",
    "Jg|M'%6~(39D3p@P&j1)q7/6un=^:6*198770#=8y7N5:5G8^B(@7ck#g1gi6,i;91U;}22}mGJ9]{Y1/w4^Xj)g",
    "Dv+b&u$bywt&*[n&$km:u`Ppl<;jTfw][V$D!(DL1lv{qwHOc\\?~?oIwqA(R%xaQ4pU^P%%e=%wbdO",
    ";{:l8<:89124wF*XHGZ:&n7i,r39w^fK4\\pIH3760\"625nw=8k0Qw4_8nO,20y5P2eHL4Ss1Y7!,i0Pl9k5c#R00b",
    "cB5D6s?1p,WELfR#3QQ2ab7i7pOXKH>6k4leSTSj002tCSFvr*WLM3A\\ON4e_w0B{41W8LKV2o2C",
    "\\LDfhpejA(S31nvFMeMy\"3S[Y\"hB%O2jT4Pv2(l~ZWUof$/Iv>4Ph*GhmU2R2ibtfWaC/p%XSKXRyKgv=GFj|PH",
    "T;ev_c.H9eY'5'7Y6zI0QqDP59'djDW4w9J\\e6M8Ya9DdLp4YK05zT9Y9Uv*wrhcqyq91SyS90iO2tla_a",
    "2OK?s2PY6(oqKshuP/B`049[SnjJ6V~t]S7}:Pi{\"PI)8_X0zT1]n5jZVy\"06:XYNmSGzO=G*!uF51?jjF&/P4",
    "a@cmez6';M_uHqsynUu1[BQSGHo\"=zDKlS^OxT`[-R\\})gF<NTPDXf(H>jhveBewE5Mop5D'xdbN",
    "#pU}7WOcFejcotz=yO(l/8rLuafge!vr5l[8h:L'8sK)MQ>99lZzWZcIIRW\"7v)^J17Jbe?l4E?ddj;@6L<BA",
    "IY68/'IhS^|:d%A.jW)vJ=VwP2v:/TNT\"BD#bqNigSM<~)u3z,-%Rf#tL|))<js-E,lQYGMnGq>I^>C]5Wx-?+U",
    "BJi#L3h8%a6XS[Zu7L7KHg21tnZA=0z0NQ77\"lYmzNCx328mIckuslt<4CxRZ649ySP5adY6Op23",
    "UM%Gs8RDTVqf3KAGl1Mu6dYuNJ4c\\TFhMByHPI2qRukZecqT710v\"NMZ29u38Vck24SrW2llXcfraZkRoYZqk",
    "90\"*G<0*B5=a2nhr6=LgNOB.fXCW3x-+F{#gf}Z%k2e:s0c0T?+YU^<B0hDqTxPh\\<-7O.$I|IvvP5",
    "fPW!fxm`hcwe-rb9UfysYw]Av1lzRBVt2TISJ]mYF^WfDGv5IdU*PORvE#gt'IKqN3GkcsIwLqRFEolIslz",
    "fD2H5c8Wr53Rl83[d85j8j>5'F67E7Ozy0tuk7v7H8EI3AczTWbVBNK068UG7wTNUy6r9YP643x2",
    "62/y9g<6[9uO25K7579hPpV+3#$v9JD5;5T[G3HQaWHhy52v98NY9s4K9`-c6Fj0GD(-7DTNk0t",
    "9=v6+?8,#>j7g1W8A@2}6139u=lX3j4RU4$(3ci07Rl]41]9=46e8j5k5W71^k264]3%39~2Y82Ve^NQ504{7r22",
    "3;UJ2<j%I*7=x?2/Q1qE_5ANgn1N6a9}`f-}7!^QH&@(6n9%8[^Ga0h4{87{p$M]w7=4}I3439",
    "fdxn0+iLLAs6hShwouTT*\"8HzSLZ1Vh_Yfqq<NPxjhA3PDp91aFH8FmCpuAjumODTULJ\"xOW_9q5KZ4dFfAt0JkFEF",
    "U9n12FcIEDwIIkT43vb1$nWa811d9v6pRxZv]6V3zm50tWU67Xs1\\V6qtb27}Fhyi9MMmgbm38Q|rwENI\\;yu2i:",
    "EhK?n8=1eZ)$C69~^J1}Y<r5^57]/!Y!2h9)hzDpA{0yeKaTB93u.//r6bhKo0nI'6a\"p\"<|%tT",
    "+6Urq/YpX9;H68XoD+f2qZ9TAf7+6913W8tJa7368oal5g5EpP_95rnZUk07O9HNflA2n6$?)r\"(svUqPNa",
    "5Dg5udo]3R}72$HR162}I6bdHa8]1ZM3es_lg8Q1XMeh9Z24407735fu5dK4'lE8yp54Nf8jPk",
    "IUlB]50A00SeYa*0G!,y>WN0E1{g>_Wvuml3exI8%3?IOu@222\\}2#\"`{774)u}GG007O[:#8\\2Gj|9j^\\V",
    "53X5U[r5zQ5v3+/7C1-46~8@50^s736'85F6EX=82[<-|V8439-oE{*375n5w30f917XY06DZ48^7n@",
    "{7B6Gyt/&n46079(6|f)36^!a&7363_s0OS4V78,C!0_8r6$jS/BQ~M[48#0j70p3|1}'E5'037}s>98Xw",
    "v{zAYu8U4}TLe|zQz8q~pb^J3RY'18)9HQtG34YErJjR9.Qk6UCEl7p$,jT~by6ptdXax?orn6*:5e<%wzuzG9Q",
    "MlTxxVBI5wmDCkCRfZP7`oheXZyj6Oe[MXc\"@%risJH)yLQ:*ck{&)(YZX44CnDjOdsjforFHwf5xyzjtiBFqH6#;6",
    ";\"oBwSvaCd0NiyLNecAcwua`KxkALbUN:M)5H'juf82\"$zGbyBvrBpSO{#inJi6Ktpf`2*F2PVdnUV>Lnw3G8Kp",
    "OK2SfVM06el^440tX2aqIW0FbN1xJsrbWlvVKgKM1LhD4u9DKLPOwfAGOfEc'rkKaw4yvL",
    "PnB2115F7R8050Z7:'@(7wOAEcoaw4C3@6^9_P7@1t0:D>iZOZl3/x2.6=D0@\"67B3u9-C79lupB1v20",
    "jhfo2WTtF6epWc4DRdXNzKSBUi`uFAAY\"zoCayhjov\":NRDgjT_h|NEq1m~GKhERgKo<sqSehkGbj",
    "E|b:\\Vd<656\\l6D92hix'm=W/H7?(1\\4Z9A99j)10#E8M:\"T35S0>%0]Ea49SPGepj{3'6=P'dBQeEw@62Q",
    "QZKevnauPSC=kXk9Ef~dfYlBCkHx$TZRlvCzo=%(NBYGGUz3ohrNdZVz[IqnT{Lbf~WlEc9F",
    "*n]ZSmK\"ga}RPIq$voT.(MeqQjroq?YkC[>L5QaU\\mUO`jpQl\"OhkNcgK:XT\\\"qvWPYp9b.^JsjYPZq4zdn",
    "eC|5:I1:6I~l)6E2o^m1}R21!8>72(6k;J2dZ<wG8]Z0x0a72BbZ9I*7Wa7,~4w0F6^7rW_V2_XT9P620l-68",
    "a:<1]Dx636C{Y98iv7E;YL,Z;I?#%|uj3WU8PG3}K13Uhv6ng\\o5jfN37^ev)BI3Py7wpPy9x(sXC"
)

CODE_CHARS: dict = { # coding_words
    "a": ["a", "A", "4", "@"],
    "b": ["b", "B", "8"],
    "c": ["c", "C"],
    "d": ["d", "D"],
    "e": ["e", "E", "3"],
    "f": ["f", "F"],
    "g": ["g", "G"],
    "h": ["h", "H"],
    "i": ["i", "I", "1", "!"],
    "j": ["j", "J"],
    "k": ["k", "K"],
    "l": ["l", "L", "1"],
    "m": ["m", "M"],
    "n": ["n", "N"],
    "o": ["o", "O", "0"],
    "p": ["p", "P"],
    "q": ["q", "Q"],
    "r": ["r", "R"],
    "s": ["s", "S", "5", "$"],
    "t": ["t", "T", "7"],
    "u": ["u", "U"],
    "v": ["v", "V"],
    "w": ["w", "W"],
    "x": ["x", "X"],
    "y": ["y", "Y"],
    "z": ["z", "Z"]
}
