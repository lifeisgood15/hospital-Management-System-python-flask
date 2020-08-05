import flask
from application import db,app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random

class staffDetails(db.Document):
    staffId         =   db.StringField(unique=True)
    staffSSN        =   db.IntField(unique=True)
    staffName       =   db.StringField(max_length=50)
    staffPhone      =   db.IntField(max_length=10)
    staffDept       =   db.StringField()
    staffDob        =   db.DateTimeField()        
    staffDoj        =   db.DateTimeField()
    staffAddress    =   db.StringField()


class userstore(db.Document):
    staffId         =   db.StringField(unique=True)
    password        =   db.StringField()
    timestamp       =   db.DateTimeField(default=datetime.datetime.now().isoformat()) 
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class patientDetails(db.Document):
    patientId       =   db.IntField(unique=True)
    patientSSN      =   db.IntField(unique=True)
    patientName     =   db.StringField( max_length=50 )
    patientAge      =   db.IntField()
    dateAdmission   =   db.DateTimeField()
    bed             =   db.IntField()
    patientAddress  =   db.StringField( max_length=150 )
    city            =   db.StringField( max_length=50 )
    state           =   db.StringField( max_length=50 )
    status          =   db.BooleanField() #True=active False=discharged

    def getBed(self,bedType):
        bedDictionary   =   {1:"General",2:"Semi Sharing",3:"Single"}
        return(bedDictionary[bedType])
    def generatePatientId(self):
        now = datetime.datetime.now()
        pid=str(now.year)[2:]+str(now.month)+str(now.day)
        pid=int(pid)*10**(9-len(pid))
        totalPatients = patientDetails.objects.count()
        flag=True
        while(flag):
            temp=pid+random.randint(0,999)
            p=patientDetails.objects(patientId=temp).first()
            if(p==None):
                flag=False
            pid=temp

        self.patientId  =   pid

    def generateRoomBill(self):
        rate={1:2000,2:4000,3:8000}
        room={}
        now = datetime.datetime.now()
        days=now-self.dateAdmission
        room['days']=days
        room['bill']=days*rate[self.bed]
        return (room)

class patient_med(db.Document):
    patientId   =   db.IntField()
    medId       =   db.IntField()
    pmed_qty    =   db.IntField()
    paid        =   db.BooleanField(default=False)

class patient_test(db.Document):
    patientId   =   db.IntField()
    testId       =   db.IntField()
    paid        =   db.BooleanField(default=False)
class test_details(db.Document):
    testId      =   db.IntField(unique=True)
    testName    =   db.StringField()
    rate        =   db.IntField()
    
class medicine_details(db.Document):
    medId       =   db.IntField(unique=True)
    medName     =   db.StringField()
    qty         =   db.IntField()
    rate        =   db.IntField()

    def get_cost(self,quantity):
        return(quantity*self.rate)

    



