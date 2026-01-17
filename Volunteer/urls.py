from django.urls import path,include
from Volunteer import views

app_name="Volunteer"


urlpatterns = [path("HomePage/",views.HomePage,name="HomePage"),
               path("MyProfile/",views.MyProfile,name="MyProfile"),
               path("EditProfile/",views.EditProfile,name="EditProfile"),
               path("ChangePassword/",views.ChangePassword,name="ChangePassword"),
               path("ViewRequest/",views.viewrequest,name="ViewRequest"),
               path("Join/<int:id>",views.join,name="Join"),
               path("ViewDonationRequest/",views.ViewDonationRequest,name="ViewDonationRequest"),
               path("ViewItem/<int:id>",views.ViewItem,name="ViewItem"),
               path("Donation/<int:id>",views.Donation,name="Donation"),
               path("logout/",views.logout,name="logout"),
               path("Complaint/",views.Complaint,name="Complaint"),
               path("ViewMyTask/",views.ViewMyTask,name="ViewMyTask"),
               path("Accepted/<int:id>",views.Accepted,name="Accepted"),
               path("InProgress/<int:id>",views.InProgress,name="InProgress"),
               path("Completed/<int:id>",views.Completed,name="Completed"),

               ]