from django.shortcuts import render, redirect
from . forms import UserRegisterForm
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import UserRegister, blogg
from newsapi import NewsApiClient
from datetime import datetime, date,  timedelta

# API_KEY = 462c26db18924aa4af4acffa50de5a05



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import blogg,  ItemSerializer
from rest_framework import status

# Global Variables
all_articles=None
st = 0
ed = 10
incr = 10
curr_frame=None


# Create your views here.
def open(request, num):
    contex={}
    if all_articles!=None:
        contex['detail']=all_articles['articles'][num:num+1]
        print(all_articles['articles'][0:1])
    return render(request, 'blog/detail.html', contex)

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
    global all_articles, st, ed, incr, curr_frame
    contex['welcome']=f"{request.user.username} to blog/news app"
    newsapi = NewsApiClient(api_key='462c26db18924aa4af4acffa50de5a05')

    today = date.today()
    pretoday = today - timedelta(days=2)

    all_articles = newsapi.get_everything(
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.in,techcrunch.com',
                                      from_param=pretoday,
                                      to=today,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

    place = st
    articel =[]
    for x in all_articles['articles'][st:ed]:
        x['ssid']=place
        place=place+1
        x['publishedAt']=x['publishedAt'].split('T')[0]
        x['publishedAt']=datetime.strptime(x['publishedAt'], "%Y-%m-%d")
        x['publishedAt']=x['publishedAt'].strftime("%d-%b-%Y")
        articel.append(x)
    contex['articel']=articel
    curr_frame={'articel':articel}

    allBlog = blogg.objects.all()
    for x in allBlog:
        x.content=x.content[:250]
    contex['allBlog']=allBlog


    return render(request, 'blog/home.html', contex)







    # print(st, ed, incr)
    # datetime_str="2022-11-27T20:30:32Z"
    # datetime_str = datetime_str.split('T')[0]
    # dateobj = datetime.strptime(datetime_str, "%Y-%m-%d")
    # print(dateobj)







    # today = date.today()
    # print(today, "------------------------------------------------Today")
    # pretoday = today - timedelta(days=2)
    # print(pretoday, "------------------------------------------------pretoday")

def nexxt(request):
    global st, ed, incr
    st = st+incr
    ed = ed+incr
    return redirect(home)

def prior(request):
    global st, ed, incr
    st = st-incr
    ed = ed-incr
    return redirect(home)

def delit(request, num):
    instance = blogg.objects.get(bid=num)
    instance.delete()
    return redirect(dashboard)

def dashboard(request):
    contex={}
    if request.method=='POST':
        titel = request.POST.get('titel')
        contentt = request.POST.get('Contentt')
        authorname = request.user.username
        now = datetime.now() 
        date_time = now.strftime("%m/%d/%Y")
        print(date_time, authorname, contentt, titel, "-----------------------------------------------------")
        if titel!="" and contentt!="":
            v=blogg(title=titel, content=contentt, authorname=authorname, bdate=date_time)
            v.save()

    userblog=blogg.objects.filter(authorname=request.user.username).values()
    contex['userblog']=userblog
    return render(request, 'blog/dashboard.html', contex)

def logout(request):
    request.session.clear()
    return redirect(loggin)

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/api/all',
        'Add': '/api/create/',
        'Update': '/api/update/<int:pk>/',
        'Delete': '/api/blog/<int:pk>/delete/'
    }
  
    return Response(api_urls)


@api_view(['POST'])
def add_items(request):
    item = ItemSerializer(data=request.data)
  
    # validating for already existing data
    if blogg.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    items = blogg.objects.all()
    serializer = ItemSerializer(items, many=True)

    # if there is something in items else raise error
    if items:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_items(request, pk):
    item = blogg.objects.get(pk=pk)
    data = ItemSerializer(instance=item, data=request.data)
  
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_items(request, pk):
    try:
        item = blogg.objects.get(bid=pk)
        res = item
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    