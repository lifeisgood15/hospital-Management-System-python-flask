from application import app,db
from flask import render_template, request, json, Response, redirect, flash,session,url_for
from application.forms import LoginForm,Patient,Medicine_form,Test_form,PatientUpdate, StaffRegister
from application.models import staffDetails, patientDetails,patient_med,medicine_details,patient_test,test_details,userstore
from datetime import datetime,time,date


#-----------------------------------------staffregister----------------------------------------------------------
@app.route("/register_staff",methods=["GET","POST"])
def register_staff():
    '''if(not session.get('dept')=='admin'):
        flash(" Only admin can add new staff members","danger")'''
    form   =   StaffRegister()
    if form.validate_on_submit():
                print("in staff submit")
                staffSSNID      =   int(form.staffSSNID.data)
                staffId         =   form.staffId.data
                staffName       =   form.staffName.data
                staffPhone      =   int(form.staffPhone.data)
                staffAddress    =   form.staffAddress.data
                dateJoining     =   datetime.combine(form.staffDoj.data, time())
                dateBirth       =   datetime.combine(form.staffDob.data, time())
                staffDept       =   form.staffDept.data
                staffPassword   =   form.staffPassword.data 

                staff =   staffDetails(staffSSN=staffSSNID,staffName=staffName,staffDoj = dateJoining ,staffDob=dateBirth,staffAddress=staffAddress ,staffId=staffId,staffDept=staffDept,staffPhone=staffPhone)
                staff.save()
                user = userstore(staffId=staffId)
                user.set_password(staffPassword) 
                user.save()
                message =   "Staff Registered with id :"+str(user.staffId)
                flash(message,"success")
                return redirect(url_for('register_staff'))
    return render_template("register_staff.html", title="New Staff", form=form, admin=True )

@app.route("/viewStaff",methods=['GET', 'POST'])
def viewStaff():
    all_staff = staffDetails.objects().order_by("staffSSN")
    return render_template("viewStaff.html", all_staff=all_staff , viewStaff = True,title="View All Staff")



#-----------------------------------------staffregister----------------------------------------------------------

#-----------------------------------------LOGIN/LOGOUT-----------------------------------------------------------

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if session.get('userId'):
        flash(f"{session['userId']}, you are already logged in!", "success")
        if (session['dept']=='reception'):
                return redirect(url_for('reception'))
        elif(session['dept']=='pharmacy'):
                return redirect(url_for('pharmacyDetails'))
        elif(session['dept']=='admin'):
                return redirect(url_for('register_staff'))
        else:
                return redirect(url_for('diagnostics'))
    form = LoginForm()
    logout_url=url_for('logout')
    if form.validate_on_submit():
        login_id    =   form.userId.data
        password    =   form.password.data 
        user        =   userstore.objects(staffId=login_id).first()

        if user and user.get_password(password):
            item    =   staffDetails.objects(staffId=login_id).first()
            print(login_id,item['staffId'])
            flash(f"{item['staffName']}, you are successfully logged in!", "success")
            session['userId']=item['staffId']
            session['dept']=item['staffDept']
            # user['timestamp']   =   datetime.now().isoformat()
            user.save()
            if (item['staffDept']=='reception'):
                return redirect(url_for('reception'))
            elif(item['staffDept']=='pharmacy'):
                return redirect(url_for('pharmacyDetails'))
            elif(item['staffDept']=='admin'):
                return redirect(url_for('register_staff'))
            else:
                return redirect(url_for('diagnostics'))

        else:
            flash("Sorry, invalid credentials.","danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/logout")
def logout():
    flash("You are successfully logged out!", "success")
    session['userId']=False 
    session['dept']=False
    session.clear()
    return redirect(url_for('login'))
#-----------------------------------------LOGIN/LOGOUT-----------------------------------------------------------
#------------------------------------------Functions-------------------------------------------------------------
def disable_fields(form,d):
    form.patientName.render_kw      =   {'disabled': d}
    form.patientAddress.render_kw   =   {'disabled': d}
    form.dateAdmission.render_kw    =   {'disabled': d}
    form.bed.render_kw              =   {'disabled': d}
    form.patientAge.render_kw       =   {'disabled': d}
    form.city.render_kw             =   {'disabled': d}
    form.state.render_kw            =   {'disabled': d}
    
def display_fields(form,item):
    print(type(item['dateAdmission']),item['dateAdmission'],item['bed'],item['patientAge'])
    form.patientId.data         =   item['patientId']
    form.patientName.data       =   item['patientName']
    form.patientAddress.data    =   item['patientAddress']    
    form.dateAdmission.data     =   item['dateAdmission'].date()
    form.bed.data               =   item['bed']
    form.patientAge.object_data =   str(item['patientAge'])
    form.city.data              =   item['city']
    form.state.data             =   item['state'] 

def readonly_fields(form,d):
    form.patientName.render_kw      =   {'readonly': d}
    form.patientAddress.render_kw   =   {'readonly': d}
    form.dateAdmission.render_kw    =   {'readonly': d}
    form.bed.render_kw              =   {'readonly': d}
    form.patientAge.render_kw       =   {'readonly': d}
    form.city.render_kw             =   {'readonly': d}
    form.state.render_kw            =   {'readonly': d}

def update_medicines_field(p_id):
    display_pmed={}
    all_patient_med=[]
    mbill=0
    meds_already    =   patient_med.objects(patientId=p_id,paid=False).order_by("-medId")
    for med in meds_already:
        display_pmed={}
        obj_med_detail = medicine_details.objects(medId=med['medId']).first()
        display_pmed['medName']=obj_med_detail['medName']
        display_pmed['qty']=med['pmed_qty']
        display_pmed['rate']=str(obj_med_detail['rate'])
        display_pmed['amount']=obj_med_detail.get_cost(med['pmed_qty'])
        mbill+=obj_med_detail.get_cost(med['pmed_qty'])
        all_patient_med.append(display_pmed)
        print(all_patient_med)
    return(all_patient_med,mbill)

def update_diagnosis_field(p_id):
    display_pdia={}
    print("in print details",p_id)
    all_patient_pdia=[]
    tbill=0
    test_already    =   patient_test.objects(patientId=p_id,paid=False).order_by("-testId")
    for test in test_already:
        display_pdia={}
        obj_dia_detail = test_details.objects(testId=test['testId']).first()
        display_pdia['testName']=obj_dia_detail['testName']
        display_pdia['amount']=obj_dia_detail['rate']
        tbill+=obj_dia_detail['rate']
        all_patient_pdia.append(display_pdia)
    print(all_patient_pdia,test_already.first())
    return(all_patient_pdia,tbill)

def is_pid(p_id):
    if(p_id==''):
        return(False)
    else:
        return(int(p_id))

def get_room_cost(item):
    rate={1:2000,2:4000,3:8000} 
    room={}
    now = datetime.now().date()
    days=now-item['dateAdmission'].date()
    room['days']=int(days.days)+1
    room['cost']=room['days']*rate[item['bed']]
    return(room)

#------------------------------------------Functions-------------------------------------------------------------

#----------------------------------------------RECEPTION---------------------------------------------------------
@app.route("/reception")
def reception():
        return render_template("reception.html", title="Registration/Admission desk executive ", reception=True)

@app.route("/newPatient",methods=['GET', 'POST'])
def newPatient():
    form   =   Patient()
    if form.validate_on_submit():
                print("in submit")
                SSNID           =   int(form.SSNID.data)
                patientName     =   form.patientName.data
                patientAge      =   int(form.patientAge.data)
                patientAddress  =   form.patientAddress.data
                dateAdmission   =   form.dateAdmission.data
                bed             =   form.bed.data
                city            =   form.city.data
                state           =   form.state.data
                dateAdmission   =   datetime.combine(dateAdmission, time())
                
                patient =   patientDetails(patientSSN=SSNID,patientName=patientName,patientAge = patientAge ,patientAddress=patientAddress ,dateAdmission=dateAdmission,bed=bed,city=city,status=1,state=state )
                patient.generatePatientId()   
                
                patient.save()
                message =   "Patient Registered with id :"+str(patient.patientId)
                flash(message,"success")
                return redirect(url_for('newPatient'))
    return render_template("newPatient.html", title="New Patient", form=form, patient=True )


@app.route("/updatePatient",methods=['GET', 'POST'])
def updatePatient():
    form   =   PatientUpdate()
    disable_fields(form,'disable')
    
    form.updatePatient.render_kw      =   {'disabled': 'disabled'}
    if(form.getDetails.data):
        form.dateAdmission.data     =   None
        form.bed.data               =   None
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        
        if(item):
                form    =   Patient(obj=item)

                disable_fields(form,False)

                form.patientId.render_kw    =   {'readonly': 'readonly'}
                form.updatePatient.render_kw      =   {'disabled': False}

        else:
                flash("Patient doesnot exist","danger")
                return redirect(url_for('updatePatient'))
        
    if (form.updatePatient.data):
        patient_id  =   form.patientId.data
        message =   ''
        if form.validate():
            item    =   patientDetails.objects.get(patientId=patient_id)
            item['patientName']     =   form.patientName.data
            item['patientAge']      =   int(form.patientAge.data)
            if(item['status']==False):
                if(item['dateAdmission']>=datetime.combine(form.dateAdmission.data, time())):
                    flash("Discharged Patient's new admission date cannot be the same or less than previous date of admission","danger")
                    return redirect(url_for('updatePatient'))

                item['status'] =True 
                message+=" Patient's status updated to active"

            item['dateAdmission']   =   datetime.combine(form.dateAdmission.data, time())
            item['state']           =   form.state.data
            item['city']            =   form.city.data
            item['patientAddress']  =   form.patientAddress.data
            item['bed']             =   form.bed.data
            
            item.save()
            updated    =   patientDetails.objects(patientId=patient_id).first()
            display_fields(form,updated)
            message="Patient "+str(item['patientId'])+" updated.  "+ message
            flash(message,"success") 
        else:
            print(form.validate())
            flash("Sorry, something went wrong","danger")
    return render_template("alterPatient.html", title="Update Patient", form=form, update=True )

@app.route("/delPatient",methods=['GET', 'POST'])
def delPatient():
    form   =   Patient()
    disable_fields(form,'disable')
    form.deletePatient.render_kw      =   {'disabled': 'disabled'}
    if(form.getDetails.data):
        form.dateAdmission.data     =   None
        form.bed.data               =   None
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        
        if(item):
                form    =   Patient(obj=item)
                disable_fields(form,'disable')

                form.patientId.render_kw    =   {'readonly': 'readonly'}
                form.deletePatient.render_kw      =   {'disabled': False}

        else:
                flash("Patient doesnot exist","danger")
                return redirect(url_for('delPatient'))
    if (form.deletePatient.data):
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        
        if(item):
            patient_id  =   form.patientId.data
            patientDetails.objects(patientId=form.patientId.data).delete()
            meds_already    =   patient_med.objects(patientId=patient_id).order_by("-medId") 
            message="Patient Deleted "
            if(meds_already):
                meds_already.delete()
                
            test_already    =   patient_test.objects(patientId=patient_id).order_by("-testId")
            if(test_already):
                test_already.delete()

        flash(message,"success")
        return redirect(url_for('delPatient'))    
    return render_template("alterPatient.html", title="Delete Patient", form=form, delete=True )


@app.route("/searchPatient",methods=['GET', 'POST'])
def searchPatient():
    form   =   Patient()
    form.dateAdmission.data     =   None
    form.bed.data               =   None
    disable_fields(form,'disable')
    if(form.getDetails.data):
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        if(item):
                form    =   Patient(obj=item)
                form.patientId.render_kw    =   {'disabled': 'disabled'}
                if(item['status']==False):
                    print("Patient has been discharged","danger")
                    return redirect(url_for('searchPatient'))
                disable_fields(form,'disable')
                form.patientId.render_kw    =   {'readonly': 'readonly'}
        else:
                flash("Patient doesnot exist","danger")
                return redirect(url_for('searchPatient'))
    return render_template("alterPatient.html", title="Search Patient", form=form, search=True )

@app.route("/viewAll",methods=['GET', 'POST'])
def viewAll():
    all_patients = patientDetails.objects(status=True).order_by("-patientId")
    return render_template("viewAll.html", all_patients=all_patients , viewAll = True,title="View All Patients")


@app.route("/patientBill",methods=['GET', 'POST'])
def patientbill():
    form = Patient() #to get patient id and display patient details
    form.dateAdmission.data     =   None
    form.bed.data               =   None
    disable_fields(form,'disable')
    datenow =   datetime.now().isoformat()
    #-----------------------------To display all bill information----------------------------
    if(form.getDetails.data):
        if(form.patientId.data==''):
            flash("Enter patient Id ","danger")
            return redirect(url_for('patientBill'))
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        
        if(item):
                if(item['status']==False):
                    flash("Patient has been discharged","danger")
                    return redirect(url_for('patientbill'))
                form    =   Patient(obj=item)
                form.patientId.render_kw    =   {'readonly': 'readonly'}
                disable_fields(form,'disable')



                all_patient_med,mbill           =   update_medicines_field(item['patientId'])
                all_patient_diagnosis,tbill     =   update_diagnosis_field(item['patientId'])
                room                            =   get_room_cost(item)
                totalCost                       =   room['cost']+mbill+tbill


                return render_template("patientBill.html", patientBill =True, title="Patient Bill",form=form,medicines=all_patient_med,diagnosis=all_patient_diagnosis,flag=1,room=room,mbill=mbill,tbill=tbill,totalCost=totalCost,datenow=datenow)
        else:
            flash("Patient not found","danger")
            return redirect(url_for('patientbill'))
    #---------update status of patient -------------     
    if(form.getBill.data):
        if(is_pid(form.patientId.data)):
        
            item=patientDetails.objects(patientId=form.patientId.data).first()
            if(item['status']==False):
                message="Patient with id :"+str(item['patientId'])+' has checked out already.'
                flash(message,"danger")
                return render_template("patientBill.html", patientBill = True,title="Patient Bill",form=form,flag=0,datenow=datenow)

            item['status']=False
            item.save()
            pmed = patient_med.objects(patientId=form.patientId.data,paid=False).update(set__paid=True)
            ptest = patient_test.objects(patientId=form.patientId.data,paid=False).update(set__paid=True)
            print(ptest)
            
            message="Patient with id : "+str(item['patientId'])+' is now discharged.'
            flash(message,"success")
            return render_template("patientBill.html", patientBill = True,title="Patient Bill",form=form,flag=0,datenow=datenow)
        
    return render_template("patientBill.html", patientBill = True,title="Patient Bill",form=form,flag=0,datenow=datenow)

#----------------------------------------PHARMACY--------------------------------------------------------
@app.route("/pharmacyDetails",methods=['GET', 'POST'])
def pharmacyDetails():
    form = Patient() #to get patient id and display patient details
    form.dateAdmission.data     =   None
    form.bed.data               =   None
    disable_fields(form,'disable')
    session['med_patient']=None

    #---------------To display patient information---------
    if(form.getDetails.data):
        if(form.patientId.data==''):
            flash("Please enter patient Id ","danger")
            return redirect(url_for('pharmacyDetails'))
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        if(item and item['status']):
                form                        =   Patient(obj=item)
                form.patientId.render_kw    =   {'readonly': 'readonly'}
                disable_fields(form,'disable')
                all_patient_med,mbill       =   update_medicines_field(item['patientId'])

                return render_template("pharmacy.html", pharmacy = True,title="Pharmacy",form=form,medicines=all_patient_med,flag=1)
        else:
            flash("Patient doesnot exist or is discharged","danger")
            return redirect(url_for('pharmacyDetails'))
    
    if(form.issueMedicine.data):
        session['med_patient']  =   int(form.patientId.data)
        return redirect(url_for('issueMed'))
    return render_template("pharmacy.html", pharmacy = True,title="Pharmacy",form=form)

@app.route("/issueMed",methods=['GET', 'POST'])
def issueMed():
    try:
        p_id    =   session['med_patient']  #from previous page
        dept    =   session['dept']
    except:
        return redirect(url_for('pharmacyDetails'))
    if(p_id==None and session['dept']=='pharmacy'):
        flash("Please enter patient id","danger")
        return redirect(url_for('pharmacyDetails'))

    all_patient_med,mbill   =   update_medicines_field(p_id)
    patient_details         =   patientDetails.objects(patientId=p_id).first()
    form_med                =   Medicine_form() 
    form_med.medicineRate.render_kw    =   {'readonly': 'readonly'}
    form_med.medicineAmount.render_kw    =   {'readonly': 'readonly'}

    if (form_med.update.data or form_med.addMedicine.data):
        if(form_med.validate_on_submit()):
            med = medicine_details.objects(medName__icontains=form_med.medicineName.data).first()
            
            if(med==None):
                flash("Out of stock","danger")
                return render_template("issueMed.html", pharmacy = True,title="Pharmacy",form_med=form_med,valid=1,medicines=all_patient_med, data=patient_details)
            else:    
                qty=int(form_med.medicineQty.data)
                if(qty>med['qty']):
                    message="Only "+str(med['qty'])+" medicines available for "+str(med['medName'])
                    flash(message,"danger")
                else:
                    med['qty']-=qty
                    med.save()  #update medicine database
                    #update patient-medicine database
                    if(patient_med.objects(patientId=p_id,medId=med['medId']).first()):
                        item=patient_med.objects(patientId=p_id,medId=med['medId']).first()
                        item['pmed_qty']+=qty 
                        item.save()
                    else:
                        pmed=patient_med(patientId=p_id,medId=med['medId'],pmed_qty=qty)
                        pmed.save()

                    flash("Medicine added","success")
                    if(form_med.update.data):
                        session['med_patient']=None 
                        return redirect(url_for('pharmacyDetails'))
                    else:
                        all_patient_med,mbill   =   update_medicines_field(p_id)
                        form_med.medicineQty.data=None
                        form_med.medicineName.data=None
                        form_med.medicineRate.data=None
                        form_med.medicineAmount.data=None
                        return render_template("issueMed.html", pharmacy = True,title="Issue Medicine",form_med=form_med,valid=1,medicines=all_patient_med, data=patient_details)
    
    if(form_med.getRate.data):
        if(form_med.validate_on_submit()):
            med= medicine_details.objects(medName__icontains=form_med.medicineName.data).first()
            
            if(med==None):
                flash("Out of stock","danger")
                return render_template("issueMed.html", pharmacy = True,title="Pharmacy",form_med=form_med,valid=1,medicines=all_patient_med, data=patient_details)
            else:    
                qty=int(form_med.medicineQty.data)
                if(qty>med['qty']):
                    message="Only "+str(med['qty'])+" medicines available for "+str(med['medName'])
                    flash(message,"danger")
                else:
                    form_med.medicineRate.data      =   med['rate']
                    form_med.medicineAmount.data    =   med.get_cost(qty)
                    form_med.medicineName.data      =   med['medName']
                    

                    
    return render_template("issueMed.html", pharmacy = True,title="Issue Medicine",form_med=form_med,valid=1,medicines=all_patient_med, data=patient_details)
#-----------------------------------PHARMACY----------------------------------------------

#------------------------------------DIAGNOSTICS---------------------------------------------
@app.route("/diagnosis",methods=['GET', 'POST'])
@app.route("/diagnostics",methods=['GET', 'POST'])
def diagnostics():
    session['dia_patient']=None 
    form = Patient()
    form.dateAdmission.data     =   None
    form.bed.data               =   None
    disable_fields(form,'disable')
    if(form.getDetails.data):
        if(form.patientId.data==''):
            flash("Enter patient Id ","danger")
            return redirect(url_for('diagnostics'))
        item    =   patientDetails.objects(patientId=form.patientId.data).first()
        if(item and item['status']):
                form    =   Patient(obj=item)
                form.patientId.render_kw    =   {'readonly': 'readonly'}
                disable_fields(form,'disable')
                all_patient_diagnosis,tbill =   update_diagnosis_field(item['patientId'])
                
                return render_template("diagnostics.html", diagnostics = True,title="Diagnosis",form=form,diagnosis=all_patient_diagnosis,flag=1)
        else:
            flash("Patient doesnot exist or is discharged","danger")
            return redirect(url_for('diagnostics'))
    
    if(form.issueDiagnosis.data):
        session['dia_patient']=int(form.patientId.data)
        return redirect(url_for('issueTest'))
    return render_template("diagnostics.html", diagnostics = True,title="Diagnosis",form=form)

@app.route("/issueTest",methods=['GET', 'POST'])
def issueTest():
    try:
        p_id=session['dia_patient']
        dept    =   session['dept']
    except:
        return redirect(url_for('diagnostics'))
    
    if(p_id==None and session['dept']=='diagnosis'):
        flash("Please enter patient id","danger")
        return redirect(url_for('diagnostics'))

    all_patient_diagnosis,tbill =   update_diagnosis_field(p_id)
    patient_details             =   patientDetails.objects(patientId=p_id).first()

    all_test                    =   test_details.objects().order_by("-testId")
    test_list                   =   [(i['testId'], i['testName']) for i in all_test]
    form_med                    =   Test_form() #form for this page
    form_med.testName.choices   =   test_list   #To pass choices to select field
    form_med.amount.render_kw=   {'readonly': 'readonly'}

    if (form_med.update.data or form_med.addTest.data):
        if(form_med.validate_on_submit()):
            test= test_details.objects(testId__iexact=form_med.testName.data).first()
            if(test==None):
                flash("Test not Found ","danger")
                return render_template("issueDiagnosis.html", issueDiagnosis = True,title="Issue Diagnosis",form_med=form_med,valid=1,diagnosis=all_patient_diagnosis, data=patient_details)
            else:    
                    ptest=patient_test(patientId=p_id,testId=test['testId'])
                    ptest.save()        #add new test to database

                    flash("Test added","success")
                    
                     
                    if(form_med.update.data):
                        session['dia_patient']=None
                        return redirect(url_for('diagnostics'))
                    else:
                        form_med.testName.data                =   None
                        form_med.amount.data                  =   None

                        all_patient_diagnosis,tbill   =   update_diagnosis_field(p_id)
                        return render_template("issueDiagnosis.html", diagnostics = True,title="Issue Diagnostics",form_med=form_med,valid=1,diagnosis=all_patient_diagnosis, data=patient_details)

    if(form_med.getRate.data):
        if(form_med.validate_on_submit()):
            obj = test_details.objects(testId__iexact=form_med.testName.data).first()
            print(obj)
            if(obj==None):
                flash("Test not Found ","danger")
                form_med.amount.data    =   None
                return render_template("issueDiagnosis.html", issueDiagnosis = True,title="Issue Diagnosis",form_med=form_med,valid=1,diagnosis=all_patient_diagnosis, data=patient_details)
            else:    
                form_med.amount.data    =   obj['rate']
                form_med.testName.data  =   obj['testName']
    
    return render_template("issueDiagnosis.html", diagnostics = True,title="Issue Diagnostics",form_med=form_med,valid=1,diagnosis=all_patient_diagnosis, data=patient_details)
#----------------------------------------DIAGNOSTICS----------------------------------------------------------
