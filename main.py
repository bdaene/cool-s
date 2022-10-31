import svg

STROKE = dict(stroke='#000000', stroke_width=0.1)


def get_straight(group_id, colors, transform):
    return svg.G(id=group_id, transform=transform, elements=[
        svg.Polyline(points=[1, 2, 2, 1, 2, -1, 1, -2, 0, -1, 0, 1, -1, 2], fill=colors[0], **STROKE),
        svg.Polyline(points=[-1, -2, -2, -1, -2, 1, -1, 2, 0, 1, 0, -1, 1, -2], fill=colors[1], **STROKE),
    ])


def get_corner(group_id, colors, transform):
    return svg.G(id=group_id, transform=transform, elements=[
        svg.Polyline(points=[-1, -2, -2, -1, -2, 1, -1, 2, 1, 2, 2, 1, 1, 0, 0, 0, 0, -1, 1, -2],
                     fill=colors[0], **STROKE),
        svg.Polyline(points=[2, -1, 1, -2, 0, -1, 2, 1], fill=colors[1], **STROKE),
    ])


def get_definitions(colors):
    for rotation in range(0, 360, 90):
        yield get_straight(f'straight_out_{rotation:03}', colors, [svg.Rotate(rotation)])
        yield get_straight(f'straight_in_{rotation:03}', colors[::-1], [svg.Rotate(rotation)])
        yield get_corner(f'corner_out_{rotation:03}', colors, [svg.Rotate(rotation)])
        yield get_corner(f'corner_in_{rotation:03}', colors[::-1], [svg.Rotate(rotation)])


def draw(size, out):
    offset = (size - 1) / 2 * 4
    if out:
        a, b = 'out', 'in'
    else:
        a, b = 'in', 'out'

    # Corners
    yield svg.Use(x=-offset, y=-offset, href=f'#corner_{a}_090')
    yield svg.Use(x=offset, y=offset, href=f'#corner_{a}_270')
    yield svg.Use(x=-offset, y=offset, href=f'#corner_{a if size % 2 else b}_000')
    yield svg.Use(x=offset, y=-offset, href=f'#corner_{a if size % 2 else b}_180')

    # Straights
    for i in range(1, size - 1):
        yield svg.Use(x=-offset, y=-offset + 4 * i, href=f'#straight_{a if i % 2 else b}_000')
        yield svg.Use(x=offset, y=-offset + 4 * i, href=f'#straight_{a if (i + size) % 2 else b}_000')
        yield svg.Use(x=-offset + 4 * i, y=-offset, href=f'#straight_{a if i % 2 else b}_090')
        yield svg.Use(x=-offset + 4 * i, y=offset, href=f'#straight_{a if (i + size) % 2 else b}_090')


def main(max_size, colors=True):
    if colors:
        colors = ('#dd7777', '#FFB60C')
    else:
        colors = ('#00000000', '#ffffff00')

    scale = 20
    canvas_size = 4 * (max_size + 1) * scale
    offset = canvas_size // 2

    definitions = svg.Defs(elements=list(get_definitions(colors)))
    main_group = svg.G(elements=[], transform=[svg.Translate(offset, offset), svg.Scale(scale)])
    canvas = svg.SVG(width=canvas_size, height=canvas_size, elements=[definitions, main_group])

    out = True
    for size in range(2 + max_size % 2, max_size + 1, 2):
        main_group.elements.extend(draw(size, out))
        out = not out

    with open('cool-s.svg', 'w') as file:
        print(canvas, file=file)


if __name__ == "__main__":
    main(max_size=6, colors=True)
