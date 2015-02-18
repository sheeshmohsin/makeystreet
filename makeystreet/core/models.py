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
	access_token = models.CharField(_('Access Token'), max_length=300)

	class Meta:
		verbose_name_plural = 'Githubprofile'

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

	class Meta:
		verbose_name_plural = 'Repository'

	def __unicode__(self):
		return self.name

class Hooks(models.Model):
	user = models.ForeignKey(User)
	repo = models.ForeignKey(Repository)
	hook_id = models.CharField(_('Hook Id'), max_length=15)
	test_url = models.URLField(_('Test Url'), max_length=300)
	ping_url = models.URLField(_('Ping Url'), max_length=300)
	name = models.CharField(_('Name'), max_length=30)
	events = models.TextField(('Events'))
	active = models.CharField(_('active'), max_length=10)
	config = models.TextField(_('Config'))
	updated_at = models.DateTimeField(_('Update at'))
	created_at = models.DateTimeField(_('Created at'))

class Activity(models.Model):
	user = models.ForeignKey(User)
	detail = models.TextField()