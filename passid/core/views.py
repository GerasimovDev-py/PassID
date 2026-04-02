from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visitor

def index(request):
    return render(request, 'core/index.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from .models import Visitor

def visitor_form(request):
    if request.method == "POST":
        try:
            valid_until_str = request.POST.get('valid_until')
            valid_until = datetime.strptime(valid_until_str, "%d.%m.%Y %H:%M")
            
            visitor = Visitor.objects.create(
                full_name=request.POST.get('full_name'),
                document_type=request.POST.get('document_type'),
                document_number=request.POST.get('document_number'),
                escort_id=request.POST.get('escort'),
                escort_phone=request.POST.get('escort_phone'),
                valid_until=valid_until
            )
            visitor.save()
            return redirect('request_success')
            
        except ValueError:
            messages.error(request, "Неверный формат даты и времени. Используйте формат ДД.ММ.ГГГГ ЧЧ:ММ")
        except Exception as e:
            messages.error(request, f"Ошибка при сохранении: {str(e)}")

    escorts = Visitor.objects.filter(status='approved')
    
    return render(request, 'core/visitor_form.html', {
        'escorts': escorts,
    })

def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'core/staff_login.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def dashboard_partial(request):
    tab = request.GET.get('tab', 'active')
    visitors = Visitor.objects.all().order_by('-created_at')
    
    if tab == 'archive':
        return render(request, 'core/dashboard_partial_archive.html', {'visitors': visitors})
    else:
        return render(request, 'core/dashboard_partial_active.html', {'visitors': visitors})

@login_required
def approve_visitor(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if visitor.status == 'pending':
        visitor.status = 'approved'
        visitor.arrival_time = timezone.now()
        visitor.save()
    return redirect('dashboard')

@login_required
def mark_departed(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if visitor.status == 'approved':
        visitor.status = 'departed'
        visitor.departure_time = timezone.now()
        visitor.save()
    return redirect('dashboard')

def request_success(request):
    return render(request, 'core/success.html')

def staff_logout(request):
    logout(request)
    return redirect('staff_login')

def check_status(request):
    if request.method == "POST":
        document_number = request.POST.get('document_number')
        if document_number:
            visitor = Visitor.objects.filter(document_number=document_number).order_by('-created_at').first()
            if visitor:
                return render(request, 'core/status_result.html', {'visitor': visitor})
            else:
                messages.error(request, 'Пропуск с таким номером документа не найден.')
        else:
            messages.error(request, 'Введите номер документа.')
    
    return render(request, 'core/check_status.html')

def status_result(request):
    return render(request, 'core/status_result.html')