from math import *
from uvtosd import uvTosd

def WGSToJTSK(phi_WGS, la_WGS):
    # WGS84 parameters
    a_WGS = 6378137.00
    b_WGS = 6356752.3142

    e2_WGS = (a_WGS**2 - b_WGS**2) / a_WGS**2
    W_WGS  = sqrt(1 - e2_WGS * sin(phi_WGS)**2)
    N_WGS  = a_WGS / W_WGS

    # (phi, lam) WGS84 -> XYZ WGS84
    X_WGS = N_WGS * cos(phi_WGS) * cos(la_WGS)
    Y_WGS = N_WGS * cos(phi_WGS) * sin(la_WGS)
    Z_WGS = N_WGS * (1 - e2_WGS) * sin(phi_WGS)

    # Helmert transformation parameters (WGS84 -> Bessel)
    om_x  = radians(4.9984 / 3600)
    om_y  = radians(1.5867 / 3600)
    om_z  = radians(5.2611 / 3600)
    m     = 1 - 3.5623e-6
    dlt_x = -570.8285
    dlt_y =  -85.6769
    dlt_z = -462.8420

    # Rotation matrix (linearised for small angles)
    R = [
        [ 1,    om_z, -om_y],
        [-om_z, 1,     om_x],
        [ om_y,-om_x,  1   ],
    ]

    # Helmert transformation -> XYZ Bessel
    X_Bes = m * (R[0][0]*X_WGS + R[0][1]*Y_WGS + R[0][2]*Z_WGS) + dlt_x
    Y_Bes = m * (R[1][0]*X_WGS + R[1][1]*Y_WGS + R[1][2]*Z_WGS) + dlt_y
    Z_Bes = m * (R[2][0]*X_WGS + R[2][1]*Y_WGS + R[2][2]*Z_WGS) + dlt_z

    # Bessel ellipsoid parameters
    a_Bes  = 6377397.155
    b_Bes  = 6356078.963
    e2_Bes = (a_Bes**2 - b_Bes**2) / a_Bes**2

    # XYZ Bessel -> (phi, lam) Bessel
    la_Bes = atan2(Y_Bes, X_Bes)

    # Iterative computation of phi_Bes (accuracy 0.001")
    p       = sqrt(X_Bes**2 + Y_Bes**2)
    phi_Bes = atan2(Z_Bes, (1 - e2_Bes) * p)
    eps     = radians(0.001 / 3600)
    for _ in range(100):
        W_Bes   = sqrt(1 - e2_Bes * sin(phi_Bes)**2)
        N_Bes   = a_Bes / W_Bes
        phi_new = atan2(Z_Bes + e2_Bes * N_Bes * sin(phi_Bes), p)
        if abs(phi_new - phi_Bes) < eps:
            phi_Bes = phi_new
            break
        phi_Bes = phi_new

    # Longitude shift to Ferro meridian
    la_Ferro = la_Bes + radians(17 + 2/3)

    # Gauss conformal projection parameters
    phi0  = radians(49.5)
    alpha = sqrt(1 + e2_Bes * cos(phi0)**4 / (1 - e2_Bes))
    u0    = asin(sin(phi0) / alpha)

    kn = (tan(phi0/2 + pi/4)**alpha
          * ((1 - sqrt(e2_Bes)*sin(phi0)) / (1 + sqrt(e2_Bes)*sin(phi0)))**(alpha*sqrt(e2_Bes)/2))
    kd = tan(u0/2 + pi/4)
    k  = kn / kd

    R_g = a_Bes * sqrt(1 - e2_Bes) / (1 - e2_Bes * sin(phi0)**2)

    # Gauss conformal projection: (phi, lam) -> (u, v) on sphere
    u = 2 * atan(1/k * (tan(phi_Bes/2 + pi/4)
        * ((1 - sqrt(e2_Bes)*sin(phi_Bes)) / (1 + sqrt(e2_Bes)*sin(phi_Bes)))**(sqrt(e2_Bes)/2))**alpha) - pi/2
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

    # (rho, eps) -> JTSK plane coordinates
    y_jtsk = rho * sin(eps_)
    x_jtsk = rho * cos(eps_)

    # Length distortion m-1
    distortion = (c * rho) / (R_g * cos(s)) - 1

    # Meridian convergence
    xi          = asin(cos(uk) * sin(d) / cos(u))
    convergence = eps_ - xi

    return y_jtsk, x_jtsk, distortion, convergence


# Input coordinates (WGS84, degrees)
points = {
    'P1': (50.0753108743, 14.4369119218),  # TB 29, Praha 2 (trigonometric point)
    'P2': (50.0756917689, 14.4354284443),  # ZB2, Praha 2 (densification point, 2nd order)
}

for name, (phi_deg, la_deg) in points.items():
    phi = radians(phi_deg)
    la  = radians(la_deg)

    y, x, dist, conv = WGSToJTSK(phi, la)

    conv_deg = degrees(conv)
    conv_min = (conv_deg % 1) * 60

    print(f"=== {name} ===")
    print(f"  WGS-84:      phi = {phi_deg:.6f} deg,  lam = {la_deg:.6f} deg")
    print(f"  JTSK:        Y = {y:.3f} m,  X = {x:.3f} m")
    print(f"  Distortion:  m-1 = {dist:.6e}")
    print(f"  Convergence: c   = {int(conv_deg)}d {conv_min:.4f}'  ({conv_deg:.6f} deg)")
    print()
