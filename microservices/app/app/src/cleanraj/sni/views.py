
from __future__ import unicode_literals

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.core import serializers
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView

from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from account import signals
from account.conf import settings
from account.forms import SignupForm, LoginUsernameForm
from account.forms import ChangePasswordForm, PasswordResetForm, PasswordResetTokenForm
from account.forms import SettingsForm
from account.hooks import hookset
from account.mixins import LoginRequiredMixin
from account.models import SignupCode, EmailAddress, EmailConfirmation, Account, AccountDeletion
from account.utils import default_redirect, get_form_data

from django.http import Http404, HttpResponseForbidden, HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, CreateView
import account.views
from .forms import SignupForm, SuggestionForm
from .models import UserProfile, location
from account.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from base64 import b64encode, b64decode
import requests

# signup view overwrided
class SignupView(account.views.SignupView):

    form_class = SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user = self.created_user,
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"]
            )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

@login_required
# profile view
def ProView(request, pk):
    user = get_object_or_404(UserProfile, user__pk=pk)
    path = ""
    for i in reversed(user.image.url):
        if i == '/':
            break
        else:
            path = i+path
    var = "{0}{1}".format(settings.MEDIA_URL, path)
    return render(request, 'sni/profile.html', {'user':user, 'var':var})

# profile detail view
class ProfileView(DetailView):
    model = UserProfile


def homeView(request):
    garbage_points = location.objects.all()
    
    return render(request, 'homepage.html',{'garbage_points':garbage_points})

def show_garbage_points(request):
    garbage_points = location.objects.all()

    garbage_points_json = serializers.serialize("json", garbage_points)

    pk = []

    for i in garbage_points:
        pk.append(i.pk)

    data = {"garbage_cords": garbage_points_json, "pk":pk}

    return HttpResponse(garbage_points_json)


# check username in ajax calls
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


# save cordinates into location model

def save_cordinates(request):
    lan = request.POST.get('lan', None)
    lon = request.POST.get('lon', None)
    image = request.POST.get('image', None)

    cords = location(lat=lan, lon=lon, garbage_pic=image)
    cords.save()
    data = {
        'Success': 'success'
    }
    return JsonResponse(data)


# views to show garbage locations to admin so he can remove it after cleaning
@login_required
def show_garbage_locations(request):
    garbage_points = location.objects.all()
    return render(request, 'sni/admin.html', {'garbage_points':garbage_points})


# view for delete item

def remove_location(request):
    pk = request.POST.get('pk', None)
    print(pk)
    print("============================")
    locationpoint = get_object_or_404(location, pk=pk)
    locationpoint.delete()
    data = {
        'Success': 'success'
    }
    return JsonResponse(data)

# view to load suggestions and use hasura data api for the same

def load_suggestions(request):

    request_json = {
            "type": "select",
            "args": {
                "table": "suggestions",
                "columns": [
                    "*"
                ]
            }
        }

    response = requests.post('https://data.anathema47.hasura-app.io/v1/query', json=request_json)

    return render(request, 'sni/suggestions.html', {'suggestionlist':response.json()})

# view to add suggestion using hasura api
def add_suggestion(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SuggestionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # save the suggestion in the using hasura data api
            suggestion = form.cleaned_data['suggestion']
            # print(suggestion)
            # print("===============================")
            # print(request.user)
            

            # redirect to suggestions page

            myheaders = {'Authorization': 'Bearer 2195e500ec67301b610b399cf33b958197f8a1a61ca2063b'}

            suggestioncontent = {
                "type": "insert",
                "args": {
                    "table": "suggestions",
                    "objects": [
                        {
                            "writer": request.user.username,
                            "content": suggestion
                        }
                    ]
                }
            }

            response = requests.post('https://data.anathema47.hasura-app.io/v1/query', json=suggestioncontent, headers=myheaders)
            return redirect('sni.views.load_suggestions')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SuggestionForm()

    return render(request, 'sni/add_suggestion.html', {'form': form})    
