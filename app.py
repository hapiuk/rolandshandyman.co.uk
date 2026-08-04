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
			"name": "Amira Shah",
			"rating": 5,
			"text": "Roland was amazing! He built both my sliding door wardrobe and Ottoman bed within 1.5 hours! He came on time and just got on with it! He does exactly as he says and does it efficiently! Will be using his services in the future as well! Highly recommend!",
			"source": "google"
		},
		{
			"name": "Arron Rankin",
			"rating": 5,
			"text": "I had Roland over to install some acoustic wall panels in our bedroom. Couldn't fault Roland and his work, we were really impressed with the overall job. Put shoe covers on, dust sheets, and cleaned and vacuumed all the mess — spotless when he finished. Communication was also very good, texts you when he's on his way and didn't let me down with dates he was coming to do the job. I'd definitely recommend.",
			"source": "google"
		},
		{
			"name": "Mohammad Zaheer",
			"rating": 5,
			"text": "First time I used Roland after seeing his reviews and he was right on time. Had 2 wardrobes and a dressing table assembled, and assembled quickly. A polite guy. Would definitely use him again.",
			"source": "google"
		},
		{
			"name": "Stephenie Ameh",
			"rating": 5,
			"text": "I can't recommend this guy enough. I needed locks fitted on 8 doors, a window blind frame fitted, a sideboard, and so many other bits done in my house. He did a fantastic job on every single one, zero fault. 3 curtain tracks reinforced as my kids keep tugging at them and now they're so sturdy. Super patient and stuck to the time and date we agreed on. I'd give 10 stars if this was an option.",
			"source": "google"
		},
		{
			"name": "Emily Lloyd",
			"rating": 5,
			"text": "I had a portable AC fitted and Roland was very kind and fitted the unit quickly. He was very friendly and very efficient, I would highly recommend him.",
			"source": "google"
		},
		{
			"name": "Blessing Omobude",
			"rating": 5,
			"text": "If you need furniture fixed, look no further. Roland is extremely careful with my pieces and made sure everything was sturdy and safe. He also left the workspace spotless when finished. Truly a professional who takes pride in their work — arrived right on time, had all the necessary tools, and knocked out several furniture repairs in no time. The quality of work is top-notch and the pricing was very fair.",
			"source": "google"
		},
		{
			"name": "Johnny Singh",
			"rating": 5,
			"text": "Roland is a very good tradesman. His work is outstanding. He has assembled all our wardrobes and beds at home. Will always be my go-to furniture assembly guy. Always takes care of my property, covers his shoes with shoe covers. Excellent prices as well.",
			"source": "google"
		},
		{
			"name": "Marcia Beckford",
			"rating": 5,
			"text": "I would highly recommend Rolands Handyman, he's very polite and professional. He assembled a few flat packs for me and I was very impressed with his work — perfectly neat.",
			"source": "google"
		},
		{
			"name": "Charley Charlie",
			"rating": 5,
			"text": "Very pleased with the work that was provided. Roland was very professional and got the job done very quickly. My new wardrobe and dresser look amazing. I will definitely be recommending.",
			"source": "google"
		},
		{
			"name": "Clair Platt",
			"rating": 5,
			"text": "Contacted Roland and he came the next day. Assembled 2 wardrobes for us and dismantled the old ones. Great job done, friendly and professional. Will be using again soon for a new shed. Highly recommend.",
			"source": "google"
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