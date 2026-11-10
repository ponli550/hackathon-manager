"""PITCH.md -> a 16:9 slide PDF, one page per '## ' heading. For the "slides as PDF" upload field when
there is no LibreOffice to convert the pptx. usage: slides_pdf.py docs/PITCH.md docs/Name-slides.pdf"""
import html, re, sys
from pathlib import Path
from weasyprint import HTML

src, out = Path(sys.argv[1]), Path(sys.argv[2])
sections = re.split(r"^## ", src.read_text(), flags=re.M)[1:]


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def body(lines):
    out, items = [], []
    for l in lines:
        m = re.match(r"^\d+\.\s+(.*)", l)
        if m:
            items.append(f"<li>{inline(m.group(1))}</li>"); continue
        if items:
            out.append("<ol>" + "".join(items) + "</ol>"); items = []
        if l.strip():
            out.append(f"<p>{inline(l)}</p>")
    if items:
        out.append("<ol>" + "".join(items) + "</ol>")
    return "".join(out)


import base64, mimetypes
def img_uri(path):
    p = (src.parent.parent / path) if not Path(path).is_absolute() else Path(path)
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def CAT(mood):
    """An original cat, drawn here, so nothing in the deck is anyone else's picture.
    moods: happy worried stern facepalm party detective judge."""
    face_eyes = {
        "happy":    '<path d="M70 88 q10 -12 20 0" class="ln"/><path d="M118 88 q10 -12 20 0" class="ln"/>',
        "worried":  '<circle cx="80" cy="88" r="6"/><circle cx="128" cy="88" r="6"/><path d="M66 72 l20 8" class="ln"/><path d="M142 72 l-20 8" class="ln"/>',
        "stern":    '<path d="M70 86 h20" class="ln"/><path d="M118 86 h20" class="ln"/><path d="M66 74 l22 6" class="ln"/><path d="M142 74 l-22 6" class="ln"/>',
        "facepalm": '<path d="M118 88 q10 -8 20 0" class="ln"/>',
        "party":    '<path d="M70 88 q10 -12 20 0" class="ln"/><path d="M118 88 q10 -12 20 0" class="ln"/>',
        "detective":'<circle cx="80" cy="88" r="5"/><circle cx="128" cy="88" r="9" fill="none" stroke="#1c1b19" stroke-width="5"/><circle cx="128" cy="88" r="3"/>',
        "judge":    '<path d="M70 86 h20" class="ln"/><path d="M118 86 h20" class="ln"/>',
    }
    mouth = {
        "happy": '<path d="M94 104 q10 10 20 0" class="ln"/>', "worried": '<path d="M96 110 q8 -8 16 0" class="ln"/>',
        "stern": '<path d="M96 108 h16" class="ln"/>', "facepalm": '<path d="M96 110 q8 -6 16 0" class="ln"/>',
        "party": '<path d="M88 102 q16 16 32 0" class="ln"/>', "detective": '<path d="M98 108 h12" class="ln"/>', "judge": '<path d="M96 108 h16" class="ln"/>',
    }
    m = mood if mood in face_eyes else "happy"
    extras = {
        # a paw over the eyes
        "facepalm": '<path class="fur" d="M50 70 q30 -20 60 0 q-5 30 -30 36 q-25 -6 -30 -36 z"/>',
        # party hat + confetti
        "party": '<path d="M104 10 L80 52 h48 z" fill="#2a4d8f" stroke="#1c1b19" stroke-width="5" stroke-linejoin="round"/><circle cx="104" cy="10" r="7" fill="#ff7a5c" stroke="#1c1b19" stroke-width="4"/>'
                 '<g fill="#ff7a5c"><rect x="20" y="20" width="10" height="10" transform="rotate(20 25 25)"/><rect x="250" y="30" width="10" height="10" transform="rotate(-30 255 35)"/><rect x="40" y="170" width="9" height="9" transform="rotate(45 44 174)"/></g>'
                 '<g fill="#2a4d8f"><circle cx="230" cy="20" r="5"/><circle cx="14" cy="120" r="5"/><circle cx="270" cy="180" r="6"/></g><g fill="#1b7f4b"><rect x="200" y="180" width="9" height="9"/><circle cx="60" cy="14" r="4"/></g>',
        # a magnifying glass in the paw instead of a stamp
        "detective": '<path d="M150 160 l50 -45" class="ln" style="stroke-width:12"/><circle cx="214" cy="103" r="26" fill="#cfe8df" fill-opacity=".6" stroke="#1c1b19" stroke-width="6"/>',
        # a gavel
        "judge": '<path d="M150 160 l56 -46" class="ln" style="stroke-width:12"/><rect x="190" y="88" width="56" height="30" rx="6" transform="rotate(-40 218 103)" fill="#9a6700" stroke="#1c1b19" stroke-width="5"/>',
    }
    stamp = '<path d="M150 160 l70 -40" class="ln" style="stroke-width:12"/><rect x="200" y="96" width="60" height="34" rx="6" transform="rotate(-30 230 113)" fill="#ff7a5c" stroke="#1c1b19" stroke-width="5"/>'
    hand = extras.get(m, stamp) if m in ("detective", "judge") else (extras.get(m, "") + stamp)
    return f"""<svg class="cat" viewBox="0 0 300 220" xmlns="http://www.w3.org/2000/svg">
<style>.ln{{fill:none;stroke:#1c1b19;stroke-width:5;stroke-linecap:round}}.fur{{fill:#f3b562;stroke:#1c1b19;stroke-width:5;stroke-linejoin:round}}</style>
<path class="fur" d="M48 60 L40 10 L85 40 Q104 30 123 40 L168 10 L160 60 Q190 95 160 140 Q104 170 48 140 Q18 95 48 60 Z"/>
<circle cx="104" cy="98" r="5"/>{face_eyes[m]}<path d="M104 96 l-7 8 h14 z" fill="#1c1b19"/>{mouth[m]}
<path d="M30 100 h-26 M30 110 h-26 M178 100 h26 M178 110 h26" class="ln"/>
<path class="fur" d="M70 150 q34 30 68 0 v55 h-68 z"/>
{hand}
</svg>"""


pages = []
for i, sec in enumerate(sections):
    title, *rest = sec.rstrip().split("\n")
    imgs = [m for l in rest for m in [re.match(r"^!\[(.*?)\]\((.+?)\)$", l.strip())] if m]
    stamps = [m.group(1) for l in rest for m in [re.match(r"^::stamp\s+(\S+)", l.strip())] if m]
    cats = [m.group(1) for l in rest for m in [re.match(r"^::cat\s+(\w+)", l.strip())] if m]
    memes = [m.group(1) for l in rest for m in [re.match(r"^::meme\s+(.+)$", l.strip())] if m]
    rest = [l for l in rest if not re.match(r"^!\[|^::", l.strip())]
    if i == 0 and cats and not stamps:
        pages.append(f'<section class="cover"><div class="cover-cat">{CAT(cats[0])}</div><h1>{inline(title)}</h1><div class="b">{body(rest)}</div><footer>{i+1} / {len(sections)}</footer></section>')
        continue
    if stamps or cats:
        art = "".join(f'<div class="stamp {w.lower()}">{html.escape(w)}</div>' for w in stamps) + "".join(CAT(m) for m in cats)
        meme_html = ""
        if memes:
            top, _, bottom = memes[0].partition("|")
            meme_html = f'<div class="meme top"><span>{html.escape(top.strip())}</span></div><div class="meme bottom"><span>{html.escape(bottom.strip())}</span></div>'
        pages.append(f'<section class="art-slide"><h1>{inline(title)}</h1><div class="art">{meme_html}{art}</div><div class="b cap">{body(rest)}</div><footer>{i+1} / {len(sections)}</footer></section>')
        continue
    if imgs:
        cap, path = imgs[0].group(1), imgs[0].group(2)
        pages.append(f'<section class="pic"><h1>{inline(title)}</h1><div class="pic-wrap"><img src="{img_uri(path)}" alt="{html.escape(cap)}"></div><div class="b cap">{body(rest)}</div><footer>{i+1} / {len(sections)}</footer></section>')
        continue
    pages.append(f'<section class="{"cover" if i == 0 else ""}"><h1>{inline(title)}</h1><div class="b">{body(rest)}</div><footer>{i+1} / {len(sections)}</footer></section>')

css = """
@page { size: 338.67mm 190.5mm; margin: 0 }
body { margin: 0; font-family: -apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1c1b19 }
section { width: 338.67mm; height: 190.5mm; padding: 22mm 26mm; box-sizing: border-box; page-break-after: always; position: relative; background: #fffaf3 }
section.cover { background: #0f3b3a; color: #f4f1ea } section.cover h1 { font-size: 68pt; border: 0; color: #f4f1ea } section.cover p { font-size: 24pt; color: #cfe8df }
h1 { font-size: 40pt; margin: 0 0 12mm; padding-bottom: 5mm; border-bottom: 3px solid #ff7a5c; font-weight: 800; letter-spacing: -.01em }
section.art-slide { padding: 16mm 26mm 14mm } section.art-slide h1 { margin-bottom: 6mm }
.art { height: 100mm; display: flex; align-items: center; justify-content: center; gap: 22mm }
.stamp { font: 900 92pt Helvetica, Arial, sans-serif; letter-spacing: .04em; padding: 6mm 14mm; border: 7px solid currentColor; border-radius: 10px; transform: rotate(-8deg); color: #ff7a5c }
.stamp.pass { color: #1b7f4b } .stamp.refused { color: #b8860b; font-size: 70pt }
.cat { height: 74mm; width: auto }
.cover-cat { position: absolute; right: 22mm; top: 26mm } .cover-cat .cat { height: 110mm }
section.cover h1, section.cover .b { position: relative; max-width: 190mm }
.art { position: relative; height: 104mm; padding: 16mm 0; box-sizing: border-box }
.art .stamp { font-size: 78pt }
.meme { position: absolute; left: 0; right: 0; text-align: center; font: 900 24pt Helvetica, Arial, sans-serif; text-transform: uppercase; letter-spacing: .02em; line-height: 1.15 }
.meme span { display: inline; background: #ffe08a; color: #1c1b19; padding: 1mm 4mm; box-decoration-break: clone; -webkit-box-decoration-break: clone }
.meme.top { top: 0 } .meme.bottom { bottom: 0 }
.b { font-size: 21pt; line-height: 1.45 } p { margin: 0 0 7mm } ol { margin: 0; padding-left: 12mm } li { margin-bottom: 5mm }
code { font-family: Menlo, monospace; font-size: .85em; background: rgba(42,77,143,.10); padding: 0 .3em; border-radius: 3px }
footer { position: absolute; bottom: 10mm; right: 26mm; font-size: 11pt; color: #8a857c }
section.pic { padding: 18mm 26mm 16mm } section.pic h1 { font-size: 30pt; margin-bottom: 8mm }
.pic-wrap { max-height: 108mm; display: flex; align-items: center; justify-content: center; border-radius: 4px; overflow: hidden }
.pic-wrap img { width: 100%; height: auto; max-height: 108mm; object-fit: contain; display: block; border-radius: 4px }
.cap { font-size: 17pt; margin-top: 6mm; color: #4a463f } .cap p { margin: 0 }
h1 { text-wrap: balance } .b p { text-wrap: pretty }
"""
HTML(string=f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>").write_pdf(out)
print(f"{len(pages)} slides -> {out}")
