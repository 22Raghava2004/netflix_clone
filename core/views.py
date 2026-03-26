from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

from .models import Movie
from django.contrib.auth.decorators import login_required
import re
from django.shortcuts import get_object_or_404
from .models import Movie,MovieList

@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies.last()
    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request, "index.html",context)

def search(request):
    if request.method=='POST':
        search_term=request.POST.get('search_term')
        movies=Movie.objects.filter(title__icontains=search_term)
        context={
            'movies':movies,
            'search_term':search_term,

        }
        return render(request,'search.html',context)
    else:
        return redirect('/')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        
        else:
            messages.info(request,"user name not founf")
            return redirect('signup')
    return render(request,'login.html')

@login_required(login_url='login')
def movie(request,pk):
    movie_uuid=pk
    movie_details=Movie.objects.get(uu_id=movie_uuid)
    context={
        'movie_details':movie_details

    }
    return render(request,'movie.html',context)




def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #user login
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                return redirect('/')
        else:
            messages.info(request,'password not matching')
            return redirect('signup')
    else:
        return render(request,'signup.html')

@login_required(login_url='login')
@require_POST
def add_to_list(request):
    if request.method=='POST':
        movie_url_id=request.POST.get('movie_id')
        uuid_pattern=r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        match =re.search(uuid_pattern,movie_url_id)
        movie_id=match.group() if match else None

        movie=get_object_or_404(Movie,uu_id=movie_id)
        movie_list,created= MovieList.objects.get_or_create(owner_user=request.user,movie=movie)

        if created:
            response_data={'status':'success','message':'Added '}
        else:
            response_data={'status':'info','message':'already added'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status':'error','message':'invalid request'},status=400)
        
    
@login_required(login_url='login')
def my_list(request):
    movie_list=MovieList.objects.filter(owner_user=request.user)
    user_movie_list=[]

    for movie in movie_list:
        user_movie_list.append(movie.movie)
    context={
        'movies':user_movie_list
    }
    return render(request,'my_list.html',context)



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload(request):
    context={}
    if request.method=='POST':
        title_of=request.POST.get('title')
        movie_description=request.POST.get('description')
        movie_release_date=request.POST.get('release_date')
        movie_genre=request.POST.get('genre')
        movie_length=request.POST.get('length')
        image_movie_card=request.FILES.get('image_card')
        image_movie_cover=request.FILES.get('image_cover')
        movie_video=request.FILES.get('video')
    

        new_movie=Movie.objects.create(title=title_of,description=movie_description,release_date=movie_release_date,genre=movie_genre,length=movie_length,
                                       image_card=image_movie_card,image_cover=image_movie_cover,video=movie_video)
        new_movie.save()

        MovieList.objects.create(owner_user=request.user,
                                 movie=new_movie)
        

    user_movies=MovieList.objects.filter(owner_user=request.user)

    context={
            'new_movie':user_movies
        }
    return render(request,'upload.html',context)
    
    
@login_required(login_url='login')
def genre(request,pk):
    movie_genre=pk
    movies=Movie.objects.filter(genre=movie_genre)
    context={
        'movies':movies,
        'movie_genre':movie_genre,
    }
    return render(request,'genre.html',context)