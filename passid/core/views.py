from django.shortcuts import render, redirect, get_object_or_404
from .models import Visitor, StaffMember
from django.contrib import messages

def index(request):
    return render(request, 'core/index.html')

def visitor_form(request):
    if request.method == "POST":
        Visitor.objects.create(
            full_name=request.POST.get('full_name'),
            passport=request.POST.get('passport'),
            phone=request.POST.get('phone'),
            organization=request.POST.get('organization'),
            escort_id=request.POST.get('escort') or None
        )   
        return redirect('request_success')
    
    escorts = Visitor.objects.filter(status='approved')
    return render(request, 'core/visitor_form.html', {'escorts': escorts})

def staff_login(request):
    if request.method == "POST":
        token = request.POST.get('token')
        if StaffMember.objects.filter(token=token).exists():
            request.session['is_staff'] = True
            return redirect('dashboard')
    return render(request, 'core/staff_login.html')

def dashboard(request):
    if not request.session.get('is_staff'):
        return redirect('staff_login')
    visitors = Visitor.objects.all().order_by('-created_at')
    return render(request, 'core/dashboard.html', {'visitors': visitors})

def approve_visitor(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    visitor.status = 'approved'
    visitor.save()
    return redirect('dashboard')

def request_success(request):
    return render(request, 'core/success.html')
