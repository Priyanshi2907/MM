from django.shortcuts import render
from django.http import JsonResponse
import os
import uuid
from . import Pool
def subcategoryinterface(request):
    return render(request,'subcategoryinterface.html')
def subcategorysubmit(request):
    try:
        categoryid=request.POST['categoryid']
        subcategoryname=request.POST['subcategoryname']
        discription=request.POST['discription']
        subcategoryicon=request.FILES['subcategoryicon']
        file=str(uuid.uuid4())+subcategoryicon.name[subcategoryicon.name.rfind('.'):]
        q="insert into subcategory(categoryid,subcategoryname,discription,subcategoryicon)values({},'{}','{}','{}')".format(categoryid,subcategoryname,discription,file)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F = open("E:/MM/assets/"+file,"wb")
        for chunk in subcategoryicon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,'subcategoryinterface.html',{'msg':"Record Succesfully Submitted"})
    except Exception as e:
        print('Error:',e)
        return render(request, 'subcategoryinterface.html', {'msg': "Fail to submit"})
def displaysubcategory(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select S. *,(select C.categoryname from category C where C.categoryid=S.categoryid) from subcategory S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'displaysubcategory.html',{'rows':rows})
    except Exception as e:
        print('error:',e)
        return render(request,'displaysubcategory.html',{'rows':[]})
def getsubcategoriesJSON(request):
    try:
        db, cmd = Pool.ConnectionPool()
        categoryid=request.GET['categoryid']
        q = "select * from subcategory where categoryid={}".format(categoryid)
        cmd.execute(q)
        rows = cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:", e)
        return JsonResponse([],safe=False)

def displaysubcategorybyid(request):
        subcategoryid=request.GET['subcategoryid']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "select * from subcategory where subcategoryid={}".format(subcategoryid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return render(request, 'Displaysubcategorybyid.html', {'row': row})
        except Exception as e:
            print("error:", e)
            return render(request, 'Displaysubcategorybyid.html', {'row': []})

def editdeletesubcategory(request):
    btn=request.GET['btn']
    subcategoryid=request.GET['subcategoryid']

    if(btn=="edit"):
        categoryid = request.GET['categoryid']
        subcategoryname=request.GET['subcategoryname']
        discription=request.GET['discription']

        try:
           db,cmd=Pool.ConnectionPool()
           q="update subcategory set categoryid={},subcategoryname='{}',discription='{}' where subcategoryid={}".format(categoryid,subcategoryname,discription,subcategoryid)
           cmd.execute(q)
           db.commit()
           db.close()
           return displaysubcategory(request)
        except Exception as e:
           print('error:',e)
           return  displaysubcategory(request)

    elif(btn=="delete"):
        try:
            db,cmd=Pool.ConnectionPool()
            q="delete from subcategory where subcategoryid={}".format(subcategoryid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displaysubcategory(request)
        except Exception as e:
            print('error:',e)
            return  displaysubcategory(request)
def editsubcategoryicon(request):
    try:
        subcategoryid=request.GET['subcategoryid']
        subcategoryname = request.GET['subcategoryname']
        subcategoryicon = request.GET['subcategoryicon']
        row=[subcategoryid,subcategoryname,subcategoryicon]
        return render(request,'editsubcategoryicon.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request, 'editsubcategoryicon.html', {'row': []})
def saveeditsubcategoryicon(request):
    try:
        subcategoryid=request.POST['subcategoryid']
        oldpicture=request.POST['oldpicture']
        picture=request.FILES['subcategoryicon']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update subcategory set subcategoryicon='{}' where subcategoryid={}".format(filename,subcategoryid)
        print(q)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("E:/MM/assets/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove("E:/MM/assets"+oldpicture)
        return displaysubcategory(request)
    except Exception as e:
        print('error:',e)
        return displaysubcategory(request)

