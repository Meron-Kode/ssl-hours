from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import VolunteerLog
from .forms import VolunteerLogForm


@login_required
def dashboard(request):
    # Filter logs for the logged-in student
    user_logs = VolunteerLog.objects.filter(student=request.user)

    # Calculate total approved hours for the progress bar
    total_hours = user_logs.filter(status='A').aggregate(Sum('hours_worked'))['hours_worked__sum'] or 0

    # Goal based on typical graduation requirements (e.g., 75 hours)
    goal = 75
    progress_percentage = (total_hours / goal) * 100 if goal > 0 else 0

    context = {
        'logs': user_logs.order_by('-volunteer_date'),
        'total_hours': total_hours,
        'progress_percentage': min(progress_percentage, 100),
        'goal': goal,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_log(request):
    if request.method == 'POST':
        form = VolunteerLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.student = request.user
            log.save()
            return redirect('dashboard')
    else:
        form = VolunteerLogForm()
    return render(request, 'add_log.html', {'form': form})
