from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics,status 
from app.models import questionModel
from rest_framework.response import Response
from app.serializers import QuestionSerializer,SignupSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

User = get_user_model()

# Create your views here.
class QuestionView(generics.CreateAPIView):
    queryset = questionModel.objects.all()
    serializer_class = QuestionSerializer

class QuestionListView(generics.ListAPIView):
    queryset = questionModel.objects.all()
    serializer_class = QuestionSerializer

# Register user to add question
class SignupUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            email = serializer.data['email']
            password = serializer.data['password']
            contact_number = serializer.data['contact_number']

            user = authenticate(username=email,password=password)

            if user is None:
                password = password
                user_save = User(first_name=first_name,last_name=last_name,email=email,contact_number=contact_number)
                user_save.set_password(password)
                user_save.save()
                content = {'message':'user registered'}
                return Response(content,status=status.HTTP_201_CREATED)
            
            content = {'message':'User already exists'}
            return Response(content,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    