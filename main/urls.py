from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("newsletter", views.newsletter, name="newsletter"),
    path("Support A Cause", views.support, name="SupportACause"),
    path("Members", views.members, name="Members"),
    path("Service", views.service, name="Service"),
    # path("Our Teams", views.ourteam, name="Our Teams"),
    path("About", views.about, name="Helping Hands About"),
    path("Partners Collaborators", views.partners, name="Partners Collaborators"),
    path("Join Us", views.joinus, name="Join Us"),
    path("Contact", views.contact, name="contact"),
    

]