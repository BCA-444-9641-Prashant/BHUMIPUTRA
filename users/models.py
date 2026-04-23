from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username

class Farm(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    crop = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    water_source = models.CharField(max_length=100)
    farm_status = models.CharField(max_length=50, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer.username}'s Farm - {self.location}"

class EquipmentOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey('adminpanel.Equipment', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total_days = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.quantity} units)"
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            # Ensure dates are date objects, not strings
            if isinstance(self.start_date, str):
                from datetime import datetime
                self.start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            if isinstance(self.end_date, str):
                from datetime import datetime
                self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            
            # Calculate total days
            self.total_days = (self.end_date - self.start_date).days + 1
            
            # Ensure rent_per_day is treated as a number
            rent_per_day = float(self.equipment.rent_per_day) if self.equipment.rent_per_day else 0
            self.total_cost = self.total_days * rent_per_day * self.quantity
        super().save(*args, **kwargs)

class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('adminpanel.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class CropSell(models.Model):
    GRADE_CHOICES = [
        ('A', 'Grade A - Premium Quality'),
        ('B', 'Grade B - Good Quality'),
        ('C', 'Grade C - Standard Quality'),
        ('D', 'Grade D - Basic Quality'),
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    photo = models.ImageField(upload_to='crops/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(help_text="Quantity in kg")
    description = models.TextField(blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Crop for Sale"
        verbose_name_plural = "Crops for Sale"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer.username} - {self.name} ({self.grade})"
    
    @property
    def total_value(self):
        return self.price * self.quantity


class CropOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_orders')
    crop = models.ForeignKey(CropSell, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity in kg")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Crop Order"
        verbose_name_plural = "Crop Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username} - {self.crop.name}"
    
    @property
    def is_delivered(self):
        return self.status == 'Delivered'
    
    @property
    def is_pending(self):
        return self.status == 'Pending'
