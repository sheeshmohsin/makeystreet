from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Githubprofile(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(_('Name'), max_length=40)
	email = models.CharField(_('Email'), max_length=40)
	public_repos = models.CharField(_('Public Repo Count'), max_length=5)
	login = models.CharField(_('Login'), max_length=30)
	avatar_url = models.URLField(_('Avatar Url'), max_length=300)
	repos_url = models.URLField(_('Repos Url'), max_length=300)
	html_url = models.URLField(_('Html Url'), max_length=300)

	def __unicode__(self):
		return self.name

class Repository(models.Model):
	user = models.ForeignKey(User)
	repo_id = models.CharField(_('Repo Id'), max_length=15)
	name = models.CharField(_('Repo Name'), max_length=30)
	full_name = models.CharField(_('Repo Full Name'), max_length=40)
	html_url = models.URLField(_('Html Url'), max_length=300)
	description = models.TextField(_('Description'))
	url = models.URLField(_('Url'), max_length=300)

	def __unicode__(self):
		return self.name
