from math import *

# Optimal stereographic projection - Albania
R = 1

# Cartographic pole
uk = 41.14066322*pi/180
vk = 20.06278679*pi/180

# Boundary point
u_j = 42.66026688*pi/180
v_j = 19.71613693*pi/180

#Transformation to the oblique aspect
s1 = asin(sin(u_j) * sin(uk) + cos(u_j) * cos(uk) * cos(vk-v_j))

#Complement of cartographic latitude
psi1 = pi/2 - s1

#Multiplicative constant
mju = (2*(cos(psi1/2))**2)/(1+(cos(psi1/2))**2)

#True parallel
psi0 = 2*acos(sqrt(mju))
s0 = pi/2 - psi0

#Scales
m1 = mju/(cos(psi1/2))**2
mk = mju/(cos(0/2))**2
m0 = mju/(cos(psi0/2))**2

#Distortions
ny1 = (m1 -1) * 1000
nyk = (mk -1) * 1000
ny0 = (m0 -1) * 1000

print(ny1, nyk, ny0)

# ── Visualisation ──────────────────────────────────────────────────────────
import numpy as np
import matplotlib.pyplot as plt

def uv_to_sd(u_deg, v_deg, uk_r, vk_r):
    u = np.radians(u_deg); v = np.radians(v_deg)
    dv = vk_r - v
    s = np.degrees(np.arcsin(np.sin(u)*sin(uk_r) + np.cos(u)*cos(uk_r)*np.cos(dv)))
    d = np.degrees(np.arctan2(np.cos(u)*np.sin(dv),
                              np.cos(u)*sin(uk_r)*np.cos(dv) - np.sin(u)*cos(uk_r)))
    return s, d

def stereo(s_deg, d_deg, s0_r):
    psi  = np.radians(90 - s_deg)
    psi0 = pi/2 - s0_r
    c    = 2 * R * cos(psi0/2)**2
    rho  = c * np.tan(psi/2)
    eps  = np.radians(d_deg)
    X = -rho * np.sin(eps)
    Y = -rho * np.cos(eps)
    return X, Y

# Grid extent
umin, umax, vmin, vmax = 38.5, 43.5, 18.5, 21.5
Du, Dv = 1.0, 1.0

fig, ax = plt.subplots(figsize=(6, 9))
ax.set_aspect('equal')

# Graticule
for u in np.arange(umin, umax + Du, Du):
    vv = np.linspace(vmin, vmax, 300)
    s, d = uv_to_sd(u, vv, uk, vk)
    X, Y = stereo(s, d, s0)
    ax.plot(X, Y, color='black', linewidth=0.4)

for v in np.arange(vmin, vmax + Dv, Dv):
    uu = np.linspace(umin, umax, 300)
    s, d = uv_to_sd(uu, v, uk, vk)
    X, Y = stereo(s, d, s0)
    ax.plot(X, Y, color='black', linewidth=0.4)

# Distortion isolines on meshgrid
llon, llat = np.meshgrid(np.linspace(vmin, vmax, 400),
                         np.linspace(umin, umax, 400))
s_m, d_m = uv_to_sd(llat, llon, uk, vk)
X_m, Y_m = stereo(s_m, d_m, s0)
psi_m = np.radians(90 - s_m)
ny_m = (mju / np.cos(psi_m/2)**2 - 1) * 1000

nu = abs(ny1)
levels_thin = np.arange(-nu*1.5, nu*1.5, nu/4)
levels_bold = [-nu, 0.0, nu]

cs1 = ax.contour(X_m, Y_m, ny_m, levels=levels_thin,
                 colors='red', linewidths=0.5)
cs2 = ax.contour(X_m, Y_m, ny_m, levels=levels_bold,
                 colors='red', linewidths=1.5)
ax.clabel(cs2, fmt='%.4f', fontsize=7, inline=True, inline_spacing=80)

# Country border
country = np.loadtxt('albanie.txt')
s_b, d_b = uv_to_sd(country[:,0], country[:,1], uk, vk)
X_b, Y_b = stereo(s_b, d_b, s0)
ax.plot(X_b, Y_b, 'b-', linewidth=1.5)

# Parameter points K, Pj
for pt, label in [((uk, vk), 'K'), ((u_j, v_j), 'Pj')]:
    s_p, d_p = uv_to_sd(degrees(pt[0]), degrees(pt[1]), uk, vk)
    X_p, Y_p = stereo(s_p, d_p, s0)
    ax.plot(X_p, Y_p, 'm.', markersize=8)
    ax.annotate(label, (X_p, Y_p), textcoords='offset points',
                xytext=(5, 3), fontsize=7, color='magenta')

ax.set_title('Albania - Stereographic projection (conformal azimuthal)', fontsize=10)
plt.tight_layout()
plt.show()
