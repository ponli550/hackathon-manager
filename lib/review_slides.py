#!/usr/bin/env python3
"""review_slides.py -- density and style-consistency check for a .pptx.

Adapted from two one-off scripts (identify_dense.py, review_slides.py) that
were hardcoded to a single client's training deck path. The CHECKS were
already generic; only the path was not. Parameterized here, not copied
verbatim -- a script that still points at someone else's file after being
"copied into hackager" is a bug, not a port.
"""
import sys
from collections import Counter
from pptx import Presentation


def review(path):
    prs = Presentation(path)
    report = {"path": str(path), "slides": len(prs.slides),
              "width_in": round(prs.slide_width.inches, 2),
              "height_in": round(prs.slide_height.inches, 2),
              "dense": [], "font_names": {}, "font_sizes": {}, "font_colors": {}}

    font_names, font_sizes, font_colors = Counter(), Counter(), Counter()
    for i, slide in enumerate(prs.slides, 1):
        title, total_text = "", ""
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            text = shape.text_frame.text.strip()
            if text and len(text) > len(title):
                title = text[:80]
            total_text += shape.text_frame.text
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.name:
                        font_names[run.font.name] += 1
                    if run.font.size:
                        font_sizes[run.font.size.pt] += 1
                    try:
                        if run.font.color and run.font.color.rgb:
                            font_colors[str(run.font.color.rgb)] += 1
                    except AttributeError:
                        pass
        word_count = len(total_text.split())
        if word_count > 60:
            report["dense"].append({"slide": i, "words": word_count, "title": title})

    report["font_names"] = dict(font_names)
    report["font_sizes"] = dict(font_sizes)
    report["font_colors"] = dict(font_colors)
    return report


if __name__ == "__main__":
    import json
    if len(sys.argv) != 2:
        print("usage: review_slides.py <deck.pptx>", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(review(sys.argv[1]), indent=2))
