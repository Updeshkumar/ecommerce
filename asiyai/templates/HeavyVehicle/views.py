from django.shortcuts import render
from ...heavyvehicle.models import heavyvehicle, Country, State, District, heavyvehicleimage
#from accounts.forms import UserImageForm  
from ...heavyvehicle.forms import ImageForm

def hvregistration(request):
    if request.method=="POST":
        if request.POST.get('vehiclename') and  request.POST.get('companyname')and request.POST.get('vehiclenumber')and request.POST.get('modelnumber')and request.POST.get('ownername')and  request.POST.get('aadharnumber')and request.POST.get('manufectoringdate'):
            db = heavyvehicle()
            db.vehiclename = request.POST.get('vehiclename')
            db.companyname = request.POST.get('companyname')
            db.vehiclenumber = request.POST.get('vehiclenumber')
            db.modelnumber = request.POST.get('modelnumber')
            db.ownername = request.POST.get('ownername')
            db.aadharnumber = request.POST.get('aadharnumber')
            db.manufectoringdate = request.POST.get('manufectoringdate')
            db.save()               
            return render(request, 'HeavyVehicle/form1.html')
    else:
        return render(request, 'HeavyVehicle/form.html')

def dependantfield(request):
        countryid = request.GET.get('country', None)
        stateid = request.GET.get('state', None)
        state = None
        district = None
        if countryid:
            getcountry = Country.objects.get(id=countryid)
            state = State.objects.filter(country=getcountry)
        if stateid:
            getstate = State.objects.get(id=stateid)
            district = District.objects.filter(state=getstate)
        country = Country.objects.all()
        return render(request, 'HeavyVehicle/form1.html', locals())

def hv_images(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, 'HeavyVehicle/form2.html', {'obj': obj})
    else:  
        form = ImageForm()
        img=heavyvehicleimage.objects.all()
    return render(request, "HeavyVehicle/form2.html", {"img": img, "form": form}) 

