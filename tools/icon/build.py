"""Builds every EwokVPN icon asset from gen3.py into the repository: python3 build.py <repo>"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen3
R = sys.argv[1]
W = os.path.join(HERE, 'build'); os.makedirs(W, exist_ok=True)
def w(name, text):
    p = os.path.join(W, name + '.svg'); open(p, 'w').write(text); return p
D, N = gen3.P['day'], gen3.P['night']
def bg_svg(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs>'
            f'<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/>'
            f'<stop offset="1" stop-color="{c["bg2"]}"/></linearGradient></defs><rect width="1024" height="1024" fill="url(#bg)"/></svg>')
svgs = {
  'full_day': gen3.svg('day'), 'full_night': gen3.svg('night'),
  'fg_day': gen3.svg('day', bg=False), 'bg_day': bg_svg(D),
  'char_day': gen3.character('day'), 'char_night': gen3.character('night'),
  'glyph_white': gen3.glyph('#FFFFFF'), 'glyph_cream': gen3.glyph('#F3E6CC'), 'glyph_brown': gen3.glyph('#5A3A22'),
  'glyph_green': gen3.glyph('#2FB04A'), 'glyph_red': gen3.glyph('#E5483C'), 'glyph_orange': gen3.glyph('#DE7A2E'),
}
jobs = [{'svg': w(k, v), 'out': os.path.join(W, k + '.png'), 'size': 1024} for k, v in svgs.items()]
json.dump(jobs, open(os.path.join(W, 'jobs.json'), 'w'))
subprocess.run(['node', os.path.join(HERE, 'render_many.js'), os.path.join(W, 'jobs.json')], check=True)
img = {k: Image.open(os.path.join(W, k + '.png')).convert('RGBA') for k in svgs}

def rp(*a): return os.path.join(R, *a)
def sized(im, s): return im.resize((s, s), Image.LANCZOS)
def shaped(im, s, radius=None):
    im = sized(im, s); m = Image.new('L', (s, s), 0); dr = ImageDraw.Draw(m)
    if radius is None: dr.ellipse((0, 0, s - 1, s - 1), fill=255)
    else: dr.rounded_rectangle((0, 0, s - 1, s - 1), radius, fill=255)
    out = im.copy(); out.putalpha(Image.composite(im.getchannel('A'), m, m) if False else m); return out
def on_canvas(im, s, frac, bg=(0, 0, 0, 0)):
    c = Image.new('RGBA', (s, s), bg); t = int(round(s * frac)); c.alpha_composite(sized(im, t), ((s - t) // 2, (s - t) // 2)); return c
def save(im, *path, **kw):
    p = rp(*path); os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p, **kw)
def ico(im, *path, sizes=(16, 24, 32, 48, 64, 128, 256)):
    save(sized(im, max(sizes)), *path, format='ICO', sizes=[(s, s) for s in sizes])
def solid(hexcolor, s=1):
    return Image.new('RGB', (s, s), hexcolor)

full, full_n = img['full_day'], img['full_night']
app_square = lambda s: shaped(full, s, s * 0.22)

# shared sources (Linux packages read ic_launcher_border.png)
save(full, 'assets/images/source/ic_launcher_border.png')
save(full_n, 'assets/images/source/ic_launcher_night.png')
save(img['char_day'], 'assets/images/source/ic_launcher_foreground.png')
save(on_canvas(img['char_day'], 1024, 0.6), 'assets/images/source/ic_launcher_splash.png')
for name, key in [('ic_notify', 'glyph_white'), ('tray_icon', 'glyph_brown'),
                  ('tray_icon_connected', 'glyph_green'), ('tray_icon_disconnected', 'glyph_red')]:
    save(img[key].resize((2048, 2048), Image.LANCZOS), 'assets/images/source/' + name + '.png')
ico(app_square(256), 'assets/images/source/ewokvpn.ico')
# in-app logo: single-colour vector, tinted by the app where needed
open(rp('assets/images/logo.svg'), 'w').write(gen3.glyph('#DE7A2E').replace('width="1024" height="1024" ', 'width="64" height="64" ') + '\n')
# tray: light glyph for dark taskbars (night), dark glyph for light taskbars (day)
for name, key in [('tray_icon', 'glyph_cream'), ('tray_icon_dark', 'glyph_brown'),
                  ('tray_icon_connected', 'glyph_green'), ('tray_icon_disconnected', 'glyph_red')]:
    save(sized(img[key], 128), 'assets/images/' + name + '.png')
    ico(img[key], 'assets/images/' + name + '.ico', sizes=(16, 24, 32, 48, 64, 128))
# Windows, web, snap
ico(app_square(256), 'windows/runner/resources/app_icon.ico')
save(app_square(1024), 'web/icon.png')
save(app_square(256), 'snap/gui/app_icon.png')
# Android launcher: bitmaps for old launchers, adaptive layers, themed-icon monochrome layer
res = 'android/app/src/main/res'
for d, k in [('mdpi', 1), ('hdpi', 1.5), ('xhdpi', 2), ('xxhdpi', 3), ('xxxhdpi', 4)]:
    s = int(48 * k); a = int(108 * k)
    save(app_square(s), res, f'mipmap-{d}', 'ic_launcher.webp', format='WEBP', lossless=True)
    save(shaped(full, s), res, f'mipmap-{d}', 'ic_launcher_round.webp', format='WEBP', lossless=True)
    save(on_canvas(img['fg_day'], a, 0.66), res, f'mipmap-{d}', 'ic_launcher_foreground.png')
    save(sized(img['bg_day'], a), res, f'mipmap-{d}', 'ic_launcher_background.png')
    save(on_canvas(img['glyph_white'], a, 0.56), res, f'mipmap-{d}', 'ic_launcher_monochrome.png')
    # notification icon: white silhouette, 24dp
    save(sized(img['glyph_white'], int(24 * k)), res, f'drawable-{d}', 'ic_stat_logo.png')
save(sized(full, 512), 'android/app/src/main/ic_launcher-playstore.png')
# Android TV banner 320x180
ban = Image.new('RGBA', (320, 180), D['bg1']); ban.alpha_composite(sized(img['char_day'], 150), (18, 15))
save(ban, res, 'mipmap-xhdpi', 'ic_banner.png')
# splash: day and night backgrounds, ewok in the middle
save(solid(D['bg1']), res, 'drawable', 'background.png'); save(solid(D['bg1']), res, 'drawable-v21', 'background.png')
save(solid(N['bg2']), res, 'drawable-night', 'background.png'); save(solid(N['bg2']), res, 'drawable-night-v21', 'background.png')
save(sized(img['char_day'], 324), res, 'drawable-xxxhdpi', 'splash.png')
save(sized(img['char_night'], 324), res, 'drawable-night-xxxhdpi', 'splash.png')
# Android 12+ splash icon: 288dp canvas, icon inside the 192dp circle
save(on_canvas(img['char_day'], 1152, 0.5), res, 'drawable-xxxhdpi', 'android12splash.png')
save(on_canvas(img['char_night'], 1152, 0.5), res, 'drawable-night-xxxhdpi', 'android12splash.png')
# iOS launch image
for sfx, s in [('', 256), ('@2x', 512), ('@3x', 768)]:
    save(sized(img['char_day'], s), f'ios/Runner/Assets.xcassets/LaunchImage.imageset/LaunchImage{sfx}.png')
save(solid(D['bg1']), 'ios/Runner/Assets.xcassets/LaunchBackground.imageset/background.png')
# iOS / macOS icon composer documents: full-bleed day and night artwork
for plat in ('ios', 'macos'):
    save(full, plat, 'Runner/AppIcon.icon/Assets/ewokvpn_day.png')
    save(full_n, plat, 'Runner/AppIcon.icon/Assets/ewokvpn_night.png')
print('done')
