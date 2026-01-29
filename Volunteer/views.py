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

def Donate(request, id):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    item = tbl_donationitems.objects.get(id=id)
    vdata = tbl_volunteer.objects.get(id=request.session["vid"])

    if request.method == "POST":
        dtype = request.POST.get("txt_type")
        remark = request.POST.get("txt_remark")
        amount = request.POST.get("txt_amount")
        donated = int(amount)

        if dtype == "Money":
            request.session["donation_data"] = {
                "donation_type": dtype,
                "donation_remark": remark,
                "donation_amount": donated,
                "volunteer_id": vdata.id,
                "donationitem_id": item.id
            }
            return redirect("Volunteer:Payment")

        else:
            tbl_donation.objects.create(
                donation_type=dtype,
                donation_remark=remark,
                donation_amount=donated,
                volunteer_id=vdata,
                donationitem_id=item,
            )
            return render(request,'Volunteer/Donation.html',{
                'msg': "Donation Success"
            })

    return render(request,'Volunteer/Donation.html',{
        'item': item
    })

def PaymentPage(request):
    donation_data = request.session.get("donation_data")
    if not donation_data:
        return redirect("Volunteer:HomePage") 

    if request.method == "POST":
        tbl_donation.objects.create(
            donation_amount=donation_data["donation_amount"],
            volunteer_id=tbl_volunteer.objects.get(id=donation_data["volunteer_id"]),
            donationitem_id=tbl_donationitems.objects.get(id=donation_data["donationitem_id"]),
        )
        del request.session["donation_data"]

        return  redirect("Volunteer:DonationPayment")

    return render(request, "Volunteer/Payment.html", {"donation": donation_data})

def DonationPayment(request):
    vdata=tbl_volunteer.objects.get(id=request.session["vid"])
    if request.method =="POST":
        amount=request.POST.get("txt_amount")
        payment=tbl_payment.objects.create(payment_amount=amount,volunteer_id=vdata)
        return render(request,'Volunteer/Payment_suc.html',{'msg':"Donation Success",'payment':payment})
    else:
        return render(request,"Volunteer/Payment.html",{"vdata":vdata})
    
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

def VolunteerCollectionRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    requests = tbl_collectionrequest.objects.filter(donation_id__user_id__place__district=volunteer.place.district)

    return render(request,"Volunteer/ViewCollectionRequest.html",{'requests':requests})


def MyCollectionRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    requests = tbl_collectionrequest.objects.filter(volunteer_id=volunteer)
    return render(request,"Volunteer/MyCollectionRequest.html",{'requests':requests})


def TakeRequest(request, id):
  
    req = tbl_collectionrequest.objects.get(id=id)

    if req.status == 0:
        req.volunteer_id = tbl_volunteer.objects.get(id=request.session["vid"])
        req.status = 1
        req.save()

    return redirect("Volunteer:VolunteerCollectionRequest")


def updatestatus(request,id,status):
  
    req = tbl_collectionrequest.objects.get(id=id)
    req.status = status
    req.save()
    return redirect("Volunteer:MyCollectionRequest")


def Team(request):
    teamdata=tbl_team.objects.all()
    volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"])
    if request.method == "POST":
     name=request.POST.get("txt_name")
     photo=request.FILES.get("file_photo")
     gender=request.POST.get("txt_gender")
     dob=request.POST.get("txt_date")
     contact=request.POST.get("txt_contact")
     
     tbl_team.objects.create(team_name=name,team_photo=photo,team_gender=gender,team_dob=dob,team_contact=contact,volunteer_id=volunteerdata)
     return render(request,"Volunteer/Team.html",{'msg':'Inserted'})
    else:
        return render(request,"Volunteer/Team.html",{'teamdata':teamdata})
    
def delteam(request,id):
    team=tbl_team.objects.get(id=id).delete()
    return redirect("Volunteer:Team")
        
