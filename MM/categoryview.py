from django.shortcuts import render
from django.http import JsonResponse
from.import Pool
import uuid
import os
def categoryinterface(request):
    return render(request,'Categoryinterface.html')
def categorysubmit(request):
    try:
        categoryname=request.POST['categoryname']
        icon=request.FILES['categoryicon']
        categoryicon=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into category(categoryname,categoryicon)values('{}','{}')".format(categoryname,categoryicon)
        db,cmd=Pool.ConnectionPool()
        cmd.execute(q)
        db.commit()
        F=open("E:/MM/assets/"+categoryicon,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"Categoryinterface.html",{'msg':'Record Successfully Submitted'})
    except Exception as e:
        print('error:',e)
        return render(request,"Categoryinterface.html",{'msg':'Fail to Submit'})
def displaycategory(request):
    try:
        db,cmd=Pool.ConnectionPool()
        q="select * from category"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,'Displayallcategory.html',{'rows':rows})
    except Exception as e:
        print("error:",e)
        return render(request, 'Displayallcategory.html', {'rows': []})
def getcategoriesJSON(request):
    try:
        db, cmd = Pool.ConnectionPool()
        q = "select * from category"
        cmd.execute(q)
        rows = cmd.fetchall()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:", e)
        return JsonResponse([],safe=False)



def displaycategorybyid(request):
        categoryid=request.GET['categoryid']
        try:
            db, cmd = Pool.ConnectionPool()
            q = "select * from category where categoryid={}".format(categoryid)
            cmd.execute(q)
            row = cmd.fetchone()
            db.close()
            return render(request, 'Displaycategorybyid.html', {'row': row})
        except Exception as e:
            print("error:", e)
            return render(request, 'Displaycategorybyid.html', {'row': []})

def editdeletecategory(request):
    btn=request.GET['btn']
    catid=request.GET['catid']
    if(btn=='edit'):
        categoryname=request.GET['categoryname']
        try:
           db,cmd=Pool.ConnectionPool()
           q="update category set categoryname='{}' where categoryid={}".format(categoryname,catid)
           cmd.execute(q)
           db.commit()
           db.close()
           return displaycategory(request)
        except Exception as e:
           print('error:',e)
           return  displaycategory(request)
    elif(btn=="delete"):
        try:
            db,cmd=Pool.ConnectionPool()
            q="delete from category where categoryid={}".format(catid)
            cmd.execute(q)
            db.commit()
            db.close()
            return  displaycategory(request)
        except Exception as e:
            print('error:',e)
            return  displaycategory(request)
def editcategoryicon(request):
    try:
        categoryid=request.GET['catid']
        categoryname = request.GET['catname']
        categoryicon = request.GET['caticon']
        row=[categoryid,categoryname,categoryicon]
        return render(request,'editcategoryicon.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request, 'editcategoryicon.html', {'row': []})

def saveeditcategoryicon(request):
    try:
        categoryid=request.POST['categoryid']
        oldpicture=request.POST['oldicon']
        picture=request.FILES['categoryicon']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="update category set categoryicon='{}' where categoryid={}".format(filename,categoryid)
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
        return displaycategory(request)
    except Exception as e:
        print('error:',e)
        return displaycategory(request)


