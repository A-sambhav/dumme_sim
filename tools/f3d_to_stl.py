"""Extract the coloured display mesh from a Fusion 360 .f3d file as binary STLs.

Fusion stores a render mesh next to the B-rep, zstd-compressed inside the .f3d zip:
  OGS.BlobFolder/OGS/DefaultScene/world            scene graph (bodies, appearances, buffers)
  OGS.BlobFolder/OGS/DefaultScene/stream_mesh_000  raw vertex/index buffers
  ProteinAssets.BlobParts/*.protein                appearance library (diffuse colours)
Only triangle meshes are kept (edges and origin-plane gizmos are dropped), and each
one takes the appearance of the body it belongs to. Fusion's internal unit is cm.

usage: f3d_to_stl.py model.f3d out_dir [scale]     (scale 0.01 -> metres)

Writes out_dir/<appearance>.stl per appearance and prints a JSON list of
{"mesh": file, "rgb": [r, g, b], "triangles": n} to stdout.
"""
import collections
import io
import json
import os
import re
import struct
import subprocess
import sys
import zipfile

SCENE = 'FusionAssetName[Active]/OGS.BlobFolder/OGS/DefaultScene/'
GUID = rb'[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}'


def read_member(path, name):
    """Read a zip member; zipfile can't do zstd (method 93), so use the zstd CLI."""
    z = zipfile.ZipFile(path)
    info = z.getinfo(name)
    if info.compress_type != 93:
        return z.read(info)
    raw = open(path, 'rb').read()
    h = info.header_offset
    n, e = struct.unpack_from('<HH', raw, h + 26)
    start = h + 30 + n + e
    return subprocess.run(['zstd', '-d', '-c'], input=raw[start:start + info.compress_size],
                          capture_output=True, check=True).stdout


def appearance_colours(f3d):
    """GUID -> diffuse RGB, from the 'Generic' appearance records."""
    names = zipfile.ZipFile(f3d).namelist()
    protein = read_member(f3d, next(n for n in names if n.endswith('.protein')))
    pz = zipfile.ZipFile(io.BytesIO(protein))
    inst = pz.read(next(n for n in pz.namelist() if n.endswith('AssetData/InstanceProperties.bin')))
    colours = {}
    for m in re.finditer(GUID, inst):
        g, i = m.group().decode(), m.start()
        rec = inst[i:i + 240]
        # the generic_diffuse colour: 3 doubles at a fixed offset in the record
        if g in colours or inst[i + 36:i + 37] == b'_' or len(rec) < 240 or rec[214] != 0x3f:
            continue
        rgb = struct.unpack_from('<3d', rec, 207)
        if all(0 <= c <= 1 for c in rgb):
            colours[g] = [round(c, 3) for c in rgb]
    return colours


f3d, out_dir = sys.argv[1], sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
world = read_member(f3d, SCENE + 'world')
stream = read_member(f3d, SCENE + 'stream_mesh_000')
colours = appearance_colours(f3d)

U = lambda s: s.encode('utf-16-le')  # noqa: E731
KM, KI, KV = U('OgsSimpleMesh'), U('AIndexBuffer'), U('VertexFormat')
KP = U('FProteinEffectAttribute')
GUID16 = re.compile(rb'(?:[0-9A-F]\x00|-\x00){36}')  # UTF-16 GUID


def find_all(k):
    out, i = [], 0
    while (i := world.find(k, i)) >= 0:
        out.append(i)
        i += 1
    return out


def skip_str(q):
    ln, = struct.unpack_from('<I', world, q)
    return q + 4 + 2 * ln


# Each body's appearance attribute precedes its face meshes in the stream.
appearance_at = []
for a in find_all(KP):
    m = GUID16.search(world, a, a + 200)
    if m:
        appearance_at.append((a, m.group().decode('utf-16-le')))

meshes = find_all(KM)
stats = collections.Counter()
tris = collections.defaultdict(list)
ai = 0
for n, j in enumerate(meshes):
    # a body's appearance attribute follows its face meshes in the stream
    while ai < len(appearance_at) and appearance_at[ai][0] < j:
        ai += 1
    look = appearance_at[ai][1] if ai < len(appearance_at) else None
    end = meshes[n + 1] if n + 1 < len(meshes) else len(world)
    p = j + len(KM) + 24  # skip bbox (6 floats)
    prim, = struct.unpack_from('<I', world, p)
    if prim != 4:  # 4 = triangle list; others are edges/points
        continue
    v = world.find(KV, p, end)
    q = skip_str(v + len(KV))
    flag, _, voff, vlen = struct.unpack_from('<IIII', world, q)
    k = world.find(KI, p, end)
    if v < 0 or k < 0 or flag != 1:
        stats['skip_layout'] += 1
        continue
    q = skip_str(k + len(KI)) + 5
    ioff, ilen = struct.unpack_from('<II', world, q)
    idx = None
    for fmt, sz in (('I', 4), ('H', 2)):
        if ilen % sz or ioff + ilen > len(stream):
            continue
        cand = struct.unpack_from(f'<{ilen // sz}{fmt}', stream, ioff)
        nv = max(cand) + 1
        if vlen % nv == 0 and 12 <= vlen // nv <= 64:
            idx, stride = cand, vlen // nv
            break
    if idx is None:
        stats['skip_index'] += 1
        continue
    if stride == 32:  # work geometry (origin planes), not the model
        stats['skip_origin'] += 1
        continue
    stats['meshes'] += 1
    verts = [tuple(c * scale for c in struct.unpack_from('<3f', stream, voff + i * stride))
             for i in range(nv)]
    key = look if look in colours else 'default'
    for a in range(0, len(idx) - 2, 3):
        tris[key].append((verts[idx[a]], verts[idx[a + 1]], verts[idx[a + 2]]))

print(dict(stats), file=sys.stderr)
os.makedirs(out_dir, exist_ok=True)
manifest = []
for i, (key, ts) in enumerate(sorted(tris.items(), key=lambda kv: -len(kv[1]))):
    rgb = colours.get(key, [0.7, 0.7, 0.7])
    name = 'part_%02d_%02x%02x%02x.stl' % (i, *(int(c * 255) for c in rgb))
    with open(os.path.join(out_dir, name), 'wb') as f:
        f.write(b'\0' * 80 + struct.pack('<I', len(ts)))
        for t in ts:
            f.write(struct.pack('<12fH', 0, 0, 0, *t[0], *t[1], *t[2], 0))
    manifest.append({'mesh': name, 'rgb': rgb, 'triangles': len(ts)})
print(json.dumps(manifest, indent=1))
