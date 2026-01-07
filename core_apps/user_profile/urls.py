from django.urls import path

from .views import (
    NextOfKinDetailsAPIView,
    NextOfKingAPIView,
    ProfileListAPiView,
    ProfileDetailView
)

urlpatterns = [
    path("all/", ProfileListAPiView.as_view(), name="all_profiles"),
    path("my-profile/", ProfileDetailView.as_view(), name="profile_detail"),
    path("my-profile/next-of-kin/", NextOfKingAPIView.as_view(), name="next_of_kin_list"),
    path("my-profile/next-of-kin/<uuid:pk>/", NextOfKinDetailsAPIView.as_view(), name="next_of_king_detail"),
]
