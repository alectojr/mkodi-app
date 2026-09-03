from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / 'mkodi' / 'static' / 'images'
OUTPUT = ROOT / 'docs' / 'MKodi_Tutorial.mp4'
WIDTH, HEIGHT = 1280, 720
FPS = 24
SCENE_SECONDS = 7

SCENES = [
    ('MKodi TAXPAYER PORTAL', 'One connected view of the taxpayer.', 'A simple digital home for records, intelligence, and payments.', 'taxpayer-market.svg'),
    ('01  ADMIN SETUP', 'Start in the admin record cabinet.', 'Official taxpayer details are prepared before account registration.', 'taxpayer-records.svg'),
    ('02  REGISTRATION', 'Register with the TIN already on file.', 'The account links to the trusted admin-managed taxpayer record.', 'taxpayer-mobile.svg'),
    ('03  DASHBOARD', 'See compliance, credit, status, and reminders.', 'Important information and actions are visible at a glance.', 'taxpayer-shop.svg'),
    ('04  360-DEGREE VIEW', 'Review identity, business, land, income, and risk.', 'A complete taxpayer picture in one readable workspace.', 'taxpayer-records.svg'),
    ('05  PAYMENTS', 'Create traceable USSD, GePG, or mobile-money requests.', 'Control numbers, statuses, transactions, and receipts stay together.', 'taxpayer-payment.svg'),
    ('06  PROFILE & SECURITY', 'Manage details, photo, and password securely.', 'The taxpayer controls their personal account experience.', 'taxpayer-mobile.svg'),
    ('MKODI', 'Clearer records. Simpler action. Stronger taxpayer service.', 'Built for accessible, connected revenue intelligence.', 'taxpayer-market.svg'),
]


def font(size, bold=False):
    name = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    return ImageFont.truetype(f'C:/Windows/Fonts/{name}', size)


def svg_image(name):
    palettes = {
        'taxpayer-market.svg': ('#2445ad', '#25a18e'),
        'taxpayer-shop.svg': ('#d45760', '#f5c542'),
        'taxpayer-mobile.svg': ('#253858', '#4267a5'),
        'taxpayer-records.svg': ('#14213d', '#0f766e'),
        'taxpayer-payment.svg': ('#1f3fbf', '#713f9e'),
    }
    start, end = palettes[name]
    image = Image.new('RGB', (WIDTH, HEIGHT), start)
    draw = ImageDraw.Draw(image)
    for x in range(WIDTH):
        blend = x / WIDTH
        color = tuple(int(int(start[i:i + 2], 16) * (1 - blend) + int(end[i:i + 2], 16) * blend) for i in (1, 3, 5))
        draw.line((x, 0, x, HEIGHT), fill=color)
    draw.ellipse((WIDTH - 360, 100, WIDTH + 120, 580), fill='#f5c542', outline='#ffffff', width=4)
    draw.rectangle((WIDTH - 540, 350, WIDTH - 180, 520), fill='#ffffff', outline='#dce6ff', width=4)
    draw.rectangle((WIDTH - 500, 390, WIDTH - 220, 420), fill='#25a18e')
    draw.rectangle((WIDTH - 500, 445, WIDTH - 290, 470), fill='#2445ad')
    return image


def frame(background, eyebrow, title, subtitle, progress):
    image = background.copy()
    overlay = Image.new('RGBA', image.size, (7, 19, 54, 105))
    image = Image.alpha_composite(image.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(image)
    left = 88
    draw.rounded_rectangle((left, 70, left + 116, 78), radius=4, fill='#f5c542')
    draw.text((left, 112), eyebrow, font=font(22, True), fill='#f5c542')
    draw.text((left, 165), title, font=font(58, True), fill='white')
    draw.text((left, 255), subtitle, font=font(28), fill='#e4ecff')
    draw.text((left, HEIGHT - 72), 'MKODI  /  TAXPAYER SERVICES PORTAL', font=font(16, True), fill='#dce6ff')
    draw.rectangle((0, HEIGHT - 12, WIDTH, HEIGHT), fill='#f5c542')
    draw.rectangle((0, HEIGHT - 12, int(WIDTH * progress), HEIGHT), fill='#25a18e')
    return image.convert('RGB')


def main():
    backgrounds = {asset: svg_image(asset) for _, _, _, asset in SCENES}
    writer = imageio_ffmpeg.write_frames(
        str(OUTPUT), (WIDTH, HEIGHT), fps=FPS, codec='libx264', pix_fmt_in='rgb24', quality=5,
    )
    writer.send(None)
    total_frames = len(SCENES) * SCENE_SECONDS * FPS
    for scene_index, (eyebrow, title, subtitle, asset) in enumerate(SCENES):
        for frame_index in range(SCENE_SECONDS * FPS):
            progress = (scene_index * SCENE_SECONDS * FPS + frame_index) / total_frames
            writer.send(frame(backgrounds[asset], eyebrow, title, subtitle, progress).tobytes())
    writer.close()
    print(f'Created {OUTPUT} ({OUTPUT.stat().st_size} bytes)')


if __name__ == '__main__':
    main()