from django.shortcuts import render
from django.http import JsonResponse
from. import Pool
from. import PoolDict
import uuid
import random
import os
from . import SendSms
from. import EmailService
from  django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def employeelogin(request):

        return render(request,'employeelogin.html')

@xframe_options_exempt
def checkemployeelogin(request):
    try:
        emailaddress=request.POST['emailaddress']
        password=request.POST['password']
        q="select * from employee where (email='{}' or mobileno='{}') and password='{}'".format(emailaddress,emailaddress,password)
        print(q)
        db,cmd=PoolDict.ConnectionPool()
        cmd.execute(q)
        result=cmd.fetchone()
        print(result)
        if(result):
            request.session['EMPLOYEE'] = result
            return render(request,'employeedashboard.html',{'result':result})
        else:
            return render(request,'employeelogin.html',{'result':result,'msg':'Invalid Email or Password'})
    except Exception as e:
     print(e)
     return render(request, 'employeelogin.html', {'result': {},'msg':'Server Error'})

@xframe_options_exempt
def employeeinterface(request):
    try:
        result=request.session['ADMIN']
        return render(request, 'EmployeeInterface.html')
    except Exception as e:
        return render(request, 'adminlogin.html')

@xframe_options_exempt
def employeesubmit(request):
    try:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        gender=request.POST['gender']
        birthdate=request.POST['birthdate']
        paddress=request.POST['paddress']
        state=request.POST['state']
        city=request.POST['city']
        caddress=request.POST['caddress']
        emailaddress=request.POST['emailaddress']
        mobilenumber=request.POST['mobilenumber']
        designation=request.POST['designation']

        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        password="".join(random.sample(['1','a','4','5','x','66','#','@'],k=7))
       
        q="insert into employee(firstname,lastname,gender,dob,paddress,stateid,cityid,caddress,email,mobileno,designation,picture,password)values('{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}')".format(firstname,lastname,gender,birthdate,paddress,state,city,caddress,emailaddress,mobilenumber,designation,filename,password)
        print(q)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("E:/MM/assets/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        result=SendSms.SendMessage("Hi {} Your Password is {}".format(firstname,password),mobilenumber)
        print(result.json())
        EmailService.SendMail(emailaddress,"Hi {} Your Password is {}".format(firstname,password))
        return render(request,'EmployeeInterface.html',{'msg':'Record Succesfully Submitted'})

    except Exception as e:

        print("error:",e)
        return render(request,'EmployeeInterface.html',{'msg':'Fail to Submit Record'})
@xframe_options_exempt
def displayall(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select E.*,(select C.cityname from cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employee E "
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'displayemployee.html',{'rows':rows})
    except Exception as e:
        print(e)
        return render(request,'displayemployee.html',{'rows':[]})

@xframe_options_exempt
def displaybyid(request):
    empid=request.GET["empid"]
    try:
        db,cmd=Pool.ConnectionPool()
        q="select E.*,(select C.cityname from cities C where C.cityid=E.cityid),(select S.statename from states S where S.stateid=E.stateid) from employee E where employeeid={}".format(empid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request,'displayemployeebyid.html',{'row':row})
    except Exception as e:
        print(e)
        return render(request,'displayemployeebyid.html',{'row':[]})
@xframe_options_exempt
def editdeleterecord(request):
    btn=request.GET['btn']
    empid = request.GET['empid']
    if(btn=="edit"):

     firstname = request.GET['firstname']
     lastname = request.GET['lastname']
     gender = request.GET['gender']
     birthdate = request.GET['birthdate']
     paddress = request.GET['paddress']
     state = request.GET['state']
     city = request.GET['city']
     caddress = request.GET['caddress']
     emailaddress = request.GET['emailaddress']
     mobilenumber = request.GET['mobilenumber']
     designation = request.GET['designation']

     try:
        db,cmd=Pool.ConnectionPool()
        q = "update employee set firstname='{}', lastname='{}', gender='{}', dob='{}', paddress='{}', stateid={}, cityid={}, caddress='{}', email='{}', mobileno='{}', designation='{}' where employeeid={}".format(
            firstname, lastname, gender, birthdate, paddress, state, city, caddress, emailaddress, mobilenumber,
            designation, empid)

        cmd.execute(q)
        db.commit()
        db.close()
        return displayall(request)
     except Exception as e:
        print("Error:" , e)
        return displayall(request)

    elif (btn=="Delete"):
        try:
            db, cmd = Pool.ConnectionPool()
            q = "delete from employee where employeeid={}".format(empid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displayall(request)
        except Exception as e:
            print(e)
            return displayall(request)

@xframe_options_exempt
def editemployeepicture(request):
    try:
        empid = request.GET['empid']
        firstname = request.GET['firstname']
        lastname = request.GET['lastname']
        picture=request.GET['picture']
        row=[empid,firstname,lastname,picture]
        return render(request,'EditEmployeePicture.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request,'EditEmployeePicture.html',{'row':[]})
@xframe_options_exempt
def saveeditpicture(request):
    try:
        empid = request.POST['empid']
        oldpicture= request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "update employee set picture='{}' where employeeid={}".format(filename,empid)
        print(q)
        db, cmd = Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/" + filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove('E:/MM/assets/'+oldpicture)
        return displayall(request)
    except Exception as e:
        print("error:",e)
        return displayall(request)

def getemployeejson(request):
    try:
        db,cmd=PoolDict.ConnectionPool()
        q="select * from employee"
        cmd.execute(q)
        rows=cmd.fetchall()
        print(rows)
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        return JsonResponse([],safe=False)
