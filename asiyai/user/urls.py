from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from . import views

router = routers.DefaultRouter()

#app_name = "user"
urlpatterns = [
    path('uploadFile', views.uploadFile),
    path('otp-verify', views.verify_mobile_otp),
    path('send-otp', views.send_otp_mobile,name="send-otp"),
    path('access-token', views.access_token),
    path('user/<int:userId>', views.get_user_profile),
    path('user', views.update_user_profile),
    path('master_data', views.get_master_data),
    path('hvbesicdetails', views.hvregistration, name="hvbesicdetails"), 
    path('reqheavyvehicle', views.requesthvregistration),
    path('hvaddress',views.hvadddress),
    path('doregistrations', views.doregistration),
    path('reqdriveroperator', views.requestdoperator),
    path('subcregistration', views.subcregistration),
    path('reqsubcontractor', views.reqsubcon),
    path('lacoregistration', views.lacoregistration),
    path('reqlacontractor', views.requestlacontractor),
    path('logout', views.logout),
    path('filter_data', views.filter_data),
    path('listrequirement/', views.ProfileView, name="list" ),
    path('images/', views.ImageView.as_view(), name="images"),
    ########### url heavy vehicle registration ###################
    path('dashboard',views.dashboard, name="dashboard"),
    path('finaldashboard',views.finaldashboard, name="finaldashboard"),
    #path('showhv/', views.showhv, name="hvregistration"),
    path('showlist', views.showlist, name="showlist"),
    path('hvdetails/<str:Id>', views.showhvone, name="hvdetails"),
    ##############driver operator url ##########
    path('dolist', views.drlist, name="dolist"),
    path('dosingle/<str:Id>', views.showdrone, name="dosingle"),

    ################ subcontructor url ####################
    path('sublist',views.subconlist,name="sublist"),
    path('subsingle/<str:Id>', views.subsingle, name='subsingle'),

    ##############Labour contructor url #########
    path('lablist', views.labourlist, name="lablist"),
    path('labsingle/<str:Id>', views.laboursingle, name="labsingle"),

################################# Category url ###############
    path('category', views.category, name="category"),
    path('notification', views.notification, name="notification"),

    path('test', views.test,name='test'),
    path('sendotp', views.sendotp,name="sendotp"),
    path('verifyotp', views.verifyotp, name="verifyotp"),
    path('account',views.account, name="account"),

    ##############choose language url##############
    path('chooselanguage',views.chooselanguage,name="chooselanguage"),
    path('firstenglish', views.firstenglish,name="firstenglish"),
    path('secondenglish',views.secondenglish,name="secondenglish"),
    path('home',views.home, name="home"),

    ############### choose profile ########
    path('profile',views.profile, name="profile"),
    path('normaluser', views.normaluser,name="normaluser"),


    ########## search fileter ######
    path('search',views.search,name='search'),
    path("test",views.test,name="test"),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

