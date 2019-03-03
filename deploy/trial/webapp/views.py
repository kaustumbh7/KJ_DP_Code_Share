from django.shortcuts import render
from fastai.text import *
from .apps import WebappConfig 

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model_predict import predict 

class call_model(APIView):

    def get(self,request):
        if request.method=='GET':
            params =  request.GET.get('sentence')  
            # sentence = 'I am very happy'
            result = predict(params)
            emotion = 'error'
            if result == '[0]':
                emotion = 'aifa'
            elif result == '[1]':
                emotion = 'disappointed'
            elif result == '[2]':
                emotion = 'excited'
            elif result == '[3]':
                emotion = 'happy'
            elif result == '[4]':
                emotion = 'neutral'             
            #return HttpResponse(params)
            return HttpResponse(emotion)

