try:
    from .pattern_convertor import convert_pattern
except ImportError:
    from pattern_convertor import convert_pattern


def build_pattern(text: str) -> str:
    if text is None:
        raise ValueError('Nebyl zadán platný text.')

    converted = convert_pattern(text)
    if converted.startswith('Chybný formát vzoru:') or converted.startswith('Nebyl zadán'):
        raise ValueError(converted)

    return converted


class PatternRozpr:
    #čte text a tvoří data pro následovníky

    def __init__(self, text: str):
        self._text = text or ''
        self._lines = self._text.replace('\r\n', '\n').replace('\r', '\n').splitlines()
        self._index = -1
        self.aktualni_rada = ''
        self.cislo_rady = 0
        self.pocet_ok = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next_row()

    def next_row(self):
        #další řada
        if self._index + 1 >= len(self._lines):
            raise StopIteration

        self._index += 1
        self.aktualni_rada = self._lines[self._index]
        self.cislo_rady = self._index + 1
        self.pocet_ok = len(self.aktualni_rada)
        return self.aktualni_rada, self.cislo_rady, self.pocet_ok


class Rada(PatternRozpr):
    #řada a její pozice

    def __init__(self, text: str, pozice_krok: int = 1):
        super().__init__(text)
        self.pozice_x = 0
        self.pozice_y = 0
        self._pozice_krok = pozice_krok
        self.cumulative_indent = 0

    def next_row(self):
        row, cislo, pocet = super().next_row()
        if 'b' in row:
            self.pozice_x = 0
        else:
            self.pozice_x = self.cumulative_indent
        self.pozice_y = self.cislo_rady * self._pozice_krok
        return row, cislo, pocet

    def add_offset(self, count: int):
        self.pozice_x += count


class AktualniOko(PatternRozpr):
    #čte řady a určuje směr

    def __init__(self, text: str, tam_zpet: bool = False):
        super().__init__(text)
        self.tam_zpet = bool(tam_zpet)
        self.ctene_oko = ''
        self.smer = False
        self._symbol_index = 0
        self._step_count = 0
        self._last_x = 0

    def set_tam_zpet(self, value: bool):
        self.tam_zpet = bool(value)
        self._update_smer()

    def _update_smer(self):
        self.smer = bool(self.tam_zpet and self.cislo_rady % 2 == 1)

    def set_current_row(self, rada: Rada):
        self.aktualni_rada = rada.aktualni_rada
        self.cislo_rady = rada.cislo_rady
        self._step_count = 0
        self.ctene_oko = ''
        self._last_x = 0
        self._update_smer()
        self._symbol_index = len(self.aktualni_rada) - 1 if self.smer else 0

    def read_next_symbol(self):
        if not self.aktualni_rada:
            raise ValueError('Aktuální řada není nastavena.')
        if self.smer and self._symbol_index < 0:
            raise StopIteration
        if not self.smer and self._symbol_index >= len(self.aktualni_rada):
            raise StopIteration

        symbol = self.aktualni_rada[self._symbol_index]
        if symbol != 'b':
            self._step_count += 1
        annotated = f'{symbol}{self._step_count}'
        if self._step_count == len(self.aktualni_rada):
            annotated += 'x'

        self._last_x = self._step_count
        if self.smer:
            self._symbol_index -= 1
        else:
            self._symbol_index += 1

        self.ctene_oko = annotated
        return self.ctene_oko

    def current_position_x(self) -> int:
        return self._last_x

    def reset_eye(self):
        self._symbol_index = 0
        self._step_count = 0
        self.ctene_oko = ''
        self._last_x = 0


class Oko(AktualniOko):
    #posílá instrukce do image makeru

    def knit(self, pozice_x: int, pozice_y: int):
        if not self.ctene_oko:
            return False

        symbol = self.ctene_oko[0]
        if (not self.smer and symbol == 'k') or (self.smer and symbol == 'p'):
            try:
                from . import test_images3
            except ImportError:
                import test_images3
            test_images3.add_knit2_at(pozice_y, pozice_x)
            return True

        return False

    def purl(self, pozice_x: int, pozice_y: int):
        if not self.ctene_oko:
            return False

        symbol = self.ctene_oko[0]
        if (not self.smer and symbol == 'p') or (self.smer and symbol == 'k'):
            try:
                from . import test_images3
            except ImportError:
                import test_images3
            test_images3.add_knit2_at(pozice_y, pozice_x, filename='purl2.png')
            return True

        return False

    def bind_off(self, pozice_x: int, pozice_y: int):
        if not self.ctene_oko:
            return False

        symbol = self.ctene_oko[0]
        if symbol == 'b':
            try:
                from . import test_images3
            except ImportError:
                import test_images3
            filename = 'bind_off1.png' if self.smer else 'bind_off2.png'
            test_images3.add_knit2_at(pozice_y, pozice_x, filename=filename)
            return True

        return False


def process_pattern(raw_text: str, tam_zpet: bool = False):
    built = build_pattern(raw_text)
    rada = Rada(built)
    oko = Oko(built, tam_zpet=tam_zpet)
    placements = []

    for _ in rada:
        oko.set_current_row(rada)
        while True:
            try:
                oko.read_next_symbol()
            except StopIteration:
                break

            pozice_x = oko.current_position_x() + rada.pozice_x
            pozice_y = rada.pozice_y
            if oko.knit(pozice_x, pozice_y):
                placements.append({
                    'cislo_rady': rada.cislo_rady,
                    'pozice_x': pozice_x,
                    'pozice_y': pozice_y,
                    'ctene_oko': oko.ctene_oko,
                    'smer': oko.smer,
                })
            elif oko.purl(pozice_x, pozice_y):
                placements.append({
                    'cislo_rady': rada.cislo_rady,
                    'pozice_x': pozice_x,
                    'pozice_y': pozice_y,
                    'ctene_oko': oko.ctene_oko,
                    'smer': oko.smer,
                })
            elif oko.bind_off(pozice_x, pozice_y):
                placements.append({
                    'cislo_rady': rada.cislo_rady,
                    'pozice_x': pozice_x,
                    'pozice_y': pozice_y,
                    'ctene_oko': oko.ctene_oko,
                    'smer': oko.smer,
                })

        count = rada.aktualni_rada.count('b')
        rada.cumulative_indent += count

    return placements


if __name__ == '__main__':
    import sys

    raw_text = sys.stdin.read()
    try:
        placements = process_pattern(raw_text)
    except ValueError as error:
        print(error)
        sys.exit(1)


            