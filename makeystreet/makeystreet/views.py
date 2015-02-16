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
	url = 'https://github.com/login/oauth/authorize/?client_id='+settings.CLIENTID+'&scope=user:email,public_repo&state=' + 'sheesh'
	return HttpResponseRedirect(url)

def callback(request):
	code = request.GET.get('code')
	state = request.GET.get('state')
	print code, state
	payload = {'client_id':settings.CLIENTID, 'client_secret':settings.CLIENTSECRET, 'code':code}
	response = requests.post('https://github.com/login/oauth/access_token', params=payload)
	response = urlparse.parse_qs(response.text)
	access_token = response['access_token'][0]
	request.session['access_token'] = access_token
	url = 'https://api.github.com/user?access_token=' + str(access_token)
	response = requests.get(url)
	url = response.json()["repos_url"]
	public_repo_count = response.json()["public_repos"]
	response = requests.get(url)
	return render_to_response('listrepo.html', {'repos':response.json(), 'count':public_repo_count}, context_instance=RequestContext(request))
