# Create your views here.

from apps.home.libtweet import twitter-listener-curlx
from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

class LoginForm(forms.Form):
	usuario = forms.CharField(max_length=100)
	contrasena = forms.CharField(widget = forms.PasswordInput())

class wordForm(forms.Form):
	word = forms.CharField(max_length=100)

def index_view(request):
	return render_to_response('home/index.html')

def tweet_view(request):
	word = request.GET.get('word', '')
	return render_to_response('home/tweet.html',
							{'title': 'Tweets...',
							'logged' : request.user.is_authenticated()})

def busquedaWord(request):
	form = wordForm()
	try:
		word = request.POST['word']
	except:		
		return render_to_response('home/vistaPrincipal.html',
							 {'form': form,
                              'title': 'Aqui va un titulo de la pag',
                              'logged' : request.user.is_authenticated()})
	print word
	return redirect('tweets/?word=' +  word, permanent=True)
		
	
def login_view(request):
	if request.user.is_authenticated():
		return redirect('vistaPrincipal',
                        permanent=True)
	form = LoginForm()
	try:
		username = request.POST['usuario']
		password = request.POST['contrasena']
		user = authenticate(username=username, password=password)
	except:
		return render_to_response('home/login.html',
                                  {'form': form,
                                   'title': "Conection"})
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('vistaPrincipal', permanent=True)
		else:
			return render_to_response('home/login.html',
                                     {'form': form,
                                      'title': 'Conection',
                                      'username' : username+" esta inactivo"})
	else:
		return render_to_response('home/login.html',
                                 {'logged' : request.user.is_authenticated(),
                                  'title': 'Conection',
                                  'form': form,
                                  'username' : username + " y su contrasena no corresponden"})
def logout_view(request):
	logout(request)
	return redirect('/login',
                    permanent=True)
		
		