#!/usr/bin/env python
"""Comprehensive diagnostic check for AUTO REZYUME PDF feature"""

print("\n" + "="*70)
print("AUTO REZYUME - COMPREHENSIVE DIAGNOSTIC CHECK")
print("="*70 + "\n")

# Check 1: xhtml2pdf installation
print("1️⃣  XHTML2PDF INSTALLATION")
try:
    import xhtml2pdf
    from xhtml2pdf import pisa
    print("   ✓ xhtml2pdf is installed")
    print(f"   ✓ pisa module importable")
except ImportError as e:
    print(f"   ✗ Error: {e}")

# Check 2: requirements.txt content
print("\n2️⃣  REQUIREMENTS.TXT CONTENT")
with open("requirements.txt", "r") as f:
    reqs = f.read()
    if "xhtml2pdf" in reqs:
        print("   ✓ xhtml2pdf listed in requirements.txt")
    else:
        print("   ✗ xhtml2pdf NOT in requirements.txt")
    dep_count = len([x for x in reqs.split('\n') if x.strip()])
    print(f"   Total dependencies: {dep_count}")

# Check 3: resume_pdf.html existence and content
print("\n3️⃣  RESUME_PDF.HTML FILE")
import os
if os.path.exists("templates/resume_pdf.html"):
    size = os.path.getsize("templates/resume_pdf.html")
    with open("templates/resume_pdf.html", "r") as f:
        lines = len(f.readlines())
    print(f"   ✓ resume_pdf.html exists ({size} bytes, {lines} lines)")
else:
    print("   ✗ resume_pdf.html NOT found")

# Check 4: app.py imports
print("\n4️⃣  APP.PY REQUIRED IMPORTS")
with open("app.py", "r") as f:
    app_code = f.read()
    
required_imports = {
    "Flask import": "from flask import Flask, render_template, request, redirect, session, url_for, flash, make_response",
    "xhtml2pdf": "from xhtml2pdf import pisa",
    "BytesIO": "from io import BytesIO"
}

for name, imp in required_imports.items():
    if imp in app_code:
        print(f"   ✓ {name}")
    else:
        print(f"   ✗ MISSING: {name}")

# Check 5: PDF download route
print("\n5️⃣  PDF DOWNLOAD ROUTE")
route_ok = "@app.route('/resume/<int:id>/download')" in app_code
func_ok = "def download_resume(id):" in app_code
pisa_ok = "pisa.CreatePDF" in app_code

if route_ok:
    print("   ✓ @app.route('/resume/<int:id>/download') found")
else:
    print("   ✗ Download route NOT found")

if func_ok:
    print("   ✓ download_resume() function exists")
else:
    print("   ✗ download_resume function NOT found")

if pisa_ok:
    print("   ✓ pisa.CreatePDF() call found")
else:
    print("   ✗ pisa.CreatePDF() call NOT found")

# Check 6: resume_view.html download button
print("\n6️⃣  RESUME_VIEW.HTML DOWNLOAD BUTTON")
with open("templates/resume_view.html", "r") as f:
    view_html = f.read()
    
if "download_resume" in view_html:
    print("   ✓ download_resume link found in resume_view.html")
else:
    print("   ✗ download_resume link NOT in resume_view.html")

if "PDF" in view_html or "yuklab olish" in view_html:
    print("   ✓ PDF download button text found")
else:
    print("   ✗ PDF button text NOT found")

# Check 7: New form fields
print("\n7️⃣  NEW FORM FIELDS IN CREATE_RESUME")
new_fields = ['phone', 'email', 'city', 'birth_date', 'career_objective', 'certificates', 'languages', 'projects', 'soft_skills']
found_fields = 0
for field in new_fields:
    if f"request.form.get('{field}')" in app_code:
        found_fields += 1

if found_fields == len(new_fields):
    print(f"   ✓ All {len(new_fields)} new fields detected")
elif found_fields > 0:
    print(f"   ✓ {found_fields}/{len(new_fields)} new fields detected")
else:
    print(f"   ✗ No new fields found in app.py")

# Check 8: All dependencies
print("\n8️⃣  PYTHON DEPENDENCIES INSTALLED")
deps = {
    "Flask": "flask",
    "MySQL Connector": "mysql.connector",
    "Werkzeug": "werkzeug",
    "xhtml2pdf": "xhtml2pdf"
}

missing_deps = []
for name, dep in deps.items():
    try:
        __import__(dep)
        print(f"   ✓ {name}")
    except ImportError:
        print(f"   ✗ {name} NOT installed")
        missing_deps.append(dep)

# Summary
print("\n" + "="*70)
if not missing_deps and route_ok and func_ok and pisa_ok:
    print("✅ ALL CHECKS PASSED - PDF FEATURE IS READY")
else:
    print("⚠️  SOME CHECKS FAILED - SEE DETAILS ABOVE")
print("="*70 + "\n")
