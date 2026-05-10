from math import *

# Optimal LCC projection - Albania
R = 1

# Cartographic pole
uk = 41.32138022*pi/180
vk = 21.01448058*pi/180

# Outer boundary parallel
u_s = 42.18000603*pi/180
v_s = 19.28578568*pi/180

# Inner boundary parallel
u_j = 41.40751839*pi/180
v_j = 20.56193876*pi/180

#Transformation to the oblique aspect
s1 = asin(sin(u_s) * sin(uk) + cos(u_s) * cos(uk) * cos(vk-v_s))
s2 = asin(sin(u_j) * sin(uk) + cos(u_j) * cos(uk) * cos(vk-v_j))

#Constant c of the conic projection
cn = log10(cos(s1)) - log10(cos(s2))
cd = log10(tan(s2/2+pi/4))-log10(tan(s1/2+pi/4))
c = cn / cd

#Compute s0
s0 = asin(c)

#Compute rho0: radius of the parallel (u = u0)
rho0_n = 2*R*cos(s0)*cos(s1)*(tan(s1/2+pi/4))**c
rho0_d = c*(cos(s0)*(tan(s0/2+pi/4))**c+cos(s1)*(tan(s1/2+pi/4))**c)
rho0 = rho0_n/rho0_d

#Compute rho1: radius of the north parallel (u = u1)
rho1 = rho0*((tan(s0/2+pi/4))/(tan(s1/2+pi/4)))**c

#Compute rho2: radius of the south parallel (u = u2)
rho2 = rho0*((tan(s0/2+pi/4))/(tan(s2/2+pi/4)))**c

#Scales
m1 = (c * rho1)/(R * cos(s1))
m2 = (c * rho2)/(R * cos(s2))
m0 = (c * rho0)/(R * cos(s0))

ny1 = (m1 -1) * 1000
ny2 = (m2 -1) * 1000
ny0 = (m0 - 1) * 1000

print(ny1, ny2, ny0)

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

def lcc(s_deg, d_deg, s0_r, rho0_v, c_v):
    s = np.radians(s_deg)
    rho = rho0_v * (tan(s0_r/2 + pi/4) / np.tan(s/2 + pi/4))**c_v
    eps = c_v * np.radians(d_deg)
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
    X, Y = lcc(s, d, s0, rho0, c)
    ax.plot(X, Y, color='black', linewidth=0.4)

for v in np.arange(vmin, vmax + Dv, Dv):
    uu = np.linspace(umin, umax, 300)
    s, d = uv_to_sd(uu, v, uk, vk)
    X, Y = lcc(s, d, s0, rho0, c)
    ax.plot(X, Y, color='black', linewidth=0.4)

# Distortion isolines on meshgrid
llon, llat = np.meshgrid(np.linspace(vmin, vmax, 400),
                         np.linspace(umin, umax, 400))
s_m, d_m = uv_to_sd(llat, llon, uk, vk)
X_m, Y_m = lcc(s_m, d_m, s0, rho0, c)
s_r = np.radians(s_m)
rho_m = rho0 * (tan(s0/2 + pi/4) / np.tan(s_r/2 + pi/4))**c
ny_m = (c * rho_m / (R * np.cos(s_r)) - 1) * 1000

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
X_b, Y_b = lcc(s_b, d_b, s0, rho0, c)
ax.plot(X_b, Y_b, 'b-', linewidth=1.5)

# Parameter points K, Ps, Pj
for pt, label in [((uk, vk), 'K'), ((u_s, v_s), 'Ps'), ((u_j, v_j), 'Pj')]:
    s_p, d_p = uv_to_sd(degrees(pt[0]), degrees(pt[1]), uk, vk)
    X_p, Y_p = lcc(s_p, d_p, s0, rho0, c)
    ax.plot(X_p, Y_p, 'm.', markersize=8)
    ax.annotate(label, (X_p, Y_p), textcoords='offset points',
                xytext=(5, 3), fontsize=7, color='magenta')

ax.set_title('Albania - Lambert (conformal conic)', fontsize=10)
plt.tight_layout()
plt.show()
