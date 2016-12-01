from __future__ import absolute_import
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from apps.forum.models import Tag, Profile, Question, Answer
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.db.models import Sum
import json

from django.core.urlresolvers import reverse
from django.views import generic
from . import forms
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Count

# Create your views here.
@login_required(login_url="login/")
def home(request):
	current_user_id = request.user.id
	current_user_object = User.objects.get(id = current_user_id)
	tags = current_user_object.profile.tags.all()
	if tags:
		# tag_list = tags.split(',')
		question_records = Question.objects.filter(tag__in = tags).order_by('-pub_date').distinct()
		# answer_records = [Answer.objects.filter(question = question_record).count() for question_record in question_records]
		answer_records = Answer.objects.filter(question__in = question_records)
		# answer_records = Answer.objects.filter(question__in= question_records).values('question') \
		# .annotate(question_count= Sum('question'))
		# count = 0
		question_answers_count = {}
		for single_answer in answer_records:
			if single_answer.question.id in question_answers_count:
				question_answers_count[single_answer.question.id] = question_answers_count[single_answer.question.id] + 1
			else:
				question_answers_count[single_answer.question.id] = 1
		context = {"tags": tags, "questions": question_records, "answers": question_answers_count}
		return render(request, "home.html", context)
	else:
		question_records = Question.objects.all()
		answer_records = Answer.objects.filter(question__in = question_records)
		question_answers_count = {}
		for single_answer in answer_records:
			if single_answer.question.id in question_answers_count:
				question_answers_count[single_answer.question.id] = question_answers_count[single_answer.question.id] + 1
			else:
				question_answers_count[single_answer.question.id] = 1
		context = {"questions": question_records, "answers": question_answers_count}
		return render(request, "home.html")

def signup(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/')
	tags = Tag.objects.all()
	context = {"tags": tags}
	return render(request, 'sign-up.html', context)

def create_user(request):
	user_name = request.POST.get('username', '')
	password = request.POST.get('password', '')
	mail = request.POST.get('email', '')
	tags = request.POST.getlist('tags', '')
	if tags:
		tags_string = ','.join(tags)
	else:
		tags_string = ''
	if User.objects.filter(username = user_name).exists():
		message = "The user name already has been created"
	elif password and mail and user_name:
		user = User.objects.create_user(user_name, mail, password)
		user.save()
		try:
			profile = user.profile
		except ObjectDoesNotExist:
			profile = Profile(user = user)
		profile.tags = Tag.objects.filter(tags__in = tags)
		profile.save()
		login(request, user)
		message = "User has been successfully created"
	else:
		message = "There is a problem with creating the user"
	context = {"message": message, "tags": tags_string}
	return render(request, 'create-user.html', context)

@login_required(login_url="login/")
def profile(request):
	current_user = request.user
	current_user_id = current_user.id
	current_user_profile_info = current_user.profile
	context = {"user": current_user, "user_id": current_user_id, "profile": current_user_profile_info}
	return render(request, 'profile.html', context)

@login_required(login_url="login/")
def question_details(request, question_id):
	current_user = request.user
	current_user_id = current_user.id
	if request.method == 'GET':
		site_path = request.get_full_path()
		question_record = Question.objects.get(id = question_id )
		total_views = question_record.views
		total_views = total_views + 1
		question_record.views = total_views
		question_record.save()
		related_question_records = Question.objects.filter(tag__in = question_record.tag.all()).exclude(id = question_record.id).order_by('-pub_date')[:10]
		answer_records = Answer.objects.filter(question = question_record )
		context = {"question_record": question_record, "answer_records": answer_records, "related_questions": related_question_records}
		return render(request, 'details.html', context)

def question_form(request):
	if request.method == 'POST':
		tags = Tag.objects.all()
		context = {"tags": tags}
		return render(request, 'content-ask-question.html', context)

def submit_question(request):
	if request.method == 'POST':
		question = request.POST.get('question', '')
		tags = request.POST.getlist('tags', '')
		current_user_object = User.objects.get(id = request.user.id)
		tag_records = Tag.objects.filter(id__in = tags)
		question_query = Question(user = current_user_object, question_text = question)
		question_query.save()
		for tag in tag_records:
			question_query.tag.add(tag)
		return HttpResponse("Success")

def tag_questions(request, pin_id):
	if request.method == 'GET':
		current_user_id = request.user.id
		current_user_object = User.objects.get(id = current_user_id)
		tags = current_user_object.profile.tags.all()
		tag_record = Tag.objects.get(id = pin_id)
		question_records = Question.objects.filter(tag = tag_record).order_by('-pub_date')
		popular_question_records = Question.objects.filter(tag = tag_record).annotate(most_viewed = Count('views'))[:10]
		answer_records = Answer.objects.filter(question__in = question_records)
		question_answers_count = {}
		for single_answer in answer_records:
			if single_answer.question.id in question_answers_count:
				question_answers_count[single_answer.question.id] = question_answers_count[single_answer.question.id] + 1
			else:
				question_answers_count[single_answer.question.id] = 1
		context = {"tags": tags, "tag": tag_record, "questions": question_records, "answers": question_answers_count, "popular_questions": popular_question_records}
		return render(request, 'tag-questions.html', context)

def answer_question(request):
	if request.method == 'POST':
		question_id = request.POST.get('question-id', '')
		answer = request.POST.get('answer', '')
		question_record = Question.objects.get(pk = question_id)
		current_user_object = User.objects.get(id = request.user.id)
		question_query = Answer(user = current_user_object, answer_text = answer, question = question_record)
		question_query.save()
		return HttpResponse("Success")

def page_not_found_view(request):
	return render(request, '404.html')