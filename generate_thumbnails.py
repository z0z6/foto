#!/usr/bin/env python3
"""
Skrypt do generowania miniatur (thumbnails) dla portfolio z0z6.
Generuje miniatury w formacie WebP w dwóch rozmiarach:
  - 400px (dla urządzeń mobilnych i małych ekranów)
  - 800px (dla desktopów i dużych ekranów)

Wymaga: pip install Pillow

Użycie:
    1. Umieść ten plik w głównym folderze repozytorium (obok folderu images/)
    2. Uruchom: python generate_thumbnails.py
    3. Skrypt utworzy folder thumbnails/ z pomniejszonymi wersjami zdjęć
    4. Zaktualizuj repozytorium: git add thumbnails/ && git commit -m "Add thumbnails"
"""

from PIL import Image
import os
import glob

# Konfiguracja
IMAGES_DIR = "images"           # Folder z oryginalnymi zdjęciami
THUMBNAILS_DIR = "thumbnails"   # Folder docelowy dla miniatur
SIZES = {
    "400": (400, 400),         # Dla urządzeń mobilnych
    "800": (800, 800),         # Dla desktopów
}
QUALITY = 85                    # Jakość WebP (0-100)

def create_thumbnail(input_path, output_path, max_size, quality):
    """Tworzy miniaturę zachowując proporcje, w formacie WebP."""
    with Image.open(input_path) as img:
        # Konwersja do RGB jeśli potrzeba
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Zmiana rozmiaru z zachowaniem proporcji
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Zapis jako WebP
        img.save(output_path, "WEBP", quality=quality, method=6)

        return os.path.getsize(output_path)

def main():
    # Utwórz folder miniatur jeśli nie istnieje
    if not os.path.exists(THUMBNAILS_DIR):
        os.makedirs(THUMBNAILS_DIR)
        print(f"Utworzono folder: {THUMBNAILS_DIR}/")

    # Znajdź wszystkie obrazki
    image_patterns = [
        os.path.join(IMAGES_DIR, "*.jpg"),
        os.path.join(IMAGES_DIR, "*.jpeg"),
        os.path.join(IMAGES_DIR, "*.png"),
        os.path.join(IMAGES_DIR, "*.webp"),
    ]

    image_files = []
    for pattern in image_patterns:
        image_files.extend(glob.glob(pattern))

    # Sortuj aby zachować kolejność
    image_files.sort()

    if not image_files:
        print(f"\nNie znaleziono obrazków w folderze {IMAGES_DIR}/")
        print("Upewnij się, że uruchamiasz skrypt z głównego folderu repozytorium.")
        return

    print(f"Znaleziono {len(image_files)} obrazków do przetworzenia...")
    print(f"Rozmiary miniatur: {', '.join(SIZES.keys())} px (max)")
    print(f"Format: WebP | Jakość: {QUALITY}%")
    print("-" * 70)

    total_original = 0
    total_thumbnail = 0

    for img_path in image_files:
        filename = os.path.basename(img_path)
        name, _ = os.path.splitext(filename)
        original_size = os.path.getsize(img_path)
        total_original += original_size

        sizes_info = []
        for size_label, max_size in SIZES.items():
            output_path = os.path.join(THUMBNAILS_DIR, f"{name}-{size_label}.webp")
            thumbnail_size = create_thumbnail(img_path, output_path, max_size, QUALITY)
            total_thumbnail += thumbnail_size
            sizes_info.append(f"{size_label}px: {thumbnail_size/1024:.1f} KB")

        reduction = (1 - total_thumbnail / total_original) * 100 if total_original > 0 else 0
        print(f"✓ {filename:15s} | oryg: {original_size/1024/1024:5.1f} MB | {' | '.join(sizes_info)}")

    print("-" * 70)
    print(f"PODSUMOWANIE:")
    print(f"  Oryginały razem:   {total_original/1024/1024:.1f} MB")
    print(f"  Miniatury razem:   {total_thumbnail/1024:.1f} KB ({total_thumbnail/1024/1024:.1f} MB)")
    print(f"  Oszczędność:       {(1 - total_thumbnail/total_original)*100:.1f}%")
    print(f"\nMiniatury zapisane w folderze: {THUMBNAILS_DIR}/")
    print("\nNastępne kroki:")
    print("  1. Sprawdź czy miniatury wyglądają poprawnie")
    print("  2. Zaktualizuj index.html (użyj nowego pliku)")
    print('  3. git add thumbnails/ && git commit -m "Add optimized thumbnails"')
    print("  4. git push")

if __name__ == "__main__":
    main()
