from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^create-user/$', views.create_user),
    url(r'^profile/$', views.profile),
    url(r'^questions/(?P<question_id>[0-9]+)', views.question_details),
    url(r'^ask-question/$', views.question_form),
    url(r'^answer-question', views.answer_question),
    url(r'^submit-question$', views.submit_question),
    url(r'^pinned/(?P<pin_id>[0-9]+)', views.tag_questions),
]

