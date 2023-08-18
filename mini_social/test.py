from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from random import randint

def current_year(request):
    template = loader.get_template("home.html") 
    current_year = datetime.now().year
    return HttpResponse(template.render({
        'current_year': current_year},
        request))



    
current_year = datetime.now().year
print(current_year)


        