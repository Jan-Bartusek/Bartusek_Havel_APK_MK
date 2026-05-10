from math import *

#Optimal Mercator projection - Albania

# Points on the cartographic equator
u1 = 42.65212667*pi/180
v1 = 20.20247814*pi/180

u2 = 39.64903031*pi/180
v2 = 20.13008780*pi/180

# Left/right border points of the belt
u3 = 41.17571062*pi/180
v3 = 19.27278722*pi/180

u4 = 41.17405211*pi/180
v4 = 21.07265105*pi/180

#Pole
vk = atan2(tan(u1)*cos(v2)-tan(u2)*cos(v1), tan(u2)*sin(v1)-tan(u1)*sin(v2))
uk = atan(-1/tan(u2)*cos(vk-v2))

#Transformation to the oblique aspect
s1 = asin(sin(u1) * sin(uk) + cos(u1) * cos(uk) * cos(vk-v1))
s2 = asin(sin(u2) * sin(uk) + cos(u2) * cos(uk) * cos(vk-v2))
s3 = asin(sin(u3) * sin(uk) + cos(u3) * cos(uk) * cos(vk-v3))
s4 = asin(sin(u4) * sin(uk) + cos(u4) * cos(uk) * cos(vk-v4))

#True parallel
s0 = acos(2*cos(s3)/(1+cos(s3)))

#Scales
m1 = cos(s0)/cos(s1)
m2 = cos(s0)/cos(s2)
m3 = cos(s0)/cos(s3)
m4 = cos(s0)/cos(s4)

#Distortions
ny1 = (m1 -1) *1000
ny2 = (m2 -1) *1000
ny3 = (m3 -1) *1000
ny4 = (m4 -1) *1000

print(ny1, ny2, ny3, ny4)

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

def mercator(s_deg, d_deg, s0_r):
    X = cos(s0_r) * np.radians(d_deg)
    Y = np.log(np.tan(np.radians(s_deg)/2 + pi/4))
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
    X, Y = mercator(s, d, s0)
    ax.plot(X, Y, color='black', linewidth=0.4)

for v in np.arange(vmin, vmax + Dv, Dv):
    uu = np.linspace(umin, umax, 300)
    s, d = uv_to_sd(uu, v, uk, vk)
    X, Y = mercator(s, d, s0)
    ax.plot(X, Y, color='black', linewidth=0.4)

# Distortion isolines on meshgrid
llon, llat = np.meshgrid(np.linspace(vmin, vmax, 400),
                         np.linspace(umin, umax, 400))
s_m, d_m = uv_to_sd(llat, llon, uk, vk)
X_m, Y_m = mercator(s_m, d_m, s0)
ny_m = (cos(s0) / np.cos(np.radians(s_m)) - 1) * 1000

nu = abs(ny4)
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
X_b, Y_b = mercator(s_b, d_b, s0)
ax.plot(X_b, Y_b, 'b-', linewidth=1.5)

# Parameter points P1, P2, Ps
for pt, label in [((u1, v1), 'P1'), ((u2, v2), 'P2'), ((u3, v3), 'Ps')]:
    s_p, d_p = uv_to_sd(degrees(pt[0]), degrees(pt[1]), uk, vk)
    X_p, Y_p = mercator(s_p, d_p, s0)
    ax.plot(X_p, Y_p, 'm.', markersize=8)
    ax.annotate(label, (X_p, Y_p), textcoords='offset points',
                xytext=(5, 3), fontsize=7, color='magenta')

ax.set_title('Albania - Mercator (conformal cylindrical)', fontsize=10)
plt.tight_layout()
plt.show()
