from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import getpass
from pathlib import Path
import os
import random

app = Flask(__name__)

# ======================
# Email configuration
# ======================
SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = 587
SMTP_USER = "enquiries@rolandshandyman.co.uk"

SMTP_PASS = os.environ.get("SMTP_PASS")

if not SMTP_PASS:
	print("⚠️ SMTP_PASS not set – emails will fail")

# ======================
# Routes
# ======================

@app.route("/")
def home():
	# =========================
	# HERO IMAGE DUMP
	# =========================

	dump_path = os.path.join(app.static_folder, "img", "dump")
	images = []

	if os.path.exists(dump_path):
		images = [
			f"img/dump/{img}"
			for img in os.listdir(dump_path)
			if img.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
		]

	random.shuffle(images)

	# =========================
	# BEFORE & AFTER GALLERY
	# =========================

	bna_path = os.path.join(app.static_folder, "img", "bna")
	before_after = []

	if os.path.exists(bna_path):
		files = [
			f for f in os.listdir(bna_path)
			if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
		]

		before_map = {}
		after_map = {}

		for file in files:
			name, _ = os.path.splitext(file)
			key = name.lower()

			if key.startswith("before"):
				suffix = key.replace("before", "")
				before_map[suffix] = f"img/bna/{file}"
			elif key.startswith("after"):
				suffix = key.replace("after", "")
				after_map[suffix] = f"img/bna/{file}"

		for suffix in sorted(before_map.keys()):
			if suffix in after_map:
				before_after.append({
					"before": before_map[suffix],
					"after": after_map[suffix],
					"label": f"Job {suffix}" if suffix else "Completed work"
				})

	# =========================
	# DUMMY GOOGLE REVIEWS
	# =========================

	reviews = [
		{
			"name": "Sarah",
			"rating": 5,
			"text": "Brilliant. Quick and clean.",
			"gallery": before_after[0] if len(before_after) > 0 else None
		},
		{
			"name": "Mark",
			"rating": 5,
			"text": "Saved me time & money.",
			"gallery": before_after[1] if len(before_after) > 1 else None
		},
		{
			"name": "Aisha",
			"rating": 5,
			"text": "Highly recommended.",
			"gallery": None
		},
		{
			"name": "Aaron",
			"rating": 5,
			"text": "Stack test reviews",
			"gallery": None
		}
	]

	return render_template(
		"home.html",
		images=images,
		reviews=reviews
	)

@app.route("/contact", methods=["POST"])
def contact():
	print("📨 Contact form submitted")

	name = request.form.get("name", "").strip()
	email = request.form.get("email", "").strip()
	phone = request.form.get("phone", "").strip()
	location = request.form.get("location", "").strip()
	postcode = request.form.get("postcode", "").strip()
	message = request.form.get("message", "").strip()
	travel_cost = request.form.get("travel_cost", "").strip()

	if not name or not email or not message:
		print("❌ Missing required fields")
		return redirect(url_for("home", sent="0"))

	cost_line = travel_cost if travel_cost else "No additional travel cost"

	msg = EmailMessage()
	msg["Subject"] = "🔧 New website enquiry – Roland's Handyman"
	msg["From"] = SMTP_USER
	msg["To"] = SMTP_USER
	msg["Reply-To"] = email

	msg.set_content(f"""
New website enquiry

Name: {name}
Email: {email}
Phone: {phone}
Location: {location}
Postcode: {postcode}
Travel cost estimate: {cost_line}

Message:
{message}
""")

	html_content = f"""
		<!doctype html>
		<html>
		<head><meta charset="utf-8"></head>
		<body style="margin:0; padding:0; background:#0e0e0e; font-family:Arial, Helvetica, sans-serif; color:#f5f5f5;">

		<div style="max-width:600px; margin:0 auto; padding:24px;">
		<div style="background:#151515; border-radius:12px; overflow:hidden; box-shadow:0 10px 30px rgba(0,0,0,0.6);">

		<div style="background:linear-gradient(135deg,#ff8a00,#d46b00); padding:20px;">
		  <div style="display:flex; align-items:center; gap:14px;">
		    <img src="cid:logo" style="height:48px; border-radius:6px; margin-right:5%;">
		    <div>
		      <h1 style="margin:0; font-size:20px; color:#111;">New Website Enquiry</h1>
		      <p style="margin:4px 0 0; font-size:13px; color:#2b1600;">Roland's Handyman</p>
		    </div>
		  </div>
		</div>

		<div style="padding:20px;">
		<p>You’ve received a new enquiry from your website.</p>

		<table width="100%" cellpadding="6" cellspacing="0" style="font-size:14px;">
		<tr><td style="color:#ff8a00;width:140px;">Name</td><td>{name}</td></tr>
		<tr><td style="color:#ff8a00;">Email</td><td>{email}</td></tr>
		<tr><td style="color:#ff8a00;">Phone</td><td>{phone or "Not provided"}</td></tr>
		<tr><td style="color:#ff8a00;">Location</td><td>{location}</td></tr>
		<tr><td style="color:#ff8a00;">Postcode</td><td>{postcode}</td></tr>
		<tr><td style="color:#ff8a00;">Travel cost</td><td>{cost_line}</td></tr>
		</table>

		<div style="margin-top:18px;">
		  <div style="color:#ff8a00;">Message</div>
		  <div style="background:#1e1e1e; border-radius:8px; padding:12px; white-space:pre-line;">
		  	{message}
		  </div>
		</div>

		<div style="margin-top:20px; text-align:right;">
		  <a href="mailto:{email}" style="
		    padding:10px 16px;
		    background:#ff8a00;
		    color:#111;
		    text-decoration:none;
		    font-weight:bold;
		    border-radius:6px;">
		    Reply to customer
		  </a>
		</div>
		</div>

		<div style="background:#111; padding:14px; text-align:center; font-size:12px; color:#888;">
		  Sent from rolandshandyman.co.uk
		</div>

		</div>
		</div>
		</body>
		</html>
"""

	msg.add_alternative(html_content, subtype="html")

	logo_path = Path("static/img/rolandslogo.png")
	if logo_path.exists():
		with open(logo_path, "rb") as f:
			msg.get_payload()[1].add_related(
				f.read(),
				maintype="image",
				subtype="png",
				cid="logo"
			)

	try:
		with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
			server.starttls()
			server.login(SMTP_USER, SMTP_PASS)
			server.send_message(msg)

		print("✅ Email sent successfully")
		return redirect(url_for("home", sent="1"))

	except Exception as e:
		print("❌ Email failed:", e)
		return redirect(url_for("home", sent="0"))

# ======================
# Run app
# ======================
if __name__ == "__main__":
	app.run(debug=True)
