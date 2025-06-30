from PIL import Image
import os

input_folder = 'photos'
output_folder = 'output'
watermark_path = 'watermark.png'
margin = 20

if not os.path.exists(watermark_path):
    raise FileNotFoundError(f"Файл водяного знака не найден: {watermark_path}")
if not os.path.exists(input_folder):
    raise FileNotFoundError(f"Папка с фото не найдена: {input_folder}")

os.makedirs(output_folder, exist_ok=True)

watermark = Image.open(watermark_path).convert("RGBA")

for filename in os.listdir(input_folder):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        continue

    try:
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")

        # Масштаб водяного знака по меньшей стороне
        scale_factor = 0.15
        base_side = min(image.width, image.height)
        wm_width = int(base_side * scale_factor)
        wm_height = int(wm_width * watermark.height / watermark.width)
        resized_wm = watermark.resize((wm_width, wm_height), Image.LANCZOS)

        position = (margin, image.height - wm_height - margin)

        base = image.copy()
        base.paste(resized_wm, position, resized_wm)

        output_path = os.path.join(output_folder, filename)
        if filename.lower().endswith(('.jpg', '.jpeg')):
            base.convert("RGB").save(output_path, "JPEG", quality=95, subsampling=0)
        else:
            base.save(output_path, "PNG")

        print(f"✔ Обработан: {filename}")
    except Exception as e:
        print(f"✖ Ошибка с {filename}: {e}")
