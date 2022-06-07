"""MM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import employeeview
from. import statecityview
from . import categoryview
from . import subcategoryview
from. import productview
from . import finalproductview
from . import supplierview
from. import purchaseview
from . import adminview
from. import issueview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminlogin/', adminview.adminlogin),
    path('checkadminlogin', adminview.checkadminlogin),

    #employee
    path('employeelogin/',employeeview.employeelogin),
    path('checkemployeelogin', employeeview.checkemployeelogin),
    path('employeeinterface/',employeeview.employeeinterface),
    path('employeesubmit',employeeview.employeesubmit),
    path('displayall/',employeeview.displayall),
    path('displayemployeebyid/',employeeview.displaybyid),
    path('editdeleterecord/', employeeview.editdeleterecord),
    path('editemployeepicture/', employeeview.editemployeepicture),
    path('saveeditpicture', employeeview.saveeditpicture),
    path('getemployeejson/', employeeview.getemployeejson),

    #category
    path('categoryinterface/',categoryview.categoryinterface),
    path('categorysubmit',categoryview.categorysubmit),
    path('displaycategory/',categoryview.displaycategory),
    path('getcategoryjson/',categoryview.getcategoriesJSON),
    path('displaycategorybyid/',categoryview.displaycategorybyid),
    path('editdeletecategory/', categoryview.editdeletecategory),
    path('editcategoryicon/', categoryview.editcategoryicon),
    path('saveeditcategoryicon', categoryview.saveeditcategoryicon),

    #subcategory
    path('subcategoryinterface/', subcategoryview.subcategoryinterface),
    path('subcategorysubmit', subcategoryview.subcategorysubmit),
    path('displaysubcategory', subcategoryview.displaysubcategory),
    path('getsubcategoryjson/', subcategoryview.getsubcategoriesJSON),

    path('displaysubcategorybyid', subcategoryview.displaysubcategorybyid),
    path('editdeletesubcategory', subcategoryview.editdeletesubcategory),
    path('editsubcategoryicon', subcategoryview.editsubcategoryicon),
    path('saveeditsubcategoryicon', subcategoryview.saveeditsubcategoryicon),

    #product
    path('productinterface', productview.productinterface),
    path('productsubmit', productview.productsubmit),
    path('displayproduct', productview.displayproduct),
    path('displayproductbyid', productview.displayproductbyid),
    path('editdeleteproduct',productview.editdeleteproduct),
    path('editproducticon',productview.editproducticon),
    path('saveeditproducticon', productview.saveeditproducticon),
    path('getproductjson/', productview.getproductsJSON),
    #Finalproduct
    path('finalproductinterface', finalproductview.finalproductinterface),
    path('finalproductsubmit', finalproductview.finalproductsubmit),
    path('displayfinalproduct', finalproductview.displayfinalproduct),
    path('getfinalproductjson/', finalproductview.getfinalproductJSON),
    path('displayfinalproductbyid', finalproductview.displayfinalproductbyid),
    path('editdeletefinalproduct', finalproductview.editdeletefinalproduct),
    path('editfinalproducticon', finalproductview.editfinalproducticon),
    path('saveeditfinalproducticon', finalproductview.saveeditfinalproducticon),
    path('displayfinalproductbyidjson/', finalproductview.DisplayFinalProductByIdJSON),
    path('finalproductalljson/', finalproductview.FinalProductAllJSON),
    path('displayupdatedstock/', finalproductview.displayupdatedstock),

    #supplier
    path('supplierinterface/', supplierview.supplierinterface),
    path('suppliersubmit', supplierview.suppliersubmit),
    path('getsupplierjson/', supplierview.getsupplierJSON),

    #purchase
    path('purchaseinterface/', purchaseview.purchaseinterface),
    path('purchasesubmit', purchaseview.purchasesubmit),
    path('displaypurchase', purchaseview.displaypurchase),
    path('displaypurchasebyid',purchaseview.displaypurchasebyid),
    path('editdeletepurchase', purchaseview.editdeletepurchase),
    path('displaypurchasealljson',purchaseview.DisplayPurchaseAllJSON),
    path('displaypurchaseproduct', purchaseview.displaypurchaseproduct),

    #fetch
    path('fetchallstates/',statecityview.FetchAllStates),
    path('fetchallcities/',statecityview.fetchallcities),
    
    #issue
    path('issueinterface/', issueview.issueinterface),
    path('issueproductsubmit', issueview.issueproductsubmit),
    path('displayallissueproduct/', issueview.DisplayAllIssueProduct),
    path('editdeleteissueproductrecord/',issueview.EditDeleteIssueProductRecord),
    path('displayissuealljson/', issueview.DisplayIssueAllJSON),
    path('displayissueproduct/', issueview.displayissueproduct),

]

