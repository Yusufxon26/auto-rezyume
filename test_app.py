#!/usr/bin/env python
"""Test script for AUTO REZYUME application"""

import urllib.request
import urllib.error
import time

print("=" * 60)
print("AUTO REZYUME - APPLICATION TEST")
print("=" * 60)

# Wait for server
time.sleep(2)

routes = [
    ('/', 'Home Page'),
    ('/register', 'Register Form'),
    ('/login', 'Login Form'),
    ('/create_resume', 'Create Resume Form'),
]

print("\n📍 ROUTE ACCESSIBILITY TEST\n")
for route, name in routes:
    try:
        r = urllib.request.urlopen(f'http://127.0.0.1:5000{route}')
        print(f"✓ {name:25} → HTTP {r.status}")
    except urllib.error.HTTPError as e:
        print(f"• {name:25} → HTTP {e.code}")
    except Exception as e:
        print(f"✗ {name:25} → {type(e).__name__}")

# Test form fields
print("\n📋 NEW FORM FIELDS VERIFICATION\n")
new_fields = [
    'phone',
    'email', 
    'city',
    'birth_date',
    'career_objective',
    'certificates',
    'languages',
    'projects',
    'soft_skills'
]

try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/create_resume')
    html = r.read().decode('utf-8')
    
    found_count = 0
    for field in new_fields:
        if f'name="{field}"' in html:
            print(f"✓ {field:20}")
            found_count += 1
        else:
            print(f"✗ {field:20} NOT FOUND")
    
    print(f"\n  → {found_count}/{len(new_fields)} fields found")
    
except Exception as e:
    print(f"✗ Error checking form: {e}")

# Check PDF functionality
print("\n📄 PDF DOWNLOAD FUNCTIONALITY CHECK\n")
try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/create_resume')
    html = r.read().decode('utf-8')
    
    if 'resume_pdf.html' in html or 'download_resume' in html or 'PDF' in html:
        print("✓ PDF download reference found in create_resume page")
    else:
        print("✗ PDF download reference NOT found")
        
    # Check if xhtml2pdf is imported
    try:
        from xhtml2pdf import pisa
        print("✓ xhtml2pdf module is installed and importable")
    except ImportError:
        print("✗ xhtml2pdf module not found")
        
except Exception as e:
    print(f"✗ Error checking PDF: {e}")

# Check imports
print("\n🔧 DEPENDENCY CHECK\n")
required_modules = [
    ('flask', 'Flask'),
    ('mysql.connector', 'MySQL Connector'),
    ('werkzeug', 'Werkzeug'),
    ('xhtml2pdf', 'xhtml2pdf'),
]

for module, name in required_modules:
    try:
        __import__(module)
        print(f"✓ {name:20} installed")
    except ImportError:
        print(f"✗ {name:20} NOT installed")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE")
print("=" * 60)
