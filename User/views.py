from django.shortcuts import render
from Admin.models import *
from Guest.models import *
from User.models import *
from Volunteer.models import *


# Create your views here.
def MyProfile(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{"userdata": userdata})
  
def EditProfile(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')

        userdata.user_name=name
        userdata.user_email=email
        userdata.user_contact=contact
        userdata.user_address=address
        userdata.save()

        return render(request,'User/EditProfile.html',{'msg':'updated'})
    else:
        return render(request,'User/EditProfile.html',{"userdata":userdata})

def ChangePassword(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    userpassword=userdata.user_password

    if request.method == "POST":
        oldpassword=request.POST.get('txt_old')
        newpassword=request.POST.get('txt_new')
        retype=request.POST.get('txt_retype')
        if userpassword==oldpassword:
            if newpassword==retype:
                userdata.user_password=newpassword
                userdata.save()
                return render(request,'User/ChangePassword.html',{"msg":"Password Updated"})
            else:
                return render(request,'User/ChangePassword.html',{"msg1":"Password Mismatch"})
        else:
            return render(request,'User/ChangePassword.html',{"msg1":"Password Incorrect"})
    else:
        return render(request,'User/ChangePassword.html')

def HomePage(request):
    return render(request,'User/HomePage.html')

def Complaint(request):
    if request.method == "POST":
        title=request.POST.get('txt_title')
        description=request.POST.get('txt_description')
        userdata=tbl_user.objects.get(id=request.session["uid"])
        
        tbl_complaint.objects.create(complaint_title=title,complaint_description=description,user_id=userdata,
                                     )
        return render(request,'User/Complaint.html',{"msg":"data inserted"})
    else:
        return render(request,'User/Complaint.html')

def Request(request):
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    requestdata=tbl_request.objects.all()
    if request.method == "POST":
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        todate=request.POST.get('txt_date')
        userdata=tbl_user.objects.get(id=request.session["uid"])

        tbl_request.objects.create(request_title=title,request_content=content,place_id=place,request_todate=todate,user_id=userdata)
        return render(request,'User/request.html',{'msg':"data inserted"})
    else:
        return render(request,'User/request.html',{'district':district,'place':place,'requestdata':requestdata})
    
def ViewDonationRequest(request):
    requestdata=tbl_donationrequest.objects.all()
    return render(request,'User/ViewDonationRequest.html',{'requestdata':requestdata})

def ViewItem(request,id):
    itemdata=tbl_donationitems.objects.all()
    return render(request,'User/ViewItem.html',{'itemdata':itemdata})

def Donate(request,id):
    item=tbl_donationitems.objects.get(id=id)
    userdata=tbl_user.objects.get(id=request.session["uid"])
    volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"])
    if request.method == "POST":
        type=request.POST.get("txt_type")
        remark=request.POST.get("txt_remark")
        amount=request.POST.get("txt_amount")

     
        tbl_donation.objects.create(donation_type=type,donation_remark=remark,
                                    donation_amount=amount,user_id=userdata,
                                    volunteer_id=volunteerdata,donationitem_id=item)
        return render(request,'User/Donate.html',{'msg':"Donation Success"})
    else:
        return render(request,'User/Donate.html',{'userdata':userdata,'volunteerdata':volunteerdata})
    