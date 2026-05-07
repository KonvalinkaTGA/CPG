import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QCheckBox

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pattern_convertor import convert_pattern
from pattern_builder import process_pattern
from test_images3 import clear_knit_placements, get_knit_placements, render_placements


class uvodni_okno(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyKnit')
        self._setup_ui()

    def _setup_ui(self):
        self.setGeometry(300, 300, 600, 600)
        self.label = QLabel('Vložte postup:')
        self.input = QTextEdit()
        self.input.setAcceptRichText(False)
        self.input.setPlaceholderText('Zadejte libovolný počet řádků, stisknutím Enter vytvoříte nový řádek.')

        self.tam_zpet_label = QLabel('Vzor zpátky a sem tam (sem_tam):')
        self.tam_zpet_checkbox = QCheckBox('Zapnout sem_tam')
        self.tam_zpet_checkbox.setChecked(False)

        self.button = QPushButton('Zadat')
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setAcceptRichText(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.tam_zpet_label)
        layout.addWidget(self.tam_zpet_checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.result)

        self.button.clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self):
        text = self.input.toPlainText()
        if not text.strip():
            self.result.setPlainText('Nebyl zadán žádný text.')
            return

        tam_zpet = self.tam_zpet_checkbox.isChecked()

        clear_knit_placements()

        try:
            converted = convert_pattern(text)
            placements = process_pattern(text, tam_zpet=tam_zpet)
        except Exception as exc:
            self.result.setPlainText(f'Chyba při převodu: {exc}')
            return

        placement_text = '\n'.join(
            f"řada {p['cislo_rady']}: x={p['pozice_x']}, y={p['pozice_y']}, oko={p['ctene_oko']}"
            for p in placements
        )
        if not placement_text:
            placement_text = 'Nenalezena žádná umístění pro knit2.png.'

        image_path = None
        image_error = None
        
        if placements:
            try:
                image_path = render_placements()
            except Exception as exc:
                image_error = str(exc)

        result_lines = [
            converted,
            f"\nVygenerovaných umístění: {len(placements)}",
            placement_text,
        ]
        
        if image_error:
            result_lines.append(f"\nChyba při vykreslení obrázku: {image_error}")
        elif image_path:
            result_lines.append(f"\n✓ Výsledný obrázek: {image_path}")
            result_lines.append("(Obrázek byl automaticky otevřen v prohlížeči)")

        self.result.setPlainText('\n'.join(result_lines))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = uvodni_okno()
    window.show()
    sys.exit(app.exec_())
