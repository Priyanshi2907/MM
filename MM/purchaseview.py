from django.shortcuts import render
from django.http import JsonResponse
import os
import uuid
from . import Pool
from . import PoolDict
def purchaseinterface(request):
    try:
        result = request.session['EMPLOYEE']
        return render(request, "purchaseinterface.html", {'result': result})
    except Exception as e:
        return render(request,'employeelogin.html')
def purchasesubmit(request):
    try:
        employeeid=request.POST['employeeid']
        categoryid=request.POST['categoryid']
        subcategoryid = request.POST['subcategoryid']
        productid = request.POST['productid']
        finalproductid= request.POST['finalproductid']
        date= request.POST['date']
        supplierid = request.POST['supplierid']
        stock = request.POST['stock']
        amount = request.POST['amount']
        db, cmd = Pool.ConnectionPool()
        q="insert into purchase(employeeid, categoryid, subcategoryid, productid, finalproductid, date, supplierid, stock, amount)values({},{},{},{},{},'{}',{},'{}','{}')".format( employeeid, categoryid, subcategoryid, productid, finalproductid, date, supplierid, stock, amount)
        print(q)
        cmd.execute(q)
        #update stock
        q="update finalproduct set price=(price+{})/2 , stock=stock+{} where finalproductid={}".format(amount,stock,finalproductid)
        cmd.execute(q)

        db.commit()
        return render(request,'purchaseinterface.html',{'msg':'Record Submitted Succesfully'})
    except Exception as e:
        print("error:",e)
        return render(request, 'purchaseinterface.html', {'msg': 'Fail to Submit'})

def displaypurchase(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select PP. *,(select C.categoryname from category C where C.categoryid=PP.categoryid), \
          (select S.subcategoryname from subcategory S where S.subcategoryid=PP.subcategoryid), \
          (select P.productname from product P where P.productid=PP.productid),\
          (select F.finalproductname from finalproduct F where F.finalproductid=PP.finalproductid),(select CONCAT(s.sfirstname,' ',s.slastname) from supplier s where s.supplierid=PP.supplierid) from purchase PP"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'displaypurchase.html',{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,'displaypurchase.html',{'rows':[]})

def displaypurchasebyid(request):
        transactionid = request.GET['transactionid']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "select * from purchase where transactionid={}".format(transactionid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return render(request, "displaypurchasebyid.html", {'row': row})
        except Exception as e:
            print("error:", e)
            return render(request, "displaypurchasebyid.html", {'row': []})

def editdeletepurchase(request):
    btn=request.GET['btn']
    transactionid=request.GET['transactionid']
    if(btn=='edit'):
        categoryid = request.GET['categoryid']
        subcategoryid = request.GET['subcategoryid']
        productid=request.GET['productid']
        finalproductid=request.GET['finalproductid']
        date=request.GET['date']
        supplierid = request.GET['supplierid']
        stock= request.GET['stock']
        amount= request.GET['amount']
        try:
           db,cmd=Pool.ConnectionPool()
           q="update purchase set categoryid={},subcategoryid={},productid={},finalproductid={},date='{}',supplierid={},stock='{}',amount='{}' where transactionid={}".format(categoryid,subcategoryid,productid,finalproductid, date, supplierid, stock, amount,transactionid)
           cmd.execute(q)
           db.commit()
           db.close()
           return displaypurchase(request)
        except Exception as e:
           print('error:',e)
           return  displaypurchase(request)
    elif(btn=="delete"):
        try:
            db,cmd=Pool.ConnectionPool()
            q="delete from purchase where transactionid={}".format(transactionid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displaypurchase(request)
        except Exception as e:
            print('error:',e)
            return  displaypurchase(request)

def DisplayPurchaseAllJSON(request):
    fromdate = request.GET['fromdate']
    todate = request.GET['todate']
    try:
        dbe, cmd = PoolDict.ConnectionPool()
        q = "select PP.*,(select C.categoryname from category C where C.categoryid = PP.categoryid) as categoryname,(select S.subcategoryname from subcategory S where S.subcategoryid = PP.subcategoryid) as subcategoryname, (select P.productname from product P where P.productid = PP.productid) as productname, (select FP.finalproductname from finalproduct FP where FP.finalproductid = PP.finalproductid) as finalproductname, (select E.firstname from employee E where E.employeeid = PP.employeeid) as dfname, (select E.lastname from employee E where E.employeeid = PP.employeeid) as flname,(select S.sfirstname from supplier S where S.supplierid = PP.supplierid) as sfname,(select S.slastname from supplier S where S.supplierid = PP.supplierid) as slname from purchase PP where date between '{}' and '{}'".format(fromdate,todate)
        #q = "select IP.*,(select C.categoryname from category C where C.categoryid = IP.categoryid) as categoryname,(select S.subcategoryname from subcategory S where S.subcategoryid = IP.subcategoryid) as subcategoryname, (select P.productname from product P where P.productid = IP.productid) as productname, (select FP.finalproductname from finalproduct FP where FP.finalproductid = IP.finalproductid) as finalproductname, (select E.firstname from employee E where E.employeeid = IP.demand_employeeid) as dfname, (select E.lastname from employee E where E.employeeid = IP.demand_employeeid) as flname,(select E.firstname from employee E where E.employeeid = IP.employeeid) as fname, (select E.lastname from employee E where E.employeeid = IP.employeeid) as lname from issue IP where dateissue between '{}' and '{}'".format(fromdate,todate)
        cmd.execute(q)
        rows = cmd.fetchall()
        dbe.close()
        return JsonResponse(rows, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse([], safe=False)


def displaypurchaseproduct(request):
    return render(request,'Listpurchaseemployee.html')
