from django.contrib import admin
from user.models import MasterContents,heavyvehivalregistrationImages,Request_Heavy_VehicalImages, Device,Request_labour_contructor, Request_SubContractor, labour_contructor, heavyvehivalregistration,Request_driver_Operator,Request_Heavy_Vehical, driveroperatorregistration, subcontractorregistration, Requirement, VedioUplaod

admin.site.register(Device)
admin.site.register(heavyvehivalregistrationImages)
admin.site.register(Request_Heavy_VehicalImages)


class VedioUploadAdmin(admin.ModelAdmin):
    list_display = ['Id', 'image_uplaod', 'vediourl']
admin.site.register(VedioUplaod, VedioUploadAdmin)


class requestrequirementAdmin(admin.ModelAdmin):
    list_display = ['Id', 'title', 'description', 'requirement_image']
admin.site.register(Requirement,requestrequirementAdmin)


class reqeustheavyvehicalAdmin(admin.ModelAdmin):
    list_display = ['Id', 'vehical_name','company_name','manufacture_date','vehiclemodelnumber', 'ownername','alternativemobilenumber','created_by', 'is_active']

admin.site.register(Request_Heavy_Vehical,reqeustheavyvehicalAdmin)


#admin.site.register(subcontractorregistration)




class labourcontractoradmin(admin.ModelAdmin):
    list_display = ['Id','labourcontractorname', 'labourwork', 'lobourinnumber', 'mobile_number','alternativemobilenumber', 'labour_image','created_by', 'is_active']

admin.site.register(labour_contructor,labourcontractoradmin)

class Request_labour_contructorAdmin(admin.ModelAdmin):
        list_display = ['Id','labourcontractorname', 'labourwork', 'lobourinnumber', 'mobile_number','alternativemobilenumber', 'labour_image','created_by', 'is_active']

admin.site.register(Request_labour_contructor,Request_labour_contructorAdmin)

class heavyvehivalregistrationAdmin(admin.ModelAdmin):
    list_display = ['Id', 'vehical_name','company_name','vehiclemodelnumber', 'manufacture_date', 'ownername','alternativemobilenumber','created_by', 'is_active']

admin.site.register(heavyvehivalregistration,heavyvehivalregistrationAdmin)


class subcontractorregistrationAdmin(admin.ModelAdmin):
    list_display = ['Id', 'contractorname', 'firmname','typeofwork', 'expriencesinyear','mobilenumber', 'license_number', 'subcontractor_image','created_by', 'is_active']
admin.site.register(subcontractorregistration, subcontractorregistrationAdmin)

class Request_SubContractorAdmin(admin.ModelAdmin):
        list_display = ['Id', 'contractorname', 'firmname','typeofwork', 'expriencesinyear','mobilenumber', 'license_number', 'subcontractor_image','created_by', 'is_active']
admin.site.register(Request_SubContractor,Request_SubContractorAdmin)

class driveroperatorregistrationAdmin(admin.ModelAdmin):
    list_display = ['Id', 'vehicalname', 'expriencesinyear', 'driveroperatorname', 'mobilenumber', 'alternet_mobilenumber', 'heavy_license','driver_image','license_image','created_by', 'is_active']
admin.site.register(driveroperatorregistration, driveroperatorregistrationAdmin)


class Request_driver_OperatorAdmin(admin.ModelAdmin):
    list_display = ['Id', 'vehicalname', 'expriencesinyear', 'driveroperatorname','mobilenumber', 'alternet_mobilenumber', 'license_number','driver_image','license_image','created_by', 'is_active']
admin.site.register(Request_driver_Operator,Request_driver_OperatorAdmin)


class MasterContentsAdmin(admin.ModelAdmin):
    list_display = ['Id','key','value','relate_to']

admin.site.register(MasterContents, MasterContentsAdmin)
