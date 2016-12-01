from django.contrib import admin
from .models import Question, Answer, Tag, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms

# Register your models here.

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'profile'

# class UserForm( forms.ModelForm ):
# 	class Meta:
# 		model= User
# 		exclude= ('email',)
# 		username = forms.EmailField(max_length=64, help_text = "The person's email address.")

# 		def clean_email( self ):
# 			email= self.cleaned_data['username']
# 			return email

class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline, )
	# form= UserForm
	# list_display = ( 'email', 'first_name', 'last_name', 'is_staff' )
	# list_filter = ( 'is_staff', )
	# search_fields = ( 'email', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Tag)