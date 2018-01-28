
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from googleplaces import GooglePlaces, types, lang
from django.http import HttpResponseRedirect

API_KEY= 'A********************************'
google_places = GooglePlaces(API_KEY)

@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
 
def search(request):
    return render_to_response('search.html', context_instance=RequestContext(request))
		
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    errors = []
    if request.method == 'POST':
       if not request.POST.get('subject',''):
              errors.append('Enter a subject.')
       if not request.POST.get('message',''):
              errors.append('Enter a message.')
       if not errors:
              send_mail(
            request.POST['subject'],
  request.POST['message'],
  request.POST.get('email', 'abc@gmail.com'),
  ['abc@gmail.com'],
   )
       return HttpResponseRedirect('/thanks.html')
    return render(request, 'contact.html', {'errors': errors})
 
def places(request):
    #define dictionary
    mylist = {}
    #define variables
    loc = ""
    key = ""
    if request.method == 'POST':
		    loc = request.POST.get('location','')
		    key = request.POST.get('keyword','')
    	
    query_result = google_places.nearby_search(
       	   location=loc, keyword=key, radius=10000
	   )
			
    for place in query_result.places:
	     
	     place.get_details()
	     mylist[place.name] = [place.formatted_address, place.local_phone_number, place.international_phone_number]
	
    return render_to_response('display_list.html', {'location':loc, 'keyword':key, 'mylist':mylist}, context_instance=RequestContext(request))


