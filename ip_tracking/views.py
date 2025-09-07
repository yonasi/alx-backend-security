from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit

def login_view(request):
    # Example login view (replace with actual login logic if needed)
    if request.method == 'POST':
        return HttpResponse("Login attempt processed")
    return HttpResponse("Login page")

# Rate-limited view for anonymous users (5 requests/minute)
@ratelimit(key='ip', rate='5/m', method='ALL', block=True)
def anonymous_limited_login(request):
    return login_view(request)

# Rate-limited view for authenticated users (10 requests/minute)
@ratelimit(key='ip', rate='10/m', method='ALL', block=True)
@login_required
def authenticated_limited_login(request):
    return login_view(request)