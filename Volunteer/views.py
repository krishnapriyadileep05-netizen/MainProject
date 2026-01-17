from django.shortcuts import render,redirect
from Guest.models import *
from Volunteer.models import *
from User.models import *


# Create your views here.

def logout(request):
    del request.session["vid"]
    return redirect("Guest:Login")

def HomePage(request): 
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        return render(request,'Volunteer/HomePage.html')

def MyProfile(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"])
        return render(request,'Volunteer/MyProfile.html',{"vdata":volunteerdata})

def EditProfile(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        vdata=tbl_volunteer.objects.get(id=request.session["vid"])
        if request.method == "POST":
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            address=request.POST.get('txt_address')

            vdata.volunteer_name=name
            vdata.volunteer_email=email
            vdata.volunteer_contact=contact
            vdata.volunteer_address=address
            vdata.save()
            return render(request,'Volunteer/EditProfile.html',{'msg':'updated'})
        else:
            return render(request,'Volunteer/EditProfile.html',{'vdata':vdata})


def ChangePassword(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        vdata=tbl_volunteer.objects.get(id=request.session["vid"])
        vpassword=vdata.volunteer_password

        if request.method == "POST":
            old=request.POST.get('txt_password')
            new=request.POST.get('txt_new')
            retype=request.POST.get('txt_retype')

            if vpassword==old:    
                if new==retype:
                    vdata.volunteer_password=new
                    vdata.save()
                    return render(request,'Volunteer/ChangePassword.html',{"msg":"Password Updtaed"})
                else:
                    return render(request,'Volunteer/ChangePassword.html',{"msg1":"Password Mismatch"})
            else:
                return render(request,'Volunteer/ChangePassword.html',{"msg1":"Password Incorrect"})

        else:   
            return render(request,'Volunteer/ChangePassword.html')
        
def viewrequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        requestdata=tbl_request.objects.all()
        return render(request,'Volunteer/ViewRequest.html',{"requestdata":requestdata})

def join(request,id):
    req= tbl_request.objects.get(id=id)
    volunteer=tbl_volunteer.objects.get(id=request.session["vid"])
    response=tbl_response.objects.filter(request_id=req,volunteer_id=volunteer).count()
    if response>0:
        return render(request,'Volunteer/ViewRequest.html',{'msg':'Already Joined'})
    else:
        tbl_response.objects.create(request_id=req,volunteer_id=volunteer)
        return render(request,'Volunteer/ViewRequest.html',{'msg':'Join Request Sended'})
    
def ViewDonationRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    else:
        requestdata=tbl_donationrequest.objects.all()
        return render(request,'Volunteer/ViewDonationRequest.html',{'requestdata':requestdata})
        
def ViewItem(request,id):
    itemdata=tbl_donationitems.objects.all()
    return render(request,'Volunteer/ViewItem.html',{'itemdata':itemdata})
    
def Donation(request,id):
    volunteerid=tbl_volunteer.objects.get(id=request.session["vid"])
    itemid=tbl_donationitems.objects.get(id=id)
    if request.method == "POST":
        type=request.POST.get("txt_type")
        remark=request.POST.get("txt_remark")
        amount=request.POST.get("txt_amount")
        
        tbl_donation.objects.create(donation_type=type,donation_remark=remark,donation_amount=amount,volunteer_id=volunteerid,donationitem_id=itemid)

        return render(request,'Volunteer/Donation.html',{'msg':'Donated'})
    else:
        return render(request,'Volunteer/Donation.html',{'volunteerid':volunteerid})
    
def Complaint(request):
    if "vid" in request.session:
        volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"]) 
        complaintdata=tbl_complaint.objects.filter(volunteer_id=request.session["vid"])
        if request.method == "POST":
            title=request.POST.get('txt_title')
            description=request.POST.get('txt_description')
            tbl_complaint.objects.create(complaint_title=title,complaint_description=description,volunteer_id=volunteerdata)
            return render(request,'Volunteer/Complaint.html',{"msg":"data inserted"})
        else:
            return render(request,'Volunteer/Complaint.html',{'volunteerdata':volunteerdata,'complaintdata':complaintdata})
    else:
        return render(request,"Guest/Login.html")
    
def ViewMyTask(request):
    responsedata=tbl_response.objects.filter(id=request.session["vid"])
    return render(request,'Volunteer/ViewMyTask.html',{'responsedata':responsedata})

def Accepted(request,id):
    adata=tbl_response.objects.get(id=id)
    adata.response_status=1
    adata.save()
    return redirect('Volunteer:ViewMyTask')

def InProgress(request,id):
    indata=tbl_response.objects.get(id=id)
    indata.response_status=2
    indata.save()
    return redirect('Volunteer:ViewMyTask')

def Completed(request,id):
    cdata=tbl_response.objects.get(id=id)
    cdata.response_status=3
    cdata.save()
    return redirect('Volunteer:ViewMyTask')

    
    