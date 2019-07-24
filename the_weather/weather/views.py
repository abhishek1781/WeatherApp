import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ae5ff5bfff03b96e55056ae0a43bca61'
    
    err_msg = ''
    message = ''
    message_class = ''
   
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
             new_city = form.cleaned_data['name']
             existing_city_count = City.objects.filter(name=new_city).count()
             if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json() 
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'  
             else:
                err_msg = 'City Already Exists in the Database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else :
            message = 'City added successfuly!'
            message_class = 'is-success'
    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for c in cities:

        r = requests.get(url.format(c)).json()

        city_weather = {
            'city' : c.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message': message,
        'message_class' : message_class
        }
    return render(request, 'weather/weather.html', context)


def delete_city(request,city_name):
    present_count = City.objects.filter(name=city_name).count()
    if present_count == 1:
        City.objects.get(name=city_name).delete()
    return redirect('home')