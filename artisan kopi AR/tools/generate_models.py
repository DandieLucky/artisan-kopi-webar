import itertools
import math
import os

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "models")
os.makedirs(OUT, exist_ok=True)

def rgba(hex_color, alpha=255):
    value = hex_color.lstrip("#")
    return np.array([int(value[i:i + 2], 16) for i in (0, 2, 4)] + [alpha], dtype=np.uint8)

def pbr(name, color, alpha=1.0, roughness=0.28, metallic=0.0):
    return PBRMaterial(
        name=name,
        baseColorFactor=rgba(color, round(alpha * 255)).tolist(),
        metallicFactor=metallic,
        roughnessFactor=roughness,
        alphaMode="BLEND" if alpha < 0.999 else "OPAQUE",
        doubleSided=True,
    )

def add(scene, name, mesh, material):
    mesh.visual.material = material
    scene.add_geometry(mesh, geom_name=name, node_name=name)

def hex_mix(stops, t):
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        if t0 <= t <= t1:
            a = rgba(c0)[:3].astype(float)
            b = rgba(c1)[:3].astype(float)
            rgb = np.clip(a + (b - a) * ((t - t0) / (t1 - t0)), 0, 255).astype(int)
            return "#{:02x}{:02x}{:02x}".format(*rgb)
    return stops[-1][1]

def lathe(profile, sections=112):
    vertices, faces = [], []
    for radius, y in profile:
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            vertices.append([radius * math.cos(angle), y, radius * math.sin(angle)])
    for j in range(len(profile)):
        j2 = (j + 1) % len(profile)
        for i in range(sections):
            i2 = (i + 1) % sections
            a, b = j * sections + i, j * sections + i2
            c, d = j2 * sections + i2, j2 * sections + i
            faces.extend([[a, b, c], [a, c, d]])
    mesh = trimesh.Trimesh(vertices=np.asarray(vertices), faces=np.asarray(faces), process=True)
    mesh.fix_normals()
    return mesh

def frustum_band(y0, y1, r0, r1, sections=112):
    vertices, faces = [], []
    for radius, y in ((r0, y0), (r1, y1)):
        for i in range(sections):
            angle = 2 * math.pi * i / sections
            vertices.append([radius * math.cos(angle), y, radius * math.sin(angle)])
    for i in range(sections):
        j = (i + 1) % sections
        a, b, c, d = i, j, sections + j, sections + i
        faces.extend([[a, b, c], [a, c, d]])
    mesh = trimesh.Trimesh(vertices=np.asarray(vertices), faces=np.asarray(faces), process=True)
    mesh.fix_normals()
    return mesh

def cylinder_y(radius, height, y, sections=96):
    mesh = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    mesh.apply_translation([0, y, 0])
    return mesh

def torus_y(major, minor, y):
    mesh = trimesh.creation.torus(major_radius=major, minor_radius=minor, major_sections=96, minor_sections=16)
    mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    mesh.apply_translation([0, y, 0])
    return mesh

def rounded_ice(extents, position, rotation):
    points = []
    # A truncated cube gives ice a recognisable block shape with softened corners.
    for perm in set(itertools.permutations((1.0, 0.76, 0.76))):
        for signs in itertools.product((-1.0, 1.0), repeat=3):
            points.append(np.asarray(perm) * np.asarray(signs) * np.asarray(extents) / 2)
    mesh = trimesh.convex.convex_hull(np.asarray(points))
    matrix = trimesh.transformations.euler_matrix(*rotation, axes="sxyz")
    mesh.apply_transform(matrix)
    mesh.apply_translation(position)
    return mesh

def sphere(radius, position, scale=(1, 1, 1)):
    mesh = trimesh.creation.icosphere(subdivisions=2, radius=radius)
    mesh.apply_scale(scale)
    mesh.apply_translation(position)
    return mesh

def tube(points, radius, sections=12):
    pts = np.asarray(points, dtype=float)
    vertices, faces = [], []
    for i, point in enumerate(pts):
        tangent = pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]
        tangent /= np.linalg.norm(tangent) + 1e-9
        reference = np.array([0.0, 1.0, 0.0])
        if abs(np.dot(tangent, reference)) > 0.92:
            reference = np.array([1.0, 0.0, 0.0])
        axis_a = np.cross(tangent, reference)
        axis_a /= np.linalg.norm(axis_a) + 1e-9
        axis_b = np.cross(tangent, axis_a)
        for j in range(sections):
            angle = 2 * math.pi * j / sections
            vertices.append(point + radius * (math.cos(angle) * axis_a + math.sin(angle) * axis_b))
    for i in range(len(pts) - 1):
        for j in range(sections):
            j2 = (j + 1) % sections
            a, b = i * sections + j, i * sections + j2
            c, d = (i + 1) * sections + j2, (i + 1) * sections + j
            faces.extend([[a, b, c], [a, c, d]])
    mesh = trimesh.Trimesh(vertices=np.asarray(vertices), faces=np.asarray(faces), process=True)
    mesh.fix_normals()
    return mesh

def front_surface_z(x, y):
    radius = 0.195 + (y - 0.105) * (0.074 / 0.915)
    return math.sqrt(max(radius * radius - x * x, 0.001)) + 0.003

ICE_POSITIONS = [
    ((0.115, 0.095, 0.115), (-0.125, 1.045, 0.015), (0.12, 0.18, -0.22)),
    ((0.115, 0.090, 0.110), (-0.025, 1.055, 0.105), (-0.10, -0.28, 0.18)),
    ((0.105, 0.090, 0.110), (0.105, 1.045, 0.055), (0.18, 0.35, 0.10)),
    ((0.110, 0.085, 0.105), (0.025, 1.035, -0.105), (-0.16, 0.15, 0.25)),
]

SPECS = {
    "aren-latte": {
        "label": "Aren Latte",
        "stops": [(0, "#ead9bd"), (.22, "#e4c99f"), (.48, "#c9965f"), (.73, "#9b5d32"), (1, "#63351f")],
        "top": "#754122", "drizzle": "#a86632", "drizzle_lines": [(-.12, .035, .2), (-.015, .030, 2.0), (.105, .025, 4.0)],
        "swirl": "#c28a50", "ice": True, "foam": None,
    },
    "butterscotch-latte": {
        "label": "Butterscotch Latte",
        "stops": [(0, "#f1e2ca"), (.25, "#ead3ad"), (.50, "#d4a16b"), (.76, "#b8753e"), (1, "#8b4b25")],
        "top": "#995526", "drizzle": "#e1a85f", "drizzle_lines": [(-.13, .030, 1.0), (-.025, .038, 3.0), (.095, .028, 5.0)],
        "swirl": "#e5b66f", "ice": True, "foam": None,
    },
    "seasalt-caramel-latte": {
        "label": "Seasalt Caramel Latte",
        "stops": [(0, "#f3e7d3"), (.25, "#e8d2b1"), (.50, "#c99567"), (.76, "#a7673b"), (1, "#814522")],
        "top": "#a45d31", "drizzle": "#c47a3c", "drizzle_lines": [(-.12, .034, .7), (-.015, .030, 2.8), (.10, .026, 4.7)],
        "swirl": "#bd793d", "ice": True, "foam": "#f4eadb",
    },
    "matcha-latte": {
        "label": "Matcha Latte",
        "stops": [(0, "#f1e7d4"), (.27, "#e6e1c7"), (.52, "#c5cd9d"), (.78, "#91a66a"), (1, "#627c43")],
        "top": "#78914d", "drizzle": "#e9e3ce", "drizzle_lines": [(-.10, .030, .8), (.015, .035, 2.8), (.11, .022, 4.5)],
        "swirl": "#eee6d2", "ice": True, "foam": None,
    },
    "americano": {
        "label": "Americano",
        "stops": [(0, "#482719"), (.30, "#512d1c"), (.58, "#683a22"), (.82, "#87502b"), (1, "#a96735")],
        "top": "#a15d30", "drizzle": "#6e3c22", "drizzle_lines": [(-.06, .025, 1.3), (.075, .025, 4.1)],
        "swirl": "#c18a53", "ice": True, "foam": None,
    },
}

def build_model(key, spec):
    scene = trimesh.Scene()

    # Thin transparent wall: the drink remains visible through the glass in mobile AR.
    glass = lathe([
        (.214, .025), (.224, .055), (.296, 1.115), (.302, 1.15),
        (.296, 1.15), (.286, 1.115), (.207, .070), (.204, .052),
    ])
    add(scene, "Very clear glass wall", glass, pbr("clear glass", "#f8fcff", .035, .035, .02))
    add(scene, "Glass foot", cylinder_y(.218, .026, .038), pbr("thick clear glass base", "#eaf5f8", .10, .06))
    add(scene, "Glass top rim", torus_y(.299, .009, 1.145), pbr("polished glass rim", "#ffffff", .72, .08))
    add(scene, "Glass base rim", torus_y(.216, .006, .061), pbr("glass base highlight", "#f4fbff", .55, .08))

    # The liquid uses separate PBR materials rather than vertex colours.
    # This keeps the five drinks visibly different in A-Frame on mobile devices.
    y_bottom, y_top = .105, 1.015
    segments = 12
    for i in range(segments):
        t0, t1 = i / segments, (i + 1) / segments
        y0 = y_bottom + (y_top - y_bottom) * t0
        y1 = y_bottom + (y_top - y_bottom) * t1
        r0 = .195 + (.270 - .195) * t0
        r1 = .195 + (.270 - .195) * t1
        band = frustum_band(y0, y1, r0, r1)
        color = hex_mix(spec["stops"], (t0 + t1) / 2)
        add(scene, "Drink gradient layer {:02d}".format(i + 1), band,
            pbr("drink layer {:02d}".format(i + 1), color, 1.0, .25))

    add(scene, "Liquid bottom", cylinder_y(.196, .008, .109), pbr("liquid base", spec["stops"][0][1], 1, .3))
    add(scene, "Liquid surface", cylinder_y(.270, .010, 1.014), pbr("coffee meniscus", spec["top"], 1, .22))

    if spec["foam"]:
        add(scene, "Sea salt cream layer", cylinder_y(.263, .018, 1.025),
            pbr("sea salt cream", spec["foam"], 1, .52))

    # Broad, visible syrup ribbons follow the front curvature of the drink.
    for line_index, (center_x, amplitude, phase) in enumerate(spec["drizzle_lines"]):
        points = []
        for step in range(32):
            t = step / 31
            y = .30 + .68 * t
            x = center_x + amplitude * math.sin(t * math.pi * 2.0 + phase)
            z = front_surface_z(x, y)
            points.append([x, y, z])
        add(scene, "Visible syrup ribbon {:02d}".format(line_index + 1),
            tube(points, .0085), pbr("syrup ribbon", spec["drizzle"], 1, .28))

    # Surface swirl, visible between the ice pieces.
    spiral = []
    for i in range(72):
        t = i / 71
        angle = 2 * math.pi * 1.8 * t + .25
        radius = .018 + .17 * t
        spiral.append([radius * math.cos(angle), 1.037 + .002 * math.sin(angle * 2), radius * math.sin(angle)])
    add(scene, "Cream and syrup surface swirl", tube(spiral, .0055),
        pbr("surface swirl", spec["swirl"], 1, .34))

    # Four bevelled, translucent ice blocks. Their shape reads as ice rather than foam.
    for i, (extents, position, rotation) in enumerate(ICE_POSITIONS):
        cube = rounded_ice(extents, position, rotation)
        tint = "#d9eef5" if i % 2 == 0 else "#eef8fb"
        add(scene, "Translucent ice cube {:02d}".format(i + 1), cube,
            pbr("ice glass", tint, .46, .075, .02))
        highlight_points = [
            [position[0] - extents[0] * .25, position[1] + extents[1] * .32, position[2] + extents[2] * .45],
            [position[0] + extents[0] * .05, position[1] + extents[1] * .36, position[2] + extents[2] * .43],
            [position[0] + extents[0] * .28, position[1] + extents[1] * .20, position[2] + extents[2] * .35],
        ]
        add(scene, "Ice highlight {:02d}".format(i + 1), tube(highlight_points, .0025),
            pbr("ice highlight", "#ffffff", .68, .08))

    # Fine condensation beads on the front of the glass.
    droplets = [(-.205, .38), (.205, .52), (-.17, .73), (.16, .84), (.04, .26)]
    for i, (x, y) in enumerate(droplets):
        z = math.sqrt(max(.296 * .296 - x * x, .001)) + .002
        bead = sphere(.008 if i % 2 else .010, [x, y, z], (1, .8, .8))
        add(scene, "Condensation bead {:02d}".format(i + 1), bead,
            pbr("condensation", "#ffffff", .34, .06))

    # Two narrow highlights define the transparent tumbler silhouette.
    for side, x in (("left", -.287), ("right", .287)):
        points = []
        for i in range(28):
            y = .12 + .98 * i / 27
            z = math.sqrt(max(.296 * .296 - x * x, .001)) + .004
            points.append([x, y, z])
        add(scene, "Glass edge highlight " + side, tube(points, .0028),
            pbr("glass highlight", "#ffffff", .55, .07))

    scene.metadata = {
        "product": spec["label"],
        "brand": "Kedai Artisan Kopi",
        "model": "Iced coffee glass with layered PBR materials",
    }
    return scene

for model_key, model_spec in SPECS.items():
    scene = build_model(model_key, model_spec)
    output_path = os.path.join(OUT, model_key + ".glb")
    with open(output_path, "wb") as output_file:
        output_file.write(scene.export(file_type="glb"))
    check = trimesh.load(output_path, force="scene")
    assert len(check.geometry) >= 35, (model_key, len(check.geometry))
    assert check.bounds[1][1] > 1.14, (model_key, check.bounds)
    print("Built", output_path, os.path.getsize(output_path), "bytes", len(check.geometry), "meshes")
