from flask import Flask, jsonify,render_template,request,flash,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,login_user,logout_user,LoginManager,current_user,login_manager
import sqlalchemy
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import ForeignKey, delete, select,Join, update

enroll_id=1
staff_id='KSSEM21'
app = Flask(__name__)
app.config['SECRET_KEY']='violin123'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/proctorbook'
db=SQLAlchemy(app)

session=db.session

@app.context_processor
def inject_zip():
    return dict(zip=zip)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Implement your user loading logic here
    return users.query.get(user_id)

class users(UserMixin,db.Model):
    user_name=db.Column(db.String(100),nullable=False)
    user_email=db.Column(db.String(100),nullable=False)
    user_password=db.Column(db.String(1000),nullable=False)
    user_type=db.Column(db.String,nullable=False)
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    def get_id(self):
        return self.user_id
    
class students(db.Model):
    student_usn=db.Column(db.String(10),nullable=False,primary_key=True)
    s_fname=db.Column(db.String(30),nullable=False)
    s_mname=db.Column(db.String(10),nullable=True)
    s_lname=db.Column(db.String(20),nullable=False)
    s_dob=db.Column(db.Date,nullable=False)
    s_address=db.Column(db.String(50),nullable=False)
    s_email=db.Column(db.String(20),nullable=False)
    s_pno=db.Column(db.String(10),nullable=False)
    s_gender=db.Column(db.String,nullable=False)
    s_fathername=db.Column(db.String(20),nullable=True)
    s_mothername=db.Column(db.String(20),nullable=True)
    s_guardian=db.Column(db.String(20),nullable=True)
    s_parentno=db.Column(db.String(10),nullable=False)
    s_proct_id=db.Column(db.Integer,nullable=False)
    s_branchid=db.Column(db.Integer,nullable=False)
    s_semid=db.Column(db.Integer,nullable=False)
    scheme_no=db.Column(db.Integer,nullable=False)

class schemes(db.Model):
    scheme_no=db.Column(db.Integer,nullable=False,primary_key=True)


class marks(db.Model):
    enroll_id=db.Column(db.Integer, nullable=False,primary_key=True)
    ia1_marks=db.Column(db.Float,nullable=True)
    ia2_marks=db.Column(db.Float,nullable=True)
    ia3_marks=db.Column(db.Float,nullable=True)
    int_marks=db.Column(db.Float,nullable=True)
    ext_marks=db.Column(db.Float,nullable=True)
    final_marks=db.Column(db.Float,nullable=True)
    

class attendance(db.Model):
    enroll_id = db.Column(db.Integer, nullable=False,primary_key=True) 
    ia1_at=db.Column(db.Float,nullable=True)
    ia2_at=db.Column(db.Float,nullable=True)
    ia3_at=db.Column(db.Float,nullable=True)
    total_at=db.Column(db.Float,nullable=True)

class sem(db.Model):
    sem_id=db.Column(db.Integer,nullable=False,primary_key=True)

class subject(db.Model):
    subject_id = db.Column(db.String(11),nullable=False,primary_key=True)
    subject_name = db.Column(db.String(30),nullable=False)
    branch_id = db.Column(db.Integer,nullable=False)
    sub_semid=db.Column(db.Integer,nullable=False)
    scheme=db.Column(db.Integer,nullable=False)

class branch(db.Model):
    branch_id = db.Column(db.Integer,nullable=False,primary_key=True)
    branch_name=db.Column(db.String(50),nullable=False)

class proctor(db.Model):
    proct_id = db.Column(db.Integer,nullable=False,primary_key=True)
    proct_name = db.Column(db.String(30),nullable=False)
    proct_branch = db.Column(db.Integer,nullable=False)
    proct_desig= db.Column(db.String(20),nullable=True)

@app.route("/")
def hello_world():
    return render_template('website.html')   
@app.route('/main_page')
def main_page():
    return render_template('main_page.html')
 

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        staff_id=request.form.get('staff_id')
        # Validate user input (optional, but recommended)
        if not username or not email or not password :
            flash('Please fill in all fields.', 'error')
            return render_template('signup.html') 
        proct=proctor.query.filter_by(proct_id=staff_id).first()
        if proct:
            user_type='p'
            print("hk")

        else:
            user_type='s'
            print("ht")

        # Check for existing user (optional, but recommended for preventing duplicates)
        existing_user = users.query.filter_by(user_email=email).first()
        if existing_user:
            print("npksdjakls")
            return render_template('signup.html')  # Stay on signup page

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)
        print(hashed_password)

        # Create a new user object
        new_user = users(user_name=username, user_email=email, user_password=hashed_password,user_type=user_type)

        # Add the new user to the database and commit changes
        print("hi")
        db.session.add(new_user)
        print("yes")
        db.session.commit()
        print("yass")
        return render_template('website.html')  # Redirect to login page after successful signup
       
    return render_template('signup.html')
@app.route("/submitdata", methods=['POST', 'GET'])
def submitdata():
    print("uo")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print("jidis")
        existing_user = users.query.filter_by(user_name=username).first()
        print(existing_user)  # Print the retrieved user object
        if existing_user and check_password_hash(existing_user.user_password, password):    
            print(existing_user.user_password)
            login_user(existing_user)
            print("ahoy")  # Log the user in using Flask-Login

            if(existing_user.user_type=='p'):
                return render_template("main_page.html",is_admin=True)
            else:  
                return redirect(url_for('main_page'))  # Redirect to the home page
        else:
            return('Invalid password', 'error')  # Display a flash message
    return render_template("website.html")  

@app.route("/sendusn", methods=['POST', 'GET'])
def sendusn():
    if request.method == 'POST':
        student_usn = request.form.get('studentusn')
        sem_no=request.form.get('semno')
        admin=request.form.get('admin')
        print("haaaaaaaaaaaaaaaaaaaa")
        subquery = select(enrollment.sub_id,
                  marks.ia1_marks, marks.ia2_marks, marks.ia3_marks, 
                  marks.int_marks, marks.ext_marks, marks.final_marks) \
          .join(enrollment, enrollment.enroll_id == marks.enroll_id) \
          .where(enrollment.s_usn == student_usn) \
          .where(enrollment.sem_no == sem_no)
        result=session.execute(subquery)
        mar=result.fetchall()
        print(result)

        student = students.query.filter_by(student_usn=student_usn).first()
        subquery = select(enrollment.sub_id,
                  attendance.ia1_at, attendance.ia2_at, attendance.ia3_at, 
                  attendance.total_at) \
          .join(enrollment, enrollment.enroll_id == attendance.enroll_id) \
          .where(enrollment.s_usn == student_usn) \
          .where(enrollment.sem_no == sem_no)
        result=session.execute(subquery)
        attu=result.fetchall()
        print(result)
        print("errodomo")
        print(admin)
        if(admin):
            if result :
                postdata=student
                printdata=mar
                publishdata=attu
                return render_template("main_page.html",postdata=postdata,printdata=printdata,publishdata=publishdata,is_admin=admin)
            else:
                postdata=student
                return render_template("main_page.html",postdata=postdata,is_admin=admin)
        else:
            if result :
                postdata=student
                printdata=mar
                publishdata=attu
                return render_template("main_page.html",postdata=postdata,printdata=printdata,publishdata=publishdata)
            else:
                postdata=student
                return render_template("main_page.html",postdata=postdata)
        
    return render_template("your_form_template.html")  # Render a form template for GET requests


@app.route("/adminpage",methods=['POST','GET'])
def adminpage():
     admin=request.form.get("admin")
     if admin:
        return render_template("test.html",is_admin=True)
     else:
        return render_template("test.html",is_admin=False)

@app.route("/proctid",methods=['POST','GET'])
def proctid():
    value=request.form.get("semfilter")
    print("next sem value")
    print(value)
    proct_id=request.form.get("proct_id")
    subquery=select(proctor.proct_id)\
                .where(proctor.proct_id==proct_id)
    result=session.execute(subquery)
    res=result.fetchall()
    print(res)
    if(res):
        print(value)
        stmt = select(students.student_usn).where(students.s_proct_id == res[0][0],students.s_semid==value)
        usn=session.execute(stmt)
        printvalue=usn.fetchall()
        values=printvalue
        print("lets go")
        return render_template('test.html',proct=True,printvalue=values,proctid=proct_id)
    else:
        return render_template('test.html',proct=False)

@app.route('/insertion',methods=['POST','GET'])
def insertion():

    return render_template("insert.html")



class enrollment(db.Model):
    enroll_id=db.Column(db.Integer,nullable=False,primary_key=True)
    s_usn=db.Column(db.String(10),nullable=False)
    sub_id=db.Column(db.String(11),nullable=False)
    sem_no=db.Column(db.Integer,nullable=False)

@app.route('/submitstudent', methods=['POST', 'GET'])
def submitstudent():
    if request.method == 'POST':
        # Extract student information
        student_usn = request.form.get('student_usn')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        date_of_birth = request.form.get('date_of_birth')
        address = request.form.get('address')
        phone_no = request.form.get('phone_no')
        email = request.form.get('email')
        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        guardian_name = request.form.get('guardian_name')
        branch = request.form.get('branch')
        sem_no = request.form.get('sem_no')
        parent_no = request.form.get('parent_no')
        proct_id = request.form.get('proct_id')
        scheme=request.form.get('schemes')
        # Validate user input (optional)
        # You can add validation logic here to ensure data integrity

        try:
            # Create new student object
            new_student = students(
            student_usn=student_usn,
            s_fname=first_name,
            s_mname=middle_name,
            s_lname=last_name,
            s_dob=date_of_birth,
            s_address=address,
            s_email=email,
            s_pno=phone_no,
            s_gender=gender,
            s_fathername=father_name,
            s_mothername=mother_name,
            s_guardian=guardian_name,
            s_parentno=parent_no,
            s_proct_id=proct_id,  # Assuming you have proctid defined elsewhere
            s_branchid=branch,
            s_semid=sem_no,
            scheme_no=scheme
            )
            print("jieho")
            # Add student to session and commit
            session.add(new_student)
            session.commit()
            # Fetch relevant subject IDs
            subject_ids = session.query(subject.subject_id).filter(
             subject.branch_id == branch,
             subject.sub_semid == sem_no,
             subject.scheme == scheme
                ).all()
            print('jai nandu baba')
            print(subject_ids)
                   
            for subject_id_tuple in subject_ids:
                subject_id = subject_id_tuple[0]  # Extract the first (and only) element of the tuple
                enrollment_new=enrollment(s_usn=student_usn,sub_id=subject_id,sem_no=sem_no)
                session.add(enrollment_new)
                print("jai ho nandu baba jai ho kulaja mata")
                session.commit()

            enrollment_ids = session.query(enrollment.enroll_id).filter(
                enrollment.s_usn==student_usn,
                enrollment.sem_no==sem_no
            ).all()
            print("vikartano arkayajeeshwaraaya namaha")
            print(enrollment_ids)  

            for enro in enrollment_ids:
                enroll=enro[0]
                marks_new=marks(enroll_id=enroll,ia1_marks=None,ia2_marks=None,ia3_marks=None,int_marks=None,ext_marks=None)
                session.add(marks_new)
                session.commit()
                attendance_new=attendance(enroll_id=enroll,ia1_at=0,ia2_at=0,ia3_at=0,total_at=0)
                session.add(attendance_new)
                session.commit()
            print("mitraya namaha")
            flash("student info added successfully")  
            return render_template("insert.html", success_message="Student added successfully!")

        except Exception as e:
            # Handle any database errors gracefully
            print(f"An error occurred: {e}")
            return render_template("insert.html", error_message="There was an error adding the student.")
    
@app.route("/back",methods=['POST','GET'])
def back():
    return render_template("test.html")

@app.route("/backupdate",methods=['POST','GET'])
def backupdate():
    pr=request.form.get("proc")
    print('ooiio')
    print(pr)
    return render_template("test.html",proctid=pr)
marks_rows=[]
sub_code=[]
@app.route("/usnformarks",methods=['POST','GET'])
def usnformarks():
    s_usn=request.form.get("index")
    proc=request.form.get("proct")
    print(s_usn)
    stmt=select(enrollment.enroll_id,enrollment.sub_id).filter(enrollment.s_usn==s_usn)
    details=session.execute(stmt)
    value=details.fetchall()
    print(value)
    nums=[]
    codes=[]
    for item in value:
        num,code=item
        nums.append(num)
        codes.append(code)
    m_row=[]
    for num in nums:
        stmt=select(marks.ia1_marks,marks.ia2_marks,marks.ia3_marks,marks.int_marks,marks.ext_marks,marks.final_marks).filter(marks.enroll_id==num)
        details=session.execute(stmt)
        m_row.append(details.fetchall())
    print(m_row)    
    if not m_row:
        return render_template("update.html",sub_code=codes,usn=s_usn)
    else:
        return render_template("update.html",marks_row=m_row,sub_codes=codes,usn=s_usn,proct=proc)
    
@app.route("/attendentry",methods=['POST','GET'])
def attendentry():
    print("testing")
    s_usn=request.form.get("inde")
    print("jjsoj")
    print(s_usn)
    stmt=select(enrollment.enroll_id,enrollment.sub_id).filter(enrollment.s_usn==s_usn)
    details=session.execute(stmt)
    value=details.fetchall()
    print(value)
    nums=[]
    codes=[]
    for item in value:
        num,code=item
        nums.append(num)
        codes.append(code)
    m_row=[]
    for num in nums:
        stmt=select(attendance.ia1_at,attendance.ia2_at,attendance.ia3_at,attendance.total_at).filter(attendance.enroll_id==num)
        details=session.execute(stmt)
        m_row.append(details.fetchall())
    print(m_row)
    if(m_row):
        print("ahppp")
        return render_template("attend.html",a_row=m_row,sub_codes=codes,usn=s_usn)
    else:
        return render_template("attend.html",sub_codes=codes,usn=s_usn)
    
@app.route('/aupdate',methods=['POST','GET'])
def aupdate():
    print("working bro")
    s_usn=request.form.get("s_usn")
    sub_id= request.form.get("sub_copy")
    marks1=request.form.get("marks00")
    marks2=request.form.get("marks01")
    marks3=request.form.get("marks02")
    if marks1=='':
        marks1=0
    else:
        marks1=float(marks1)
    if marks2=='':
        marks2=0 
    else:
        marks2=float(marks2)
    if marks3=='':
        marks3=0
    else:
        marks3=float(marks3)
    
    if marks1>0 and marks2>0 and marks3>0:
        marks4=marks1+marks2+marks3
        marks4=marks4/3
    print(marks4)
    print(s_usn)
    print(sub_id)
    print(marks1)
    print(marks2)    
    print(marks3)        
    print (type(marks1))  
    s=select(enrollment.enroll_id).filter(enrollment.s_usn==s_usn,enrollment.sub_id==sub_id)
    usn=session.execute(s)
    res=usn.fetchall()
    print("jinja")
    print(res[0][0])
    update_attendance=update(attendance).where(attendance.enroll_id==res[0][0]).values(ia1_at=marks1,ia2_at=marks2,ia3_at=marks3,total_at=marks4)
    session.execute(update_attendance)
    print("ay yo white")
    session.commit()
    print("lsjd")
    stmt=select(enrollment.enroll_id,enrollment.sub_id).filter(enrollment.s_usn==s_usn)
    details=session.execute(stmt)
    value=details.fetchall()
    print(value)
    nums=[]
    codes=[]
    for item in value:
        num,code=item
        nums.append(num)
        codes.append(code)
    m_row=[]
    for num in nums:
        stmt=select(attendance.ia1_at,attendance.ia2_at,attendance.ia3_at,attendance.total_at).filter(attendance.enroll_id==num)
        details=session.execute(stmt)
        m_row.append(details.fetchall())
    print(m_row)
    if(m_row):
        print("ahppp")
        return render_template("attend.html",a_row=m_row,sub_codes=codes,usn=s_usn)
    else:
        return render_template("attend.html",sub_codes=codes,usn=s_usn)

@app.route('/mupdate', methods=['POST'])
def update_marks():
    try:
        s_usn=request.form.get("s_usn")
        sub_id= request.form.get("sub_copy")
        marks1=request.form.get("marks00")
        marks2=request.form.get("marks01")
        marks3=request.form.get("marks02")
        marks4=request.form.get("marks03")
        marks5=request.form.get("marks04")
        print(type(marks1))
        if marks1=='':
            marks1=None
        else:
            marks1=float(marks1)
        if marks2=='':
            marks2=None
        else:
            marks2=float(marks2)
        if marks3=='':
            marks3=None
        else:
            marks3=float(marks3)
        if marks4=='':
            marks4=None
        else:
            marks4=float(marks4)
        if marks5=='':
            marks5=None
        else:
            marks5=float(marks5)
        print(s_usn)
        print(sub_id)
        print(marks1)
        print(marks2)    
        print(marks3)    
        print(marks4)    
        print(marks5)  
        print (type(marks1))  
        s=select(enrollment.enroll_id).filter(enrollment.s_usn==s_usn,enrollment.sub_id==sub_id)
        usn=session.execute(s)
        res=usn.fetchall()
        print("jinja")
        print(res)
        finmarks=0
        if(marks4>0)and(marks5>0)and(((marks1>0)and (marks2>0))or((marks2>0)and(marks3>0))or((marks1>0)and(marks3>0))):
            finmarks=marks4+marks5
        update_marks=update(marks).where(marks.enroll_id==res[0][0]).values(ia1_marks=marks1,ia2_marks=marks2,ia3_marks=marks3,int_marks=marks4,ext_marks=marks5,final_marks=finmarks)
        session.execute(update_marks)
        print("ay yo black")
        session.commit()
    except sqlalchemy.exc.OperationalError as e:
        if 'Marks validation failed' in str(e):  # Check for the custom error message
            # Extract specific validation errors from the message
            validation_errors = str(e).split(': ')[-1].strip()
            flash(f'Marks update failed: {validation_errors}', 'error')
        else:
            # Handle other potential errors (e.g., database connectivity issues)
            flash(f'An unexpected error occurred: {str(e)}', 'error')
    finally:
        session.close()  # Always close the session

        stmt=select(enrollment.enroll_id,enrollment.sub_id).filter(enrollment.s_usn==s_usn)
    details=session.execute(stmt)
    value=details.fetchall()
    print(value)
    nums=[]
    codes=[]
    for item in value:
        num,code=item
        nums.append(num)
        codes.append(code)
    m_row=[]
    for num in nums:
        stmt=select(marks.ia1_marks,marks.ia2_marks,marks.ia3_marks,marks.int_marks,marks.ext_marks,marks.final_marks).filter(marks.enroll_id==num)
        details=session.execute(stmt)
        m_row.append(details.fetchall())
    print(m_row)    
    if not m_row:
        return render_template("update.html",sub_code=codes,usn=s_usn)
    else:
        flash("marks updated successfully")
        return render_template("update.html",marks_row=m_row,sub_codes=codes,usn=s_usn)
    
    
@app.route("/deletestudent",methods=['POST','GET'])
def deletestudent():
    s_usn=request.form.get("deletes")
    print(s_usn)
    enroll=select(enrollment.enroll_id).filter(enrollment.s_usn==s_usn)
    lis=session.execute(enroll)
    en_id=lis.fetchall()
    print("istanbul")
    print(en_id)
    for id in en_id:
        print(id[0])
        enro=session.query(enrollment).filter(enrollment.enroll_id==id[0]).first()
        if enro is not None:
            session.delete(enro)
            session.commit()
        print("iam done with this")
    stud=session.query(students).filter(students.student_usn==s_usn).first()
    if stud is not None:
        session.delete(stud)
        session.commit()
        print("jai bholenath")
        return render_template("test.html",flag=True)
    else:
        return render_template("test.html")
    
@app.route("/home",methods=['POST','GET'])
def home():
    admin=request.form.get("admin")
    if(admin):
        return render_template("main_page.html",is_admin=True)
    else:
        
        return render_template("main_page.html",is_admin=False)

@app.route("/logout",methods=['POST','GET'])
def logout():
    return render_template("website.html")
app.run(debug=True)  




