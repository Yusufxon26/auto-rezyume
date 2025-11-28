from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_connection
import os
import re

app = Flask(__name__)
app.secret_key = "auto_rezyume_secret_key"

# Rasm fayllarini saqlash joyi
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


# Ro'yxatdan o'tish
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Parolni tekshirish (kamita 6 belgi, raqam, harf)
        if len(password) < 6 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            flash("Parol kamita 6 ta belgidan iborat bo'lishi, harf va raqam bo'lishi kerak!", "danger")
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password_hash))
                conn.commit()
                flash("Ro'yxatdan muvaffaqiyatli o'tdingiz! Endi tizimga kiring.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash("Bu email allaqachon ro'yxatdan o'tgan!", "warning")
            finally:
                cursor.close()
                conn.close()
    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
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
                flash(f"Salom, {user['name']}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Email yoki parol noto'g'ri!", "danger")
    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE user_id=%s", (session['user_id'],))
        resumes = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard.html', resumes=resumes, user=session['user_name'])
    return render_template('dashboard.html', resumes=[], user=session.get('user_name', ''))


# Yangi rezyume
@app.route('/create_resume', methods=['GET', 'POST'])
def create_resume():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        full_name = request.form['full_name']
        profession = request.form['profession']
        about = request.form['about']
        education = request.form['education']
        experience = request.form['experience']
        skills = request.form['skills']
        template = request.form['template']

        # Rasm yuklash
        photo_path = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                import uuid
                filename = str(uuid.uuid4()) + '_' + filename
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
            elif photo and photo.filename != '':
                flash("Faqat JPG, JPEG yoki PNG formatida rasm yuklashingiz mumkin!", "warning")
                return render_template('resume_form.html')

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO resumes (user_id, full_name, profession, about, education, experience, skills, template_name, photo_path)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (session['user_id'], full_name, profession, about, education, experience, skills, template, photo_path))
                conn.commit()
                cursor.close()
                conn.close()
                flash("Rezyume muvaffaqiyatli yaratildi!", "success")
                return redirect(url_for('dashboard'))
            except Exception as e:
                flash(f"Xato: {str(e)}", "danger")
    return render_template('resume_form.html')


# Rezyume ko'rish
@app.route('/resume/<int:id>')
def view_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM resumes WHERE id=%s", (id,))
        resume = cursor.fetchone()
        cursor.close()
        conn.close()
        if resume:
            return render_template('resume_view.html', resume=resume)
    return redirect(url_for('dashboard'))


# Rezyumeni tahrirlash
@app.route('/resume/<int:id>/edit', methods=['GET', 'POST'])
def edit_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Rezyumeni olish
    cursor.execute("SELECT * FROM resumes WHERE id=%s AND user_id=%s", (id, session['user_id']))
    resume = cursor.fetchone()
    
    if not resume:
        cursor.close()
        conn.close()
        return "Rezyume topilmadi", 404
    
    # POST – yangilash
    if request.method == 'POST':
        full_name = request.form['full_name']
        profession = request.form['profession']
        about = request.form['about']
        education = request.form['education']
        experience = request.form['experience']
        skills = request.form['skills']
        
        cursor.execute("""
            UPDATE resumes SET
                full_name=%s, profession=%s, about=%s, education=%s,
                experience=%s, skills=%s
            WHERE id=%s AND user_id=%s
        """, (full_name, profession, about, education, experience, skills, id, session['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash("Rezyume muvaffaqiyatli tahrirlandi!", "success")
        return redirect(url_for('dashboard'))
    
    cursor.close()
    conn.close()
    return render_template('resume_edit.html', resume=resume)


# Rezyumeni o'chirish
@app.route('/resume/<int:id>/delete', methods=['POST'])
def delete_resume(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Faqat o'ziga tegishli bo'lsa o'chirsin
    cursor.execute("DELETE FROM resumes WHERE id=%s AND user_id=%s", (id, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Rezyume o'chirildi!", "success")
    return redirect(url_for('dashboard'))


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
