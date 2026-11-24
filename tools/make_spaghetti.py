"""Generate a 3D-print "spaghetti" failure mesh (tangled filament nest) as binary STL.

Each strand is a filament tube following a curly random path: its heading turns
with a smoothly varying rate (that makes the loops), is pulled back toward the
nest when it wanders out, and sags under 'gravity' so the nest is densest near
the bed. Origin = centre of the nest footprint on the bed surface, +Z up.

usage: make_spaghetti.py out.stl [seed]
"""
import struct
import sys

import numpy as np

SIDES = 6                 # tube cross-section polygon
FIL_R = 0.00085           # 1.75 mm filament
NEST = np.array([0.050, 0.040, 0.030])  # nest half-size x, y and height (m)
STRANDS = 45
STEPS = 220
STEP = 0.0016             # path step (m)


def strand(rng):
    p = rng.uniform(-1, 1, 3) * NEST * [0.8, 0.8, 0]
    p[2] = rng.uniform(FIL_R, NEST[2])
    d = rng.normal(size=3)
    d /= np.linalg.norm(d)
    axis = rng.normal(size=3)
    pts = [p.copy()]
    for _ in range(STEPS):
        axis += rng.normal(scale=0.35, size=3)            # slowly changing curl axis
        axis /= np.linalg.norm(axis)
        rate = rng.uniform(0.12, 0.35)                     # loop radius ~5-13 mm
        d = d * np.cos(rate) + np.cross(axis, d) * np.sin(rate) + axis * (axis @ d) * (1 - np.cos(rate))
        q = p / NEST
        if q[0] ** 2 + q[1] ** 2 > 1:                      # steer back into the nest
            d[:2] -= 0.25 * q[:2]
        d[2] -= 0.04 + (0.3 if p[2] > NEST[2] else 0)      # sag
        d /= np.linalg.norm(d)
        p = p + d * STEP
        if p[2] < FIL_R:                                   # lie on the bed
            p[2], d[2] = FIL_R, abs(d[2]) * 0.3
        pts.append(p.copy())
    return np.array(pts)


def tube(path):
    """Triangles of a tube along `path` (parallel-transport frames)."""
    t = np.gradient(path, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True)
    n = np.cross(t[0], [0, 0, 1] if abs(t[0][2]) < 0.9 else [1, 0, 0])
    n /= np.linalg.norm(n)
    rings = []
    ang = np.linspace(0, 2 * np.pi, SIDES, endpoint=False)
    for i, c in enumerate(path):
        n = n - t[i] * (n @ t[i])
        n /= np.linalg.norm(n)
        b = np.cross(t[i], n)
        rings.append(c + FIL_R * (np.outer(np.cos(ang), n) + np.outer(np.sin(ang), b)))
    tris = []
    for a, b in zip(rings[:-1], rings[1:]):
        for k in range(SIDES):
            k2 = (k + 1) % SIDES
            tris += [(a[k], b[k], b[k2]), (a[k], b[k2], a[k2])]
    return tris


def main():
    rng = np.random.default_rng(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
    tris = []
    for _ in range(STRANDS):
        tris += tube(strand(rng))
    with open(sys.argv[1], 'wb') as f:
        f.write(b'\0' * 80 + struct.pack('<I', len(tris)))
        for t in tris:
            f.write(struct.pack('<12fH', 0, 0, 0, *t[0], *t[1], *t[2], 0))
    v = np.array(tris).reshape(-1, 3)
    print(f'{len(tris)} triangles, bounds {v.min(0).round(3)} .. {v.max(0).round(3)}')


if __name__ == '__main__':
    main()
