Django Breadcrumb Stasher

The purpose of this django plugin, is to easily create "save" points in django views, to return to once 
the user has completed a certain process. Let's say the user attempts to do a certain action, but must
do a DIFFERENT action, before starting the desired action. When the user is done doing the required action,
it would certainly be nice if you automatically returned the user to the DESIRED action. 

In your views.py file, you could see something like the following. Please note that this will most likely 
not work by simply dropping it into your current code, although I'd definitely smile if it did!

The real power in this plugin, is that the breadcrumbs could originate from multiple sources, and still
all lead back to the original stasher.

```python
import breadcrumb_stasher
from django.shortcuts import render, redirect

# No breadcrumbs existed, the views use this view as the fallback url
def default_action(request):
	return render(request, 'default_action.html')

@breadcrumb_stasher.stash
def desired_action(request):
	# First requirement must be met
	if request.session.get('completed_requirement_1', '0') != '1':
		return redirect('views.required_action_1')

	# Then perhaps another
	if request.session.get('completed_requirement_2', '0') != '1':
		return redirect('views.required_action_2')

	return render(request, 'desired_action.html')

def required_action_1(request):
	if request.method == 'POST':
		request.session['completed_requirement_1'] = '1'

		# Redirect to the most recent breadcrumb, fallback to views.default_action if none are found!
		return breadcrumb_stasher.redirect(request, 'views.default_action')

	return render(request, 'required_action_1.html')

def required_action_2(request):
	if request.method == 'POST':
		request.session['completed_requirement_2'] = '1'

		# Redirect to the most recent breadcrumb, fallback to views.default_action if none are found!
		return breadcrumb_stasher.redirect(request, 'views.default_action')

	return render(request, 'required_action_2.html')
```