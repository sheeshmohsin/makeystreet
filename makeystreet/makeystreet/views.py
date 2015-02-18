import json
import requests
import urlparse

from core.models import *
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
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

@login_required
def profile(request):
	if len(request.user.githubprofile_set.all())==1:
		return HttpResponseRedirect('/listrepo/')
	else:
		return render_to_response('link.html', context_instance=RequestContext(request))

@login_required
def linkgithub(request):
	url = 'https://github.com/login/oauth/authorize/?client_id='+settings.CLIENTID+'&scope=user:email,public_repo&state=' + 'sheesh'
	return HttpResponseRedirect(url)

@login_required
def callback(request):
	code = request.GET.get('code')
	state = request.GET.get('state')
	print code, state
	payload = {'client_id':settings.CLIENTID, 'client_secret':settings.CLIENTSECRET, 'code':code}
	response = requests.post('https://github.com/login/oauth/access_token', params=payload)
	response = urlparse.parse_qs(response.text)
	access_token = response['access_token'][0]
	request.session['access_token'] = access_token
	print access_token
	url = 'https://api.github.com/user?access_token=' + str(access_token)
	response = requests.get(url)
	response = response.json()
	a = Githubprofile(user=request.user, name=response["name"], email=response["email"], 
		public_repos=response["public_repos"], login=response["login"], avatar_url = response["avatar_url"], 
		repos_url= response["repos_url"], html_url=response["html_url"], access_token=access_token)
	a.save()
	url = response["repos_url"]
	public_repo_count = response["public_repos"]
	response = requests.get(url)
	repos = response.json()
	for repo in repos:
		b = Repository(user=request.user, repo_id=repo["id"], name=repo["name"], full_name=repo["full_name"],
		 html_url=repo["html_url"], description=repo["description"], url=repo["url"])
		b.save()
	return HttpResponseRedirect('/listrepo/')

@login_required
def listrepo(request):
	prof = request.user.githubprofile_set.all()[0]
	public_repo_count = prof.public_repos
	repos = request.user.repository_set.all()
	return render_to_response('listrepo.html', {'repos':repos, 'count':public_repo_count}, context_instance=RequestContext(request))

@login_required
def create_hook(request, repo_id):
    repo = request.user.repository_set.get(repo_id=repo_id)
    prof = request.user.githubprofile_set.all()[0]
    url = 'https://api.github.com/repos/'+prof.login+'/'+repo.name+'/hooks?access_token=' + prof.access_token
    print url
    payload = """{"name": "web", "active": true, "events": [ "push", "pull_request" ], "config": { "url": "http://37d43d42.ngrok.com/webhook/%s/", "content_type": "json" }}"""%str(prof.login)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=payload, headers=headers)
    response = response.json()
    a = Hooks(user=request.user, repo=repo, hook_id=response["id"], test_url=response["test_url"],
     ping_url=response["ping_url"], name=response["name"], events=response["events"],
     active=response["active"], config=response["config"], updated_at=response["updated_at"],
     created_at=response["created_at"])
    a.save()
    return HttpResponseRedirect('/listrepo/')

@csrf_exempt
def webhook(request, login):
	response = request.body
	result = json.loads(response)
	print result
	userprof = Githubprofile.objects.get(login=login)
	a = Activity(user=userprof.user, detail=request.body)
	a.save()
	return HttpResponse("ok")

@login_required
def activity(request):
	activities = request.user.activity_set.all()
	return render_to_response('activity.html', {'activities':activities}, context_instance=RequestContext(request))

