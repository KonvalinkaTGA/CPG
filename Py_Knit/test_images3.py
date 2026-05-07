import os
import tempfile
import atexit
import subprocess
import shutil
from typing import Optional, Tuple
from PIL import Image, ImageDraw

RESAMPLE = getattr(Image, 'Resampling', Image).LANCZOS
DEFAULT_TILE_SIZE = (612,695)
knit_placements = []
temp_path = None


def add_knit2_at(pozice_y: int, pozice_x: int, filename: str = 'knit2.png'):
    """Register a knit placement for the requested position."""
    placement = {
        'file': filename,
        'pozice_y': pozice_y,
        'pozice_x': pozice_x,
    }
    knit_placements.append(placement)
    print(f"Added {filename} at pozice_y={pozice_y}, pozice_x={pozice_x}")
    return placement


def get_knit_placements():
    return list(knit_placements)


def clear_knit_placements():
    knit_placements.clear()


def _find_tile_image(filename: str) -> Optional[str]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(script_dir, filename)
    if os.path.exists(candidate):
        return candidate

    fallback_names = ['Knit2.png', 'knit2.png']
    for name in fallback_names:
        candidate = os.path.join(script_dir, name)
        if os.path.exists(candidate):
            return candidate

    return None


def _get_output_directory() -> str:
    # First priority: current working directory
    cwd = os.getcwd()
    if os.path.isdir(cwd):
        return cwd
    
    
def _open_image(image_path: str):
    """Open the image with the system's default image viewer."""
    if not os.path.exists(image_path):
        return
    
    try:
        if os.name == 'nt':  # Windows
            os.startfile(image_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.Popen(['xdg-open', image_path])
    except Exception:
        pass


def render_placements(tile_filename: str = 'knit2.png', output_path: Optional[str] = None,
                      tile_size: Optional[Tuple[int, int]] = None, auto_open: bool = True, vertical_factor: float = 0.65) -> str:
    #vytvoř všechny placementy
    if not knit_placements:
        raise ValueError('Žádná umístění k vykreslení.')

    if tile_size is None:
        tile_size = DEFAULT_TILE_SIZE

    tile_width, tile_height = tile_size
    
    # Načti obrázky
    tile_images = {}
    for placement in knit_placements:
        filename = placement.get('file', 'knit2.png')
        if filename not in tile_images:
            tile_path = _find_tile_image(filename)
            tile_image = None
            if tile_path is not None:
                tile_image = Image.open(tile_path).convert('RGBA')
            
            
            else:
                tile_image = tile_image.resize(tile_size, RESAMPLE)
            
            tile_images[filename] = tile_image

    max_x = max(p['pozice_x'] for p in knit_placements)
    max_y = max(p['pozice_y'] for p in knit_placements)

    canvas_width = (max_x - 1) * tile_width + tile_width
    canvas_height = int((max_y - 1) * tile_height * vertical_factor + tile_height)
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))

    for placement in knit_placements:
        filename = placement.get('file', 'knit2.png')
        # Purl se vykresli na konci, pro překrytí
        if filename == 'purl2.png':
            continue
        
        tile_image = tile_images[filename]
        px = (placement['pozice_x'] - 1) * tile_width
        py = int((max_y - placement['pozice_y']) * tile_height * vertical_factor)
        canvas.paste(tile_image, (px, py), tile_image)
    
    # Vykresli purl2.png na konci, aby zakryly ostatní
    for placement in knit_placements:
        filename = placement.get('file', 'knit2.png')
        if filename != 'purl2.png':
            continue
        
        tile_image = tile_images[filename]
        # Zmenšit purl2.png na 80% a posunout ji tak, aby zůstala centrovaná
        purl_size = (int(tile_width * 1), int(tile_height * 0.66))
        purl_image = tile_image.resize(purl_size, RESAMPLE)
        
        px = (placement['pozice_x'] - 1) * tile_width
        py = int((max_y - placement['pozice_y']) * tile_height * vertical_factor)
        # Posunout Y o 20% dolů pro centrování
        py += int(tile_height * vertical_factor * 0.23)
        
        
        canvas.paste(purl_image, (px, py), purl_image)

    if output_path is None:
        output_dir = _get_output_directory()
        output_filename = 'PyKnit_output.png'
        output_path = os.path.join(output_dir, output_filename)

    canvas.save(output_path, 'PNG')
    
    if auto_open:
        _open_image(output_path)
    
    return output_path


def concat_images(image_paths, size: Tuple[int, int] = DEFAULT_TILE_SIZE, shape=None, vertical_factor: float = 1):
    # Open images and resize them with alpha support
    width, height = size
    images = map(Image.open, image_paths)
    images = [image.convert('RGBA').resize(size, RESAMPLE)
              for image in images]

    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    canvas_width = width * shape[1]
    if shape[0] == 1:
        canvas_height = height
    else:
        canvas_height = int((shape[0] - 1) * height * vertical_factor + height)
    image_size = (canvas_width, canvas_height)
    image = Image.new('RGBA', image_size, (0, 0, 0, 0))

    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = (width * col, int(height * row * vertical_factor))
            print(offset)
            idx = row * shape[1] + col
            image.paste(images[idx], offset, images[idx])

    return image


def main():
    # Get list of image paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, 'PyKnit')

    if not os.path.exists(folder):
        print(f"Složka '{folder}' nebyla nalezena.")
        print(f"Hledám JPG obrázky v adresáři skriptu: {script_dir}")
        folder = script_dir

    image_paths = [os.path.join(folder, f)
                   for f in os.listdir(folder) if f.endswith('.png')]

    if not image_paths:
        print(f"CHYBA: Nebyl nalezen žádný PNG soubor ve složce '{folder}'")
        print("Prosím umístěte obrázky (.png) do stejné složky jako skript.")
        return

    grid_size = (300, 300)
    grid_rows = 20
    grid_stitches = 4
    total_images = grid_rows * grid_stitches
    image_array = [os.path.join(folder, "Knit2.png") for _ in range(total_images)]

    image = concat_images(image_array, grid_size, (grid_rows, grid_stitches), vertical_factor=0.5)

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        temp_path = tmp.name
    image.save(temp_path, 'PNG')
    print(f"Dočasný obrázek byl otevřen: {temp_path}")
    print("Soubor bude smazán po ukončení programu.")

    try:
        image.show()
    except Exception as e:
        print(f"Nelze otevřít obrázek automaticky: {e}")


def cleanup_temp():
    global temp_path
    if temp_path:
        try:
            os.remove(temp_path)
        except OSError:
            pass


atexit.register(cleanup_temp)


if __name__ == '__main__':
    main()
