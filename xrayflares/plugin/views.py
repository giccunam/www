from django.shortcuts import render
from django.http import HttpResponse
from .models import Flux, MyUser
from .forms import MyUserForm
from datetime import datetime
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
def index(request):
    data = Flux.objects.values()    
    now = datetime.now()
    flux = Flux(now, 1.0,"hello")
    flux.save()
    return HttpResponse(data,content_type='application/json')

class MyUserView(View):
    form_class = MyUserForm
    template_name = 'plugin/info.html'
    initial = {'key': 'value'}  # Reemplaza con los valores que necesites
    
    #http://myservice.com/xrayflares/<id_key>/api/
    def get(self, request, *args, **kwargs): 
        id_key = self.kwargs['id_key']  
        try:
            data = MyUser.objects.get(id=id_key)                        
            form= self.form_class(instance=data)
        except MyUser.DoesNotExist:
            form=self.form_class(initial=self.initial)
            #paciente_count = Paciente.objects.filter().count()
            id_key=0
        return render(request, self.template_name, {'form':form, 'id_key':id_key})
    
    #http://127.0.0.1:8000/plugin/17/api/
    def post(self, request, *args, **kwargs):
        if 'cancel_page_button' in request.POST:
            return HttpResponseRedirect('/cancelar')
        id_key = self.kwargs['id_key']
        if 'save_page_button' in request.POST:
            try:
                instance = MyUser.objects.get(id=id_key)
                form = self.form_class(request.POST or None, instance=instance) 
            except MyUser.DoesNotExist:
                #form=self.form_class(instance=pacient)
                form = self.form_class(request.POST) 
            if form.is_valid():
                myuser = form.save()    
                return render(request, 'plugin/saved.html', {'myuser': myuser})
        return HttpResponseRedirect('/')

                
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyUserView, self).dispatch(*args, **kwargs)


    #return HttpResponse(data,content_type='application/json')

    
