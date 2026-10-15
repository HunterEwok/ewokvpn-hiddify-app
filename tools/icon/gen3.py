import math
def fluffy(cx, cy, rx, ry, n, tuft, phase=0.0):
    """Closed path of an ellipse whose edge is broken into fur tufts."""
    pts=[]
    for i in range(n):
        a0=2*math.pi*i/n+phase; a1=2*math.pi*(i+0.5)/n+phase
        pts.append((cx+rx*math.cos(a0), cy+ry*math.sin(a0)))
        k=1+tuft*(0.6+0.8*((i*7919)%13)/12)/max(rx,ry)
        # tuft tip leans a little to one side, like brushed fur
        a1+=0.35*math.pi/n
        pts.append((cx+rx*k*math.cos(a1), cy+ry*k*math.sin(a1)))
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(0,len(pts),2):
        tip=pts[i+1]; nxt=pts[(i+2)%len(pts)]
        d+=f' L{tip[0]:.1f},{tip[1]:.1f} L{nxt[0]:.1f},{nxt[1]:.1f}'
    return d+' Z'

import random
def strands(cx, cy, rx, ry, n, color, width, length, seed, ox=None, oy=None, inner=0.0):
    """Hair strands scattered over an ellipse, combed outwards from (ox, oy)."""
    rnd=random.Random(seed); ox=cx if ox is None else ox; oy=cy if oy is None else oy
    out=[]
    for _ in range(n):
        a=rnd.uniform(0,2*math.pi); r=math.sqrt(rnd.uniform(inner,1))
        x=cx+rx*r*math.cos(a); y=cy+ry*r*math.sin(a)
        dx,dy=x-ox,y-oy; m=math.hypot(dx,dy) or 1; dx,dy=dx/m,dy/m
        L=length*rnd.uniform(0.6,1.3); bend=rnd.uniform(-0.5,0.5)
        x2=x+dx*L; y2=y+dy*L; qx=(x+x2)/2-dy*L*bend*0.5; qy=(y+y2)/2+dx*L*bend*0.5
        out.append(f'<path d="M{x:.1f},{y:.1f} Q{qx:.1f},{qy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity="0.85"/>')
    return out
P = {
 'day':   dict(bg1='#F3E9D2', bg2='#E3D3B0', disc='#B9C79A', hood='#DE7A2E', hoodS='#B85D1F', fur='#7E5232', furD='#4E301B', furL='#A97C55', muzzleD='#B89A78', ear='#4A2E1C', cheek='#E4D3B8', line='#3A2414', eye='#140C08', shine='#FFFFFF', tongue='#D9606A', mouth='#5A2418', text='#3A2414', sub='#7A5A3A', star=None),
 'night': dict(bg1='#1F2D63', bg2='#0A1230', disc='#2E3F7E', hood='#C9692A', hoodS='#9C4E1A', fur='#6E4629', furD='#3E2716', furL='#957049', muzzleD='#A08664', ear='#3C2516', cheek='#CBBBA0', line='#1A0F08', eye='#08060A', shine='#BFFFF6', tongue='#C9525C', mouth='#40180F', text='#EAF2FF', sub='#AFC2EE', star='#FFFFFF'),
}
def ewok(c):
    L=c['line']; W='stroke="%s" stroke-width="14" stroke-linejoin="round" stroke-linecap="round"'%L
    o=[]
    # ears
    for cx in (300,724):
        o.append(f'<path d="{fluffy(cx,250,80,80,24,32)}" fill="{c["fur"]}" stroke="{c["furD"]}" stroke-width="5" stroke-linejoin="round"/>')
        o.append(f'<path d="{fluffy(cx,258,44,44,10,16,0.3)}" fill="{c["ear"]}"/>')
        o+=strands(cx,250,70,70,26,c["furL"],7,26,cx,inner=0.35)
    # hood with draped, ragged hem down to the shoulders
    o.append(f'<path d="M262,420 C262,250 370,180 512,180 C654,180 762,250 762,420 C762,520 790,620 830,720 L770,700 L745,760 L690,725 L640,790 L590,745 L512,800 L434,745 L384,790 L334,725 L279,760 L254,700 L194,720 C234,620 262,520 262,420 Z" fill="{c["hood"]}" {W}/>')
    # hood fold shading
    o.append(f'<path d="M300,600 C330,650 380,690 430,705" fill="none" stroke="{c["hoodS"]}" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<path d="M724,600 C694,650 644,690 594,705" fill="none" stroke="{c["hoodS"]}" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<path d="M420,215 C470,200 560,200 610,215" fill="none" stroke="{c["hoodS"]}" stroke-width="12" stroke-linecap="round"/>')
    # face opening
    o.append(f'<path d="{fluffy(512,452,164,176,46,34)}" fill="{c["fur"]}" stroke="{c["furD"]}" stroke-width="5" stroke-linejoin="round"/>')
    # shaggy strands combed outwards from the snout
    o+=strands(512,452,150,165,70,c["furD"],8,40,1,512,520)
    o+=strands(512,452,150,165,45,c["furL"],6,34,2,512,520)
    # fluffy lower fur fringe along the jaw
    # soft, raised brows
    for s in (-1,1):
        o.append(f'<path d="M{512+s*58},352 Q{512+s*100},334 {512+s*140},354" fill="none" stroke="{c["cheek"]}" stroke-width="15" stroke-linecap="round"/>')
    # round bear eyes, set wide
    for s in (-1,1):
        cx=512+s*96
        o.append(f'<circle cx="{cx}" cy="420" r="42" fill="{c["eye"]}"/>')
        o.append(f'<circle cx="{cx+14}" cy="404" r="14" fill="{c["shine"]}"/>')
        o.append(f'<circle cx="{cx-12}" cy="438" r="6" fill="{c["shine"]}" opacity="0.85"/>')
    # broad protruding bear snout
    o.append(f'<path d="{fluffy(512,532,112,82,22,26,0.1)}" fill="{c["cheek"]}"/>')
    o+=strands(512,540,95,65,40,c["muzzleD"],5,26,3,512,500,inner=0.2)
    # big bear nose
    o.append(f'<path d="M462,488 C462,462 562,462 562,488 C562,516 532,534 512,538 C492,534 462,516 462,488 Z" fill="{c["furD"]}" stroke="{c["line"]}" stroke-width="10" stroke-linejoin="round"/>')
    o.append(f'<ellipse cx="496" cy="480" rx="14" ry="7" fill="#FFFFFF" opacity="0.5"/>')
    # closed, wide friendly smile
    o.append(f'<path d="M512,538 L512,566" stroke="{c["line"]}" stroke-width="11" stroke-linecap="round"/>')
    o.append(f'<path d="M440,548 Q470,600 512,566 Q554,600 584,548" fill="none" stroke="{c["line"]}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    return o

def svg(theme, text=True, bg=True):
    c=P[theme]
    tf='translate(512 0) scale(0.84) translate(-512 0)' if text else 'translate(512 512) scale(0.98) translate(-512 -490)'
    o=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs>',
       f'<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>',
       '<mask id="moon"><rect x="-80" y="-80" width="160" height="160" fill="#fff"/><circle cx="22" cy="-16" r="42" fill="#000"/></mask>',
       '</defs>']
    if bg:
        o.append('<rect width="1024" height="1024" fill="url(#bg)"/>')
        if c['star']:
            for x,y,r in [(130,160,5),(240,80,3),(880,130,4),(920,330,3),(100,420,3),(800,60,3),(940,560,4),(80,640,3)]:
                o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="0.8"/>')
    o.append(f'<g transform="{tf}">')
    # backdrop disc: sun by day, moon glow by night
    o.append(f'<circle cx="512" cy="470" r="330" fill="{c["disc"]}" opacity="0.8"/>')
    o+=ewok(c)
    o.append('</g>')
    if theme=='day':
        rays=''.join(f'<rect x="-6" y="-72" width="12" height="22" rx="6" fill="#F2B632" transform="rotate({a})"/>' for a in range(0,360,45))
        o.append(f'<g transform="translate(888 132)">{rays}<circle r="40" fill="#F6C445"/></g>')
    else:
        o.append('<g transform="translate(888 132)"><circle r="48" fill="#FFE7A3" mask="url(#moon)"/></g>')
    o.append('<g>')
    o.append('</g>')
    if text:
        o.append(f'<text x="512" y="880" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" letter-spacing="10" fill="{c["text"]}">VPN</text>')
        o.append(f'<text x="512" y="952" text-anchor="middle" font-family="Inter" font-weight="600" font-size="54" letter-spacing="4" fill="{c["sub"]}">by Ewok</text>')
    o.append('</svg>')
    return '\n'.join(o)
if __name__=='__main__':
    for th in ('day','night'):
        open(f'{th}.svg','w').write(svg(th)); open(f'{th}_mark.svg','w').write(svg(th,text=False))

CHAR_VIEWBOX = "150 105 724 724"

def character(theme):
    """The ewok alone on a transparent background, cropped square."""
    return '\n'.join([f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="{CHAR_VIEWBOX}">'] + ewok(P[theme]) + ['</svg>'])

def glyph(color):
    """Single-colour silhouette: ears and hood, with the face cut out and the eyes, nose and smile inside."""
    hood = ('M262,420 C262,250 370,180 512,180 C654,180 762,250 762,420 C762,520 790,620 830,720 L770,700 L745,760 '
            'L690,725 L640,790 L590,745 L512,800 L434,745 L384,790 L334,725 L279,760 L254,700 L194,720 '
            'C234,620 262,520 262,420 Z')
    # face hole drawn as an ellipse; evenodd cuts it out of the hood
    face = 'M354,455 A158,170 0 1 0 670,455 A158,170 0 1 0 354,455 Z'
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="{CHAR_VIEWBOX}">',
        f'<circle cx="300" cy="250" r="96" fill="{color}"/>',
        f'<circle cx="724" cy="250" r="96" fill="{color}"/>',
        f'<path d="{hood} {face}" fill="{color}" fill-rule="evenodd"/>',
        f'<circle cx="420" cy="425" r="40" fill="{color}"/>',
        f'<circle cx="604" cy="425" r="40" fill="{color}"/>',
        f'<path d="M466,498 C466,472 558,472 558,498 C558,522 530,540 512,544 C494,540 466,522 466,498 Z" fill="{color}"/>',
        f'<path d="M512,544 L512,566 M440,552 Q470,604 512,568 Q554,604 584,552" fill="none" stroke="{color}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>',
        '</svg>'])
