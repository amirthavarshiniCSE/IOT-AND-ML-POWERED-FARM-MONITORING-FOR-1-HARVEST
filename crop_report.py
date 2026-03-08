import json
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---------- GROQ CONFIG ----------
client = Groq(api_key="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")

# ---------- LOAD JSON ----------
with open("recommendation.json", "r") as f:
    data = json.load(f)

# ---------- CALCULATE AVERAGES ----------
avg_temp = sum(x["Temperature"] for x in data) / len(data)
avg_moisture = sum(x["Moisture"] for x in data) / len(data)
avg_ph = sum(x["pH"] for x in data) / len(data)
avg_n = sum(x["Nitrogen"] for x in data) / len(data)
avg_p = sum(x["Phosphorous"] for x in data) / len(data)
avg_k = sum(x["Potassium"] for x in data) / len(data)

# ---------- ENGLISH PROMPT ----------
english_prompt = f"""
You are an agricultural expert.

Farm Summary:
Average Temperature: {avg_temp:.2f}
Average Soil Moisture: {avg_moisture:.2f}
Average Soil pH: {avg_ph:.2f}
Average Nitrogen: {avg_n:.2f}
Average Phosphorus: {avg_p:.2f}
Average Potassium: {avg_k:.2f}

Recommend the best crop for the next season.
Explain why the crop is suitable.
Suggest three alternative crops.
Give soil improvement advice.
"""

# ---------- GENERATE ENGLISH REPORT ----------
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": english_prompt}]
)

english_report = response.choices[0].message.content


# ---------- TAMIL PROMPT ----------
tamil_prompt = f"""
நீங்கள் ஒரு வேளாண்மை நிபுணர்.

பண்ணை தரவு:

வெப்பநிலை: {avg_temp:.2f}
மண் ஈரப்பதம்: {avg_moisture:.2f}
pH: {avg_ph:.2f}
நைட்ரஜன்: {avg_n:.2f}
பாஸ்பரஸ்: {avg_p:.2f}
பொட்டாசியம்: {avg_k:.2f}

அடுத்த பருவத்திற்கு ஏற்ற பயிரை பரிந்துரைக்கவும்.
"""

# ---------- GENERATE TAMIL REPORT ----------
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": tamil_prompt}]
)

tamil_report = response.choices[0].message.content


# ---------- GENERATE PDF ----------
file_name = "crop_recommendation_report.pdf"

c = canvas.Canvas(file_name, pagesize=A4)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap

# Register Tamil font
pdfmetrics.registerFont(TTFont('Tamil', 'NotoSansTamil-Regular.ttf'))

file_name = "crop_recommendation_report.pdf"
c = canvas.Canvas(file_name, pagesize=A4)

page_width = 595
margin = 70
text_width = 80   # characters per line (adjustable)

# Title
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(page_width/2, 800, "Smart Agriculture Crop Recommendation")

c.line(80, 790, 520, 790)

y = 760

# -------- ENGLISH SECTION --------
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(page_width/2, y, "English Report")
y -= 30

c.setFont("Helvetica", 11)

for paragraph in english_report.split("\n"):
    
    wrapped = textwrap.wrap(paragraph, text_width)

    for line in wrapped:
        c.drawString(margin, y, line)
        y -= 15

        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = 750

    y -= 5


# -------- TAMIL SECTION --------
y -= 20
c.setFont("Tamil", 14)
c.drawCentredString(page_width/2, y, "தமிழ் அறிக்கை")
y -= 30

c.setFont("Tamil", 11)

for paragraph in tamil_report.split("\n"):

    wrapped = textwrap.wrap(paragraph, text_width)

    for line in wrapped:
        c.drawCentredString(page_width/2, y, line)
        y -= 15

        if y < 100:
            c.showPage()
            c.setFont("Tamil", 11)
            y = 750

    y -= 5
c.save()

print("Styled PDF report generated successfully!")