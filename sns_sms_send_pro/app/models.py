from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
import boto3
# Create your models here.

# Extended user model , I am using authemail package to extend the user
class MyUser(EmailAbstractUser):
    contact_number = models.CharField('contact',max_length=243,blank=True, null=True)

    objects = EmailUserManager()
    

class questionModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    question = models.CharField(max_length=243,blank=True, null=True)
    answer = models.CharField(max_length=243,blank=True, null=True)
    questioned_date = models.DateTimeField(auto_now_add=True)
    answered_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question    

    def __str__(self):
        return self.answer

    def __Unicode__(self):
        return self.user    

# signal to perform post_save operation on question add and answer add
def save_question(sender,**kwargs):
    obj = kwargs['instance']
    question = obj.question
    answer = obj.answer
    user = obj.user
    
    # aws credentials 
    aws_id = "<aws_id>"
    aws_secret = "<aws_secret>"
    region = '<aws_region>'

    sns =  boto3.client(
		'sns',
		aws_access_key_id = aws_id,
		aws_secret_access_key = aws_secret,
		region_name=region				
	)
    try:
        user = get_user_model().objects.get(email=user)
        contact_number = user.contact_number #fetching user contact number from user model
        u_contact = '+91'+contact_number 
        print(u_contact)

        print(user)
        if answer == "" and question == "":
            print("fields are empty")
        elif answer != "" and question != "":

            # publishing or sending sms using sns service by passing users phone number
            sns.publish(PhoneNumber=u_contact,Message=answer)
            print("from admin answers to the user")
        elif question != "":
            print("user asks question to the admin")
        else:
            print("answer to the user from admin") 
    except get_user_model().DoesNotExist:
        print('------')

post_save.connect(save_question,sender=questionModel)