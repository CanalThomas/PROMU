import sys
sys.path.insert(1, "../wave2shape/src/")
# https://github.com/lylyhan/wave2shape/tree/80d93a54e49ecb0855b441af15661ae091358031

from ftm_u_shape import getsounds_imp_gaus
import sounddevice as sd

def main():
    m1 = 20
    m2 = 20
    r1 = 0.5
    r2 = 0.5
    w11 = 2000
    tau11 = 0.1
    p = 0.2
    D = 0.1
    alpha = 0.7
    sr=22050
    y = getsounds_imp_gaus(m1, m2, r1, r2, w11, tau11, p, D, alpha, sr)
    inp = input(">>>")
    while inp != "stop":
        sd.play(y, sr)
        inp = input(">>>")

if __name__ == "__main__":
    main()