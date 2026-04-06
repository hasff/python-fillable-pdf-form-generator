from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

OUTPUT_FILE = "output/patient_admission_form.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4

COLOR_PRIMARY   = HexColor("#1B4F72")   # dark blue — headers, titles
COLOR_SECTION   = HexColor("#D6EAF8")   # light blue — section backgrounds
COLOR_FIELD_BG  = HexColor("#F8F9FA")   # near-white — text field backgrounds
COLOR_BORDER    = HexColor("#AEB6BF")   # gray — field borders
COLOR_TEXT      = HexColor("#1C1C1C")   # near-black — body text

MARGIN_LEFT     = 50
MARGIN_RIGHT    = PAGE_WIDTH - 50
CONTENT_WIDTH   = MARGIN_RIGHT - MARGIN_LEFT

FIELD_HEIGHT    = 20
LINE_HEIGHT     = 28


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def draw_section_header(c, y, title):
    """Draw a colored section header bar with title."""
    c.setFillColor(COLOR_PRIMARY)
    c.rect(MARGIN_LEFT, y - 6, CONTENT_WIDTH, 22, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN_LEFT + 8, y + 4, title.upper())
    return y - 20


def draw_label(c, x, y, text):
    """Draw a small gray label above a field."""
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 8)
    c.drawString(x, y, text)


def draw_text_field(c, x, y, width, name, label):
    """Draw a labeled text input field."""
    draw_label(c, x, y + 2, label)
    c.setFillColor(COLOR_FIELD_BG)
    c.setStrokeColor(COLOR_BORDER)
    c.rect(x, y - FIELD_HEIGHT, width, FIELD_HEIGHT, fill=1, stroke=1)
    c.acroForm.textfield(
        name=name,
        tooltip=label,
        x=x + 2,
        y=y - FIELD_HEIGHT + 2,
        width=width - 4,
        height=FIELD_HEIGHT - 4,
        borderColor=COLOR_BORDER,
        fillColor=COLOR_FIELD_BG,
        textColor=COLOR_TEXT,
        forceBorder=True,
        fontSize=9,
    )
    return y - FIELD_HEIGHT - 8


def draw_checkbox(c, x, y, name, label):
    """Draw a single labeled checkbox."""
    c.acroForm.checkbox(
        name=name,
        tooltip=label,
        x=x,
        y=y - 12,
        size=12,
        borderColor=COLOR_BORDER,
        fillColor=white,
        forceBorder=True,
    )
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(x + 16, y - 10, label)


def draw_horizontal_line(c, y):
    """Draw a light separator line."""
    c.setStrokeColor(COLOR_BORDER)
    c.setLineWidth(0.5)
    c.line(MARGIN_LEFT, y, MARGIN_RIGHT, y)


# ─────────────────────────────────────────────
# FORM SECTIONS
# ─────────────────────────────────────────────

def draw_header(c, y):
    """Clinic name, logo placeholder, form title."""
    # Logo placeholder
    # c.setFillColor(COLOR_SECTION)
    # c.rect(MARGIN_LEFT, y - 50, 60, 50, fill=1, stroke=0)
    # c.setFillColor(COLOR_PRIMARY)
    # c.setFont("Helvetica-Bold", 7)
    # c.drawCentredString(MARGIN_LEFT + 30, y - 28, "LOGO")

    c.drawImage("logo.png", MARGIN_LEFT, y - 50, width=60, height=50, preserveAspectRatio=True, mask='auto')

    # Clinic name
    c.setFillColor(COLOR_PRIMARY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN_LEFT + 70, y - 20, "HealthFirst Medical Centre")
    c.setFont("Helvetica", 9)
    c.setFillColor(COLOR_TEXT)
    c.drawString(MARGIN_LEFT + 70, y - 34, "123 Wellness Avenue, Lisbon, Portugal  |  +351 210 000 000  |  info@healthfirst.pt")

    # Form title
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(COLOR_PRIMARY)
    c.drawRightString(MARGIN_RIGHT, y - 20, "PATIENT ADMISSION FORM")
    c.setFont("Helvetica", 8)
    c.setFillColor(COLOR_TEXT)
    c.drawRightString(MARGIN_RIGHT, y - 55, "*Please complete all fields in block capitals")

    return y - 65


def draw_personal_info(c, y):
    """Section 1 — Personal Information."""
    y = draw_section_header(c, y, "1. Personal Information")

    # Row 1: First name / Last name / Date of birth
    col1 = MARGIN_LEFT
    col2 = MARGIN_LEFT + CONTENT_WIDTH * 0.38
    col3 = MARGIN_LEFT + CONTENT_WIDTH * 0.72

    w1 = CONTENT_WIDTH * 0.35
    w2 = CONTENT_WIDTH * 0.32
    w3 = CONTENT_WIDTH * 0.28

    draw_text_field(c, col1, y, w1, "first_name", "First Name *")
    draw_text_field(c, col2, y, w2, "last_name", "Last Name *")
    draw_text_field(c, col3, y, w3, "date_of_birth", "Date of Birth (DD/MM/YYYY) *")
    y -= LINE_HEIGHT + 4

    # Row 2: Gender / NIF / NHS Number
    draw_text_field(c, col1, y, w1, "gender", "Gender")
    draw_text_field(c, col2, y, w2, "national_id", "National ID / NIF *")
    draw_text_field(c, col3, y, w3, "nhs_number", "NHS / SNS Number")
    y -= LINE_HEIGHT + 4

    # Row 3: Address (full width)
    draw_text_field(c, MARGIN_LEFT, y, CONTENT_WIDTH, "address", "Home Address *")
    y -= LINE_HEIGHT + 4

    # Row 4: City / Postal Code / Country
    draw_text_field(c, col1, y, w1, "city", "City *")
    draw_text_field(c, col2, y, w2, "postal_code", "Postal Code *")
    draw_text_field(c, col3, y, w3, "country", "Country *")
    y -= LINE_HEIGHT + 4

    # Row 5: Phone / Email
    half = CONTENT_WIDTH * 0.48
    draw_text_field(c, MARGIN_LEFT, y, half, "phone", "Phone Number *")
    draw_text_field(c, MARGIN_LEFT + CONTENT_WIDTH * 0.52, y, half, "email", "Email Address")
    y -= LINE_HEIGHT + 4

    return y - 4


def draw_insurance_info(c, y):
    """Section 2 — Insurance Information."""
    y = draw_section_header(c, y, "2. Insurance Information")

    half = CONTENT_WIDTH * 0.48
    col2 = MARGIN_LEFT + CONTENT_WIDTH * 0.52

    draw_text_field(c, MARGIN_LEFT, y, half, "insurer_name", "Insurance Provider")
    draw_text_field(c, col2, y, half, "policy_number", "Policy Number")
    y -= LINE_HEIGHT + 4

    draw_text_field(c, MARGIN_LEFT, y, half, "gp_name", "GP / Family Doctor Name")
    draw_text_field(c, col2, y, half, "gp_phone", "GP Phone Number")
    y -= LINE_HEIGHT + 4

    return y - 4


def draw_medical_history(c, y):
    """Section 3 — Medical History (checkboxes + free text)."""
    y = draw_section_header(c, y, "3. Medical History")

    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN_LEFT, y, "Please tick any conditions that apply:")
    y -= 10

    # Checkboxes — 3 columns
    conditions = [
        ("cond_diabetes",       "Diabetes"),
        ("cond_hypertension",   "Hypertension"),
        ("cond_heart_disease",  "Heart Disease"),
        ("cond_asthma",         "Asthma / Respiratory"),
        ("cond_allergies",      "Allergies"),
        ("cond_cancer",         "Cancer (current or past)"),
        ("cond_mental_health",  "Mental Health Condition"),
        ("cond_epilepsy",       "Epilepsy"),
        ("cond_other",          "Other"),
    ]

    col_w = CONTENT_WIDTH / 3
    for i, (name, label) in enumerate(conditions):
        col = MARGIN_LEFT + (i % 3) * col_w
        row_y = y - (i // 3) * 18
        draw_checkbox(c, col, row_y, name, label)

    y -= (len(conditions) // 3 + 1) * 18 - 4

    # Current medications
    draw_text_field(c, MARGIN_LEFT, y, CONTENT_WIDTH, "medications", "Current Medications (name and dosage)")
    y -= LINE_HEIGHT + 4

    draw_text_field(c, MARGIN_LEFT, y, CONTENT_WIDTH, "allergies_detail", "Known Allergies (medication, food, other)")
    y -= LINE_HEIGHT + 4

    return y - 4


def draw_emergency_contact(c, y):
    """Section 4 — Emergency Contact."""
    y = draw_section_header(c, y, "4. Emergency Contact")

    col2 = MARGIN_LEFT + CONTENT_WIDTH * 0.52
    half = CONTENT_WIDTH * 0.48

    draw_text_field(c, MARGIN_LEFT, y, half, "emergency_name", "Full Name *")
    draw_text_field(c, col2, y, half, "emergency_relation", "Relationship to Patient *")
    y -= LINE_HEIGHT + 4

    draw_text_field(c, MARGIN_LEFT, y, half, "emergency_phone", "Phone Number *")
    draw_text_field(c, col2, y, half, "emergency_email", "Email Address")
    y -= LINE_HEIGHT + 4

    return y - 4


def draw_consent(c, y):
    """Section 5 — Consent & Signature."""
    y = draw_section_header(c, y, "5. Consent & Signature")

    # Consent checkboxes
    consents = [
        ("consent_treatment",   "I consent to the medical treatment and examinations deemed necessary by the clinical team."),
        ("consent_data",        "I consent to the processing of my personal and medical data in accordance with GDPR."),
        ("consent_share",       "I consent to sharing relevant medical information with other healthcare providers involved in my care."),
    ]

    y += 10

    for name, label in consents:
        draw_checkbox(c, MARGIN_LEFT, y, name, label)
        y -= 18

    y -= 8

    # Signature + date row
    sig_width = CONTENT_WIDTH * 0.55
    date_width = CONTENT_WIDTH * 0.35
    date_x = MARGIN_RIGHT - date_width

    draw_label(c, MARGIN_LEFT, y + 2, "Patient Signature *")
    c.setStrokeColor(COLOR_BORDER)
    c.setFillColor(COLOR_FIELD_BG)
    c.rect(MARGIN_LEFT, y - 36, sig_width, 36, fill=1, stroke=1)

    draw_text_field(c, date_x, y, date_width, "signature_date", "Date (DD/MM/YYYY) *")

    y -= 50

    return y


def draw_footer(c, y):
    """Page footer with form reference."""
    draw_horizontal_line(c, y)
    c.setFont("Helvetica", 7)
    c.setFillColor(COLOR_BORDER)
    c.drawString(MARGIN_LEFT, y - 12, "HealthFirst Medical Centre  |  Patient Admission Form  |  v1.0 — 2026")
    c.drawRightString(MARGIN_RIGHT, y - 12, "* Required fields")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def generate_form():
    import os
    os.makedirs("output", exist_ok=True)

    c = canvas.Canvas(OUTPUT_FILE, pagesize=A4)
    c.setTitle("Patient Admission Form — HealthFirst Medical Centre")
    c.setAuthor("HealthFirst Medical Centre")
    c.setSubject("Patient Admission Form")

    y = PAGE_HEIGHT - 32

    y = draw_header(c, y)

    y -= 15
    SPACE_BETWEEN_SECTIONS = 10
    y = draw_personal_info(c, y) - SPACE_BETWEEN_SECTIONS
    y = draw_insurance_info(c, y) - SPACE_BETWEEN_SECTIONS
    y = draw_medical_history(c, y) - SPACE_BETWEEN_SECTIONS
    y = draw_emergency_contact(c, y) - SPACE_BETWEEN_SECTIONS
    y = draw_consent(c, y) - SPACE_BETWEEN_SECTIONS

    draw_footer(c, y + 5)

    c.save()
    print(f"Form generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_form()
