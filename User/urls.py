from django.urls import path,include
from User import views
app_name="User"


urlpatterns = [
    path("MyProfile/",views.MyProfile,name="MyProfile"),
    path("EditProfile/",views.EditProfile,name="EditProfile"),
    path("ChangePassword/",views.ChangePassword,name="ChangePassword"),
    path("HomePage/",views.HomePage,name="HomePage"),
    path("Complaint/",views.Complaint,name="Complaint"),
    path("Request/",views.Request,name="Request"),
    path("ViewDonationRequest/",views.ViewDonationRequest,name="ViewDonationRequest"),
    path("ViewItem/<int:id>",views.ViewItem,name="ViewItem"),
    path("Donate/<int:id>",views.Donate,name="Donate"),
    path("logout/",views.logout,name="logout"),


]