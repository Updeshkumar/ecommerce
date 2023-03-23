from django.db import models
from rest_framework import status
#from config.configConstants import UserType
from config.configConstants import UserType


class MasterContents(models.Model):
    Id = models.AutoField(primary_key=True)
    key = models.CharField(max_length = 200)
    value = models.CharField(max_length = 200)
    relate_to = models.IntegerField()
    class Meta:
        db_table = 'user_mastercontents'

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    country_code = models.IntegerField(91, null=True,blank=True)
    mobile_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=4,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(default=False, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20,null=False,blank=False, default="USER")
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=1,null=False)
    is_delete = models.BooleanField(default=0,null=False)
    gender = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'user'

#  This class is use for create the preference model
class Device(models.Model):

    device_id = models.AutoField(primary_key=True)
    refresh_token = models.CharField(max_length=500,default=False, null=True)
    device_type = models.CharField(max_length=20)
    device_token = models.CharField(max_length=255,default=False, null=True)
    aws_arn = models.CharField(max_length=255, null=True)
    created_by =  models.ForeignKey(User, db_column = 'created_by',related_name='device_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=1,null=False)
    
    class Meta:
        db_table = 'device'


#  labour contracot registrations

class labour_contructor(models.Model):
    Id = models.AutoField(primary_key=True)
    labourcontractorname = models.CharField(max_length=300)
    labourwork = models.CharField(max_length=200)
    emailId = models.CharField(max_length=100)
    lobourinnumber = models.CharField(max_length=500)
    mobile_number = models.CharField(max_length=12)
    skilledlabour =  models.IntegerField(null=False,blank=False)
    unskilledlabour = models.IntegerField(blank=False)
    professionallabour = models.IntegerField(null=False)
    Aadharnumberfrontimage = models.CharField(max_length=25)
    alternativemobilenumber = models.CharField(max_length=15)
    Aadharnumberbackimage = models.CharField(max_length=25)
    labour_image = models.CharField(max_length=500)
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)
    class Meta:
        db_table = 'labour_contructor'


            # ###################Heavy Vehical Registrations #####################


class heavyvehivalregistration(models.Model):
    Id = models.AutoField(primary_key=True, )
    vehical_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length = 100)
    emailId = models.CharField(max_length=100)
    ownername = models.CharField(max_length=300)
    vehicleregistrationnumber = models.CharField(max_length=20)
    Aadharnumberfrontimage = models.CharField(max_length=25)
    Aadharnumberbackimage = models.CharField(max_length=25)
    vehicle_image = models.FileField(max_length=1000)
    manufacture_date = models.CharField(max_length=100)
    alternativemobilenumber = models.CharField(max_length=20)
    vehiclemodelnumber = models.CharField(max_length=50)
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "heavyvehivalregistration"




class heavyvehivalregistrationImages(models.Model):
    id = models.AutoField(primary_key=True, )
    regId = models.IntegerField()
    images = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    class  Meta:
        db_table = "heavyvehivalregistrationImages"
    


#############driver operator registrations class #####################

class driveroperatorregistration(models.Model):
    Id = models.AutoField(primary_key=True, )
    vehicalname = models.CharField(max_length=200)
    expriencesinyear = models.IntegerField(blank=False, null=False)
    driveroperatorname = models.CharField(max_length=200)
    mobilenumber = models.CharField(max_length=20)
    alternet_mobilenumber = models.CharField(max_length=20)
    heavy_license = models.CharField(max_length=100)
    emailId = models.CharField(max_length=100)
    Aadharnumberfrontimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    Aadharnumberbackimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    driver_image = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    license_image = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "driveroperatorregistration"

#############Sub contractor  registrations class #####################

class subcontractorregistration(models.Model):
    Id = models.AutoField(primary_key=True, )
    contractorname = models.CharField(max_length=100)
    firmname = models.CharField(max_length=500)
    typeofwork = models.CharField(max_length=100)
    emailId = models.CharField(max_length=50)
    expriencesinyear = models.IntegerField(blank=False, null=False)
    license_number = models.CharField(max_length=50)
    Aadharnumberfrontimage = models.CharField(max_length=25)
    Aadharnumberbackimage = models.CharField(max_length=25)
    mobilenumber = models.CharField(max_length=20)
    subcontractor_image = models.FileField(max_length=500)
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "subcontractorregistration"
        
        
class Request_SubContractor(models.Model):
    Id = models.AutoField(primary_key=True, )
    contractorname = models.CharField(max_length=100)
    firmname = models.CharField(max_length=500)
    expriencesinyear = models.IntegerField(blank=False, null=False)
    license_number = models.CharField(max_length=50)
    typeofwork = models.CharField(max_length=50)
    mobilenumber = models.CharField(max_length=50)

    subcontractor_image = models.CharField(max_length=500, blank=True, null=True)
    Aadharnumberfrontimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    Aadharnumberbackimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "request_subcontractor"
        
        
class Requirement(models.Model):
    Id = models.AutoField(primary_key=True, )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    requirement_image = models.CharField(max_length=500)
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    #image = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "requirement"
        
class VedioUplaod(models.Model):
    Id = models.AutoField(primary_key=True)
    image_uplaod = models.CharField(max_length=500)
    vediourl = models.CharField(max_length=100)
    class Meta:
        db_table = "vedioupload"


        
        
################# Request Api ###############

class Request_Heavy_Vehical(models.Model):
    Id = models.AutoField(primary_key=True, )
    vehical_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    vehical_number = models.CharField(max_length=500)
    ownername = models.CharField(max_length=300)
    alternativemobilenumber = models.CharField(max_length=20)
    vehicle_image =  models.CharField(max_length=255, blank=True, null=True)
    manufacture_date = models.CharField(max_length=100)
    vehiclemodelnumber = models.CharField(max_length=50)
    Aadharnumberfrontimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    Aadharnumberbackimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")

    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "request_heavy_vehical"

class Request_Heavy_VehicalImages(models.Model):
    id = models.AutoField(primary_key=True, )
    Request_Heavy_Vehical = models.ForeignKey(Request_Heavy_Vehical, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    class  Meta:
        db_table = "Request_Heavy_VehicalImages"



        
class Request_labour_contructor(models.Model):
    Id = models.AutoField(primary_key=True)
    labourcontractorname = models.CharField(max_length=300)
    labourwork = models.CharField(max_length=200)
    lobourinnumber = models.CharField(max_length=12)
    mobile_number = models.CharField(max_length=20)
    alternativemobilenumber = models.CharField(max_length=20)
    labour_image = models.CharField(max_length=500,blank=True, null=True)
    Aadharnumberfrontimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    Aadharnumberbackimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)


    class Meta:
        db_table = 'request_labour_contructor'
        
class Request_driver_Operator(models.Model):
    Id = models.AutoField(primary_key=True, )
    vehicalname = models.CharField(max_length=200)
    expriencesinyear = models.IntegerField(blank=False, null=False)
    driveroperatorname = models.CharField(max_length=200)
    alternet_mobilenumber = models.IntegerField()
    mobilenumber = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50)
    driver_image = models.FileField(max_length=500, blank=True, null=True)
    license_image = models.FileField(max_length=500, blank=True, null=True)
    Aadharnumberfrontimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")
    Aadharnumberbackimage = models.ImageField(upload_to="user/static/Uploaded/UserProfiles/")

    created_by =  models.IntegerField()
    is_active = models.BooleanField(default=1,null=False)

    class Meta:
        db_table = "request_driver_operator"
        
