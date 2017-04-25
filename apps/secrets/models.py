# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re

NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

# Create your models here.
class UserManager(models.Manager):

	def register(self, postData):

		errors = []

		if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['first_name']) < 1:
			errors.append('Missing field.')

		if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
			errors.append('First name and/or last name cannot be fewer than 2 characters.')

		if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
			errors.append('First name and/or last name can only contain letters.')

		if not EMAIL_REGEX.match(postData['email']):
			errors.append('Email is invalid.')

		if not PW_REGEX.match(postData['password']):
			errors.append('Password is invalid. Cannot be fewer than 8 characters.')

		if postData['password'] != postData['confirm_pw']:
			errors.append('Passwords do not match.')

		# search for email in database
		if User.objects.filter(email=postData['email']):
			errors.append('Email already exists.')

		return errors

	def create_user(self, postData):
		hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())

		new_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], hashed_pw=hashed_pw)
		return new_user.id

	def login(self, postData):

		errors = []

		if not User.objects.filter(email=postData['email']):
			errors.append('Username and/or password are invalid.')
		else:
			if bcrypt.hashpw(postData['password'].encode('utf-8'), User.objects.get(email=postData['email']).hashed_pw.encode('utf-8')) != User.objects.get(email=postData['email']).hashed_pw:
				errors.append('Username and/or password are invalid.')

		return errors

class SecretManager(models.Manager):
	def delete_secret(self, secret_id):
		Secret.objects.get(id=secret_id).delete()
		return secret_id

	def add_secret(self, postData):
		secret = Secret.objects.create(content=postData['secret'], user=User.objects.get(id=postData['user_id']))
		secret_id = secret.id
		return secret_id

	def like(self, postData):
		user = User.objects.get(id=postData['user_id'])
		secret = Secret.objects.get(id=postData['secret_id'])
		secret.likes.add(user)

	def unlike(self, postData):
		user = User.objects.get(id=postData['user_id'])
		secret = Secret.objects.get(id=postData['secret_id'])
		secret.likes.remove(user)
		

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hashed_pw = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Secret(models.Model):
	content = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User)
	likes = models.ManyToManyField(User, related_name="secrets")

	objects = SecretManager()
