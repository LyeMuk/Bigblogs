from django.shortcuts import render, redirect
from . forms import UserRegisterForm
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import UserRegister


# Create your views here.

def password_check(passwd): 
    SpecialSym =['$', '@', '#', '%']
    val = "" 
    if len(passwd) < 6:
        val ='length should be at least 6'
        return val     
    if len(passwd) > 20:
        val ='length should be not be greater than 20'
        return val     
    if not any(char.isdigit() for char in passwd):
        val ='Password should have at least one numeral'
        return val    
    if not any(char.isupper() for char in passwd):
        val ='Password should have at least one uppercase letter'
        return val    
    if not any(char.islower() for char in passwd):
        val ='Password should have at least one lowercase letter'
        return val    
    if not any(char in SpecialSym for char in passwd):
        val ='Password should have at least one of the symbols $@#'
        return val
    return val

def loggin(request):
    contex={'Alert':''}
    if request.method=='POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username= username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                contex['Alert']="Login Credentials could not match/ wrong credentials"
        return render(request, 'blog/login.html', contex)     
    return render(request, 'blog/login.html', contex)

def signup(request):
    contex={}
    contex['Alert']=""
    if request.method=='POST':
        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                if password_check(form['password'].value())!="":
                    raise Exception(password_check(form['password'].value()))
                user = User.objects.create_user(username=form['uname'].value(),email=form['email'].value(),password=form['password'].value())
                form.save()
                user = authenticate(username= form['uname'].value(), password=form['password'].value())
                login(request, user)
                return redirect("home")
            except Exception as exp:
                contex['Alert']=exp
    regForm = UserRegisterForm()
    contex['regForm']=regForm
    return render(request, 'blog/signup.html', contex)

def forgot(request):
    contex={}
    if request.method=='POST':
        try:
            uname=request.POST['uname']
            email=request.POST['email']
            sques=request.POST['sques']
            passw=request.POST['passw']
            repass=request.POST['repass']
            if passw!=repass:
                raise Exception("Password Not matched")
            userobj = User.objects.get(username=uname , email=email)
            regobj = UserRegister.objects.get(uname=uname , email=email)
            if userobj and regobj:
                if regobj.securityQuestion == sques:
                    userobj.set_password(passw)
                    userobj.save()
                    regobj.password = passw
                    regobj.save() 
                    contex['sucess']="password changed sucessfully please consider login"
                    return render(request, 'blog/login.html', contex)  
                else:
                    contex['Alert']="security question answe dont match"


        except Exception as exp:
            contex['Alert']=exp
    return render(request, 'blog/forgot.html', contex)


def home(request):
    contex={}
    contex['welcome']=f"{request.user.username} to blog/news app"
    return render(request, 'blog/home.html', contex)

