from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,SelectField,TextAreaField,ValidationError
from wtforms.validators import DataRequired, NumberRange,Regexp,InputRequired,Length,EqualTo
from wtforms.fields.html5 import DateField
import datetime
from application.models import patientDetails,medicine_details,staffDetails

            
def my_length_check(form, field):
    if len(field.data)!=9:
        raise ValidationError('This field is 9 digits long')
    
def my_age_check(form, field):
    try:
        int(field.data)
        if len(field.data)>3 :
            raise ValidationError('Invalid age')
    except:
        raise ValidationError('Invalid age')
def my_date_check(form,field):
    if(field.data>datetime.datetime.today().date()):
        raise ValidationError("Admission date cannot be greater than today's date")
def validate_SSNID(form,field):
    try:
        int(field.data)
        print(field.data)
        patientSSNID= patientDetails.objects(patientSSN=field.data).first()
        if patientSSNID:
            status=patientSSNID['status']
            if(status):
                raise ValidationError("Already exists")
            else:
                raise ValidationError("Patient Exists and is discharged")
    except:
        raise ValidationError('Please enter integers only')
        

class LoginForm(FlaskForm): 
    userId   = StringField("STAFF ID", validators=[DataRequired()])
    password = PasswordField("PASSWORD", validators=[DataRequired()])
    submit   = SubmitField("LOGIN")

class Patient(FlaskForm):
    SSNID           =   StringField("Patient SSN ID", validators=[DataRequired(),my_length_check,validate_SSNID] )
    patientId       =   StringField("Patient ID")
    patientName     =   StringField("Patient Name", validators=[DataRequired()])
    patientAge      =   StringField("Age",validators=[DataRequired(),my_age_check])
    dateAdmission   =   DateField("Date of Admission",format='%Y-%m-%d',validators=[DataRequired(), my_date_check],default=datetime.datetime.today().date())
    bed             =   SelectField('Bed Type', coerce=int,choices=[(1, 'GENERAL'), (2, 'SEMI SHARING'), (3, 'SINGLE')],validators=[DataRequired()])
    patientAddress  =   TextAreaField("Patient Address",validators=[DataRequired()])
    city            =   StringField("City", validators=[DataRequired()])
    state           =   StringField("State", validators=[DataRequired()])
    status          =   BooleanField("ACTIVE/DISCHARGED")
    submit          =   SubmitField("Add Patient")
    reset           =   SubmitField("Reset")
    getDetails      =   SubmitField("GET")
    updatePatient   =   SubmitField("Update Patient")
    deletePatient   =   SubmitField("Delete Patient")
    issueMedicine   =   SubmitField("Issue Medicines")
    issueDiagnosis  =   SubmitField("Issue Diagnosis")
    getBill         =   SubmitField("Confirm")
    printBill       =   SubmitField("Print",render_kw={"onclick":"window.print()"})

class PatientUpdate(FlaskForm):
    SSNID           =   StringField("Patient SSN ID")
    patientId       =   StringField("Patient ID",validators=[my_length_check])
    patientName     =   StringField("Patient Name", validators=[DataRequired()])
    patientAge      =   StringField("Age",validators=[DataRequired(),my_age_check])
    dateAdmission   =   DateField("Date of Admission",format='%Y-%m-%d',validators=[DataRequired(), my_date_check],default=datetime.datetime.today().date())
    bed             =   SelectField('Bed Type', coerce=int,choices=[(1, 'GENERAL'), (2, 'SEMI SHARING'), (3, 'SINGLE')],validators=[DataRequired()])
    patientAddress  =   TextAreaField("Patient Address",validators=[DataRequired()])
    city            =   StringField("City", validators=[DataRequired()])
    state           =   StringField("State", validators=[DataRequired()])
    status          =   BooleanField("ACTIVE/DISCHARGED")
    submit          =   SubmitField("Add Patient")
    getDetails      =   SubmitField("GET")
    updatePatient   =   SubmitField("Update Patient")
    deletePatient   =   SubmitField("Delete Patient")
    issueMedicine   =   SubmitField("Issue Medicines")
    issueDiagnosis  =   SubmitField("Issue Diagnosis")
    getBill         =   SubmitField("Confirm")


    

class Medicine_form(FlaskForm):
    medicineId      =   StringField("Medicine Id")
    medicineName    =   StringField("Medicine Name",validators=[DataRequired()])
    medicineQty     =   StringField(" Quantity",validators=[DataRequired()])     
    medicineRate    =   StringField(" Rate")
    medicineAmount  =   StringField(" Amount")
    addMedicine     =   SubmitField("Add")
    update          =   SubmitField("Update")
    getRate         =   SubmitField("Get")

class Test_form(FlaskForm):
    testId      =   StringField("Test Id",id=1)
    testName    =   SelectField("Test Name",id=1,coerce=int,validators=[DataRequired()])
    amount      =   StringField(" Amount",id=1)
    addTest     =   SubmitField("Add",id=1)
    update      =   SubmitField("Update")
    getRate     =   SubmitField("Get",id=1)



def validate_SSNID_staff(form,field):
    staffSSNID= staffDetails.objects(staffSSN=int(field.data))
    if(staffSSNID):
        raise ValidationError("Already exists")
    
def my_staffid_check(form,field):
    item    =   staffDetails.objects(staffId__iexact=field.data).first()
    if(item):
        raise ValidationError("Already taken")


class StaffRegister(FlaskForm):
    staffSSNID    =   StringField("Staff SSN ID",validators=[DataRequired(),my_length_check,validate_SSNID_staff])
    staffId       =   StringField("Staff Login ID",validators=[InputRequired(),my_staffid_check,Length(min=8,max=35,message="Id must be of size > 8 and <35"),Regexp('^[a-zA-Z0-9_]{8,35}', message="Username must contain only letters numbers or underscore")])
    staffName     =   StringField("Staff Name", validators=[DataRequired()])
    staffPhone    =   StringField("Phone",validators=[DataRequired(),Regexp('^[0-9]{10}', message="Must only contain integers")])
    staffDoj      =   DateField("Date of Admission",format='%Y-%m-%d',validators=[DataRequired(), my_date_check],default=datetime.datetime.today().date())
    staffDob      =   DateField("Date of birth",format='%Y-%m-%d',validators=[DataRequired(), my_date_check])
    staffDept     =   SelectField('Staff Department',choices=[('reception', 'reception'), ('pharmacy', 'pharmacy'), ('diagnosis', 'diagnosis')],validators=[DataRequired()])
    staffAddress   =  TextAreaField("Staff Address",validators=[DataRequired()])
    staffPassword   =   PasswordField("Password", validators=[InputRequired(), Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', message="Password must contain 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character"),EqualTo('confirm', message='Passwords must match')])
    confirm         = PasswordField('Repeat Password')
    staffRegister   =   SubmitField("Register Staff")
    
