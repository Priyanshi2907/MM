from django.shortcuts import render
from django.http import JsonResponse
import os
import uuid
from . import Pool
from. import PoolDict
def finalproductinterface(request):
    return render(request,'finalproductinterface.html')
def finalproductsubmit(request):
    try:
         categoryid = request.POST['categoryid']
         subcategoryid = request.POST['subcategoryid']
         productid = request.POST['productid']
         finalproductname = request.POST['finalproductname']
         size = request.POST['size']
         sizeunit= request.POST['sizeunit']
         weight = request.POST['weight']
         weightunit = request.POST['weightunit']
         colour = request.POST['colour']
         price = request.POST['price']
         stock = request.POST['stock']
         icon = request.FILES['finalproducticon']
         finalproducticon = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
         q = "insert into finalproduct(categoryid,subcategoryid,productid,finalproductname,size,sizeunit,weight,weightunit,colour,price,stock,finalproducticon)values({},{},{},'{}',{},'{}',{},'{}','{}',{},{},'{}')".format(
         categoryid, subcategoryid, productid, finalproductname,size,sizeunit,weight,weightunit,colour,price,stock,finalproducticon)
         db, cmd = Pool.ConnectionPool()
         print(q)
         cmd.execute(q)
         db.commit()
         file = open("E:/MM/assets/" + finalproducticon, "wb")
         for chunk in icon.chunks():
          file.write(chunk)
         file.close()
         db.close()
         return render(request, 'finalproductinterface.html', {'msg': 'Record Submitted Succesfully'})
    except Exception as e:
            print("error:", e)
            return render(request, 'finalproductinterface.html', {'msg': 'Fail to Submit'})

def displayfinalproduct(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select F. *,(select C.categoryname from category C where C.categoryid=F.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid=F.subcategoryid),(select P.productname from product P where P.productid=F.productid) from finalproduct F"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'displayfinalproduct.html',{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,'displayfinalproduct.html',{'rows':[]})

def getfinalproductJSON(request):
    try:
        db, cmd = Pool.ConnectionPool()
        productid=request.GET['productid']
        q = "select * from finalproduct where productid={}".format(productid)
        cmd.execute(q)
        rows = cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:", e)
        return JsonResponse([],safe=False)




def displayfinalproductbyid(request):
        finalproductid=request.GET['finalproductid']
        try:
            db,cmd=Pool.ConnectionPool()
            q = "select F. *,(select C.categoryname from category C where C.categoryid=F.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid=F.subcategoryid),(select P.productname from product P where P.productid=F.productid) from finalproduct F".format(finalproductid)
            cmd.execute(q)
            row=cmd.fetchone()
            db.close()
            return render(request,"displayfinalproductbyid.html", {'row': row})
        except Exception as e:
            print("error:",e)
            return render(request, "displayfinalproductbyid.html",{'row':[]})
def editdeletefinalproduct(request):
    btn=request.GET['btn']
    finalproductid=request.GET['finalproductid']
    if(btn=='edit'):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid=request.GET['productid']
        finalproductname=request.GET['finalproductname']
        size=request.GET['size']
        sizeunit = request.GET['sizeunit']
        weight= request.GET['weight']
        weightunit= request.GET['weightunit']
        colour= request.GET['colour']
        price= request.GET['price']
        stock = request.GET['stock']
        try:
           db,cmd=Pool.ConnectionPool()
           q="update finalproduct set categoryid={},subcategoryid={},productid={},finalproductname='{}',size={},sizeunit='{}',weight={},weightunit='{}',colour='{}',price={},stock={} where finalproductid={}".format(categoryid,subcategoryid,productid,finalproductname, size, sizeunit, weight, weightunit, colour, price, stock,finalproductid)
           cmd.execute(q)
           db.commit()
           db.close()
           return displayfinalproduct(request)
        except Exception as e:
           print('error:',e)
           return  displayfinalproduct(request)
    elif(btn=="delete"):
        try:
            db,cmd=Pool.ConnectionPool()
            q="delete from finalproduct where finalproductid={}".format(finalproductid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displayfinalproduct(request)
        except Exception as e:
            print('error:',e)
            return  displayfinalproduct(request)
def editfinalproducticon(request):
    try:
        finalproductid=request.GET['finalproductid']
        finalproductname = request.GET['finalproductname']
        finalproducticon = request.GET['icon']
        row=[finalproductid,finalproductname,finalproducticon]
        return render(request,'editfinalproducticon.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request, 'editfinalproducticon.html', {'row': []})
def saveeditfinalproducticon(request):
    try:
        finalproductid=request.POST['finalproductid']
        oldpicture = request.POST['oldpicture']
        finalproducticon=request.FILES['finalproducticon']
        file=str(uuid.uuid4())+finalproducticon.name[finalproducticon.name.rfind('.'):]
        q = "update finalproduct set finalproducticon='{}' where finalproductid={}".format(file,finalproductid)
        db, cmd = Pool.ConnectionPool()
        print(q)
        cmd.execute(q)
        db.commit()
        f = open("E:/MM/assets/" + file, "wb")
        for chunk in finalproducticon.chunks():
           f.write(chunk)
        f.close()
        db.close()
        os.remove("E:/MM/assets/"+oldpicture)
        return displayfinalproduct(request)
    except Exception as e:
        print("error:",e)
        return displayfinalproduct(request)

# fetch the total stock of final product
def DisplayFinalProductByIdJSON(request):
    finalproductid = request.GET['finalproductid']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select FP.*,(select C.categoryname from category C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = FP.subcategoryid), (select P.productname from product P where P.productid = FP.productid) from finalproduct FP where finalproductid = {}".format(finalproductid)
        cmd.execute(q)
        row = cmd.fetchone()
        dbe.close()
        return JsonResponse(row, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def FinalProductAllJSON(request):
    pattern = request.GET['pattern']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select FP.*,(select C.categoryname from category C where C.categoryid = FP.categoryid),(select S.subcategoryname from subcategory S where S.subcategoryid = FP.subcategoryid), (select P.productname from product P where P.productid = FP.productid) from finalproduct FP where finalproductname like '%{}%'".format(pattern)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)

def displayupdatedstock(request):
    return render(request,'ListProductEmployee.html')

