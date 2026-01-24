# Vesica_Piscis_Inner_Green_Only_INTERACTIVE_NO_INERTIA.py
# Full 3D-interaktion – INGEN automatisk rotation / tröghet

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
import os

pio.renderers.default = "browser"

# ------------------------------------------------------------
# GEOMETRI (oförändrad)
# ------------------------------------------------------------

def create_vesica_circles(r, n=200):
    t = np.linspace(0, 2*np.pi, n)
    x1, y1 = r * np.cos(t) - r/2, r * np.sin(t)
    x2, y2 = r * np.cos(t) + r/2, r * np.sin(t)
    return (x1, y1), (x2, y2)

def rotate_3d(x, y, z, ax, ay, az):
    rad_x, rad_y, rad_z = np.deg2rad(ax), np.deg2rad(ay), np.deg2rad(az)

    if ax != 0:
        y, z = y*np.cos(rad_x) - z*np.sin(rad_x), y*np.sin(rad_x) + z*np.cos(rad_x)
    if ay != 0:
        x, z = x*np.cos(rad_y) + z*np.sin(rad_y), -x*np.sin(rad_y) + z*np.cos(rad_y)
    if az != 0:
        x, y = x*np.cos(rad_z) - y*np.sin(rad_z), x*np.sin(rad_z) + y*np.cos(rad_z)

    return x, y, z

def vesica_circle_nodes(r, rotation=(0,0,0)):
    angles = [0, np.pi/2, np.pi, 3*np.pi/2]
    nodes = []

    for sign in (-1, 1):
        cx_offset = sign * r/2
        for a in angles:
            x = r * np.cos(a) + cx_offset
            y = r * np.sin(a)
            z = 0.0
            rx, ry, rz = rotate_3d(
                np.array([x]), np.array([y]), np.array([z]),
                *rotation
            )
            nodes.append([rx[0], ry[0], rz[0]])

    return nodes

# ------------------------------------------------------------
# BYGG STRUKTUREN
# ------------------------------------------------------------

R = 1.5
GREEN = "#00ff66"

rotations = [
    (45, 45, 0),
    (45, -45, 0),
    (-45, 45, 0),
    (-45, -45, 0)
]

traces = []
nodes = []

for rot in rotations:
    (c1x, c1y), (c2x, c2y) = create_vesica_circles(R)
    for cx, cy in [(c1x, c1y), (c2x, c2y)]:
        z = np.zeros_like(cx)
        rx, ry, rz = rotate_3d(cx, cy, z, *rot)
        traces.append(go.Scatter3d(
            x=rx, y=ry, z=rz,
            mode="lines",
            line=dict(color=GREEN, width=4),
            opacity=0.9,
            showlegend=False,
            hoverinfo="none"
        ))

    nodes.extend(vesica_circle_nodes(R, rot))

# Trådar
for i in range(len(nodes)):
    for j in range(i+1, len(nodes)):
        traces.append(go.Scatter3d(
            x=[nodes[i][0], nodes[j][0]],
            y=[nodes[i][1], nodes[j][1]],
            z=[nodes[i][2], nodes[j][2]],
            mode="lines",
            line=dict(color="white", width=1),
            opacity=0.18,
            showlegend=False,
            hoverinfo="none"
        ))

# Noder
traces.append(go.Scatter3d(
    x=[n[0] for n in nodes],
    y=[n[1] for n in nodes],
    z=[n[2] for n in nodes],
    mode="markers",
    marker=dict(size=4, color=GREEN),
    showlegend=False,
    hoverinfo="none"
))

# ------------------------------------------------------------
# INTERAKTIV SCEN – UTAN TRÖGHET
# ------------------------------------------------------------

fig = go.Figure(data=traces)

fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode="data",
        dragmode="orbit"  # manuell rotation
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

OUTPUT = "Inner_Green_Vesica_INTERACTIVE_NO_INERTIA.html"
fig.write_html(
    OUTPUT,
    config=dict(
        scrollZoom=True,
        displayModeBar=True,
        displaylogo=False,
        responsive=True,
        staticPlot=False  # 🔑 interaktiv men utan lås
    )
)

webbrowser.open("file://" + os.path.abspath(OUTPUT))
fig.show()
