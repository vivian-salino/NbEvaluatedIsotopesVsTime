import numpy as np
from scipy import optimize
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import os

Release = {}
NbIso = {}

#---
#  Data from ENDF-B/I to VI.8 (United States)
#---

# https://www.nndc.bnl.gov/csewg/docs/endf-manual.pdf
# Appendix I: A History of the ENDF System and its Formats and Procedures
NbIso['ENDF-B/I'] = 58 # "The evaluations for ENDF/B-I were taken from the existing evaluations of neutron interactions for 58 materials"
Release['ENDF-B/I'] = 1968 # "Version I of the ENDF/B data file was released in July 1968"
Release['ENDF-B/II'] = 1970 # "Version II of the ENDF/B data file was released in August 1970." Compatible with ENDF comments (August or september 1970)
Release['ENDF-B/III'] = 1972 # "Version III of the ENDF/B data file was released in late 1972." Compatible with ENDF comments (1972)
Release['ENDF-B/IV'] = 1975 # "Version IV of the ENDF/B data file was released in February 1975" Compatible with ENDF comments (REV-JUN75)
Release['ENDF-B/V.2'] = 1985 # "Version V.2 was released in January 1985." In ENDF files, it says "endf/b-v.2"
# https://www.nndc.bnl.gov/endfdocs/ENDF-102-1970-1.pdf
# BNL-50274, p.163-165
NbIso['ENDF-B/II'] = 26 + 25 + 10 # = 61, which is also output of ENDF.sh *AND* verified by scrolling
# Output of ENDF.sh (verified by scrolling)
NbIso['ENDF-B/III'] = 133
NbIso['ENDF-B/IV'] = 90
NbIso['ENDF-B/V.2'] = 18+4+11+6+3+2+7+20+8+7+2+5+13+3+3+3+9+1+1+1+1+1+1

# Nota for ENDF-B/VI.8. https://www.nndc.bnl.gov/endf-b6.8/ states:
# "Neutron sublibrary contains data for 328 materials, out of which 13 are
# elemental evaluations and 315 are isotopic." It appears to be plain wrong.
# We found 329 materials with 16 elemental evaluations (C0, Mg0, Si0, S0, Cl0,
# K0, Ca0, Ti0, V0, Ga0, Zr0, Mo0, Cd0, In0 ,Hf0, W0) and 313 isotopes (H1, H2,
# H3, He3, He4, Li6, Li7, Be9, B10, B11, N14, N15, O16, O17, F19, Na23, Mg24,
# Al27, Si28, Si29, Si30, P31, S32, Cl35, Cl37, Ar40, K41, Sc45, Ti46, Ti47,
# Ti48, Ti50, Cr50, Cr52, Cr53, Cr54, Mn55, Fe54, Fe56, Fe57, Fe58, Co59, Ni58,
# Ni59, Ni60, Ni61, Ni62, Ni64, Cu63, Cu65, Ge72, Ge73, Ge74, Ge76, As75, Se74,
# Se76, Se77, Se78, Se80, Se82, Br79, Br81, Kr78, Kr80, Kr82, Kr83, Kr84, Kr85,
# Kr86, Rb85, Rb86, Rb87, Sr84, Sr86, Sr87, Sr88, Sr89, Sr90, Y89, Y90, Y91,
# Zr90, Zr91, Zr92, Zr93, Zr94, Zr95, Zr96, Nb93, Nb94, Nb95, Mo92, Mo94, Mo95,
# Mo96, Mo97, Mo98, Mo99, Mo100, Tc99, Ru96, Ru98, Ru99, Ru100, Ru101, Ru102,
# Ru103, Ru104, Ru105, Ru106, Rh103, Rh105, Pd102, Pd104, Pd105, Pd106, Pd107,
# Pd108, Pd110, Ag107, Ag109, Ag111, Cd106, Cd108, Cd110, Cd111, Cd112, Cd113,
# Cd114, Cd115m, Cd116, In113, In115, Sn112, Sn114, Sn115, Sn116, Sn117, Sn118,
# Sn119, Sn120, Sn122, Sn123, Sn124, Sn125, Sn126, Sb121, Sb123, Sb124, Sb125,
# Sb126, Te120, Te122, Te123, Te124, Te125, Te126, Te127m, Te128, Te129m,
# Te130, Te132, I127, I129, I130, I131, I135, Xe124, Xe126, Xe128, Xe129,
# Xe130, Xe131, Xe132, Xe133, Xe134, Xe135, Xe136, Cs133, Cs134, Cs135, Cs136,
# Cs137, Ba134, Ba135, Ba136, Ba137, Ba138, Ba140, La139, La140, Ce140, Ce141,
# Ce142, Ce143, Ce144, Pr141, Pr142, Pr143, Nd142, Nd143, Nd144, Nd145, Nd146,
# Nd147, Nd148, Nd150, Pm147, Pm148, Pm148m, Pm149, Pm151, Sm144, Sm147, Sm148,
# Sm149, Sm150, Sm151, Sm152, Sm153, Sm154, Eu151, Eu152, Eu153, Eu154, Eu155,
# Eu156, Eu157, Gd152, Gd154, Gd155, Gd156, Gd157, Gd158, Gd160, Tb159, Tb160,
# Dy160, Dy161, Dy162, Dy163, Dy164, Ho165, Er166, Er167, Lu175, Lu176, Hf174,
# Hf176, Hf177, Hf178, Hf179, Hf180, Ta181, Ta182, W182, W183, W184, W186,
# Re185, Re187, Ir191, Ir193, Au197, Pb206, Pb207, Pb208, Bi209, Th230, Th232,
# Pa231, Pa232, Pa233, U232, U233, U234, U235, U236, U237, U238, Np236, Np237,
# Np238, Np239, Pu236, Pu237, Pu238, Pu239, Pu240, Pu241, Pu242, Pu243, Pu244,
# Am241, Am242, Am242m, Am243, Cm241, Cm242, Cm243, Cm244, Cm245, Cm246, Cm247,
# Cm248, Bk249, Cf249, Cf250, Cf251, Cf252, Cf253, Es253).

# Nine of the elemental material (C, Mg, S, K, Ca, Ti, V, Ga, W) can only be
# represented as such. Breakdown into natural abundances are not possible, due
# to lack of natural isotopes. But six elemental materials (Si, Cl, Zr, Mo, Cd,
# In, Hf) are available both as such and also for each natural isotope.

# A few isotopic breakdown were released later, after the elemental material :
# elemental Si and Cl were released in ENDF-B/VI.0 and their breakdown in
# ENDF-B/VI.5 and 8, respectively. But all the others, i.e. a large majority,
# were released at the same time, in ENDF-B/VI.0. The only possible explanation
# is therefore the (real) intention to offer both possibilities, not meant
# as a supersede. It can only be seen as a "convenience" they wish to offer.

# Output of ENDF.sh
NbIso['ENDF-B/VI.0'] = 320
NbIso['ENDF-B/VI.1'] = 320
NbIso['ENDF-B/VI.2'] = 320
NbIso['ENDF-B/VI.3'] = 320
NbIso['ENDF-B/VI.4'] = 322
NbIso['ENDF-B/VI.5'] = 325
NbIso['ENDF-B/VI.6'] = 325
NbIso['ENDF-B/VI.7'] = 325
NbIso['ENDF-B/VI.8'] = 329

# https://www.nndc.bnl.gov/endf-b6.8/index.html
Release['ENDF-B/VI.0'] = 1990
Release['ENDF-B/VI.1'] = 1991
Release['ENDF-B/VI.2'] = 1993
Release['ENDF-B/VI.3'] = 1995
Release['ENDF-B/VI.4'] = 1996
Release['ENDF-B/VI.5'] = 1998
Release['ENDF-B/VI.6'] = 1999
Release['ENDF-B/VI.7'] = 2000
Release['ENDF-B/VI.8'] = 2001

#---
#  Data from ENDF-B/VII to VIII (United States)
#---
# Output of ENDF.sh
NbIso['ENDF-B/VII.0'] = 393
NbIso['ENDF-B/VII.1'] = 423
NbIso['ENDF-B/VIII.0'] = 557

# https://www.nndc.bnl.gov/endf-b7.0/ : "ENDF/B-VII.0 has been released on December 15, 2006"
Release['ENDF-B/VII.0'] = 2006
# https://www.nndc.bnl.gov/endf-b7.1/ : "[...] released the ENDF/B-VII.1 library on December 22, 2011"
Release['ENDF-B/VII.1'] = 2011
# https://www.nndc.bnl.gov/endf-b8.0/ : "On February 2, 2018, CSEWG released its latest revision of the ENDF/B library, ENDF/B-VIII.0."
Release['ENDF-B/VIII.0'] = 2018

#---
#  JENDL data (Japan)
#---
# https://wwwndc.jaea.go.jp/jendl/jendl.html
NbIso['JENDL-1'] = 72 # "Number of Nuclides"
Release['JENDL-1'] = 1977
Release['JENDL-2'] = 1985
Release['JENDL-3.1'] = 1990
Release['JENDL-3.2'] = 1994
Release['JENDL-3.3'] = 2002
Release['JENDL-4.0'] = 2010
Release['JENDL-5'] = 2021

# Output of JENDL.sh
NbIso['JENDL-2'] = 181
NbIso['JENDL-3.1'] = 324
NbIso['JENDL-3.2'] = 340
NbIso['JENDL-3.3'] = 340 # Slight inconsistency : https://wwwndc.jaea.go.jp/jendl/jendl.html website says 337
NbIso['JENDL-4.0'] = 406
NbIso['JENDL-5'] = 795

#---
#  JEFF data (Europe)
#---

# https://www.oecd-nea.org/jcms/pl_36766/index-to-the-jef-1-nuclear-data-library-volume-i?details=true
NbIso['JEF-1'] = 3*63 + 3*35 + 1 # p.6-7
# Title : "Index to the JEF-1 Nuclear Data Library, Volume I, General Purpose File (July 1985)."
Release['JEF-1'] = 1985

# https://www.oecd-nea.org/dbforms/data/eva/evatapes/jef_22/
# "The current version of the general purpose library was released in January 1992."
Release['JEF-2.2'] = 1992
# https://www.oecd-nea.org/dbforms/data/eva/evatapes/jeff_30/
# "This general purpose library was released in April 2002."
Release['JEFF-3.0'] = 2002
# https://www.oecd-nea.org/dbforms/data/eva/evatapes/jeff_31/JEFF31/index-JEFF-N_1.html
# "JEFF-3.1, Contents of the neutron files, Date: 4 May 2005"
Release['JEFF-3.1'] = 2005
# https://www.oecd-nea.org/dbforms/data/eva/evatapes/jeff_31/index-JEFF3.1.1.html
# "The JEFF-3.1.1 neutron reaction file has been updated in January 2009"
Release['JEFF-3.1.1'] = 2009
# https://inis.iaea.org/search/search.aspx?orig_q=RN:43056224
# "JEFF 3.1.2 - Joint evaluated nuclear data library for fission and fusion applications - February 2012 (DVD)"
# "The JEFF-3.1.2 version, released in February 2012"
Release['JEFF-3.1.2'] = 2012
# https://www.oecd-nea.org/dbdata/jeff/jeff33/
# "JEFF-3.3 was officially released on November 20, 2017."
Release['JEFF-3.3'] = 2017
# https://www.oecd-nea.org/dbdata/jeff/jeff40/t2/
# "JEFF-4T2.2 (22/02/2023)"
Release['JEFF-4T2.2'] = 2023

# Output of JEFF.sh
NbIso['JEF-2.2'] = 313
NbIso['JEFF-3.0'] = 340
NbIso['JEFF-3.1'] = 381
NbIso['JEFF-3.1.1'] = 381
NbIso['JEFF-3.1.2'] = 381
NbIso['JEFF-3.3'] = 562
NbIso['JEFF-4T2.2'] = 564

#---
#  TENDL data : "2800 isotopes living longer than 1 second"
#  https://tendl.web.psi.ch/tendl_2021/tendl2021.html
#----
for year in list(range(2008, 2015)) + list(range(2015, 2023, 2)):
    Release['TENDL-' + str(year)] = year
    NbIso['TENDL-' + str(year)] = 2800

#---
#  Prepare the graph glitter
#---
def tex_fonts():
    tex_fonts = {
        # Use LaTeX to write all text
        "text.usetex": True,
        "font.family": "serif",
        # Use 12pt font in plots, to match 12pt font in document
        "axes.labelsize": 12,
        "font.size": 12,
        # Make the legend/label fonts a little smaller
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10
    }
    return tex_fonts
plt.rcParams.update(tex_fonts())
# https://matplotlib.org/stable/gallery/color/named_colors.html
mcolors = matplotlib.colors.TABLEAU_COLORS
green = mcolors['tab:green']
blue = mcolors['tab:blue']
red = mcolors['tab:red']
orange = mcolors['tab:orange']
colors = []

#---
#  Combine all the data to be plotted
#---
evaluations = []
years = []
NbIsos = []
for evaluation in Release.keys():
    print(evaluation, Release[evaluation], NbIso[evaluation])
    evaluations.append(evaluation)
    years.append(Release[evaluation])
    NbIsos.append(NbIso[evaluation])
    if evaluation.startswith('ENDF-B'):
        colors.append(green) # As in ENDF-B/VIII logo : https://www.nndc.bnl.gov/endf-b8.0/
    elif evaluation.startswith('JEF'):
        colors.append(blue) # As in European flag
    elif evaluation.startswith('JENDL-'):
        colors.append(red) # A red circle against a white background, as in Japanese flag
    elif evaluation.startswith('TENDL'):
        colors.append(orange)
    else:
        raise NameError(evaluation + ' is not a known evaluation')

#---
#  Plot and apply some more graph glitter
#---
ratio = 20 # TENDL subplot represents one over...
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,
# https://stackoverflow.com/questions/10388462/matplotlib-different-size-subplots
                               gridspec_kw={'height_ratios': [1, ratio-1]})
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
fig.subplots_adjust(hspace=0)
# plot the same data on both axes
ax1.scatter(years, NbIsos, color = colors)
ax2.scatter(years, NbIsos, color = colors)
# zoom-in / limit the view to different portions of the data
ax1.set_ylim(2790, 2810)
ax2.set_ylim(0, 850)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()
# Add cut-out stanted lines
d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                      linestyle="none", color='k', mec='k', mew=1, clip_on=False)
slant = 0.2
ax1.plot([0, 1], [slant, slant], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1-slant/(ratio-1), 1-slant/(ratio-1)], transform=ax2.transAxes, **kwargs)
# For TENDL, only one ytick : 2800
ax1.set_yticks(ticks=[2800])
# Have also ticks on the right axis
ax1.tick_params(right=True, labelright=True)
ax2.tick_params(right=True, labelright=True)
# Add an axis label
ax2.set(ylabel='Number of materials : isotopes, natural elements, etc.')
# Let the future outside the figure (otherwise, that would be presomptuous)
ax1.set_xlim(right = 2024)
# https://stackoverflow.com/questions/1726391/matplotlib-draw-grid-lines-behind-other-graph-elements
ax2.grid(linewidth = 0.5)
ax2.set_axisbelow(True)
# Add a legend
# https://stackoverflow.com/questions/47391702/how-to-make-a-colored-markers-legend-from-scratch
# https://stackoverflow.com/questions/21285885/remove-line-through-marker-in-matplotlib-legend
label1 = matplotlib.lines.Line2D([], [], marker = 'o', linestyle='None',
        label = r'ENDF-B/$x$ (USA)', color = green)
label2 = matplotlib.lines.Line2D([], [], marker = 'o', linestyle='None',
        label = r'JEF-$x$ and JEFF-$x$' + ' (mainly Europe)', color = blue)
label3 = matplotlib.lines.Line2D([], [], marker = 'o', linestyle='None',
        label = r'JENDL-$x$ (Japan)', color = red)
label4 = matplotlib.lines.Line2D([], [], marker = 'o', linestyle='None',
        label = 'TENDL (IAEA)', color = orange)
legend = ax2.legend(handles=[label1, label2, label3, label4], framealpha = 1)
for txt in legend.get_texts():
    if txt.get_text().startswith('ENDF-B/'):
        txt.set_color(green)
    elif txt.get_text().startswith('JEF'):
        txt.set_color(blue)
    elif txt.get_text().startswith('JENDL'):
        txt.set_color(red)
    elif txt.get_text().startswith('TENDL'):
        txt.set_color(orange)

#---
#  Add annotations for several important points
#---
# https://matplotlib.org/stable/tutorials/text/annotations.html#basic-annotation
for [evaluation, text, va, ha, addx, addy] in [['ENDF-B/I', 'I', 'top', 'right', 0, 0],
                                               ['ENDF-B/II', 'II', 'top', 'left', 0, 0],
                                               ['ENDF-B/III', 'III', 'bottom', 'center', 0, 0],
                                               ['ENDF-B/IV', 'IV', 'bottom', 'left', 0, 0],
                                               ['JENDL-1', 'JENDL-1', 'center', 'left', 0, -1],
                                               ['ENDF-B/V.2', 'ENDF-B/V.2', 'center', 'left', 0, -1],
                                               ['JENDL-2', 'JENDL-2', 'center', 'left', 0, -1],
                                               ['JEF-1', 'JEF-1', 'top', 'right', 0, 0],
                                               ['JENDL-3.1', 'JENDL-3.1', 'bottom', 'right', 0, 0],
                                               ['JEF-2.2', 'JEF-2.2', 'top', 'center', 0, -2],
                                               ['JENDL-3.2', '3.2', 'bottom', 'center', 0, 0],
                                               ['ENDF-B/VI.6', 'VI', 'top', 'center', 0, -4],
                                               ['JEFF-3.0', '3.0', 'top', 'left', 0, 0],
                                               ['JEFF-3.1', '3.1', 'bottom', 'right', 0, 0],
                                               ['JEFF-3.1.1', '3.1.1', 'top', 'center', 0, 0],
                                               ['JEFF-3.1.2', '3.1.2', 'center', 'left', 0, -1],
                                               ['ENDF-B/VII.0', 'VII.0', 'bottom', 'center', 0, 0],
                                               ['JENDL-4.0', '4.0', 'bottom', 'center', 0, 2],
                                               ['ENDF-B/VII.1', 'VII.1', 'center', 'left', 0, -1],
                                               ['JEFF-3.3', 'JEFF-3.3', 'center', 'right', 0, -1],
                                               ['ENDF-B/VIII.0', 'VIII.0', 'top', 'center', 0, -2],
                                               ['JEFF-4T2.2', '4T2.2', 'bottom', 'right', 9, -1],
                                               ['JENDL-5', 'JENDL-5', 'top', 'right', 0, 0]]:
    offset = 5
    # Vertical alignement
    if va == 'bottom':
        yoffset = +offset + addy
    elif va == 'top':
        yoffset = -offset + addy
    elif va == 'center' or va == 'baseline':
        yoffset = 0 + addy
    # Horizontal alignement
    if ha == 'right':
        xoffset = -offset + addx
    elif ha == 'left':
        xoffset = +offset + addx
    elif ha == 'center':
        xoffset = 0 + addx
    # Evaluation-dependent color
    if evaluation.startswith('ENDF-B'):
        color = green # As in ENDF-B/VIII.0 logo : https://www.nndc.bnl.gov/endf-b8.0/
    elif evaluation.startswith('JEF'):
        color = blue # As in European flag
    elif evaluation.startswith('JENDL-'):
        color = red # A red circle on a white background, as in Japanese flag
    elif evaluation.startswith('TENDL'):
        color = orange
    ax2.annotate(text, color = color,
                 xy = (Release[evaluation], NbIso[evaluation]),
                 xycoords = 'data',
                 xytext = (xoffset, yoffset),
                 textcoords = 'offset points',
                 va = va, ha = ha)

# title='Number of materials in evaluations in ENDF-6 format'
# title='Nombre de matériaux dans les évaluations au format ENDF-6'

# The term "material" refers either to a single isotope, or a mixture of isotopes: a natural element, a molecule, an alloy, lumped fission products, etc.
# Le terme "matériau" désigne soit un isotope unique, soit un mélange d'isotopes : un élément naturel, une molécule, un alliage, des produits de fission regroupés, etc.

fig.savefig('NbIso.png', bbox_inches='tight', dpi=600)
fig.savefig('NbIso.pdf', bbox_inches='tight')
os.system('pdftops -level3 -eps NbIso.pdf NbIso.eps')

# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter16.04-Least-Squares-Regression-in-Python.html
def func(x, a, b):
    y = a*x + b
    return y
# Retrieve data for a fit
xdata = []
ydata = []
for evaluation in Release.keys():
    if not evaluation.startswith('TENDL'):
        xdata.append(Release[evaluation])
        ydata.append(NbIso[evaluation])
# Linear fitting
a, b = optimize.curve_fit(func, xdata = xdata, ydata = ydata)[0]

print('Traditional evaluations will almost certainly reach 2800 isotopes (as in TENDL) in year ' + str(int(round((2800 - b)/a))))
