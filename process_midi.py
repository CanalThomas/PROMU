import sys
sys.path.insert(1, "../wave2shape/src/")
# https://github.com/lylyhan/wave2shape/tree/80d93a54e49ecb0855b441af15661ae091358031

from ftm_u_shape import getsounds_imp_gaus

from typing import Dict
import numpy as np
import torch
import auraloss


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
    r1 = d[60] / 128 # X - Erae
    r2 = d[61] / 128 # Y - Erae
    w11 = d[15] / # pitch
    tau11 = d[48] / # sustain
    p = d[49] / # damp
    D = d[50] / # inharmonicity
    alpha = d[51] / # squareness
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
