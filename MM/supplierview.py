from django.shortcuts import render
from  django.http import JsonResponse
from. import Pool
def supplierinterface(request):
    return render(request,'supplierinterface.html')
def suppliersubmit(request):
    try:
        sfirstname = request.POST['sfirstname']
        slastname = request.POST['slastname']
        emailaddress= request.POST['emailaddress']
        mobno=request.POST['mobilenumber']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        db,cmd=Pool.ConnectionPool()
        q="insert into supplier(sfirstname,slastname,emailaddress,mobno,address,state,city)values('{}','{}','{}','{}','{}','{}','{}')".format(sfirstname,slastname,emailaddress,mobno,address,state,city)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,'supplierinterface.html',{'msg':'Record succesfully submitted'})
    except Exception as e:
        print("error:", e)
        return render(request, 'supplierinterface.html', {'msg': 'Fail to Submit Record'})
def getsupplierJSON(request):
    try:
     db,cmd=Pool.ConnectionPool()
     q="select * from supplier"
     cmd.execute(q)
     rows=cmd.fetchall()
     db.commit()
     db.close()
     return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:",e)
        return JsonResponse([], safe=False)

