from django.shortcuts import render
from django.views import View #import standard view, get and post purposes

#render default/index.html for the get request
class Index(View):#for get/post
    def get(self, request, *args, **kwargs):#get request
        return render(request, 'default/index.html')

class Music(View):#for get/post
    def get(self, request, *args, **kwargs):#get request
        return render(request, 'default/music.html')

class StressAssessment(View):#for get/post
    def get(self, request, *args, **kwargs):#get request
        return render(request, 'default/stressassessment.html')


