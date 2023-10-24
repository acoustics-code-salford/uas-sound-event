import numpy as np


def test_sine(t, f_0=440, A=0.75, fs=48000):
    t_samples = np.linspace(0, t, fs*t)
    sig = np.zeros_like(t_samples)

    for i, sample in enumerate(t_samples):
        sig[i] = np.sin(2*np.pi*f_0*sample) * A

    return sig


def load_params(csv_file):
    str_params = np.loadtxt(
        csv_file,
        delimiter=',',
        skiprows=1,
        usecols=np.arange(1, 4),
        dtype='str'
    ).reshape(-1, 3)  # reshape in case of single-event flight

    return [[np.array(cell.strip().split(' '), dtype=int)
            for cell in row]
            for row in str_params]


def nearest_whole_fraction(pos):
    n = np.round(pos).astype(int)
    s = (
        - (- pos % 1)
        if np.round(pos).astype(int) > pos
        else pos % 1
    )
    return n, s


def cart_to_sph(xyz, return_r=True):
    '''Transform between cartesian and polar co-ordinates.'''
    r = np.linalg.norm(xyz, axis=0)
    x, y, z = xyz

    theta = np.arctan2(y, x) % (2 * np.pi)
    phi = np.arccos(z / r)

    return np.array([theta, phi, r]) if return_r else np.array([theta, phi])


def vector_t(start, end, speeds, fs=48000):
        v_0, v_T = speeds
        distance = np.linalg.norm(start - end)
        # heading of source
        vector = ((end - start) / distance)
        # acceleration
        a = ((v_T**2) - (v_0**2)) / (2 * distance)
        # number of time steps in samples for operation
        n_output_samples = fs * ((v_T-v_0) / a) if a != 0 else \
            (distance / v_0) * fs

        # array of positions at each time step
        x_t = np.array([
            [
                (v_0 * (t / fs))
                + ((a * (t / fs)**2) / 2)
                for t in range(int(n_output_samples))
            ]
        ]).T

        # map to axes
        xyz = (start + vector * x_t).T
        return xyz