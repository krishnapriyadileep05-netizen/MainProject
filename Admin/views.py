from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from Volunteer.models import *

# Create your views here.
def AdminRegistration(request):
    data=tbl_admin.objects.all()

    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")

        checkemail = tbl_admin.objects.filter(admin_email=email).count()
        if checkemail > 0:
            return render(request,'Admin/AdminRegistration.html',{'msg':"Email Already Exist"})
        else:
            tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
            return render(request,'Admin/AdminRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/AdminRegistration.html',{"AdminRegistration":data})

def HomePage(request):
    return render(request,"Admin/HomePage.html")

def District(request):
    data=tbl_district.objects.all()

    if request.method=="POST":
        district=request.POST.get("txt_name")
        checkdistrict = tbl_district.objects.filter(district_name=district).count()
        if checkdistrict > 0:
            return render(request,'Admin/District.html',{'msg':"District Already Exist"})
        else:
             tbl_district.objects.create(district_name=district)

        return render(request,'Admin/District.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/District.html',{"district":data})
    
def Category(request):
    data=tbl_category.objects.all()

    if request.method=="POST":
        category=request.POST.get("txt_category")
        tbl_category.objects.create(category_name=category)

        return render(request,'Admin/Category.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Category.html',{"category":data})

def deldistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:District")
def editdistrict(request,id):
    editdata=tbl_district.objects.get(id=id)
    if request.method=="POST":
        district=request.POST.get("txt_name")
        editdata.district_name=district
        editdata.save()
        return redirect("Admin:District")
    else:
        return render(request,'Admin/District.html',{'editdata':editdata})

def delcategory(request,id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Admin:Category")
def editcategory(request,id):
    editdata=tbl_category.objects.get(id=id)
    if request.method=="POST":
        category=request.POST.get("txt_category")
        editdata.category_name=category
        editdata.save()
        return redirect("Admin:Category")
    else:
        return render(request,'Admin/Category.html',{'editdata':editdata})

        
def delAdminRegistration(request,id):
    tbl_admin.objects.get(id=id).delete()
    return redirect("Admin:AdminRegistration")
def editAdminRegistration(request,id):
    editdata=tbl_admin.objects.get(id=id)
    if request.method=="POST":
        AdminRegistration=request.POST.get("txt_name")
        editdata.admin_name=AdminRegistration
        
        editdata.save()
        return redirect("Admin:AdminRegistration")
    else:
        return render(request,'Admin/AdminRegistration.html',{'editdata':editdata})

def Place(request):
    data=tbl_district.objects.all()
    placedata=tbl_place.objects.all()
    if request.method=="POST":
        place=request.POST.get("txt_name")
        district = tbl_district.objects.get(id=request.POST.get("sel_district"))
        tbl_place.objects.create(place_name=place, district=district)

        return render(request,'Admin/Place.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Place.html',{"district":data,'place':placedata})

        
def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:Place")
def editplace(request,id):
    district=tbl_district.objects.all()
    editdata=tbl_place.objects.get(id=id)
    if request.method=="POST":
        Place=request.POST.get("txt_name")
        editdata.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        editdata.place_name=Place
        editdata.save()
        return redirect("Admin:Place")
    else:
        return render(request,'Admin/Place.html',{'editdata':editdata,'district':district})

def Subcategory(request):
    cdata=tbl_category.objects.all()
    sdata=tbl_subcategory.objects.all()
    if request.method=="POST":
        subcategory=request.POST.get("txt_subcategory")
        category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        tbl_subcategory.objects.create(subcategory_name=subcategory, category=category)


        return render(request,'Admin/Subcategory.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Subcategory.html',{"category":cdata,'subcategory':sdata})

def delsub(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:Subcategory")

def editsub(request,id):
    category=tbl_category.objects.all()
    editdata=tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        Subcategory=request.POST.get("txt_subcategory")
        editdata.category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        editdata.subcategory_name=Subcategory
        
        editdata.save()
        return redirect("Admin:Subcategory")
    else:
        return render(request,'Admin/Subcategory.html',{'editdata':editdata,'category':category})

def UserList(request):
    userdata=tbl_user.objects.all()
    return render(request,'Admin/UserList.html',{"users":userdata,})


def VolunteerList(request):
    pending=tbl_volunteer.objects.filter(volunteer_status = 0)
    accept=tbl_volunteer.objects.filter(volunteer_status = 1)
    reject=tbl_volunteer.objects.filter(volunteer_status = 2)
    return render(request,'Admin/VolunteerList.html',{"pending":pending,'accept':accept,'reject':reject})
    
def acceptvolunteer(request,id):
    vdata=tbl_volunteer.objects.get(id=id)
    vdata.volunteer_status=1
    vdata.save()
    return redirect("Admin:VolunteerList")

def rejectvolunteer(request,id):
    vdata=tbl_volunteer.objects.get(id=id)
    vdata.volunteer_status=2
    vdata.save()
    return redirect("Admin:VolunteerList")

def ViewRequest(request):
    pending=tbl_request.objects.filter(request_status = 0)
    accept=tbl_request.objects.filter(request_status = 1)
    reject=tbl_request.objects.filter(request_status = 2)

    return render(request,'Admin/ViewRequest.html',{"pending":pending,"accept":accept,"reject":reject})

def acceptrequest(request,id):
    rdata=tbl_request.objects.get(id=id)
    rdata.request_status=1
    rdata.save()
    return redirect('Admin:ViewRequest')

def rejectrequest(request,id):
    rdata=tbl_request.objects.get(id=id)
    rdata.request_status=2
    rdata.save()
    return redirect('Admin:ViewRequest')

def ViewResponse(request,id):
    responsedata=tbl_response.objects.filter(request_id=id)
    return render(request,'Admin/ViewResponse.html',{"responsedata":responsedata})

def Camp(request):
    campdata=tbl_camp.objects.all()
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method=="POST":
        details=request.POST.get("txt_details")
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"])

        tbl_camp.objects.create(camp_details=details,place_id=place,volunteer_id=volunteerdata)
        return redirect('Admin:Camp')
    else:
        return render(request,'Admin/Camp.html',{'district':district,'place':place,'camp':campdata})
        
def Start(request,id):
    sdata=tbl_camp.objects.get(id=id)
    sdata.camp_status=1
    sdata.save()
    return redirect('Admin:Camp')

def End(request,id):
    edata=tbl_camp.objects.get(id=id)
    edata.camp_status=2
    edata.save()
    return redirect('Admin:Camp')

def AssignVolunteer(request,id):
    volunteer = tbl_volunteer.objects.filter(volunteer_status = 1)
    return render(request,"Admin/AssignVolunteer.html",{'volunteerdata':volunteer})

def DonationRequest(request):
    requestdata=tbl_donationrequest.objects.all()
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method == "POST":
        details=request.POST.get("txt_details")
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))

        tbl_donationrequest.objects.create(donationrequest_details=details,place_id=place)
        return redirect('Admin:DonationRequest')
    else:
        return render(request,"Admin/DonationRequest.html",{'district':district,'place':place,'requestdata':requestdata})
    
def delrequest(request,id):
    tbl_donationrequest.objects.get(id=id).delete()
    return redirect('Admin:DonationRequest')

def AddItem(request,id):
    requestDat=tbl_donationrequest.objects.get(id=id)
    itemdata=tbl_donationitems.objects.all()
    if request.method =="POST":
        name=request.POST.get("txt_name")
        count=request.POST.get("txt_count")
        tbl_donationitems.objects.create(donationitems_name=name,donationitems_count=count,donationrequest_id=requestDat)
        return render(request,'Admin/AddItem.html',{'msg':"Inserted",'id':id})
    else:
        return render(request,"Admin/AddItem.html",{'itemdata':itemdata})
    
def delitem(request,id):
    tbl_donationitems.objects.get(id=id).delete()
    return redirect('Admin:DonationRequest')

def ViewDonation(request):
    viewdonationdata=tbl_donation.objects.all()   
    return render(request,'Admin/ViewDonation.html',{'viewdonationdata':viewdonationdata})

def Assign(request,aid):
    district=tbl_district.objects.all()
    volunteerdata=tbl_volunteer.objects.get(id=aid)
    if request.method == "POST":
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))    
        description=request.POST.get('txt_description')
        tbl_assigndonation.objects.create(volunteer_id=volunteerdata,place_id=place,assigndonation_description=description)
        return render(request,'Admin/Assign.html',{'msg':"Assigned"})
    else:
        return render(request,'Admin/Assign.html',{'district':district,'volunteerdata':volunteerdata})