import numpy as np

ML = 4
MH = 2

P1 = 50e3

Fp = 1e3

Rf = P1 / (ML - 1)
R = P1 / (MH * ML - 1)
C = (
        (
            ( (ML - 1) * np.sqrt(ML + 1) * ( (MH * ML - 1) ** (3 / 2) ) )
            *
            np.sqrt( (MH - 1) / ( (ML - 1) * (MH * ML - 1) ) )
        )
        /
        ( 2 * np.pi * ML * P1 * Fp * (MH - 1) * np.sqrt(MH + 1) )
)

print(f"Rf = {Rf}")
print(f"R = {R}")
print(f"C = {C}")