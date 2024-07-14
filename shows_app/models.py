from datetime import datetime
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ShowManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data["title"]) < 2:
            errors['title']="Title is required and should be more than 2 characters."
        if len(post_data["network"]) <3:
            errors['network'] = "Network is required and should be more than 3 characters."
        if len(post_data["description"]) > 0 and len(post_data["description"]) <10:
            errors["description"] = "Description is optionial but if it's present should be more than 10 characters."
        if post_data["release_date"]:
            try:
                release_date = datetime.strptime(post_data["release_date"], '%Y-%m-%d')
                if release_date > datetime.now():
                    errors["release_date"] = "Release date can not be in the future."
            except ValueError:
                errors["release_date"] = "Release date must be in YYYY-MM-DD format." 
            
            
        return errors
        
    

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ShowManager()
    
    @classmethod
    def get_all_shows(cls):
        return cls.objects.all()
    
    @classmethod
    def new_show(cls, data):
        return cls.objects.create(title=data['title'], network=data['network'], release_date=data['release_date'], description=data['description'])
    
    @classmethod
    def get_one_show(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def update_show(cls, data):
        show = cls.get_one_show(data['id'])
        if show:
            show.title = data['title']
            show.network = data['network']
            show.release_date = data['release_date']
            show.description = data['description']
            show.save()  
            return show
        return None
    
    @classmethod
    def delete_show(cls, id):
        show = cls.get_one_show(id=id)
        if show:
            show.delete()
            return True
        return False
    
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data["firstName"]) <2 or len(post_data["lastName"]) <2:
            errors['name'] = "First name and last name should be more than 2 characters"
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["email"] = "Invalid email format"
        if len(post_data['password']) < 8:
            errors['password'] = "Password should be more than 8 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = "Password and conform password must match!"
        if post_data.get("birthday"):
            try:
                birthday = datetime.strptime(post_data["birthday"], '%Y-%m-%d')
                if birthday > datetime.now():
                    errors["birthday"] = "Birthday cannot be in the future."
                
                # Calculate age
                today = datetime.now()
                age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
                
                if age < 13:
                    errors["birthday"] = "You should be at least 13 years old to register."
            except ValueError:
                errors["birthday"] = "Birthday must be in YYYY-MM-DD format."
            
        return errors
    
class User(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    
    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)
    
    @classmethod
    def destroy(cls, id):
        cls.objects.get(id=id).delete()
    
    @classmethod
    def add(cls, data):
        return cls.objects.create(firstName = data["firstName"], lastName = data["lastName"], email = data["email"], birthday = data["birthday"], password = data["password"])
    
    
    
