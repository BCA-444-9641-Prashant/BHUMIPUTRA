from django.db import models

class Scheme(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    description = models.TextField()
    photo = models.ImageField(upload_to='schemes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    temperature = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    water_level = models.CharField(max_length=100)
    market_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_rent', 'On Rent'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='equipment/', blank=True, null=True)
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=1)
    total_quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def is_available(self):
        return self.quantity_available > 0 and self.status == 'available'
    
    def save(self, *args, **kwargs):
        # Ensure quantities are integers
        try:
            if self.quantity_available is None:
                self.quantity_available = 1
            if self.total_quantity is None:
                self.total_quantity = 1
                
            self.quantity_available = int(self.quantity_available)
            self.total_quantity = int(self.total_quantity)
        except (ValueError, TypeError):
            self.quantity_available = 1
            self.total_quantity = 1
        
        # Auto-update status based on quantity
        if self.quantity_available == 0:
            self.status = 'on_rent'
        elif self.quantity_available > 0 and self.status == 'on_rent':
            self.status = 'available'
        super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    training_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
