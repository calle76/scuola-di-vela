# Onde da vento con fetch limitato, SPM 1984 (eq. 3-39, 3-40; UA = 0.71 U10^1.23, unità SI), limite di mare formato gH/UA^2 = 0.243, gT/UA = 8.13
import math
g = 9.81
print("vento kn | fetch km | Hs m | Tp s | lungh. m | celerità kn | ripidità H/L | Lwl/lungh.")
for kn in (6, 8, 10, 12, 15, 20):
    U = kn * 0.5144; UA = 0.71 * U ** 1.23
    for F in (2e3, 5e3, 10e3, 20e3):
        x = g * F / UA**2
        H = min(0.0016 * x**0.5, 0.243) * UA**2 / g
        T = min(0.286 * x**(1/3), 8.13) * UA / g
        L = g * T**2 / (2 * math.pi); c = g * T / (2 * math.pi)
        print(f"{kn:8} | {F/1e3:8.0f} | {H:4.2f} | {T:4.2f} | {L:8.1f} | {c/0.5144:11.1f} | 1/{L/H:5.0f} | {3.38/L:4.2f}")
