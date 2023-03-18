import torch
import auraloss


def midi_parameters_to_theta(d):
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
    theta: ?
    """
    # TODO
    pass


def ftm(theta):
    pass


def process(y: torch.Tensor):
    pass


def unprocess(out: torch.Tensor) -> float:
    pass


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
