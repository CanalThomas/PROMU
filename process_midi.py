import sys
sys.path.insert(1, "../wave2shape/src/")
# https://github.com/lylyhan/wave2shape/tree/80d93a54e49ecb0855b441af15661ae091358031

from ftm_u_shape import getsounds_imp_gaus

from typing import Dict
from math import pi
import numpy as np
import torch
import auraloss


def fit_in_range(midi_value, min_range, max_range):
    tmp_value = midi_value / 128
    result_value = min_range + (max_range - min_range) * tmp_value
    return result_value


def midi_parameters_to_theta(d: Dict[str | int, int]) -> tuple:
    """Convertit les paramètres venant des messages MIDI en paramètres physiques theta

    Args:
    d: dict {
        "velocity": 0, # velocity of the stroke
        60: 64, # X - Erae
        61: 64, # Y - Erae
        48: 64, # sustain
        49: 64, # damp
        50: 64, # inharmonicity
        51: 64, # squareness
        15: 64, # pitch
    }

    Output:
    theta: (
        m1: int,
        m2: int,
        r1: float,
        r2: float,
        w11: int,
        tau11: float,
        p: float,
        D: float,
        alpha: float,
        sr: int,
    )
    """
    m1, m2 = 5, 5
    r1 = fit_in_range(d["60"], 0.005, 0.995) # X - Erae
    r2 = fit_in_range(d["61"], 0.005, 0.995) # Y - Erae
    w11 = 2 * pi * 2 ** ((d["15"] - 69.0) / 12.0) # pitch
    tau11 = fit_in_range(d["48"], 0.01, 0.5) # sustain
    p = fit_in_range(d["49"], 0.0, 0.35) # damp
    D = fit_in_range(d["50"], 0.0, 10.0) # inharmonicity
    alpha = fit_in_range(d["51"], 0.01, 1.0) # squareness
    sr = 22050
    theta = (m1, m2, r1, r2, w11, tau11, p, D, alpha, sr)
    return theta


def ftm(theta: tuple) -> np.ndarray:
    return getsounds_imp_gaus(*theta)


def process(y: np.ndarray) -> torch.Tensor:
    return torch.Tensor(y)


def unprocess(out: torch.Tensor) -> float:
    return out.item()


def measure_loss(d, d_target, loss=auraloss.freq.MultiResolutionSTFTLoss()) -> float:
    theta = midi_parameters_to_theta(d)
    theta_target = midi_parameters_to_theta(d_target)

    soundwave = ftm(theta) # play this sound directly
    soundwave_target = ftm(theta_target)

    y_hat = process(soundwave)
    y_target = process(soundwave_target)

    out = loss(y_hat, y_target)
    out = unprocess(out)

    return out
