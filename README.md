Django Breadcrumb Stasher

The purpose of this django plugin, is to easily create "save" points in django views, to return to once 
the user has completed a certain process. Let's say the user attempts to do a certain action, but must
do a DIFFERENT action, before starting the desired action. When the user is done doing the required action,
it would certainly be nice if you automatically returned the user to the DESIRED action. 

In your views.py file, you could see something like the following. Please note that this will most likely 
not work by simply dropping it into your current code, although I'd definitely smile if it did!

```python
import breadcrumb_stasher
from django.shortcuts import render, redirect

# No breadcrumbs existed, so it will fall back to here according to the logic in required_action(request)
def default_action(request):
	return render(request, 'default_action.html')

@breadcrumb_stasher.stash
def desired_action(request):
	if request.session.get('completed_requirements', '0') != '1':
		return redirect('views.required_action')

	return render(request, 'desired_action.html')

def required_action(request):
	if request.method == 'POST':
		request.session['completed_requirements'] = '1'

		# Redirect to the most recent breadcrumb, fallback to views.default_action if none are found!
		return breadcrumb_stasher.redirect(request, 'views.default_action')

	return render(request, 'required_action.html')
```