from rest_framework import serializers
from app.models import questionModel

class QuestionSerializer(serializers.ModelSerializer):
    class Meta():
        model = questionModel
        fields = '__all__'

class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=243,required=False)
    last_name = serializers.CharField(max_length=243,required=False)
    email = serializers.CharField(max_length=243,required=True)
    password  = serializers.CharField(max_length=243,required=True)
    contact_number = serializers.CharField(max_length=243,required=True)