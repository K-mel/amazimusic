import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import os

URL = "https://amazimusic.fr"
OUT = r"C:\Users\kamel\projets\amazi\amazi-qr.png"

# QR code avec modules arrondis
qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=3,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    back_color=(22, 19, 17),   # #161311 fond sombre
    fill_color=(233, 195, 73), # #e9c349 or/doré
)

img = img.convert("RGBA")
w, h = img.size

# Cadre avec padding et texte AMAZI en bas
PAD = 40
BOTTOM = 80
canvas = Image.new("RGBA", (w + PAD*2, h + PAD + BOTTOM), (22, 19, 17, 255))
canvas.paste(img, (PAD, PAD))

# Ligne décorative or
draw = ImageDraw.Draw(canvas)
y_line = h + PAD + 10
draw.rectangle([PAD, y_line, w + PAD, y_line + 2], fill=(233, 195, 73))

# Texte AMAZI
try:
    font_big = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 28)
    font_sm  = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 14)
except:
    font_big = ImageFont.load_default()
    font_sm  = font_big

cx = (w + PAD*2) // 2

# "AMAZI" en terracotta
draw.text((cx, y_line + 18), "AMAZI", font=font_big, fill=(255, 182, 149), anchor="mt")
# URL en gris clair
draw.text((cx, y_line + 52), "amazimusic.fr", font=font_sm, fill=(160, 141, 133), anchor="mt")

canvas.save(OUT)
print("QR code saved:", OUT)
print("Size:", canvas.size)
