# Roland's Handyman

Official website for **Roland's Handyman**, showcasing professional handyman and property maintenance services.

Designed, developed and maintained by HapiTech.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (Jinja2 Templates)
- **WSGI Server:** Gunicorn
- **Reverse Proxy:** NGINX
- **Process Management:** systemd
- **SSL:** Let's Encrypt

---

## Project Structure

```
rolandshandyman/
├── app.py
├── wsgi.py
├── requirements.txt
├── templates/
├── static/
├── instance/
└── uploads/
```

---

## Local Development

```bash
python -m venv venv

# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

---

## Deployment

The production application is served using **Gunicorn** behind **NGINX** with SSL provided by **Let's Encrypt**.

---

## Copyright

© HapiTech.

All rights reserved.

This project was developed exclusively for Roland's Handyman by HapiTech.

The source code is proprietary and may not be copied, redistributed, modified or reused without written permission from HapiTech.

[![Built by HapiTech](https://img.shields.io/badge/Built%20by-HapiTech-2563eb?style=for-the-badge)](https://hapitech.dev)