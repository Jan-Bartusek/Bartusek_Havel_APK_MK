from math import *
from uvtosd import uvTosd
from ukol1 import WGSToJTSK


def WGSToJTSK_NoEllipsoid(phi_WGS, la_WGS):
    # Neglect ellipsoid change: skip Helmert, use WGS84 (phi, lam) directly
    # as if they were Bessel coordinates
    a_Bes  = 6377397.155
    b_Bes  = 6356078.963
    e2_Bes = (a_Bes**2 - b_Bes**2) / a_Bes**2

    # Longitude shift to Ferro meridian (using WGS84 longitude directly)
    la_Ferro = la_WGS + radians(17 + 2/3)

    # Gauss conformal projection parameters
    phi0  = radians(49.5)
    alpha = sqrt(1 + e2_Bes * cos(phi0)**4 / (1 - e2_Bes))
    u0    = asin(sin(phi0) / alpha)

    kn = (tan(phi0/2 + pi/4)**alpha
          * ((1 - sqrt(e2_Bes)*sin(phi0)) / (1 + sqrt(e2_Bes)*sin(phi0)))**(alpha*sqrt(e2_Bes)/2))
    kd = tan(u0/2 + pi/4)
    k  = kn / kd

    R_g = a_Bes * sqrt(1 - e2_Bes) / (1 - e2_Bes * sin(phi0)**2)

    # Gauss conformal projection: (phi_WGS, lam_WGS) treated as Bessel -> (u, v)
    u = 2 * atan(1/k * (tan(phi_WGS/2 + pi/4)
        * ((1 - sqrt(e2_Bes)*sin(phi_WGS)) / (1 + sqrt(e2_Bes)*sin(phi_WGS)))**(sqrt(e2_Bes)/2))**alpha) - pi/2
    v = alpha * la_Ferro

    # Cartographic pole coordinates
    uk = radians(59 + 42/60 + 42.6969/3600)
    vk = radians(42 + 31/60 + 31.41725/3600)

    # Pole rotation: (u, v) -> (s, d)
    s, d = uvTosd(u, v, uk, vk)

    # Lambert conic conformal projection
    s0   = radians(78.5)
    c    = sin(s0)
    rho0 = R_g / tan(s0) * 0.9999

    rho  = rho0 * (tan(s0/2 + pi/4) / tan(s/2 + pi/4))**c
    eps_ = c * d

    y_jtsk = rho * sin(eps_)
    x_jtsk = rho * cos(eps_)

    return y_jtsk, x_jtsk


# Input coordinates (WGS84, degrees) - real GPS measurements, Praha 2
points = {
    'P1': (50.0753108743, 14.4369119218),  # TB 29
    'P2': (50.0756917689, 14.4354284443),  # ZB2
}

for name, (phi_deg, la_deg) in points.items():
    phi = radians(phi_deg)
    la  = radians(la_deg)

    y,  x,  _, _ = WGSToJTSK(phi, la)
    yn, xn        = WGSToJTSK_NoEllipsoid(phi, la)

    print(f"=== {name} ===")
    print(f"  JTSK (full):       Y = {y:.3f} m,  X = {x:.3f} m")
    print(f"  JTSK (no Helmert): Y = {yn:.3f} m,  X = {xn:.3f} m")
    print(f"  Difference:        dY = {yn-y:.3f} m,  dX = {xn-x:.3f} m")
    print()
