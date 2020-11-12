#!/usr/bin/env python-sirius

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as mpl_gs

SORTING_QUADS = [
    'Q30_60A', 'Q30-002',
    'Q30_80A', 'Q30-002',
    'Q30_95A', 'Q30-002',
    'Q30_110A', 'Q30-002',
    'Q30_120A', 'Q30-002',
    'Q30_140A', 'Q30-002',
    'Q30_150A', 'Q30-002',
    ]

q30_60A_fnames = [
    'main_60A/MULTIPOLES--10A.txt',
    'main_60A/MULTIPOLES--8A.txt',
    'main_60A/MULTIPOLES--6A.txt',
    'main_60A/MULTIPOLES--4A.txt',
    'main_60A/MULTIPOLES--2A.txt',
    'main_60A/MULTIPOLES-0A.txt',
    'main_60A/MULTIPOLES-2A.txt',
    'main_60A/MULTIPOLES-4A.txt',
    'main_60A/MULTIPOLES-6A.txt',
    'main_60A/MULTIPOLES-8A.txt',
    'main_60A/MULTIPOLES-10A.txt',
    ]

q30_80A_fnames = [
    'main_80A/MULTIPOLES--10A.txt',
    'main_80A/MULTIPOLES--8A.txt',
    'main_80A/MULTIPOLES--6A.txt',
    'main_80A/MULTIPOLES--4A.txt',
    'main_80A/MULTIPOLES--2A.txt',
    'main_80A/MULTIPOLES-0A.txt',
    'main_80A/MULTIPOLES-2A.txt',
    'main_80A/MULTIPOLES-4A.txt',
    'main_80A/MULTIPOLES-6A.txt',
    'main_80A/MULTIPOLES-8A.txt',
    'main_80A/MULTIPOLES-10A.txt',
    ]

q30_95A_fnames = [
    'main_95A/MULTIPOLES--10A.txt',
    'main_95A/MULTIPOLES--8A.txt',
    'main_95A/MULTIPOLES--6A.txt',
    'main_95A/MULTIPOLES--4A.txt',
    'main_95A/MULTIPOLES--2A.txt',
    'main_95A/MULTIPOLES-0A.txt',
    'main_95A/MULTIPOLES-2A.txt',
    'main_95A/MULTIPOLES-4A.txt',
    'main_95A/MULTIPOLES-6A.txt',
    'main_95A/MULTIPOLES-8A.txt',
    'main_95A/MULTIPOLES-10A.txt',
    ]

q30_110A_fnames = [
    'main_110A/MULTIPOLES--10A.txt',
    'main_110A/MULTIPOLES--8A.txt',
    'main_110A/MULTIPOLES--6A.txt',
    'main_110A/MULTIPOLES--4A.txt',
    'main_110A/MULTIPOLES--2A.txt',
    'main_110A/MULTIPOLES-0A.txt',
    'main_110A/MULTIPOLES-2A.txt',
    'main_110A/MULTIPOLES-4A.txt',
    'main_110A/MULTIPOLES-6A.txt',
    'main_110A/MULTIPOLES-8A.txt',
    'main_110A/MULTIPOLES-10A.txt',
    ]

q30_120A_fnames = [
    'main_120A/MULTIPOLES--10A.txt',
    'main_120A/MULTIPOLES--8A.txt',
    'main_120A/MULTIPOLES--6A.txt',
    'main_120A/MULTIPOLES--4A.txt',
    'main_120A/MULTIPOLES--2A.txt',
    'main_120A/MULTIPOLES-0A.txt',
    'main_120A/MULTIPOLES-2A.txt',
    'main_120A/MULTIPOLES-4A.txt',
    'main_120A/MULTIPOLES-6A.txt',
    'main_120A/MULTIPOLES-8A.txt',
    'main_120A/MULTIPOLES-10A.txt',
    ]

q30_140A_fnames = [
    'main_140A/MULTIPOLES--10A.txt',
    'main_140A/MULTIPOLES--8A.txt',
    'main_140A/MULTIPOLES--6A.txt',
    'main_140A/MULTIPOLES--4A.txt',
    'main_140A/MULTIPOLES--2A.txt',
    'main_140A/MULTIPOLES-0A.txt',
    'main_140A/MULTIPOLES-2A.txt',
    'main_140A/MULTIPOLES-4A.txt',
    'main_140A/MULTIPOLES-6A.txt',
    'main_140A/MULTIPOLES-8A.txt',
    'main_140A/MULTIPOLES-10A.txt',
    ]

q30_150A_fnames = [
    'main_150A/MULTIPOLES--10A.txt',
    'main_150A/MULTIPOLES--8A.txt',
    'main_150A/MULTIPOLES--6A.txt',
    'main_150A/MULTIPOLES--4A.txt',
    'main_150A/MULTIPOLES--2A.txt',
    'main_150A/MULTIPOLES-0A.txt',
    'main_150A/MULTIPOLES-2A.txt',
    'main_150A/MULTIPOLES-4A.txt',
    'main_150A/MULTIPOLES-6A.txt',
    'main_150A/MULTIPOLES-8A.txt',
    'main_150A/MULTIPOLES-10A.txt',
    ]


def get_sorting(sextupoles=False):

    SORTING = SORTING_SEXTS if sextupoles else SORTING_QUADS
    magnets = SORTING[::2]
    serials = SORTING[1::2]
    fams = dict()
    for magnet, serial in zip(magnets, serials):
        fam = magnet
        if fam not in fams:
            fams[fam] = [serial]
        else:
            fams[fam].append(serial)
    return fams


def multipole_plot(magnets, currents, harmonics, multipoles_normal, multipoles_skew, harm, typ):
    idx = harmonics.index(harm)
    if typ == 'normal':
        data = multipoles_normal[:, idx]
        title = 'Normal'
    else:
        data = multipoles_skew[:, idx]
        title = 'Skew'
    title += ' multipole values for harmonic n = {}'.format(harm)

    data = data * currents
    fig, ax = plt.subplots()
    x = np.arange(len(magnets))
    ax.bar(x, data)
    ax.set_title(title)
    ax.set_xlabel('Integrated multipole [T/m^(n-1)]'.format(harm))
    ax.set_ylabel('Integrated multipole [T/m^(n-1)]'.format(harm))
    ax.set_xticks(x)
    ax.set_xticklabels(magnets, rotation=90)
    plt.show()


def multipole_read_file(fname):

    with open(fname, 'r') as fp:
        lines = fp.readlines()

    magnets = list()
    harmonics = list()
    currents = list()
    multipoles_normal = list()
    multipoles_skew = list()
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            if '# harmonics' in line:
                _, harmonics = line.split('):')
                harmonics = [int(word) for word in harmonics.split()]
                # print(harmonics)
            continue
        magnet, current, *mpoles = line.split()
        mpoles = [float(mpole) for mpole in mpoles]
        # first column: magnet name
        magnets.append(magnet)
        # second column: measurement current
        currents.append(float(current))
        # next group: normal multipoles for all harmonics, normalized by excitation current
        multipoles_normal.append(mpoles[:len(harmonics)])
        # next group: skew multipoles for all harmonics, normalized by excitation current
        multipoles_skew.append(mpoles[len(harmonics):])

    currents = np.array(currents)
    multipoles_normal = np.array(multipoles_normal)
    multipoles_skew = np.array(multipoles_skew)

    return magnets, currents, harmonics, multipoles_normal, multipoles_skew


def multipole_get_avg(fname, magnets_fam, exclude_harms):
    magnets, currents, harmonics, multipoles_normal, multipoles_skew = multipole_read_file(fname)
    indices = [magnets.index(mag) for mag in magnets_fam]
    selection = \
        list(set(np.arange(len(harmonics))) - set([harmonics.index(h) for h in exclude_harms]))
    # print(selection)
    print(selection)
    print(multipoles_normal.shape)
    nmpoles = multipoles_normal[:, selection]
    smpoles = multipoles_skew[:, selection]
    nmpoles = nmpoles[indices, :]
    smpoles = smpoles[indices, :]
    currents = currents[indices]
    for i in range(len(currents)):
        nmpoles[i, :] *= currents[i]
        smpoles[i, :] *= currents[i]

    current = np.mean(currents)
    nmpoles_avg = np.mean(nmpoles, 0)
    smpoles_avg = np.mean(smpoles, 0)
    nmpoles_std = np.std(nmpoles, 0)
    smpoles_std = np.std(smpoles, 0)

    return current, harmonics, nmpoles_avg, smpoles_avg, nmpoles_std, smpoles_std


def excdata_print(fam, fnames, exclude_harms, label, main_harmonic, sextupoles=False, extrapolation_current=None):

    fams = get_sorting(sextupoles)
    magnets_fam = fams[fam]

    # get data from file and build
    excdata_avg = list()
    excdata_std = list()
    for fname in fnames:
        current, harmonics, nmpoles_avg, smpoles_avg, nmpoles_std, smpoles_std = \
            multipole_get_avg(fname, magnets_fam, exclude_harms)
        datum = np.array([0.0, ] * (1 + len(nmpoles_avg) + len(smpoles_avg)))
        datum[0] = current
        datum[1::2] = nmpoles_avg
        datum[2::2] = smpoles_avg
        excdata_avg.append(datum.copy())
        datum[1::2] = nmpoles_std
        datum[2::2] = smpoles_std
        excdata_std.append(datum.copy())

    # if len(excdata_avg) == 12:
    #     zero_neg = np.array(excdata_avg[5][1:])
    #     zero_pos = np.array(excdata_avg[6][1:])
    #     zero_mean = (zero_neg + zero_pos)/2
    #     excdata_avg.pop(5)
    #     excdata_avg.pop(5)
    #     excdata_avg.insert(5, [0, ] + list(zero_mean))
    #     excdata_avg = np.array(excdata_avg)


    # # linear extrapolation at I = 0
    # datum1 = excdata_avg[0]
    # datum2 = excdata_avg[1]
    # x1, x2 = datum1[0], datum2[0]
    # y1, y2 = np.array(datum1[1:]), np.array(datum2[1:])
    # b = (x2 * y1 - x1 * y2) / (x2 - x1)
    # excdata_avg.insert(0, [0,] + list(b))
    # excdata_avg = np.array(excdata_avg)

    # datum1 = excdata_std[0]
    # datum2 = excdata_std[1]
    # x1, x2 = datum1[0], datum2[0]
    # y1, y2 = np.array(datum1[1:]), np.array(datum2[1:])
    # b = (x2 * y1 - x1 * y2) / (x2 - x1)
    # excdata_std.insert(0, [0,] + list(b))
    # excdata_std = np.array(excdata_avg)

    if extrapolation_current:
        pass

    print('# HEADER')
    print('# ======')
    print('# label             {}'.format(label))
    print('# harmonics         ', end='')
    for h in harmonics:
        if h not in exclude_harms:
            print('{} '.format(h), end='')
    print()
    print('# main_harmonic     {}'.format(main_harmonic))
    print('# rescaling factor  1.002908')
    print('# units             Ampere  ', end='')
    for h in harmonics:
        if h not in exclude_harms:
            if h == 0:
                fmt = 'T*m'
            elif h == 1:
                fmt = 'T'
            elif h == 2:
                fmt = 'T/m'
            else:
                fmt = 'T/m^{}'.format(h-1)
            print('{} {}  '.format(fmt, fmt), end='')
    print()
    print()
    print('# EXCITATION DATA')
    print('# ===============')

    for line in excdata_avg:
        print('{:+09.4f} '.format(line[0]), end='')
        for i in range(len(line[1:])//2):
            if harmonics[i] not in exclude_harms:
                print('{:+.4e} {:+.4e}  '.format(line[1+2*i+0], line[1+2*i+1]), end='')
        print()
    print()

    print('# COMMENTS')
    print('# ========')
    print('# 1. generated automatically with "excdata.py"')
    print('# 2. data taken from rotcoil measurements')
    print('# 3. data for zero current is extrapolated from data points with lowest measured currents')
    print('# 4. average excitation curves for magnets:', end='')
    for i in range(len(magnets_fam)):
        if i % 10 == 0:
            print('\n#    ', end='')
        print('{} '.format(magnets_fam[i]), end='')
    print()

    print()
    print('# POLARITY TABLE')
    print('# ==============')
    print('#')
    print('# Magnet function         | IntStrength(1) | IntField(2) | ConvSign(3) | Current(4)')
    print('# ------------------------|----------------|-------------|-------------|-----------')
    print('# dipole                  | Angle > 0      | BYL  < 0    | -1.0        | I > 0')
    print('# corrector-horizontal    | HKick > 0      | BYL  > 0    | +1.0        | I > 0')
    print('# corrector-vertical      | VKick > 0      | BXL  < 0    | -1.0        | I > 0')
    print('# quadrupole (focusing)   | KL    > 0      | D1NL < 0    | -1.0        | I > 0')
    print('# quadrupole (defocusing) | KL    < 0      | D1NL > 0    | -1.0        | I > 0')
    print('# quadrupole (skew)       | KL    < 0      | D1SL > 0    | -1.0        | I > 0')
    print('# sextupole  (focusing)   | SL    > 0      | D2NL < 0    | -1.0        | I > 0')
    print('# sextupole  (defocusing) | SL    < 0      | D2NL > 0    | -1.0        | I > 0')
    print('#')
    print('# Defs:')
    print('# ----')
    print('# BYL   := \int{dz By|_{x=y=0}}.')
    print('# BXL   := \int{dz Bx|_{x=y=0}}.')
    print('# D1NL  := \int{dz \\frac{dBy}{dx}_{x=y=0}}')
    print('# D2NL  := (1/2!) \int{dz \\frac{d^2By}{dx^2}_{x=y=0}}')
    print('# D1SL  := \int{dz \\frac{dBx}{dx}_{x=y=0}}')
    print('# Brho  := magnetic rigidity.')
    print('# Angle := ConvSign * BYL / abs(Brho)')
    print('# HKick := ConvSign * BYL / abs(Brho)')
    print('# VKick := ConvSign * BXL / abs(Brho)')
    print('# KL    := ConvSign * D1NL / abs(Brho)')
    print('# KL    := ConvSign * D1SL / abs(Brho)')
    print('# SL    := ConvSign * D2NL / abs(Brho)')
    print('#')
    print('# Obs:')
    print('# ---')
    print('# (1) Parameter definition.')
    print('#     IntStrength values correspond to integrated PolynomA and PolynomB parameters')
    print('#     of usual beam tracking codes, with the exception that VKick has its sign')
    print('#     reversed with respecto to its corresponding value in PolynomA.')
    print('# (2) Sirius coordinate system and Lorentz force.')
    print('# (3) Conversion sign for IntField <-> IntStrength')
    print('# (4) Convention of magnet excitation polarity, so that when I > 0 the strength')
    print('#     of the magnet has the expected conventional sign.')
    print('')
    print('# STATIC DATA FILE FORMAT')
    print('# =======================')
    print('#')
    print('# These static data files should comply with the following formatting rules:')
    print('# 1. If the first alphanumeric character of the line is not the pound sign')
    print('#    then the lines is a comment.')
    print('# 2. If the first alphanumeric character is "#" then if')
    print('#    a) it is followed by "[<parameter>] <value>" a parameter names <parameter>')
    print('#       is define with value <value>. if the string <value> has spaces in it')
    print('#       it is split as a list of strings.')
    print('#    b) otherwise the line is ignored as a comment line.')

    return harmonics, excdata_avg, excdata_std


def excdata_read(magnet):
    # print(magnet)
    if 'Q30_60A' in magnet:
        fnames = q30_60A_fnames
    elif 'Q30_80A' in magnet:
        fnames = q30_80A_fnames
    elif 'Q30_95A' in magnet:
        fnames = q30_95A_fnames
    elif 'Q30_110A' in magnet:
        fnames = q30_110A_fnames
    elif 'Q30_120A' in magnet:
        fnames = q30_120A_fnames
    elif 'Q30_140A' in magnet:
        fnames = q30_140A_fnames

    currents = list()
    mpoles_normal = list()
    mpoles_skew = list()
    for fname in fnames:
        magnets, currs, harmonics, multipoles_normal, multipoles_skew = \
            multipole_read_file(fname)
        idx_magnet = magnets.index(magnet)
        curr = currs[idx_magnet]
        mpoles_normal.append(curr * np.array(multipoles_normal[idx_magnet, :]))
        mpoles_skew.append(curr * np.array(multipoles_skew[idx_magnet, :]))
        currents.append(curr)
    currents = np.array(currents)
    mpoles_normal = np.array(mpoles_normal)
    mpoles_skew = np.array(mpoles_skew)
    return harmonics, currents, mpoles_normal, mpoles_skew


def excdata_read_family(fam, sextupoles=False):
    families = get_sorting(sextupoles)
    magnets = families[fam]
    currents = list()
    mpoles_normal = list()
    mpoles_skew = list()
    for magnet in magnets:
        harmonics, currs, mpoles_n, mpoles_s = excdata_read(magnet)
        currents.append(currs)
        mpoles_normal.append(mpoles_n)
        mpoles_skew.append(mpoles_s)
    currents = np.array(currents)
    mpoles_normal = np.array(mpoles_normal)
    mpoles_skew = np.array(mpoles_skew)
    return magnets, harmonics, currents, mpoles_normal, mpoles_skew

def excdata_Q30_60A():
    fam = 'Q30_60A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_60A_fnames
    label = 'si-quadrupole-q30-60A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 60A main coil')
    plt.show()

def excdata_Q30_80A():
    fam = 'Q30_80A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_80A_fnames
    label = 'si-quadrupole-q30-80A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 80A main coil')
    plt.show()

def excdata_Q30_95A():
    fam = 'Q30_95A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_95A_fnames
    label = 'si-quadrupole-q30-95A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 95A main coil')
    plt.show()

def excdata_Q30_110A():
    fam = 'Q30_110A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_110A_fnames
    label = 'si-quadrupole-q30-110A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 110A main coil')
    plt.show()

def excdata_Q30_120A():
    fam = 'Q30_120A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_120A_fnames
    label = 'si-quadrupole-q30-120A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 120A main coil')
    plt.show()

def excdata_Q30_140A():
    fam = 'Q30_140A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_140A_fnames
    label = 'si-quadrupole-q30-140A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 140A main coil')
    plt.show()

def excdata_Q30_150A():
    fam = 'Q30_150A'
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fnames = q30_150A_fnames
    label = 'si-quadrupole-q30-150A'
    main_harmonic = '1 normal'

    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)

    excdata_avg = np.array(excdata_avg)

    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    plt.plot(currents, excdata_avg[:, 1 + 2*idx], 'o--')
    plt.xlabel('Current [A]')
    plt.ylabel('GL [T]')
    plt.grid()
    plt.title('Q30 Trim Excitation Curve - 150A main coil')
    plt.show()


def excdata_all_Q30(normalize):
    # exclude_harms = [0, ]
    exclude_harms = [ ]
    fig = plt.figure(figsize=(12, 8))
    gs = mpl_gs.GridSpec(1, 1)
    gs.update(left=0.10, right=0.80, hspace=0, wspace=0.25)
    ax = plt.subplot(gs[0, 0])

    fam = 'Q30_60A'
    fnames = q30_60A_fnames
    label = 'si-quadrupole-q30-60A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 60
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 60A')

    fam = 'Q30_80A'
    fnames = q30_80A_fnames
    label = 'si-quadrupole-q30-80A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 80
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 80A')

    fam = 'Q30_95A'
    fnames = q30_95A_fnames
    label = 'si-quadrupole-q30-95A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 95
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 95A')

    fam = 'Q30_110A'
    fnames = q30_110A_fnames
    label = 'si-quadrupole-q30-110A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 110
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 110A')

    fam = 'Q30_120A'
    fnames = q30_120A_fnames
    label = 'si-quadrupole-q30-120A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 120
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 120A')

    fam = 'Q30_140A'
    fnames = q30_140A_fnames
    label = 'si-quadrupole-q30-140A'
    main_harmonic = '1 normal'
    harmonics, excdata_avg, excdata_std = excdata_print(fam, fnames, exclude_harms, label, main_harmonic)
    excdata_avg = np.array(excdata_avg)
    excdata_avg -= excdata_avg[5, :]
    currents = excdata_avg[:, 0]
    idx = harmonics.index(1)
    main_curr = 1
    if normalize:
        main_curr = 140
    ax.plot(currents, excdata_avg[:, 1 + 2*idx]/main_curr, 'o--', label='main = 140A')

    print(currents)
    ax.set_xlabel('Current [A]')

    if normalize:
        ax.set_ylabel(r'GL/Imain [T]/[A]')
        ax.set_title('Q30 Trim Excitation Curves Normalized by Main Coil Current - Ramp Down')
    else:
        ax.set_ylabel(r'GL [T]')
        ax.set_title('Q30 Trim Excitation Curves - Ramp Down')
    ax.grid()
    ax.legend(bbox_to_anchor=(1.0, 1.0), frameon=True, fontsize=12)
    plt.tight_layout(True)
    plt.savefig('q30_trim_excdata_10A_to_m10A_rampdown.png', dpi=300)
    plt.show()


# Q30 quadrupoles
# excdata_Q30_60A()
# excdata_Q30_80A()
# excdata_Q30_95A()
# excdata_Q30_110A()
# excdata_Q30_120A()
# excdata_Q30_140A()
# excdata_Q30_150A()
excdata_all_Q30(normalize=False)
