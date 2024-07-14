from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Show, User
import bcrypt

def login_register_page(request):
    return render(request, "login_register.html")

def index(request):
    if "user_id" not in request.session:
        return redirect("/logout")
    data = {
        "shows": Show.get_all_shows(),
        "user": User.get_by_id(request.session['user_id'])
    }
    return render(request, "all_shows.html", data)

def new_show(request):
    return render(request, "create_show.html")

def create_new_show(request):
    if "user_id" not in request.session:
        return redirect("/logout")
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/shows/new")
    show = Show.objects.filter(title=request.POST['title'])
    if show.exists():
        messages.error(request, "This show is already registered.")
        return redirect("/shows/new")
    Show.new_show({
        "title": request.POST['title'],
        "network": request.POST['network'],
        "release_date": request.POST['release_date'],
        "description": request.POST['description']
    })
    return redirect("/shows")

def view_one_show(request, id):
    if "user_id" not in request.session:
        return redirect("/logout")
    data = {
        "show": Show.get_one_show(id)
    }
    return render(request, "show.html", data)

def edit_show(request, id):
    data={
        "show": Show.get_one_show(id)
    }
    return render(request, "edit_show.html", data)

def update_show(request, id):
    if "user_id" not in request.session:
        return redirect("/logout")
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/shows/{id}/edit')
    show = Show.objects.filter(title=request.POST['title']).exclude(id=id)
    if show.exists():
        messages.error(request, "This show is already registered.")
        return redirect(f'/shows/{id}/edit')
    Show.update_show({
        "id": id,
        "title": request.POST['title'],
        "network": request.POST['network'],
        "release_date": request.POST['release_date'],
        "description": request.POST['description']
    })
    messages.success(request, "Show updated successfully!")
    return redirect(f'/shows/{id}')

def delete_show(request, id):
    if "user_id" not in request.session:
        return redirect("/logout")
    Show.delete_show(id)
    return redirect("/shows")

def register(request):
    if "email_error" in request.session:
        del request.session['email_error']
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    results = User.objects.filter(email = request.POST['email'])
    if len(results)>0:
        request.session['email_error'] = "This email already exists, please use another email."
        return redirect("/")
    else:
        user = User.add({
            'firstName': request.POST['firstName'],
            'lastName': request.POST['lastName'],
            'email': request.POST['email'],
            "birthday": request.POST['birthday'],
            'password': bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            
        })
        request.session['user_id'] = user.id
    return redirect("/shows")

def login(request):
    if 'email_error' in request.session:
        del request.session['email_error']
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect("/shows")
    request.session['email_error'] = "Invalid Login"
    return redirect("/")

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect("/")

