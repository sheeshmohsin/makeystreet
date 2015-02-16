import requests
import urlparse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.core.files import File
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.template import Context
from django.contrib.auth.decorators import login_required

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def profile(request):
	return render_to_response('profile.html', context_instance=RequestContext(request))

def linkgithub(request):
	url = 'https://github.com/login/oauth/authorize/?client_id=20b5ef1babc98bb04129&scope=user:email,public_repo&state=' + 'sheesh'
	return HttpResponseRedirect(url)

def callback(request):
	code = request.GET.get('code')
	state = request.GET.get('state')
	print code, state
	payload = {'client_id':'20b5ef1babc98bb04129', 'client_secret':'e789cd37ef68d0e1d5eff821ca7a6a9e1c7118f3', 'code':code}
	response = requests.post('https://github.com/login/oauth/access_token', params=payload)
	response = urlparse.parse_qs(response.text)
	access_token = response['access_token']
	request.session['access_token'] = access_token
	return render_to_response('listrepo.html', context_instance=RequestContext(request))
