from google.oauth2 import id_token
from google.auth.transport import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
from google.oauth2 import id_token
from google.auth.transport import requests
from PIL import Image

# if user not signed in, sends them to log in 
def signin(request):
    if request.session.get('rank', 'anon')=='anon':
        return render(request, 'account/signin.html')
    else:
        return redirect("/account/")

# if a user tries to sign out by URL, redirects to account. if there is a POST request to this url, flushes the session and sends them to confirmation
def signout(request):
    if request.method == "GET":
        return redirect("/account/")
    else:
        request.session.flush()
        return render(request, "account/signout.html")

 
 # default account page. send to sign in if not signed in, otherwise displays user info
def default(request):
    if request.session.get('rank','anon')=='anon':
        return redirect('/account/signin/')
    else:
        userInz=models.member.objects.get(pk=request.session['user']) #get user from session
        return render(request, 'account/myaccount.html', {
            'name': userInz.name,
            'email' : userInz.email,
            'rank' : userInz.ranking,
            'image' : userInz.pic,
            'about' : userInz.about,
        })

# lets members edit their info
def manage(request):
    if request.session.get('rank','anon')=='anon':
        return redirect('/account/signin/')
    if request.method == "POST":
        userInz=models.member.objects.get(pk=request.session['user']) 
        form = models.manageForm(request.POST, request.FILES, instance=userInz)
        if form.is_valid():
            form.save()
            request.session['name']=userInz.name
            return redirect("/account/")
    else:
        userInz=models.member.objects.get(pk=request.session['user'])
        form = models.manageForm(instance=userInz)
    return render(request, "account/manage.html", {'form' : form})

# a lot of this code is from google btw
@csrf_exempt #the csrf is from google, not django, and is verified. can't get django's csrf to work tho due to origin of post
def authG(request):
    if request.method == "GET":
       return redirect("/account/")
    elif request.method == "POST":

        csrf_tok_cookie = request.COOKIES.get('g_csrf_token')
        # check valid csrf token
        if not csrf_tok_cookie:
            return HttpResponse("Something went wrong, no csrf cookie")
        csrf_tok_body = request.POST.get('g_csrf_token')
        if not csrf_tok_body:
            return HttpResponse("Something went wrong, no csrf cookie from google")
        if csrf_tok_cookie != csrf_tok_body:
            return HttpResponse("Could not verify csrf")
        #get token from google
        tok = request.POST.get("credential")  
        try:
            # logs user in via their google ID, or makes an entry in member if they do not have an account yet.
            idinfo = id_token.verify_oauth2_token(tok, requests.Request(), "316865720473-94ccs1oka6ev4kmlv5ii261dirvjkja0.apps.googleusercontent.com")
            if not(models.gLogIn.objects.filter(googleID=idinfo['sub']).exists()):
                #when we implement other sign in methods, we will need to ask the user if they already have an account
                #if so, have user sign in via user/pass or other method and then get that member entry so gLogInz points to it 
                userInz = models.member.objects.create(name=idinfo['given_name'], email = idinfo['email'])
                gLogInz = models.gLogIn.objects.create(googleID=idinfo['sub'], pointTo=userInz)
            else:
                gLogInz=models.gLogIn.objects.get(googleID=idinfo['sub'])
                userInz=gLogInz.pointTo
            request.session['rank']=userInz.ranking
            request.session['user']=userInz.pk # will need to change this just to the pk of username
            request.session['name']=userInz.name
        except ValueError:
            return HttpResponse("Something went wrong, invalid credentials from Google (somehow)")
            pass
        return redirect("/account/")