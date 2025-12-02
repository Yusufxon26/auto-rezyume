from flask import Flask, render_template, request, redirect, session, url_for, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_connection
import os
import re
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "auto_rezyume_secret_key_2025"

# ⚠️ HAJM CHEKLOVLARINI OSHIRISH - Entity too large xatosini hal qilish
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['MAX_FORM_MEMORY_SIZE'] = 16 * 1024 * 1024  # 16MB

# Upload settings
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== HOME ====================
@app.route('/')
def home():
    return render_template('index.html')

# ==================== REGISTER ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Parol tekshiruvi
        if len(password) < 6 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            flash("Parol kamita 6 ta belgidan iborat, harf va raqam bo'lishi kerak!", "danger")
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        conn = get_connection()
        
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                             (name, email, password_hash))
                conn.commit()
                flash("Ro'yxatdan muvaffaqiyatli o'tdingiz!", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash("Bu email allaqachon ro'yxatdan o'tgan!", "warning")
            finally:
                cursor.close()
                conn.close()
    
    return render_template('register.html')


# ==================== LOGIN ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                flash(f"Xush kelibsiz, {user['name']}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Email yoki parol noto'g'ri!", "danger")
    
    return render_template('login.html')

# ==================== DASHBOARD ====================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE user_id=%s ORDER BY created_at DESC", 
                      (session['user_id'],))
        resumes = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard.html', resumes=resumes)
    
    return render_template('dashboard.html', resumes=[])


# ==================== CREATE RESUME ====================
@app.route('/create_resume', methods=['GET', 'POST'])
def create_resume():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Shaxsiy ma'lumotlar
        full_name = request.form.get('full_name')
        profession = request.form.get('profession')
        phone = request.form.get('phone')
        email = request.form.get('email')
        city = request.form.get('city')
        address = request.form.get('address')
        birth_date = request.form.get('birth_date')
        
        # Kasbiy
        career_objective = request.form.get('career_objective')
        
        # Ta'lim
        education_institution = request.form.get('education_institution')
        education_degree = request.form.get('education_degree')
        education_field = request.form.get('education_field')
        education_years = request.form.get('education_years')
        education_details = request.form.get('education_details')
        
        # Ish tajribasi
        work_company = request.form.get('work_company')
        work_position = request.form.get('work_position')
        work_years = request.form.get('work_years')
        work_duties = request.form.get('work_duties')
        
        # Ko'nikmalar
        technical_skills = request.form.get('technical_skills')
        soft_skills = request.form.get('soft_skills')
        
        # Qo'shimcha
        languages = request.form.get('languages')
        certificates = request.form.get('certificates')
        projects = request.form.get('projects')
        achievements = request.form.get('achievements')
        interests = request.form.get('interests')
        
        template = request.form.get('template', 'professional')
        
        # Rasm yuklash - Hajm tekshirish bilan
        photo_path = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename and allowed_file(photo.filename):
                # Fayl hajmini tekshirish
                photo.seek(0, os.SEEK_END)
                file_length = photo.tell()
                photo.seek(0)
                
                if file_length > 5 * 1024 * 1024:  # 5MB
                    flash("Rasm hajmi 5MB dan katta bo'lmasligi kerak!", "warning")
                    return render_template('resume_form.html')
                
                filename = secure_filename(photo.filename)
                filename = f"{uuid.uuid4()}_{filename}"
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo_path = f"uploads/{filename}"
        
        # Bazaga saqlash
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO resumes (
                        user_id, full_name, profession, phone, email, city, address, birth_date,
                        career_objective, education_institution, education_degree, education_field,
                        education_years, education_details, work_company, work_position, work_years,
                        work_duties, technical_skills, soft_skills, languages, certificates,
                        projects, achievements, interests, template_name, photo_path
                    ) VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                    )
                """, (
                    session['user_id'], full_name, profession, phone, email, city, address, birth_date,
                    career_objective, education_institution, education_degree, education_field,
                    education_years, education_details, work_company, work_position, work_years,
                    work_duties, technical_skills, soft_skills, languages, certificates,
                    projects, achievements, interests, template, photo_path
                ))
                conn.commit()
                flash("Rezyume muvaffaqiyatli yaratildi!", "success")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"Xato: {e}", "danger")
            finally:
                cursor.close()
                conn.close()
    
    return render_template('resume_form.html')


# ==================== VIEW RESUME ====================
@app.route('/resume/<int:id>')
def view_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE id=%s AND user_id=%s", (id, session['user_id']))
        resume = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if resume:
            return render_template('resume_view.html', resume=resume)
    
    flash("Rezyume topilmadi!", "warning")
    return redirect(url_for('dashboard'))

# ==================== DOWNLOAD PDF ====================
@app.route('/resume/<int:id>/download')
def download_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE id=%s AND user_id=%s", (id, session['user_id']))
        resume = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if resume:
            try:
                from xhtml2pdf import pisa
                from io import BytesIO
                
                html = render_template("resume_pdf.html", resume=resume)
                pdf = BytesIO()
                pisa.CreatePDF(BytesIO(html.encode("utf-8")), pdf)
                
                response = make_response(pdf.getvalue())
                response.headers["Content-Type"] = "application/pdf"
                response.headers["Content-Disposition"] = f"attachment; filename=CV_{resume['full_name']}.pdf"
                return response
            except Exception as e:
                flash(f"PDF yaratishda xato: {e}", "danger")
                return redirect(url_for('view_resume', id=id))
    
    return redirect(url_for('dashboard'))


# ==================== DELETE RESUME ====================
@app.route('/resume/<int:id>/delete', methods=['POST'])
def delete_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM resumes WHERE id=%s AND user_id=%s", (id, session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Rezyume o'chirildi!", "info")
    
    return redirect(url_for('dashboard'))

# ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
