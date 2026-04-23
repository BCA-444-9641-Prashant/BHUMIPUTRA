from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Scheme, Crop, Equipment, Course
from users.models import User, Farm

@csrf_protect
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('adminpanel:admin_dashboard')
                else:
                    messages.error(request, 'Access denied. Admin privileges required.')
            else:
                messages.error(request, 'Invalid username or password')
    return render(request, 'adminpanel/admin_login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    context = {
        'total_users': User.objects.count(),
        'total_farmers': User.objects.filter(role='farmer').count(),
        'total_buyers': User.objects.filter(role='buyer').count(),
        'total_schemes': Scheme.objects.count(),
        'total_crops': Crop.objects.count(),
        'total_equipment': Equipment.objects.count(),
        'total_courses': Course.objects.count(),
        'total_farms': Farm.objects.count(),
    }
    return render(request, 'adminpanel/admin_dashboard.html', context)

@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    users = User.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'adminpanel/user_list.html', {'page_obj': page_obj})

@login_required
def user_create(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                password=password,
                role=role
            )
            messages.success(request, 'User created successfully')
            return redirect('user_list')
    
    return render(request, 'adminpanel/user_create.html')

@login_required
def user_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.role = request.POST.get('role')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request, 'User updated successfully')
        return redirect('user_list')
    
    return render(request, 'adminpanel/user_update.html', {'user': user})

@login_required
def user_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('user_list')

@login_required
def scheme_home(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    return render(request, 'adminpanel/scheme_home.html')

@login_required
def scheme_list(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    schemes = Scheme.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/scheme_list.html', {'schemes': schemes})

@login_required
def scheme_create(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        
        Scheme.objects.create(
            title=title,
            subtitle=subtitle,
            description=description,
            photo=photo
        )
        messages.success(request, 'Scheme created successfully')
        return redirect('adminpanel:scheme_home')
    
    return render(request, 'adminpanel/scheme_create.html')

@login_required
def scheme_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    scheme = get_object_or_404(Scheme, pk=pk)
    if request.method == 'POST':
        scheme.title = request.POST.get('title')
        scheme.subtitle = request.POST.get('subtitle')
        scheme.description = request.POST.get('description')
        if request.FILES.get('photo'):
            scheme.photo = request.FILES.get('photo')
        scheme.save()
        messages.success(request, 'Scheme updated successfully')
        return redirect('adminpanel:scheme_home')
    
    return render(request, 'adminpanel/scheme_update.html', {'scheme': scheme})

@login_required
def scheme_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    scheme = get_object_or_404(Scheme, pk=pk)
    scheme.delete()
    messages.success(request, 'Scheme deleted successfully')
    return redirect('adminpanel:scheme_home')

@login_required
def crop_list(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    crops = Crop.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/crop_list.html', {'crops': crops})

@login_required
def crop_create(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        temperature = request.POST.get('temperature')
        soil_type = request.POST.get('soil_type')
        water_level = request.POST.get('water_level')
        market_price = request.POST.get('market_price')
        image = request.FILES.get('image')
        
        Crop.objects.create(
            name=name,
            description=description,
            temperature=temperature,
            soil_type=soil_type,
            water_level=water_level,
            market_price=market_price,
            image=image
        )
        messages.success(request, 'Crop created successfully')
        return redirect('adminpanel:crop_list')
    
    return render(request, 'adminpanel/crop_create.html')

@login_required
def crop_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        crop.name = request.POST.get('name')
        crop.description = request.POST.get('description')
        crop.temperature = request.POST.get('temperature')
        crop.soil_type = request.POST.get('soil_type')
        crop.water_level = request.POST.get('water_level')
        crop.market_price = request.POST.get('market_price')
        if request.FILES.get('image'):
            crop.image = request.FILES.get('image')
        crop.save()
        messages.success(request, 'Crop updated successfully')
        return redirect('adminpanel:crop_list')
    
    return render(request, 'adminpanel/crop_update.html', {'crop': crop})

@login_required
def crop_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    crop = get_object_or_404(Crop, pk=pk)
    crop.delete()
    messages.success(request, 'Crop deleted successfully')
    return redirect('adminpanel:crop_list')

@login_required
def equipment_list(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    equipment = Equipment.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/equipment_list.html', {'equipment': equipment})

@login_required
@csrf_protect
def equipment_create(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        rent_per_day = float(request.POST.get('rent_per_day', 0))
        photo = request.FILES.get('photo')
        total_quantity = int(request.POST.get('total_quantity', 1))
        quantity_available = int(request.POST.get('quantity_available', 1))
        
        # Validation
        if not name or not description:
            messages.error(request, 'Name and description are required.')
            return render(request, 'adminpanel/equipment_create.html')
        
        if rent_per_day <= 0:
            messages.error(request, 'Rent per day must be greater than 0.')
            return render(request, 'adminpanel/equipment_create.html')
        
        if total_quantity <= 0 or quantity_available < 0:
            messages.error(request, 'Quantities must be positive numbers.')
            return render(request, 'adminpanel/equipment_create.html')
        
        if quantity_available > total_quantity:
            messages.error(request, 'Available quantity cannot be more than total quantity.')
            return render(request, 'adminpanel/equipment_create.html')
        
        Equipment.objects.create(
            name=name,
            description=description,
            rent_per_day=rent_per_day,
            photo=photo,
            total_quantity=total_quantity,
            quantity_available=quantity_available
        )
        messages.success(request, 'Equipment created successfully')
        return redirect('adminpanel:equipment_list')
    
    return render(request, 'adminpanel/equipment_create.html')

@login_required
@csrf_protect
def equipment_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        rent_per_day = float(request.POST.get('rent_per_day', 0))
        total_quantity = int(request.POST.get('total_quantity', 1))
        quantity_available = int(request.POST.get('quantity_available', 1))
        
        # Validation
        if not name or not description:
            messages.error(request, 'Name and description are required.')
            return render(request, 'adminpanel/equipment_update.html', {'equipment': equipment})
        
        if rent_per_day <= 0:
            messages.error(request, 'Rent per day must be greater than 0.')
            return render(request, 'adminpanel/equipment_update.html', {'equipment': equipment})
        
        if total_quantity <= 0 or quantity_available < 0:
            messages.error(request, 'Quantities must be positive numbers.')
            return render(request, 'adminpanel/equipment_update.html', {'equipment': equipment})
        
        if quantity_available > total_quantity:
            messages.error(request, 'Available quantity cannot be more than total quantity.')
            return render(request, 'adminpanel/equipment_update.html', {'equipment': equipment})
        
        equipment.name = name
        equipment.description = description
        equipment.rent_per_day = rent_per_day
        equipment.total_quantity = total_quantity
        equipment.quantity_available = quantity_available
        if request.FILES.get('photo'):
            equipment.photo = request.FILES.get('photo')
        equipment.save()
        messages.success(request, 'Equipment updated successfully')
        return redirect('adminpanel:equipment_list')
    
    return render(request, 'adminpanel/equipment_update.html', {'equipment': equipment})

@login_required
@csrf_protect
def equipment_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    equipment = get_object_or_404(Equipment, pk=pk)
    equipment.delete()
    messages.success(request, 'Equipment deleted successfully')
    return redirect('equipment_list')

@login_required
def course_list(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/course_list.html', {'courses': courses})

@login_required
def course_create(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        training_details = request.POST.get('training_details')
        image = request.FILES.get('image')
        
        Course.objects.create(
            name=name,
            description=description,
            price=price,
            training_details=training_details,
            image=image
        )
        messages.success(request, 'Course created successfully')
        return redirect('adminpanel:course_list')
    
    return render(request, 'adminpanel/course_create.html')

@login_required
def course_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.name = request.POST.get('name')
        course.description = request.POST.get('description')
        course.price = request.POST.get('price')
        course.training_details = request.POST.get('training_details')
        if request.FILES.get('image'):
            course.image = request.FILES.get('image')
        course.save()
        messages.success(request, 'Course updated successfully')
        return redirect('adminpanel:course_list')
    
    return render(request, 'adminpanel/course_update.html', {'course': course})

@login_required
def course_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('course_list')

@login_required
def farm_monitoring(request):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    farms = Farm.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/farm_monitoring.html', {'farms': farms})

@login_required
def farm_update(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    farm = get_object_or_404(Farm, pk=pk)
    if request.method == 'POST':
        farm.location = request.POST.get('location')
        farm.size = request.POST.get('size')
        farm.crop = request.POST.get('crop')
        farm.soil_type = request.POST.get('soil_type')
        farm.water_source = request.POST.get('water_source')
        farm.farm_status = request.POST.get('farm_status')
        farm.save()
        messages.success(request, 'Farm updated successfully')
        return redirect('farm_monitoring')
    
    return render(request, 'adminpanel/farm_update.html', {'farm': farm})

@login_required
def farm_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('adminpanel:admin_login')
    
    farm = get_object_or_404(Farm, pk=pk)
    farm.delete()
    messages.success(request, 'Farm deleted successfully')
    return redirect('farm_monitoring')

def admin_logout(request):
    logout(request)
    return redirect('adminpanel:admin_login')

@csrf_protect
def csrf_test(request):
    if request.method == 'POST':
        return HttpResponse("CSRF Test Successful!")
    return render(request, 'adminpanel/csrf_test.html')
