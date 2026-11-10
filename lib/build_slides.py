#!/usr/bin/env python3
"""build_slides.py -- a real pitch deck from a project's OWN pitch card.

Not generate_training_slides.py copied over: that script's content (colors
aside) was hardcoded to one client's Johor AI training curriculum -- reusing
it verbatim for a hackathon pitch would mean shipping a deck about someone
else's training program. What's reused is the STRUCTURE (16:9, theme
constants, a text-box helper) -- the content comes from parsing the
project's actual docs/PITCH.md, one slide per `##` section, because
that file is the thing a human (or Sonnet, confirmed before spending) already
wrote and reviewed. Nothing here invents slide content.
"""
import re
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
COLOR_DARK = RGBColor(0, 51, 102)
COLOR_TEXT = RGBColor(51, 51, 51)
COLOR_WHITE = RGBColor(255, 255, 255)
FONT = "Calibri"


def parse_sections(md_text):
    """## heading -> body text, in order. The pitch card's own structure IS
    the deck's structure -- one-liner, problem, why-not-a-wrapper, market,
    open-source strategy, demo script -- whatever headings it actually has."""
    sections = []
    for block in re.split(r"^## ", md_text, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        title = lines[0].strip() if lines else "(untitled)"
        body = "\n".join(lines[1:]).strip()
        sections.append((title, body))
    return sections


def add_title_slide(prs, name, one_liner):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    box = slide.shapes.add_textbox(Inches(0.8), Inches(2.6), SLIDE_W - Inches(1.6), Inches(1.5))
    tf = box.text_frame
    tf.text = name
    tf.paragraphs[0].font.size = Pt(44)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = COLOR_DARK
    tf.paragraphs[0].font.name = FONT
    if one_liner:
        p = tf.add_paragraph()
        p.text = one_liner
        p.font.size = Pt(20)
        p.font.color.rgb = COLOR_TEXT
        p.font.name = FONT


def add_content_slide(prs, title, body):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    head = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), SLIDE_W - Inches(1.2), Inches(0.9))
    hf = head.text_frame
    hf.text = title
    hf.paragraphs[0].font.size = Pt(30)
    hf.paragraphs[0].font.bold = True
    hf.paragraphs[0].font.color.rgb = COLOR_DARK
    hf.paragraphs[0].font.name = FONT

    box = slide.shapes.add_textbox(Inches(0.6), Inches(1.5), SLIDE_W - Inches(1.2), SLIDE_H - Inches(2.0))
    tf = box.text_frame
    tf.word_wrap = True
    lines = [l for l in body.splitlines() if l.strip() and not l.strip().startswith(("![", "::"))] or ["(not yet written)"]
    tf.text = lines[0].lstrip("- ").strip()
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = COLOR_TEXT
    tf.paragraphs[0].font.name = FONT
    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line.lstrip("- ").strip()
        p.font.size = Pt(20)
        p.font.color.rgb = COLOR_TEXT
        p.font.name = FONT


def build(name, card_path, out_path):
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    text = open(card_path, encoding="utf-8").read()
    sections = parse_sections(text)
    one_liner = sections[0][1].splitlines()[0] if sections and sections[0][1] else ""
    add_title_slide(prs, name, one_liner)
    for title, body in sections:
        add_content_slide(prs, title, body)

    prs.save(out_path)
    return len(sections) + 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: build_slides.py <name> <card.md> <out.pptx>", file=sys.stderr)
        sys.exit(2)
    n = build(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"{n} slides -> {sys.argv[3]}")
