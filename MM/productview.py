import os
from django.http import JsonResponse
from django.shortcuts import render
from . import Pool
import uuid
def productinterface(request):
    return render(request,'productinterface.html')
def productsubmit(request):
    try:
        categoryid=request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productname = request.POST['productname']
        pdiscription= request.POST['pdiscription']
        icon=request.FILES['producticon']
        producticon=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into product(categoryid,subcategoryid,productname,productdiscription,producticon)values({},{},'{}','{}','{}')".format(categoryid,subcategoryid,productname,pdiscription,producticon)
        db, cmd = Pool.ConnectionPool()
        print(q)
        cmd.execute(q)
        db.commit()
        file=open("E:/MM/assets/"+producticon,"wb")
        for chunk in icon.chunks():
            file.write(chunk)
        file.close()
        db.close()
        return render(request,'productinterface.html',{'msg':'Record Submitted Succesfully'})
    except Exception as e:
        print("error:",e)
        return render(request, 'productinterface.html', {'msg': 'Fail to Submit'})
def displayproduct(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select P.*,(select C.categoryname from category C where C.categoryid=P.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid=P.subcategoryid) from product P"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'displayproduct.html',{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,'displayproduct.html',{'rows':[]})
def getproductsJSON(request):
    try:
        db, cmd = Pool.ConnectionPool()
        subcategoryid=request.GET['subcategoryid']
        q = "select * from product where subcategoryid={}".format(subcategoryid)
        cmd.execute(q)
        rows = cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:", e)
        return JsonResponse([],safe=False)


def displayproductbyid(request):
        productid = request.GET['productid']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "select * from product where productid={}".format(productid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return render(request, 'Displayproductbyid.html', {'row': row})
        except Exception as e:
            print("error:", e)
            return render(request, 'Displayproductbyid.html', {'row': []})

def editdeleteproduct(request):
    btn=request.GET['btn']
    productid=request.GET['productid']
    if(btn=='edit'):
        categoryid=request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productname=request.GET['PRODUCTNAME']
        productdiscription=request.GET['PDISCRIPTION']

        try:
           db,cmd=Pool.ConnectionPool()
           q="update product set categoryid={},subcategoryid={},productname='{}',productdiscription='{}' where productid={}".format(categoryid,subcategoryid,productname,productdiscription,productid)
           cmd.execute(q)
           db.commit()
           db.close()
           return displayproduct(request)
        except Exception as e:
           print('error:',e)
           return  displayproduct(request)
    elif(btn=="delete"):
        try:
            db,cmd=Pool.ConnectionPool()
            q="delete from product where productid={}".format(productid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displayproduct(request)
        except Exception as e:
            print('error:',e)
            return  displayproduct(request)
def editproducticon(request):
    try:
        productid=request.GET['productid']
        productname = request.GET['productname']
        producticon = request.GET['producticon']
        row=[productid,productname,producticon]
        return render(request,'editproducticon.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request, 'editproducticon.html', {'row': []})
def saveeditproducticon(request):
    try:
        productid=request.POST['productid']
        oldpicture = request.POST['oldpicture']
        producticon=request.FILES['producticon']
        file=str(uuid.uuid4())+producticon.name[producticon.name.rfind('.'):]
        q = "update product set producticon='{}' where productid={}".format(file,productid)
        db, cmd = Pool.ConnectionPool()
        print(q)
        cmd.execute(q)
        db.commit()
        f = open("E:/MM/assets/" + file, "wb")
        for chunk in producticon.chunks():
           f.write(chunk)
        f.close()
        db.close()
        os.remove("E:/MM/assets/"+oldpicture)
        return displayproduct(request)
    except Exception as e:
        print("error:",e)
        return displayproduct(request)



