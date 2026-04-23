from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from datetime import datetime
import razorpay
from .models import User, Farm, EquipmentOrder, CourseEnrollment, CropSell, CropOrder
from adminpanel.models import Scheme, Crop, Equipment, Course

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Basic validation
        if not username or not email or not password or not role:
            messages.error(request, 'Please fill all required fields')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif len(password) < 4:
            messages.error(request, 'Password must be at least 4 characters')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=name,
                    phone=phone,
                    role=role
                )
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request, str(e))

    
    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
        else:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.role == 'farmer':
                    return redirect('farmer_dashboard')
                elif user.role == 'buyer':
                    return redirect('buyer_dashboard')
                else:
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        
        try:
            user = User.objects.get(username=username, phone=phone)
            return redirect('change_password', username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or phone number')
    
    return render(request, 'users/forgot_password.html')

def change_password(request, username):
    try:
        user = User.objects.get(username=username)
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully. Please login.')
                return redirect('login')
        
        return render(request, 'users/change_password.html', {'username': username})
    
    except User.DoesNotExist:
        messages.error(request, 'Invalid user')
        return redirect('login')

@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        return redirect('login')
    
    farm = Farm.objects.filter(farmer=request.user).first()
    
    # Get course statistics
    user_enrollments = CourseEnrollment.objects.filter(user=request.user)
    completed_courses = user_enrollments.filter(status='Completed').count()
    ongoing_courses = user_enrollments.filter(status='Active').count()
    
    context = {
        'farm': farm,
        'total_schemes': Scheme.objects.count(),
        'total_crops': Crop.objects.count(),
        'total_equipment': Equipment.objects.filter(status='available').count(),
        'total_courses': Course.objects.count(),
        'completed_courses': completed_courses,
        'ongoing_courses': ongoing_courses,
    }
    return render(request, 'users/farmer_dashboard.html', context)

@login_required
def buyer_dashboard(request):
    if request.user.role != 'buyer':
        return redirect('login')
    
    context = {
        'total_crops': Crop.objects.count(),
        'total_equipment': Equipment.objects.filter(status='available').count(),
        'total_courses': Course.objects.count(),
    }
    return render(request, 'users/buyer_dashboard.html', context)

@login_required
def farm_details(request):
    if request.user.role != 'farmer':
        return redirect('login')
    
    farm = Farm.objects.filter(farmer=request.user).first()
    
    if request.method == 'POST':
        if farm:
            farm.location = request.POST.get('location')
            farm.size = request.POST.get('size')
            farm.crop = request.POST.get('crop')
            farm.soil_type = request.POST.get('soil_type')
            farm.water_source = request.POST.get('water_source')
            farm.farm_status = request.POST.get('farm_status')
            farm.save()
            messages.success(request, 'Farm details updated successfully')
        else:
            Farm.objects.create(
                farmer=request.user,
                location=request.POST.get('location'),
                size=request.POST.get('size'),
                crop=request.POST.get('crop'),
                soil_type=request.POST.get('soil_type'),
                water_source=request.POST.get('water_source'),
                farm_status=request.POST.get('farm_status')
            )
            messages.success(request, 'Farm details created successfully')
        
        return redirect('farm_details')
    
    return render(request, 'users/farm_details.html', {'farm': farm})

@login_required
def scheme_view(request):
    schemes = Scheme.objects.all().order_by('-created_at')
    return render(request, 'users/scheme_view.html', {'schemes': schemes})

@login_required
def scheme_detail(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk)
    return render(request, 'users/scheme_detail.html', {'scheme': scheme})

@login_required
def crop_cards(request):
    crops = Crop.objects.all().order_by('-created_at')
    return render(request, 'users/crop_cards.html', {'crops': crops})

@login_required
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, 'users/crop_detail.html', {'crop': crop})

@login_required
def equipment_list(request):
    equipment = Equipment.objects.filter(status='available').order_by('-created_at')
    orders = EquipmentOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/equipment_list.html', {'equipment': equipment, 'orders': orders})

@login_required
def rent_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        quantity = request.POST.get('quantity', 1)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Validate inputs
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 1
        
        # Validate dates
        if not start_date or not end_date:
            messages.error(request, 'Please select both start and end dates.')
            return redirect('equipment_list')
        
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date_obj > end_date_obj:
                messages.error(request, 'Start date cannot be after end date.')
                return redirect('equipment_list')
                
            if start_date_obj < datetime.now().date():
                messages.error(request, 'Start date cannot be in the past.')
                return redirect('equipment_list')
                
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('equipment_list')
        
        try:
            equipment = get_object_or_404(Equipment, pk=equipment_id)
            
            # Check if equipment is available
            if not equipment.is_available:
                messages.error(request, f'{equipment.name} is currently not available for rent.')
                return redirect('equipment_list')
            
            # Check if enough equipment is available
            if equipment.quantity_available < quantity:
                messages.error(request, f'Only {equipment.quantity_available} units available. Cannot rent {quantity} units.')
                return redirect('equipment_list')
            
            # Create the rental order
            order = EquipmentOrder.objects.create(
                user=request.user,
                equipment=equipment,
                quantity=quantity,
                start_date=start_date_obj,
                end_date=end_date_obj,
                status='confirmed',
                payment_status='paid' if payment_method == 'cod' else 'pending'
            )
            
            if payment_method == 'cod':
                # Update equipment quantity immediately for COD
                equipment.quantity_available -= quantity
                equipment.save()
                messages.success(request, f'Successfully rented {quantity} unit(s) of {equipment.name} from {start_date} to {end_date}. Total cost: ₹{order.total_cost}')
                return redirect('order_history')
            else:
                # Redirect to Razorpay payment
                return redirect('razorpay_payment', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Error processing rental: {str(e)}')
            return redirect('equipment_list')
    
    return redirect('equipment_list')

@login_required
def razorpay_payment(request, order_id):
    order = get_object_or_404(EquipmentOrder, pk=order_id, user=request.user)
    
    if order.payment_status == 'paid':
        return redirect('order_history')
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': int(order.total_cost * 100),  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1',
        'notes': {
            'equipment_order_id': order.id,
            'user_id': request.user.id,
            'equipment_name': order.equipment.name
        }
    })
    
    context = {
        'order': order,
        'razorpay_order': razorpay_order,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'callback_url': request.build_absolute_uri('/payment/success/'),
    }
    
    return render(request, 'users/razorpay_payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            # Debug: Print received data
            print("Payment success - POST data:", request.POST)
            
            # Get Razorpay payment details
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            print(f"Payment ID: {payment_id}")
            print(f"Order ID: {order_id}")
            print(f"Signature: {signature}")
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
                
                # Get equipment order from Razorpay order notes
                razorpay_order = client.order.fetch(order_id)
                equipment_order_id = razorpay_order['notes']['equipment_order_id']
                
                # Update equipment order
                order = EquipmentOrder.objects.get(id=equipment_order_id)
                order.payment_status = 'paid'
                order.save()
                
                # Update equipment quantity
                equipment = order.equipment
                equipment.quantity_available -= order.quantity
                equipment.save()
                
                messages.success(request, 'Payment successful! Your equipment rental has been confirmed.')
                return redirect('order_history')
                
            except Exception as e:
                print(f"Payment verification error: {str(e)}")
                messages.error(request, 'Payment verification failed. Please contact support.')
                return redirect('payment_failed')
                
        except Exception as e:
            print(f"Payment processing error: {str(e)}")
            messages.error(request, f'Payment processing error: {str(e)}')
            return redirect('payment_failed')
    
    return redirect('equipment_list')

@login_required
def payment_failed(request):
    return render(request, 'users/payment_failed.html')

@login_required
def cart(request):
    # This would typically handle cart functionality
    return render(request, 'users/cart.html')

@login_required
def order_history(request):
    orders = EquipmentOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/order_history.html', {'orders': orders})

@login_required
def course_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'users/course_list.html', {'courses': courses})

@login_required
@csrf_protect
def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        
        try:
            course = get_object_or_404(Course, pk=course_id)
            
            # Check if already enrolled
            if CourseEnrollment.objects.filter(user=request.user, course=course).exists():
                messages.warning(request, 'You are already enrolled in this course.')
                return redirect('course_list')
            
            # Create enrollment
            enrollment = CourseEnrollment.objects.create(
                user=request.user,
                course=course,
                status='Active'  # Use 'Active' to match the model default
            )
            
            messages.success(request, f'Successfully enrolled in {course.name}!')
            return redirect('my_courses')
            
        except Exception as e:
            messages.error(request, f'Error enrolling in course: {str(e)}')
            return redirect('course_list')
    
    return redirect('course_list')

@login_required
def my_courses(request):
    enrollments = CourseEnrollment.objects.filter(user=request.user).order_by('-enrollment_date')
    return render(request, 'users/my_courses.html', {'enrollments': enrollments})

@login_required
def add_crop_sell(request):
    if request.user.role != 'farmer':
        return redirect('login')
    
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        crop_grade = request.POST.get('crop_grade')
        crop_price = request.POST.get('crop_price')
        crop_quantity = request.POST.get('crop_quantity')
        crop_description = request.POST.get('crop_description')
        crop_photo = request.FILES.get('crop_photo')
        
        if crop_name and crop_grade and crop_price and crop_quantity:
            crop = CropSell.objects.create(
                farmer=request.user,
                name=crop_name,
                grade=crop_grade,
                price=crop_price,
                quantity=crop_quantity,
                description=crop_description,
                photo=crop_photo
            )
            messages.success(request, f'Crop "{crop.name}" has been added for sale successfully!')
            return redirect('manage_crops')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'users/add_crop_sell.html')

@login_required
def manage_crops(request):
    if request.user.role != 'farmer':
        return redirect('login')
    
    crops = CropSell.objects.filter(farmer=request.user).order_by('-created_at')
    
    context = {
        'crops': crops,
        'total_crops': crops.count(),
        'sold_crops': crops.filter(is_sold=True).count(),
        'unsold_crops': crops.filter(is_sold=False).count(),
    }
    
    return render(request, 'users/manage_crops.html', context)

@login_required
def buy_crops(request):
    if request.user.role != 'buyer':
        return redirect('login')
    
    crops = CropSell.objects.filter(is_sold=False).order_by('-created_at')
    
    context = {
        'crops': crops,
    }
    
    return render(request, 'users/buy_crops.html', context)

@login_required
def crop_orders(request):
    if request.user.role != 'buyer':
        return redirect('login')
    
    orders = CropOrder.objects.filter(buyer=request.user).order_by('-created_at')
    
    # Calculate statistics
    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    completed_orders = orders.filter(status='Delivered').count()
    total_spent = sum(order.total_amount for order in orders if order.payment_status == 'Paid')
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_spent': total_spent,
    }
    
    return render(request, 'users/crop_orders.html', context)

@login_required
def create_crop_order(request):
    if request.user.role != 'buyer':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Unauthorized access'})
        return redirect('login')
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        quantity = request.POST.get('quantity')
        delivery_address = request.POST.get('delivery_address')
        
        try:
            crop = CropSell.objects.get(id=crop_id, is_sold=False)
            
            # Check if enough quantity is available
            if int(quantity) > crop.quantity:
                error_msg = 'Not enough quantity available!'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': error_msg})
                messages.error(request, error_msg)
                return redirect('buy_crops')
            
            # Calculate total amount
            total_amount = float(quantity) * float(crop.price)
            
            # Create order
            order = CropOrder.objects.create(
                buyer=request.user,
                crop=crop,
                quantity=quantity,
                total_amount=total_amount,
                delivery_address=delivery_address,
                status='Pending',
                payment_status='Paid'  # Set to Paid since payment was completed
            )
            
            # Update crop quantity
            crop.quantity -= int(quantity)
            if crop.quantity == 0:
                crop.is_sold = True
            crop.save()
            
            success_msg = f'Order placed successfully! Order ID: #{order.id}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'order_id': order.id})
            messages.success(request, success_msg)
            return redirect('crop_orders')
            
        except CropSell.DoesNotExist:
            error_msg = 'Crop not found or already sold!'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
            messages.error(request, error_msg)
            return redirect('buy_crops')
        except Exception as e:
            error_msg = f'Error placing order: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
            messages.error(request, error_msg)
            return redirect('buy_crops')
    
    return redirect('buy_crops')

def logout_view(request):
    logout(request)
    return redirect('login')
