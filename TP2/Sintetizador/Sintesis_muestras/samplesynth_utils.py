import numpy as np
from numpy.fft import fft, ifft

def shift_pitch(signal, fs, f_ratio):

    peaks = find_peaks(signal, fs)
    new_signal = psola(signal, peaks, f_ratio)
    return new_signal


def find_peaks(signal, fs, max_hz=950, min_hz=75, analysis_win_ms=40, max_change=1.005, min_change=0.995):

    n = len(signal)
    min_period = fs // max_hz
    max_period = fs // min_hz

    # compute pitch periodicity
    sequence = int(analysis_win_ms / 1000 * fs)  # analysis sequence length in samples
    periods = compute_periods_per_sequence(signal, sequence, min_period, max_period)

    # find the peaks

    peaks = [np.argmax(signal[:int(periods[0]*1.1)])]
    while True:
        prev = peaks[-1]
        idx = prev // sequence  # current autocorrelation analysis window
        if prev + int(periods[idx] * max_change) >= n:
            break
        # find maximum near expected location
        peaks.append(prev + int(periods[idx] * min_change) + np.argmax(signal[prev + int(periods[idx] * min_change): prev + int(periods[idx] * max_change)]))
    return np.array(peaks)


def compute_periods_per_sequence(signal, sequence, min_period, max_period):

    offset = 0  # current sample offset
    periods = []  # period length of each analysis sequence

    autoc_peak = min_period
    while offset < len(signal):
        fourier = fft(signal[offset: offset + sequence])
        fourier[0] = 0  # remove DC component
        autoc = ifft(fourier * np.conj(fourier)).real

        try:
            autoc_peak += np.argmax(autoc[min_period: max_period])
        except ValueError:
            break
        periods.append(autoc_peak)
        offset += sequence

    return periods


def psola(signal, peaks, f_ratio):

    n = len(signal)
    # Interpolate
    new_signal = np.zeros(n)
    new_peaks_ref = np.linspace(0, len(peaks) - 1, int(len(peaks) * f_ratio))
    new_peaks = np.zeros(len(new_peaks_ref)).astype(int)

    for i in range(len(new_peaks)):
        weight = new_peaks_ref[i] % 1
        left = np.floor(new_peaks_ref[i]).astype(int)
        right = np.ceil(new_peaks_ref[i]).astype(int)
        new_peaks[i] = int(peaks[left] * (1 - weight) + peaks[right] * weight)

    # PSOLA
    for j in range(len(new_peaks)):
        # find the corresponding old peak index
        i = np.argmin(np.abs(peaks - new_peaks[j]))
        # get the distances to adjacent peaks
        p1 = [new_peaks[j] if j == 0 else new_peaks[j] - new_peaks[j-1],
              n - 1 - new_peaks[j] if j == len(new_peaks) - 1 else new_peaks[j+1] - new_peaks[j]]
        # edge case truncation
        if peaks[i] - p1[0] < 0:
            p1[0] = peaks[i]
        if peaks[i] + p1[1] > n - 1:
            p1[1] = n - 1 - peaks[i]
        # linear OLA window
        window = list(np.linspace(0, 1, p1[0] + 1)[1:]) + list(np.linspace(1, 0, p1[1] + 1)[1:])
        # center window from original signal at the new peak
        new_signal[new_peaks[j] - p1[0]: new_peaks[j] + p1[1]] += window * signal[peaks[i] - p1[0]: peaks[i] + p1[1]]
    return new_signal



