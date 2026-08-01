from django.shortcuts import render, redirect
from .forms import RSVPForm
from .models import RSVPResponse
import json

def index(request):
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            drinks = form.cleaned_data.get('drinks', [])
            RSVPResponse.objects.create(
                name=form.cleaned_data['name'],
                attendance=form.cleaned_data['attendance'],
                drinks=', '.join(drinks)
            )
            return redirect('success')
    else:
        form = RSVPForm()
    
    return render(request, 'rsvp/index.html', {'form': form})

def success(request):
    return render(request, 'rsvp/success.html')

def stats(request):
    total_guests = RSVPResponse.objects.count()
    attending = RSVPResponse.objects.filter(attendance='yes').count()
    not_attending = RSVPResponse.objects.filter(attendance='no').count()
    
    all_drinks = RSVPResponse.objects.exclude(drinks__exact='').values_list('drinks', flat=True)
    drinks_count = {}
    for drinks_str in all_drinks:
        for drink in drinks_str.split(', '):
            if drink:  # пропускаем пустые
                drinks_count[drink] = drinks_count.get(drink, 0) + 1
    
    context = {
        'total_guests': total_guests,
        'attending': attending,
        'not_attending': not_attending,
        'drinks_labels': json.dumps(list(drinks_count.keys())),
        'drinks_values': json.dumps(list(drinks_count.values())),
        'responses': RSVPResponse.objects.all().order_by('-created_at'),
    }
    
    return render(request, 'rsvp/stats.html', context)