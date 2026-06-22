"""
BiTalih OddBoost PowerPoint Generator
Generates a 6-slide 16:9 presentation using python-pptx.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree
import copy

# ──────────────────────────────────────────────
# STYLE CONSTANTS
# ──────────────────────────────────────────────
TEXT_DARK    = RGBColor(0x19, 0x19, 0x19)
TEXT_MUTED   = RGBColor(0x6C, 0x6F, 0x73)
LINE_COLOR   = RGBColor(0xE6, 0xE6, 0xE6)
ACCENT       = RGBColor(0xE8, 0x59, 0x0C)
ACCENT_SOFT  = RGBColor(0xFD, 0xEE, 0xE2)
WF_DARK      = RGBColor(0x3C, 0x40, 0x43)
WF_GRAY      = RGBColor(0x9A, 0xA0, 0xA6)
WF_LIGHT     = RGBColor(0xF1, 0xF3, 0xF4)
WF_LIGHT2    = RGBColor(0xE8, 0xEA, 0xED)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)

FONT_NAME = "Arial"

# ──────────────────────────────────────────────
# HELPER: STRIKETHROUGH
# ──────────────────────────────────────────────
def apply_strikethrough(run):
    """Apply single strikethrough to a run."""
    r_elem = run._r
    # Find or create rPr element
    rPr = r_elem.find(qn('a:rPr'))
    if rPr is None:
        rPr = etree.SubElement(r_elem, qn('a:rPr'))
        t_elem = r_elem.find(qn('a:t'))
        if t_elem is not None:
            r_elem.remove(rPr)
            idx = list(r_elem).index(t_elem)
            r_elem.insert(idx, rPr)
    rPr.set('strike', 'sngStrike')


# ──────────────────────────────────────────────
# HELPER: ADD TEXT BOX (simple, single run)
# ──────────────────────────────────────────────
def add_textbox(slide, left, top, width, height,
                text, font_size=14, bold=False,
                color=None, align=PP_ALIGN.LEFT,
                wrap=True, italic=False):
    if color is None:
        color = TEXT_DARK
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = FONT_NAME
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


# ──────────────────────────────────────────────
# HELPER: ADD RECTANGLE (optionally rounded)
# ──────────────────────────────────────────────
def add_rect(slide, left, top, width, height,
             fill_color=None, line_color=None,
             line_width_pt=0.75, rounded=False,
             line_dash=None):
    if rounded:
        shape = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
    else:
        shape = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()

    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width_pt)
        if line_dash:
            shape.line.dash_style = line_dash
    else:
        shape.line.fill.background()

    return shape


# ──────────────────────────────────────────────
# HELPER: ADD OVAL (for kicker dot)
# ──────────────────────────────────────────────
def add_oval(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


# ──────────────────────────────────────────────
# HELPER: SET SHAPE TEXT (single paragraph, single run)
# ──────────────────────────────────────────────
def set_shape_text(shape, text, font_size=11, bold=False,
                   color=None, align=PP_ALIGN.LEFT, italic=False):
    if color is None:
        color = TEXT_DARK
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    if p.runs:
        run = p.runs[0]
    else:
        run = p.add_run()
    run.text = text
    run.font.name = FONT_NAME
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return tf


# ──────────────────────────────────────────────
# HELPER: ADD PARAGRAPH WITH BOLD + NORMAL TEXT
# ──────────────────────────────────────────────
def add_mixed_paragraph(tf, bold_text, normal_text,
                         font_size=14,
                         bold_color=None, normal_color=None,
                         space_before_pt=4, indent_left=0.15):
    if bold_color is None:
        bold_color = TEXT_DARK
    if normal_color is None:
        normal_color = TEXT_DARK

    p = tf.add_paragraph()
    p.space_before = Pt(space_before_pt)
    if indent_left:
        from pptx.util import Inches as _I
        p.level = 0

    if bold_text:
        run_b = p.add_run()
        run_b.text = bold_text
        run_b.font.name = FONT_NAME
        run_b.font.size = Pt(font_size)
        run_b.font.bold = True
        run_b.font.color.rgb = bold_color

    if normal_text:
        run_n = p.add_run()
        run_n.text = " " + normal_text if bold_text else normal_text
        run_n.font.name = FONT_NAME
        run_n.font.size = Pt(font_size)
        run_n.font.bold = False
        run_n.font.color.rgb = normal_color

    return p


# ──────────────────────────────────────────────
# HELPER: ADD KICKER (dot + label) and slide number
# ──────────────────────────────────────────────
def add_kicker_and_number(slide, kicker_text, slide_num):
    # Orange dot
    add_oval(slide, 0.35, 0.18, 0.1, 0.1, ACCENT)
    # Kicker text
    add_textbox(slide, 0.5, 0.14, 9.0, 0.28,
                kicker_text, font_size=10, bold=False,
                color=TEXT_MUTED, align=PP_ALIGN.LEFT)
    # Slide number bottom-right
    add_textbox(slide, 12.4, 7.1, 0.6, 0.3,
                str(slide_num), font_size=11,
                color=TEXT_MUTED, align=PP_ALIGN.RIGHT)


# ──────────────────────────────────────────────
# HELPER: ACCENT SQUARE BULLET + TEXT (for bullet lists)
# ──────────────────────────────────────────────
def add_bullet_row(slide, left_x, y, width, bold_text, normal_text,
                   font_size=14, bullet_size=0.07):
    """Add a small ACCENT square bullet + bold + normal text line."""
    # Small orange square
    sq = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE,
        Inches(left_x), Inches(y + 0.055), Inches(bullet_size), Inches(bullet_size)
    )
    sq.fill.solid()
    sq.fill.fore_color.rgb = ACCENT
    sq.line.fill.background()

    # Text box to the right of bullet
    txBox = slide.shapes.add_textbox(
        Inches(left_x + bullet_size + 0.06),
        Inches(y),
        Inches(width),
        Inches(0.5)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    if bold_text:
        rb = p.add_run()
        rb.text = bold_text
        rb.font.name = FONT_NAME
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK

    if normal_text:
        rn = p.add_run()
        rn.text = " " + normal_text if bold_text else normal_text
        rn.font.name = FONT_NAME
        rn.font.size = Pt(font_size)
        rn.font.bold = False
        rn.font.color.rgb = TEXT_DARK

    return txBox


# ──────────────────────────────────────────────
# SLIDE 1 — Yonetici Ozeti
# ──────────────────────────────────────────────
def build_slide1(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "URUN STRATEJISI  ·  SABIT IHTIMALLI AT YARISI",
        1
    )

    # Title
    add_textbox(slide, 0.4, 0.38, 12.6, 0.85,
                "Odd Boost: rakipler nasil yapiyor, BiTalih nasil konumlanmali",
                font_size=28, bold=True, color=TEXT_DARK)

    # Intro paragraph
    intro = (
        "Odd Boost bir bonus degil. "
        "Operatorun marjini bilincli feda edip secili bir orana piyasa ustu fiyat vermesidir. "
        "Uc isi var: yeni uye cekmek, her gun geri getirmek, yuksek marjli urune (kombine) yonlendirmek."
    )
    add_textbox(slide, 0.4, 1.28, 12.3, 0.65,
                intro, font_size=14, color=TEXT_DARK)

    # Separator line
    ln = add_rect(slide, 0.4, 2.0, 12.3, 0.01,
                  fill_color=LINE_COLOR, line_color=None)

    # 5 bullet points
    bullets = [
        ("Baglam:",
         "Bu, BiTalih'in sabit ihtimalli (fixed odds) at yarisi urunudur. "
         "Sabitlenebilir oran oldugu icin UK bookmaker modeli birebir uygulanir; "
         "mustehek (ganyan) kisitlari burada gecerli degil."),
        ("Boost ailesi:",
         "tekli fiyat boost, kombine boost (gun ici kosular arasi), jeton boost, "
         "ekstra plase, Best Odds Guaranteed (BOG), para iade special."),
        ("BOG one cikiyor.",
         "Sabit ihtimalli yarisinin en guclu deger mekanigi: "
         "aldigin oran ile baslangic orani (SP) karsilastirilir, "
         "hep musteri lehine odenir. Erken benimsemek net farklilasma saglar."),
        ("Boost'u sadakat motoruna bagla.",
         "Gunluk jeton ANBEAN Kulubu odulu olur, koleksiyon karti ekonomisine eklenir."),
        ("Guardrail sart.",
         "Maksimum stake dusuk, win-only, dar zaman penceresi. "
         "Yarista likidite hizli doner."),
    ]

    y_start = 2.1
    y_step  = 0.78

    for i, (bold_t, normal_t) in enumerate(bullets):
        add_bullet_row(slide, 0.4, y_start + i * y_step, 12.0,
                       bold_t, normal_t, font_size=14)

    # Small note
    add_textbox(slide, 0.4, 6.92, 12.3, 0.38,
                "Rakip gorsel sayfasi (3. slayt) bos birakildi; ekran goruntuleri sonradan eklenecek.",
                font_size=11, italic=True, color=TEXT_MUTED)

    return slide


# ──────────────────────────────────────────────
# SLIDE 2 — Ne Zaman ve Nasil Devreye Giriyor
# ──────────────────────────────────────────────
def build_slide2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "NE ZAMAN  ·  NASIL DEVREYE GIRIYOR",
        2
    )

    add_textbox(slide, 0.4, 0.38, 12.3, 0.55,
                "Tetikleme modelleri ve zamanlama",
                font_size=26, bold=True, color=TEXT_DARK)

    # 2x2 card layout
    cards = [
        {
            "label": "RETENTION",
            "title": "Gunluk jeton",
            "body":  "Musteriye gunde 1 oran artirma hakki verilir, "
                     "istedigi kupona kendi uygular.",
            "sub":   "Tetik: her gece 00:00 yenilenir. Amac gunluk aktif kullanici (DAU).",
            "ref":   "Ref: Ladbrokes Odds Boost",
        },
        {
            "label": "ACQUISITION",
            "title": "Event super boost",
            "body":  "Buyuk kosuda ana sayfada dev banner. "
                     "Operator bu bahisten zarari goze alir.",
            "sub":   "Tetik: buyuk kosutan 60-90 dk once. Amac yeni uye ve sosyal medyada viral olmak.",
            "ref":   "Ref: Bet365 Super Boost",
        },
        {
            "label": "MARGIN",
            "title": "Kombine boost (Acca)",
            "body":  "Kupona kosular eklendikce toplam kazanc yuzdesel artar. "
                     "Cok bacakli kombine kitap icin daha karlidir.",
            "sub":   "Tetik: surekli acik. Amac oyuncuyu 3 yerine 5-8 kosua itmek.",
            "ref":   "",
        },
        {
            "label": "CRM",
            "title": "Segment tetikli",
            "body":  "Lapsed, VIP, favori jokey veya hipodrom bazli hedefli boost. "
                     "Reaktivasyon kampanyalari.",
            "sub":   "Tetik: davranisa gore otomatik. Amac kayip oyuncuyu geri cagirmak.",
            "ref":   "",
        },
    ]

    positions = [
        (0.35, 1.05),  # top-left
        (6.75, 1.05),  # top-right
        (0.35, 4.0),   # bottom-left
        (6.75, 4.0),   # bottom-right
    ]
    card_w = 6.1
    card_h = 2.7

    for card, (cx, cy) in zip(cards, positions):
        # Card background
        bg = add_rect(slide, cx, cy, card_w, card_h,
                      fill_color=WF_LIGHT, line_color=LINE_COLOR,
                      line_width_pt=0.5, rounded=True)

        # ACCENT label
        add_textbox(slide, cx + 0.18, cy + 0.15, card_w - 0.3, 0.25,
                    card["label"],
                    font_size=10, bold=True, color=ACCENT)

        # Bold title
        add_textbox(slide, cx + 0.18, cy + 0.43, card_w - 0.3, 0.35,
                    card["title"],
                    font_size=13, bold=True, color=TEXT_DARK)

        # Body
        add_textbox(slide, cx + 0.18, cy + 0.82, card_w - 0.3, 0.75,
                    card["body"],
                    font_size=12, color=TEXT_DARK)

        # Sub
        add_textbox(slide, cx + 0.18, cy + 1.57, card_w - 0.3, 0.6,
                    card["sub"],
                    font_size=11, color=TEXT_MUTED)

        # Ref
        if card["ref"]:
            add_textbox(slide, cx + 0.18, cy + 2.3, card_w - 0.3, 0.25,
                        card["ref"],
                        font_size=10, italic=True, color=WF_GRAY)

    # Small note
    add_textbox(
        slide, 0.4, 6.9, 12.5, 0.4,
        "At yarisi penceresi dar: standart yaris boost'u yaris gunu ~10:00'da acilir, "
        "baslamaya ~15 dk kala kapanir. Likidite hizli degistigi icin limitler de dusuk tutulur.",
        font_size=11, italic=False, color=TEXT_MUTED
    )

    return slide


# ──────────────────────────────────────────────
# SLIDE 3 — Rakip Ekranlari (placeholder)
# ──────────────────────────────────────────────
def build_slide3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "RAKIP EKRANLARI  ·  GORSEL ALANI",
        3
    )

    add_textbox(slide, 0.4, 0.38, 12.3, 0.55,
                "Rakip ekran goruntuleri (sonradan eklenecek)",
                font_size=26, bold=True, color=TEXT_DARK)

    placeholders = [
        {
            "operator": "Bet365",
            "feature":  "Super Boost",
            "desc":     "Event banner, ustu cizili eski fiyat ve yeni boost fiyati (was/now). "
                        "Loss-leader mantigi.",
        },
        {
            "operator": "Ladbrokes",
            "feature":  "Odds Boost jetonu",
            "desc":     "Gunluk jeton ('1 boost hakkin var') ve kupona uygulama akisi. "
                        "Retention mekanigi.",
        },
        {
            "operator": "Bet365 / Betfred",
            "feature":  "Acca Boost merdiveni",
            "desc":     "Bacak sayisina gore artan kazanc yuzdesi tablosu. "
                        "Margin artirici yapi.",
        },
        {
            "operator": "William Hill",
            "feature":  "Ekstra Plase / BOG",
            "desc":     "Yarista ekstra plase rozeti ('5 sira odeme') ve Best Odds Guaranteed isareti.",
        },
    ]

    positions = [
        (0.35, 1.05),
        (6.75, 1.05),
        (0.35, 4.0),
        (6.75, 4.0),
    ]
    card_w = 6.1
    card_h = 2.75

    for ph, (cx, cy) in zip(placeholders, positions):
        # Header bar
        hdr = add_rect(slide, cx, cy, card_w, 0.38,
                       fill_color=WF_LIGHT2, line_color=LINE_COLOR,
                       line_width_pt=0.5)

        # Operator name
        add_textbox(slide, cx + 0.12, cy + 0.06, card_w * 0.55, 0.28,
                    ph["operator"],
                    font_size=12, bold=True, color=WF_DARK)

        # Feature label (ACCENT, right-aligned)
        add_textbox(slide, cx + card_w * 0.55, cy + 0.06, card_w * 0.42, 0.28,
                    ph["feature"],
                    font_size=11, bold=False, color=ACCENT,
                    align=PP_ALIGN.RIGHT)

        # Dashed placeholder main area
        main_box = add_rect(slide, cx + 0.12, cy + 0.48, card_w - 0.24, 1.55,
                            fill_color=WF_LIGHT, line_color=WF_GRAY,
                            line_width_pt=0.75, line_dash=MSO_LINE_DASH_STYLE.DASH)

        # Centered placeholder text inside dashed box
        add_textbox(slide, cx + 0.12, cy + 0.95, card_w - 0.24, 0.5,
                    "Ekran goruntusunu buraya ekle",
                    font_size=12, color=WF_GRAY,
                    align=PP_ALIGN.CENTER)

        # Description below
        txBox = slide.shapes.add_textbox(
            Inches(cx + 0.12), Inches(cy + 2.13),
            Inches(card_w - 0.24), Inches(0.52)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        rb = p.add_run()
        rb.text = "Ne gostermeli: "
        rb.font.name = FONT_NAME
        rb.font.size = Pt(10)
        rb.font.bold = True
        rb.font.color.rgb = WF_DARK
        rn = p.add_run()
        rn.text = ph["desc"]
        rn.font.name = FONT_NAME
        rn.font.size = Pt(10)
        rn.font.color.rgb = TEXT_MUTED

    # Small note
    add_textbox(
        slide, 0.4, 6.9, 12.5, 0.4,
        "Her kutuya gercek ekran goruntusunu yerlesstir; "
        "alttaki aciklama o gorselin ne anlatmasi gerektigini hatirlat.",
        font_size=11, italic=True, color=TEXT_MUTED
    )

    return slide


# ──────────────────────────────────────────────
# SLIDE 4 — Boost Tipleri ve Hesaplama
# ──────────────────────────────────────────────
def build_slide4(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "MEKANIK  ·  NASIL HESAPLANIYOR",
        4
    )

    add_textbox(slide, 0.4, 0.38, 12.3, 0.55,
                "Boost tipleri ve matematigi",
                font_size=26, bold=True, color=TEXT_DARK)

    add_textbox(
        slide, 0.4, 0.98, 12.3, 0.45,
        "100 TL stake uzerinden temsili ornekler (sabit ihtimalli at yarisi). "
        "Operator maliyeti yaklasik degerdir; standart oran zaten marj icerdigi icin "
        "gercek beklenen maliyet biraz daha dusuktur.",
        font_size=13, color=TEXT_MUTED
    )

    # Table setup
    table_left  = 0.4
    table_top   = 1.5
    col_widths  = [2.1, 5.3, 4.6]   # inches
    row_height  = 0.72
    total_w     = sum(col_widths)
    headers     = ["Tip", "Hesap", "Sonuc (100 TL)"]

    rows_data = [
        (
            "Tekli fiyat boost",
            "Atin orani 4.50 -> 5.50. Getiri = stake x oran.",
            "450 yerine 550. Oyuncuya +100 TL deger. Kitaba beklenen maliyet yaklasik %22 stake.",
        ),
        (
            "Kombine boost (gun ici kosular)",
            "3 kosur x 3.00 = 27.00 oran. Kazanc (getiri - stake) x (1+%15).",
            "Net kazanc 2.600 -> 2.990. Toplam getiri 2.700 -> 3.090. Yuzde orana degil net kazanca isler.",
        ),
        (
            "Jeton / kar boost",
            "Oran 2.00, kara +%50. Kar 100 -> 150.",
            "Getiri 200 -> 250. Efektif oran 2.50. Max stake cap'li.",
        ),
        (
            "Ekstra plase",
            "Oran sabit. Her-yol = kazan + plase. Odenen sira 3 -> 5.",
            "Tutar ayni, kazanma ihtimali artar. 4. ve 5. de artik oder.",
        ),
        (
            "Best Odds Guaranteed (BOG)",
            "Aldigin oran 6.00. SP 8.00 ise 8.00'den, SP 5.00 ise 6.00'dan odenir.",
            "SP yuksekse -> 800, dusukse -> 600. Hep musteri lehine asimetri.",
        ),
    ]

    # Header row
    x_offset = table_left
    for ci, (hdr, cw) in enumerate(zip(headers, col_widths)):
        cell_bg = add_rect(slide, x_offset, table_top, cw, row_height * 0.62,
                           fill_color=ACCENT, line_color=None)
        add_textbox(slide, x_offset + 0.08, table_top + 0.1, cw - 0.1, 0.38,
                    hdr, font_size=12, bold=True, color=WHITE)
        x_offset += cw

    # Data rows
    alt_fills = [WF_LIGHT, WHITE]
    for ri, row_data in enumerate(rows_data):
        y = table_top + 0.62 * 0.62 + ri * row_height * 0.88 + 0.02
        # Adjust spacing: each row ~0.65 tall
        y = table_top + 0.42 + ri * 0.98
        x_offset = table_left
        fill = alt_fills[ri % 2]
        for ci, (cell_text, cw) in enumerate(zip(row_data, col_widths)):
            add_rect(slide, x_offset, y, cw, 0.9,
                     fill_color=fill, line_color=LINE_COLOR,
                     line_width_pt=0.3)
            add_textbox(slide, x_offset + 0.08, y + 0.06, cw - 0.12, 0.82,
                        cell_text, font_size=11, color=TEXT_DARK)
            x_offset += cw

    # Small note
    add_textbox(
        slide, 0.4, 6.86, 12.3, 0.44,
        "BOG sabit ihtimalliye ozgudur: oran kilitlenmis oldugu icin 'en iyi oran' garantisi verilebilir. "
        "Mustehek sistemde karsiligi yoktur, bu yuzden guclu farklilasma noktasidir.",
        font_size=11, italic=True, color=TEXT_MUTED
    )

    return slide


# ──────────────────────────────────────────────
# SLIDE 5 — At Yarisi Ozel Dinamikler ve BiTalih Oyun Plani
# ──────────────────────────────────────────────
def build_slide5(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "AT YARISI  ·  OZEL DINAMIKLER",
        5
    )

    add_textbox(slide, 0.4, 0.38, 12.3, 0.55,
                "Sabit ihtimalli yarista boost playbook'u",
                font_size=26, bold=True, color=TEXT_DARK)

    # ---- LEFT COLUMN ----
    lx = 0.4
    add_textbox(slide, lx, 1.05, 5.8, 0.35,
                "Mekanikler (UK referansi)",
                font_size=14, bold=True, color=TEXT_DARK)

    left_bullets = [
        ("Best Odds Guaranteed (BOG).",
         "Aldigin fiyattan SP yuksek cikarsa SP'den odenirsin. "
         "Yarisinin en guclu deger mekanigi."),
        ("Ekstra plase.",
         "Buyuk sahali handikaplarda odenen sira artar. "
         "Saha kalabaliksa deger yuksek."),
        ("Para iade special.",
         "'Favoriye 2. olursa iade', dusme veya foto-finish iadesi. Guven satisi."),
        ("Nap of the day + jokey/antrenor ozel.",
         "Gunun ati veya populer isim uzerinden paket boost."),
        ("Limitler.",
         "Likidite hizli dondugu icin max stake dusuk, "
         "exotic bahislerde kisit."),
    ]

    y = 1.45
    for bold_t, normal_t in left_bullets:
        txBox = slide.shapes.add_textbox(
            Inches(lx + 0.18), Inches(y), Inches(5.6), Inches(0.78)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_before = Pt(3)
        rb = p.add_run()
        rb.text = bold_t
        rb.font.name = FONT_NAME
        rb.font.size = Pt(13)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK
        rn = p.add_run()
        rn.text = " " + normal_t
        rn.font.name = FONT_NAME
        rn.font.size = Pt(13)
        rn.font.color.rgb = TEXT_DARK
        y += 0.92

    # Vertical separator line
    ln = add_rect(slide, 6.55, 1.0, 0.01, 5.7,
                  fill_color=LINE_COLOR, line_color=None)

    # ---- RIGHT COLUMN ----
    rx = 6.75
    add_textbox(slide, rx, 1.05, 6.0, 0.35,
                "BiTalih oyun plani",
                font_size=14, bold=True, color=TEXT_DARK)

    right_bullets = [
        ("BOG'u amiral mekanik yap.",
         "En gorunur, en guclu vaat. Buyuk kosularla baslat, "
         "'BiTalih garantisi' diye markala."),
        ("Ekstra plase'yi cok atli handikaplarda ac.",
         "Degerin en yuksek oldugu yer burasi."),
        ("Iade special'i sinirli ve viral senaryoda kullan.",
         "Favoriye 2., foto-finish. Butceyi koru."),
        ("Gunun ati boost'unu editoryal takvime bagla.",
         "Push ile dagit, start oncesi kapat."),
        ("Limitleri siki tut.",
         "Dusuk max stake, win-only, dar pencere."),
    ]

    y = 1.45
    for bold_t, normal_t in right_bullets:
        txBox = slide.shapes.add_textbox(
            Inches(rx + 0.18), Inches(y), Inches(5.8), Inches(0.78)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.space_before = Pt(3)
        rb = p.add_run()
        rb.text = bold_t
        rb.font.name = FONT_NAME
        rb.font.size = Pt(13)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK
        rn = p.add_run()
        rn.text = " " + normal_t
        rn.font.name = FONT_NAME
        rn.font.size = Pt(13)
        rn.font.color.rgb = TEXT_DARK
        y += 0.92

    # Small note
    add_textbox(
        slide, 0.4, 6.86, 12.5, 0.44,
        "Siralama onerisi: once gunluk jeton (retention) ve BOG (farklilasma), "
        "sonra kombine boost (margin), en son event super boost (acquisition).",
        font_size=11, italic=True, color=TEXT_MUTED
    )

    return slide


# ──────────────────────────────────────────────
# SLIDE 6 — BiTalih Wireframe ve Durusu
# ──────────────────────────────────────────────
def build_slide6(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_kicker_and_number(
        slide,
        "BITALIH  ·  WIREFRAME VE DURUSU",
        6
    )

    add_textbox(slide, 0.4, 0.38, 12.3, 0.55,
                "Ekran taslaklari (siyah-beyaz)",
                font_size=26, bold=True, color=TEXT_DARK)

    # ── 2x2 wireframe card grid ──
    card_w  = 5.8
    card_h  = 2.65
    pad     = 0.1
    xs = [0.35, 6.78]
    ys = [1.02, 3.82]

    def wf_card(cx, cy, card_h=card_h):
        """Draw a phone-card-style wireframe container."""
        bg = add_rect(slide, cx, cy, card_w, card_h,
                      fill_color=WF_LIGHT, line_color=WF_DARK,
                      line_width_pt=0.75, rounded=True)
        return bg

    def wf_tb(left, top, width, height, text, fs=9,
              bold=False, color=None, align=PP_ALIGN.LEFT):
        if color is None:
            color = WF_DARK
        return add_textbox(slide, left, top, width, height,
                           text, font_size=fs, bold=bold,
                           color=color, align=align)

    def wf_dark_btn(cx, cy, bw, bh, label, fs=10):
        btn = add_rect(slide, cx, cy, bw, bh,
                       fill_color=WF_DARK, line_color=None, rounded=True)
        add_textbox(slide, cx, cy + 0.02, bw, bh - 0.04,
                    label, font_size=fs, bold=True,
                    color=WHITE, align=PP_ALIGN.CENTER)

    def wf_dashed_box(cx, cy, bw, bh):
        return add_rect(slide, cx, cy, bw, bh,
                        fill_color=WF_LIGHT2, line_color=WF_GRAY,
                        line_width_pt=0.75,
                        line_dash=MSO_LINE_DASH_STYLE.DASH)

    def wf_thin_line(cx, cy, bw):
        add_rect(slide, cx, cy, bw, 0.015,
                 fill_color=WF_GRAY, line_color=None)

    # ─── WF1: Gunun Kosusu Boost'u (top-left) ───
    cx, cy = xs[0], ys[0]
    wf_card(cx, cy)

    # "15:30 Veliefendi - Sezar"
    wf_tb(cx + pad, cy + 0.08, card_w - 2*pad, 0.22,
          "15:30 Veliefendi  -  Sezar", fs=9, color=WF_GRAY)

    # Dashed boost box
    db_y = cy + 0.33
    db_h = 0.8
    wf_dashed_box(cx + pad, db_y, card_w - 2*pad, db_h)

    wf_tb(cx + pad + 0.08, db_y + 0.06, 2.2, 0.2,
          "Gunun Kosusu Boost", fs=8, color=WF_GRAY)

    # Strikethrough price + arrow + new price
    price_tb = slide.shapes.add_textbox(
        Inches(cx + pad + 0.08), Inches(db_y + 0.3),
        Inches(3.0), Inches(0.36)
    )
    ptf = price_tb.text_frame
    ptf.word_wrap = False
    pp = ptf.paragraphs[0]
    pp.alignment = PP_ALIGN.LEFT

    r_old = pp.add_run()
    r_old.text = "5.50"
    r_old.font.name = FONT_NAME
    r_old.font.size = Pt(14)
    r_old.font.bold = False
    r_old.font.color.rgb = WF_GRAY
    try:
        apply_strikethrough(r_old)
    except Exception:
        pass

    r_arr = pp.add_run()
    r_arr.text = "  ->  "
    r_arr.font.name = FONT_NAME
    r_arr.font.size = Pt(12)
    r_arr.font.color.rgb = WF_GRAY

    r_new = pp.add_run()
    r_new.text = "6.50"
    r_new.font.name = FONT_NAME
    r_new.font.size = Pt(16)
    r_new.font.bold = True
    r_new.font.color.rgb = WF_DARK

    # "+%18" badge (dark, top-right of dashed box)
    badge_x = cx + card_w - pad - 0.82
    add_rect(slide, badge_x, db_y + 0.08, 0.72, 0.28,
             fill_color=WF_DARK, line_color=None, rounded=True)
    wf_tb(badge_x, db_y + 0.1, 0.72, 0.22, "+%18", fs=9,
          bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # "KUPONA EKLE" button
    wf_dark_btn(cx + pad, db_y + db_h + 0.08,
                card_w - 2*pad, 0.32, "KUPONA EKLE", fs=10)

    # Countdown
    cd_y = db_y + db_h + 0.47
    add_rect(slide, cx + pad, cd_y, card_w - 2*pad, 0.26,
             fill_color=WF_LIGHT2, line_color=WF_GRAY, line_width_pt=0.4)
    wf_tb(cx + pad + 0.1, cd_y + 0.04, 1.5, 0.2,
          "Firsat bitisi", fs=9, color=WF_GRAY)
    wf_tb(cx + card_w - pad - 1.2, cd_y + 0.04, 1.1, 0.2,
          "00:12:40", fs=9, bold=True, color=WF_DARK,
          align=PP_ALIGN.RIGHT)

    # Two thin list placeholder lines
    wf_thin_line(cx + pad, cd_y + 0.35, card_w - 2*pad)
    wf_thin_line(cx + pad, cd_y + 0.52, card_w - 2*pad)

    # Label below card
    add_textbox(slide, cx, cy + card_h + 0.04, card_w, 0.28,
                "Sabit oranli tekli fiyat boost. Was/now + geri sayim (FOMO).",
                font_size=10, color=TEXT_MUTED)

    # ─── WF2: Jeton cüzdani (top-right) ───
    cx, cy = xs[1], ys[0]
    wf_card(cx, cy)

    # Dashed box with token info
    db2_y = cy + 0.1
    wf_dashed_box(cx + pad, db2_y, card_w - 2*pad, 0.78)

    # Circle "+" icon placeholder
    add_oval(slide, cx + pad + 0.08, db2_y + 0.22, 0.28, 0.28, WF_GRAY)
    wf_tb(cx + pad + 0.12, db2_y + 0.27, 0.22, 0.2,
          "+", fs=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    wf_tb(cx + pad + 0.44, db2_y + 0.12, 3.2, 0.24,
          "Odds Boost  -  1 hakkin var", fs=11, bold=True, color=WF_DARK)
    wf_tb(cx + pad + 0.44, db2_y + 0.4, 2.2, 0.22,
          "Kuponuna uygula", fs=10, color=WF_GRAY)

    # Toggle (right side)
    tog_x = cx + card_w - pad - 0.7
    tog_rect = add_rect(slide, tog_x, db2_y + 0.38, 0.6, 0.24,
                        fill_color=WF_DARK, line_color=None, rounded=True)
    wf_tb(tog_x + 0.05, db2_y + 0.4, 0.5, 0.2,
          "ON", fs=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # New odds box
    odds_y = db2_y + 0.9
    add_rect(slide, cx + pad, odds_y, card_w - 2*pad, 0.5,
             fill_color=WF_LIGHT2, line_color=WF_GRAY, line_width_pt=0.4)

    wf_tb(cx + pad + 0.1, odds_y + 0.08, 1.0, 0.24,
          "Yeni oran:", fs=10, color=WF_GRAY)

    # Strikethrough 2.00 -> 2.50
    str_tb = slide.shapes.add_textbox(
        Inches(cx + pad + 1.15), Inches(odds_y + 0.06),
        Inches(2.5), Inches(0.32)
    )
    stf = str_tb.text_frame
    stf.word_wrap = False
    sp = stf.paragraphs[0]
    r_old2 = sp.add_run()
    r_old2.text = "2.00"
    r_old2.font.name = FONT_NAME
    r_old2.font.size = Pt(12)
    r_old2.font.color.rgb = WF_GRAY
    try:
        apply_strikethrough(r_old2)
    except Exception:
        pass
    r_new2 = sp.add_run()
    r_new2.text = "  2.50"
    r_new2.font.name = FONT_NAME
    r_new2.font.size = Pt(14)
    r_new2.font.bold = True
    r_new2.font.color.rgb = WF_DARK

    # +%25 badge
    add_rect(slide, cx + card_w - pad - 0.78, odds_y + 0.1, 0.68, 0.26,
             fill_color=WF_DARK, line_color=None, rounded=True)
    wf_tb(cx + card_w - pad - 0.78, odds_y + 0.12, 0.68, 0.2,
          "+%25", fs=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # BOOST'U KULLAN button
    btn_y = odds_y + 0.58
    wf_dark_btn(cx + pad, btn_y, card_w - 2*pad, 0.32, "BOOST'U KULLAN", fs=10)

    # Two thin placeholder lines
    wf_thin_line(cx + pad, btn_y + 0.4, card_w - 2*pad)
    wf_thin_line(cx + pad, btn_y + 0.57, card_w - 2*pad)

    add_textbox(slide, cx, cy + card_h + 0.04, card_w, 0.28,
                "Gunluk 1 hak, kuponda toggle ile uygula. ANBEAN Kulup odulu.",
                font_size=10, color=TEXT_MUTED)

    # ─── WF3: Kombine selalesi (bottom-left) ───
    cx, cy = xs[0], ys[1]
    wf_card(cx, cy)

    # Header: "Gun ici kosular" + "+%25"
    wf_tb(cx + pad, cy + 0.12, 3.0, 0.3,
          "Gun ici kosular", fs=11, color=WF_DARK)
    wf_tb(cx + card_w - pad - 1.2, cy + 0.08, 1.1, 0.36,
          "+%25", fs=16, bold=True, color=WF_DARK,
          align=PP_ALIGN.RIGHT)

    # Separator
    wf_thin_line(cx + pad, cy + 0.46, card_w - 2*pad)

    # Ladder bars
    bar_data = [
        ("3 kosur -> +5%",  1.0, WF_GRAY),
        ("5 kosur -> +25%", 2.5, WF_GRAY),
        ("8 kosur -> +50%", card_w - 2*pad - 0.2, WF_DARK),
    ]
    bar_h    = 0.22
    bar_base = cy + 0.55
    for bi, (label, bar_w_val, bar_fill) in enumerate(bar_data):
        by = bar_base + bi * 0.36
        # Thin bar
        add_rect(slide, cx + pad + 0.1, by + 0.04, bar_w_val, bar_h,
                 fill_color=bar_fill, line_color=None)
        wf_tb(cx + pad + 0.18, by + 0.06, bar_w_val + 0.1, 0.2,
              label, fs=9, bold=(bar_fill == WF_DARK),
              color=(WHITE if bar_fill == WF_DARK else WF_DARK))

    # Stepper
    step_y = bar_base + 3 * 0.36 + 0.05
    add_rect(slide, cx + pad, step_y, 0.32, 0.3,
             fill_color=WF_LIGHT2, line_color=WF_GRAY, line_width_pt=0.5)
    wf_tb(cx + pad, step_y + 0.04, 0.32, 0.24,
          "-", fs=12, bold=True, color=WF_DARK, align=PP_ALIGN.CENTER)
    wf_tb(cx + pad + 0.4, step_y + 0.05, 2.5, 0.24,
          "5 kosur secili", fs=10, color=WF_DARK)
    add_rect(slide, cx + pad + 3.2, step_y, 0.32, 0.3,
             fill_color=WF_LIGHT2, line_color=WF_GRAY, line_width_pt=0.5)
    wf_tb(cx + pad + 3.2, step_y + 0.04, 0.32, 0.24,
          "+", fs=12, bold=True, color=WF_DARK, align=PP_ALIGN.CENTER)

    # Button
    btn3_y = step_y + 0.38
    wf_dark_btn(cx + pad, btn3_y, card_w - 2*pad, 0.32,
                "KOMBINEYi TAMAMLA", fs=10)

    add_textbox(slide, cx, cy + card_h + 0.04, card_w, 0.28,
                "Kosu ekledikce carpan buyur. Margin artirici.",
                font_size=10, color=TEXT_MUTED)

    # ─── WF4: BOG + Ekstra Plase (bottom-right) ───
    cx, cy = xs[1], ys[1]
    wf_card(cx, cy)

    # "Buyuk Handikap - 14 at"
    wf_tb(cx + pad, cy + 0.1, card_w - 2*pad, 0.24,
          "Buyuk Handikap  -  14 at", fs=9, color=WF_GRAY)

    # Dark bar "EN IYI ORAN GARANTISI"
    bog_bar_y = cy + 0.38
    add_rect(slide, cx + pad, bog_bar_y, card_w - 2*pad, 0.33,
             fill_color=WF_DARK, line_color=None)
    wf_tb(cx + pad + 0.1, bog_bar_y + 0.06, 3.5, 0.24,
          "EN IYI ORAN GARANTISI", fs=9, bold=True, color=WHITE)
    # BOG badge
    add_rect(slide, cx + card_w - pad - 0.7, bog_bar_y + 0.04, 0.6, 0.24,
             fill_color=ACCENT, line_color=None, rounded=True)
    wf_tb(cx + card_w - pad - 0.7, bog_bar_y + 0.06, 0.6, 0.2,
          "BOG", fs=9, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # Dashed box with big odds
    db4_y = bog_bar_y + 0.41
    wf_dashed_box(cx + pad, db4_y, card_w - 2*pad, 0.65)
    wf_tb(cx + pad + 0.1, db4_y + 0.06, 1.2, 0.38,
          "6.00", fs=22, bold=True, color=WF_DARK)
    wf_tb(cx + pad + 1.4, db4_y + 0.12, card_w - 2*pad - 1.4, 0.42,
          "SP yuksekse SP'den odenir", fs=10, color=WF_GRAY)

    # Ekstra plase pill
    pill_y = db4_y + 0.73
    add_rect(slide, cx + pad, pill_y, card_w - 2*pad, 0.3,
             fill_color=WF_LIGHT2, line_color=WF_GRAY,
             line_width_pt=0.5, rounded=True)
    wf_tb(cx + pad + 0.1, pill_y + 0.05, card_w - 2*pad - 0.1, 0.22,
          "Ekstra plase: 5 sira", fs=10, color=WF_DARK,
          align=PP_ALIGN.CENTER)

    # OYNA button
    oyna_y = pill_y + 0.38
    wf_dark_btn(cx + pad, oyna_y, card_w - 2*pad, 0.32, "OYNA", fs=10)

    # Two thin placeholder lines
    wf_thin_line(cx + pad, oyna_y + 0.4, card_w - 2*pad)
    wf_thin_line(cx + pad, oyna_y + 0.57, card_w - 2*pad)

    add_textbox(slide, cx, cy + card_h + 0.04, card_w, 0.28,
                "Sabit ihtimalliye ozgu deger. Amiral farklilasma mekanigi.",
                font_size=10, color=TEXT_MUTED)

    # ── "BiTalih Durusu" section below 2x2 grid ──
    section_y = ys[1] + card_h + 0.38

    # Thin separator
    add_rect(slide, 0.4, section_y - 0.06, 12.5, 0.02,
             fill_color=LINE_COLOR, line_color=None)

    add_textbox(slide, 0.4, section_y, 4.0, 0.3,
                "BiTalih durusu",
                font_size=14, bold=True, color=TEXT_DARK)

    # NOTE: y position is near bottom; compact layout
    durusu_bullets = [
        ("BOG ile farklilasma.",
         "Sabit ihtimalli yarisinin en guclu vaadi; rakipte yokken sen erken benimse."),
        ("Gunluk jeton = DAU + sadakat.",
         "ANBEAN Kulup'e gom, koleksiyon kartina bagla."),
        ("Kombine boost = margin.",
         "Gun ici kosular arasi, bacak arttikca artan carpan."),
        ("Event super boost = acquisition.",
         "Buyuk kosu, viral algi icin dusuk limitli."),
        ("Her boost'a guardrail.",
         "Maksimum stake, win-only, dar zaman penceresi, net ve kisa T&C."),
    ]

    # Use a single textbox with multiple paragraphs for compactness
    txBox = slide.shapes.add_textbox(
        Inches(0.4), Inches(section_y + 0.32),
        Inches(12.5), Inches(0.9)
    )
    tf2 = txBox.text_frame
    tf2.word_wrap = True

    for bi, (bold_t, normal_t) in enumerate(durusu_bullets):
        p = tf2.paragraphs[0] if bi == 0 else tf2.add_paragraph()
        p.space_before = Pt(2)
        p.alignment = PP_ALIGN.LEFT

        rb = p.add_run()
        rb.text = bold_t
        rb.font.name = FONT_NAME
        rb.font.size = Pt(11)
        rb.font.bold = True
        rb.font.color.rgb = TEXT_DARK

        rn = p.add_run()
        rn.text = "  " + normal_t
        rn.font.name = FONT_NAME
        rn.font.size = Pt(11)
        rn.font.color.rgb = TEXT_DARK

    return slide


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Building slide 1 ...")
    build_slide1(prs)

    print("Building slide 2 ...")
    build_slide2(prs)

    print("Building slide 3 ...")
    build_slide3(prs)

    print("Building slide 4 ...")
    build_slide4(prs)

    print("Building slide 5 ...")
    build_slide5(prs)

    print("Building slide 6 ...")
    build_slide6(prs)

    out = "/home/user/prediction-markets/BiTalih_OddBoost.pptx"
    prs.save(out)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
