from django.db import models

# Create your models here.

class Supervisor(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    supervisor = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, default='NULL')
    supervisor = models.BooleanField(default=False, null=True)    

class TravelAuthForm(models.Model):
    today_date = models.DateField()
    #submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, db_column='submitted_by', null=True)
    signature = models.CharField(max_length=100)
    date_of_travel_from_date = models.DateField()
    date_of_travel_to_date = models.DateField()
    conference_name = models.CharField(max_length=200)
    conference_location = models.CharField(max_length=100)
    reason_for_travel = models.TextField()
    people_travelling = models.DecimalField(max_digits=10, decimal_places=2)
    hotel_cost = models.DecimalField(max_digits=10, decimal_places=2)
    conference_registration_cost = models.DecimalField(max_digits=10, decimal_places=2)
    airfare_train_cost = models.DecimalField(max_digits=10, decimal_places=2)
    car_rental_cost = models.DecimalField(max_digits=10, decimal_places=2)
    other_misc_costs = models.DecimalField(max_digits=10, decimal_places=2)
    total_estimated_costs = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField()
    supervisor = models.CharField(max_length=100)
    associate_director = models.CharField(max_length=100)  
    first_approval = models.BooleanField(default=False)
    second_approval = models.BooleanField(default=False)
    final_approval_status = models.CharField(max_length=10, choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], null=True)
  

class Person(models.Model):
    travel_auth_form = models.ForeignKey(TravelAuthForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()    