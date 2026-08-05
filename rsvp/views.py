from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RSVPForm
from .models import RSVPResponse

# Simple shared password gating response deletion on the (unauthenticated) stats page —
# checked server-side so it isn't readable from page source, unlike a client-only JS check.
DELETE_PASSWORD = "arina6767"

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

    # Sort once, derive the chart data and the text breakdown from the same
    # sorted sequence so they can never disagree on order or counts.
    drinks_sorted = sorted(drinks_count.items(), key=lambda item: item[1], reverse=True)

    context = {
        'total_guests': total_guests,
        'attending': attending,
        'not_attending': not_attending,
        # NB: pass raw lists here, NOT json.dumps(...) — the stats.html template
        # uses the `json_script` filter, which already serializes to JSON itself.
        # Serializing twice turned the array into a string that Chart.js then
        # read character-by-character (that was the "Ш а м п а н..." bug).
        'drinks_labels': [name for name, _ in drinks_sorted],
        'drinks_values': [count for _, count in drinks_sorted],
        'drinks_stats': [{'name': name, 'count': count} for name, count in drinks_sorted],
        'responses': RSVPResponse.objects.all().order_by('-created_at'),
    }

    return render(request, 'rsvp/stats.html', context)

def delete_response(request, pk):
    response = get_object_or_404(RSVPResponse, pk=pk)
    if request.method == 'POST':
        if request.POST.get('password') == DELETE_PASSWORD:
            response.delete()
            messages.success(request, f'Ответ «{response.name}» удалён.')
        else:
            messages.error(request, 'Неверный пароль — ответ не удалён.')
    return redirect('stats')