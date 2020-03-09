from app import domain
from app import model


class Loader:
    coordinates = []
    material = {}

    def load(self, path):

        def read():
            with open(path) as file:
                lines = file.read().splitlines()

                for line in lines:
                    if line:
                        yield line.split(" ")

                raise StopIteration

        name = 'None'
        color = (.5, .5, .5)
        cstype = 'None'
        mtl = None

        coordinate_arg = lambda: tuple(float(arg) for arg in args)
        unique_arg = lambda: args[0]

        for cmd, *args in read():
            # Argument
            if cmd == 'v':
                self.coordinates.append(coordinate_arg())
                continue

            if cmd == 'newmtl':
                mtl = unique_arg()
                continue

            if cmd == 'Kd':
                self.material[mtl] = coordinate_arg()
                mtl = None
                continue

            if cmd in ['o', 'g']:
                name = str(unique_arg())
                continue

            if cmd == 'usemtl':
                color = self.material[unique_arg()]
                continue

            if cmd == 'cstype':
                cstype = 'Bezier' if unique_arg() == 'bezier' else 'BSpine'
                continue

            # Window
            if cmd == 'w':
                model.LANDSCAPE.recenter(coordinate_arg())
                continue

            # Object
            type = {
                'p': 'Point',
                'l': 'Line' if len(args) == 2 else 'Chain',
                'f': 'Face',
                # 'curv2': cstype + '_curve',
                'curv': cstype + '_curve',
                'surf': cstype + '_surface',
            }[cmd]

            obj_args = dict(zip(
                ['name', 'type', 'color', 'coordinates'],
                (name, type, color, [self.get_coordinate(i) for i in args])
            ))

            domain.create(**obj_args)

            name, color, cstype, = 'None', (0, 0, 0), 'None'

    def get_coordinate(self, i):
        return self.coordinates[int(i)-1]