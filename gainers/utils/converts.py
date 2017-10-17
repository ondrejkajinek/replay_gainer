# coding: utf8


def convert_gain(orig_gain):
    gain = orig_gain[:-3] if orig_gain.endswith(" dB") else orig_gain
    try:
        return "%.2f dB" % float(gain)
    except ValueError:
        raise ValueError("Invalid gain value: %r" % orig_gain)


def convert_peak(peak):
    try:
        return "%.6f" % float(peak)
    except ValueError:
        raise ValueError("Invalid peak value: %r", peak)
