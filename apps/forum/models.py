from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

# Create your models here.

class Tag(models.Model):
	tag_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.tag_text


class Question(models.Model):
	tag = models.ManyToManyField(Tag)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	question_text = models.CharField(max_length = 500)
	pub_date = models.DateTimeField(default = timezone.now)
	views = models.BigIntegerField(default = 0)
	status = models.BooleanField(default = True)

	def __str__(self):
		return self.question_text


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE, blank = True, null = True)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	answer_text = RichTextField(config_name='awesome_ckeditor')
	pub_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.answer_text
		

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	tags = models.ManyToManyField(Tag)
	profile_bio = models.CharField(max_length = 400, default = '')
	short_description = models.TextField(default = '')

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()