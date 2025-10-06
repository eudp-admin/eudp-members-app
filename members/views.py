# members/views.py

# 1. Imports (ሁሉንም በአንድ ቦታ ማሰባሰብ)
import csv
import qrcode
import base64
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
from django.templatetags.static import static
from .models import Member, Announcement, GENDER_CHOICES, REGION_CHOICES
from .forms import MemberCreationForm, MemberUpdateForm
from django.utils.safestring import mark_safe

# 2. Authentication and Basic Pages
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'members/landing_page.html')

def register_member(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = MemberCreationForm(request.POST, request.FILES)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=phone_number, password=password)
            member = form.save(commit=False)
            member.user = user
            member.save()
# መልዕክቱን እንፈጥራለን
            success_message = f'<i class="fas fa-check-circle me-2"></i> እንኳን ደስ አለዎት! ምዝገባዎ ተሳክቷል! በስልክ ቁጥርዎን እንድ ተጠቃሚ ስም (Username) በመጠቀም መግባት ይችላሉ።'
            
            # መልዕክቱን 'safe' መሆኑን ምልክት አድርገን እንልካለን
            messages.success(request, mark_safe(success_message))
            return redirect('login') 
    else:
        form = MemberCreationForm()

    context = {'form': form, 'page_title': 'አዲስ አባል መመዝገቢያ'}
    return render(request, 'members/register_form.html', context)


# 3. Member-Specific Views (Profile, etc.)
@login_required
def profile(request):
    member_profile = Member.objects.get(user=request.user)
    context = {'member': member_profile}
    return render(request, 'members/profile.html', context)

@login_required
def profile_update(request):
    member_profile = Member.objects.get(user=request.user)
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, request.FILES, instance=member_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'የግል መረጃዎ በተሳካ ሁኔታ ተስተካክሏል!')
            return redirect('profile')
    else:
        form = MemberUpdateForm(instance=member_profile)
    context = {'form': form, 'page_title': 'የግል መረጃ ማስተካከያ'}
    return render(request, 'members/profile_update_form.html', context)


# 4. Staff/Admin Views (Dashboard, Lists, etc.)
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('profile')

    user = request.user
    base_queryset = Member.objects.filter(is_active=True)
    
    if not user.is_superuser and user.groups.filter(name='የክልል አስተባባሪ').exists():
        try:
            coordinator_profile = Member.objects.get(user=user)
            if coordinator_profile.is_coordinator and coordinator_profile.coordinator_region:
                base_queryset = base_queryset.filter(region=coordinator_profile.coordinator_region)
            else:
                base_queryset = Member.objects.none()
        except Member.DoesNotExist:
            base_queryset = Member.objects.none()

    gender_map = dict(GENDER_CHOICES)
    gender_distribution = list(base_queryset.values('gender').annotate(count=Count('gender')))
    for item in gender_distribution:
        item['gender_display'] = gender_map.get(item['gender'], item['gender'])

    region_map = dict(REGION_CHOICES)
    members_by_region = list(base_queryset.values('region').annotate(count=Count('region')).order_by('-count'))
    for item in members_by_region:
        item['region_display'] = region_map.get(item['region'], item['region'])

    recent_members = base_queryset.order_by('-date_joined')[:5]
    members_by_year_data = base_queryset.annotate(year=ExtractYear('date_joined')).values('year').annotate(count=Count('id')).order_by('year')
    
    context = {
        'page_title': 'የአስተዳደር ዳሽቦርድ',
        'total_members': base_queryset.count(),
        'gender_distribution': gender_distribution,
        'members_by_region': members_by_region,
        'recent_members': recent_members,
        'bar_chart_labels': [str(item['year']) for item in members_by_year_data],
        'bar_chart_data': [item['count'] for item in members_by_year_data],
        'pie_chart_labels': [item['gender_display'] for item in gender_distribution],
        'pie_chart_data': [item['count'] for item in gender_distribution],
    }
    return render(request, 'members/dashboard.html', context)

@login_required
def member_list(request):
    if not request.user.is_staff:
        return redirect('profile')
    
    queryset = Member.objects.filter(is_active=True).order_by('-date_joined')
    query = request.GET.get('query')
    region = request.GET.get('region')

    if query:
        queryset = queryset.filter(
            Q(full_name__icontains=query) | 
            Q(membership_id__icontains=query)
        ).distinct()
    if region:
        queryset = queryset.filter(region__icontains=region)

    context = {'page_title': 'የአባላት ዝርዝር', 'members': queryset}
    return render(request, 'members/member_list.html', context)

@login_required
def member_detail(request, pk):
    if not request.user.is_staff:
        # አባሉ ራሱ ከሆነ ማየት ይችላል
        try:
            member = Member.objects.get(pk=pk)
            if request.user == member.user:
                pass # ፍቀድለት
            else:
                return redirect('profile') # ካልሆነ ወደ ፕሮፋይሉ ይመለስ
        except Member.DoesNotExist:
            return redirect('member_list')
    
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        messages.error(request, "አባሉ አልተገኘም!")
        return redirect('member_list')
    context = {'member': member}
    return render(request, 'members/member_detail.html', context)

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-date_posted')
    context = {'page_title': 'ዜና እና ማስታወቂያዎች', 'announcements': announcements}
    return render(request, 'members/announcement_list.html', context)

@login_required
def export_members_csv(request):
    if not request.user.is_staff:
        return redirect('profile')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="eudp_members_report.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['ሙሉ ስም', 'የአባልነት መለያ', 'ስልክ ቁጥር', 'ጾታ', 'ክልል', 'የተመዘገበበት ቀን'])
    
    queryset = Member.objects.filter(is_active=True).order_by('full_name')
    # ... (የፍለጋ ሎጂክ እዚህ መጨመር ይቻላል) ...

    for member in queryset:
        writer.writerow([
            member.full_name,
            member.membership_id,
            member.phone_number,
            member.get_gender_display(),
            member.get_region_display(),
            member.date_joined.strftime('%Y-%m-%d')
        ])
    return response

@login_required
def member_id_card(request, pk):
    try:
        member = Member.objects.get(pk=pk)
        if not request.user.is_staff and request.user != member.user:
            messages.error(request, "ይህንን ገጽ ለማየት ፍቃድ የለዎትም።")
            return redirect('profile')
    except Member.DoesNotExist:
        messages.error(request, "አባሉ አልተገኘም!")
        return redirect('member_list')

    qr_data = f"ስም: {member.full_name}\nመለያ ቁጥር: {member.membership_id}"
    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {'member': member, 'qr_code_base64': qr_code_base64}
    return render(request, 'members/id_card.html', context)