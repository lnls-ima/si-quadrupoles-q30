#!/usr/bin/env python-sirius
"""."""

import numpy as np
import matplotlib.pyplot as plt
from lnls import rotcoil as r



RotCoilMeas = r.RotCoilMeas_SIQuadQ30


qfb = {
    'SI-02M1:MA-QFB': 'Q30-016',
    'SI-02M2:MA-QFB': 'Q30-032',
    'SI-04M1:MA-QFB': 'Q30-010',
    'SI-04M2:MA-QFB': 'Q30-019',
    'SI-06M1:MA-QFB': 'Q30-008',
    'SI-06M2:MA-QFB': 'Q30-036',
    'SI-08M1:MA-QFB': 'Q30-011',
    'SI-08M2:MA-QFB': 'Q30-035',
    'SI-10M1:MA-QFB': 'Q30-009',
    'SI-10M2:MA-QFB': 'Q30-020',
    'SI-12M1:MA-QFB': 'Q30-029',
    'SI-12M2:MA-QFB': 'Q30-014',
    'SI-14M1:MA-QFB': 'Q30-013',
    'SI-14M2:MA-QFB': 'Q30-024',
    'SI-16M1:MA-QFB': 'Q30-005',
    'SI-16M2:MA-QFB': 'Q30-021',
    'SI-18M1:MA-QFB': 'Q30-025',
    'SI-18M2:MA-QFB': 'Q30-030',
    'SI-20M1:MA-QFB': 'Q30-023',
    'SI-20M2:MA-QFB': 'Q30-022',
}


qfp = {
    'SI-03M1:MA-QFP': 'Q30-033',
    'SI-03M2:MA-QFP': 'Q30-027',
    'SI-07M1:MA-QFP': 'Q30-017',
    'SI-07M2:MA-QFP': 'Q30-006',
    'SI-11M1:MA-QFP': 'Q30-026',
    'SI-11M2:MA-QFP': 'Q30-034',
    'SI-15M1:MA-QFP': 'Q30-015',
    'SI-15M2:MA-QFP': 'Q30-031',
    'SI-19M1:MA-QFP': 'Q30-007',
    'SI-19M2:MA-QFP': 'Q30-004',
}


def select_dataset(serial):
    """."""
    data = RotCoilMeas(serial)
    maxc_idx = data.get_max_current_index()
    data = data.get_data_set_measurements('M1')
    return data[maxc_idx]


def get_serials(magnet_family):
    """."""
    serials = []
    for magnet in magnet_family:
        serial = magnet_family[magnet]
        serials.append(serial.replace('Q30-', ''))
    return serials


def get_analysis_data(family):
    """."""
    serials = get_serials(family)
    current = []
    xcenter = []
    ycenter = []
    quadrupole = []
    roterror = []
    for serial in serials:
        data = select_dataset(serial)
        c = data.main_coil_current_avg
        h = data.harmonics
        main_idx = h.index(RotCoilMeas.main_harmonic)
        x = data.magnetic_center_x
        y = data.magnetic_center_y
        n = data.intmpole_normal_avg[main_idx]
        s = data.intmpole_skew_avg[main_idx]
        e = data.rotation_error
        current.append(c)
        xcenter.append(x)
        ycenter.append(y)
        quadrupole.append(n)
        roterror.append(e)
        sfmt = '{}  {:.3f} A  {:+.4f} T  {:+5.1f} um  {:+5.1f} um  {:06.3f}'
        print(sfmt.format(serial, c, n, x, y, e))

    q = np.array(quadrupole)
    m, s, maxmin = np.mean(q), np.std(q), np.max(q) - np.min(q)
    print('- integrated quadrupole [T]: {:+.4f} ± {:.4f} ({:.3f} %), maxmin: {:.4f} ({:.3f} %)'.format(m, s, 100*s/m, maxmin, 100*maxmin/m))
    x = np.array(xcenter)
    m, s, maxmin = np.mean(x), np.std(x), np.max(x) - np.min(x)
    print('- xcenter [um]:               {:+.1f} ± {:.1f}, maxmin: {:.1f}'.format(m, s, maxmin))
    y = np.array(ycenter)
    m, s, maxmin = np.mean(y), np.std(y), np.max(y) - np.min(y)
    print('- ycenter [um]:               {:+.1f} ± {:.1f}, maxmin: {:.1f}'.format(m, s, maxmin))
    e = np.array(roterror)
    m, s, maxmin = np.mean(e), np.std(e), np.max(e) - np.min(e)
    print('- rotation error [mrad]:      {:+.1f} ± {:.1f}, maxmin: {:.1f} '.format(m, s, maxmin))
    print('')
    return serials, current, quadrupole, xcenter, ycenter, roterror



fams = [qfb, qfp]



def plot_integrated_quadrupole():
    """."""

    n = 0
    serials = []

    label = 'QFB'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), quadrupole0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)), quadrupole0, 'bo', label=label)
    avg0 = np.mean(quadrupole0)
    plt.plot(len(serials) + np.arange(len(serials0)),
            [avg0, ]*len(quadrupole0), '--b')
    serials += serials0

    label = 'QFP'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), quadrupole1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)), quadrupole1, 'go', label=label)
    avg1 = np.mean(quadrupole1)
    plt.plot(len(serials) + np.arange(len(serials1)),
            [avg1, ]*len(quadrupole1), '--g')
    serials += serials1

    plt.xlabel('Serial Number')
    # plt.xlabel('Magnet Index')
    plt.ylabel('Integrated Quadrupole [T]')
    plt.title('Q30 Integrated Quadrupoles ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_xcenter():
    """."""

    n = 0
    serials = []

    label = 'QFB'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), xcenter0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             xcenter0, 'bo', label=label)
    avg0 = np.mean(xcenter0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(xcenter0), '--b')
    serials += serials0

    label = 'QFP'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), xcenter1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             xcenter1, 'go', label=label)
    avg1 = np.mean(xcenter1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(xcenter1), '--g')
    serials += serials1

    plt.xlabel('Serial Number')
    plt.ylabel('Magnetic Center [um]')
    plt.title(
        'Q30 Horizontal Magnetic Center ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_ycenter():
    """."""

    n = 0
    serials = []

    label = 'QFB'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), ycenter0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             ycenter0, 'bo', label=label)
    avg0 = np.mean(ycenter0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(ycenter0), '--b')
    serials += serials0

    label = 'QFP'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), ycenter1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             ycenter1, 'go', label=label)
    avg1 = np.mean(ycenter1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(ycenter1), '--g')
    serials += serials1

    plt.xlabel('Serial Number')
    plt.ylabel('Magnetic Center [um]')
    plt.title(
        'Q30 Vertical Magnetic Center ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_roterror():
    """."""

    n = 0
    serials = []

    label = 'QFB'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), roterror0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             roterror0, 'bo', label=label)
    avg0 = np.mean(roterror0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(roterror0), '--b')
    serials += serials0

    label = 'QFP'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), roterror1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             roterror1, 'go', label=label)
    avg1 = np.mean(roterror1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(roterror1), '--g')
    serials += serials1



    plt.xlabel('Serial Number')
    plt.ylabel('Roll error [mrad]')
    plt.title(
        'Q30 Rotation Error ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()



plot_integrated_quadrupole()
plot_xcenter()
plot_ycenter()
plot_roterror()
