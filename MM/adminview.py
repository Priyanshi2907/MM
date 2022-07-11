from django.shortcuts import render
from. import PoolDict

def adminlogin(request):
    try:
        #result=request.session['ADMIN']
        return render(request, 'admindashboard.html')
    except Exception as e:
        return render(request,"adminlogin.html")
def checkadminlogin(request):
    emailid=request.POST['emailid']
    password=request.POST['password']
    try:
        db,cmd=PoolDict.ConnectionPool()
        q="select * from admin where emailid='{}' and password='{}'".format(emailid,password)
        cmd.execute(q)
        result=cmd.fetchone()
        print(result)
        if(result):
            request.session['ADMIN']=result
            return render(request,'admindashboard.html',{'result':result})
        else:
            return render(request,'adminlogin.html',{'result':result,'msg':'Invalid email or password'})

    except Exception as e:
        print('error:',e)
        return render(request,"adminlogin.html",{'result':{},'msg':'Server Error'})

