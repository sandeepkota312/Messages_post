from django.shortcuts import redirect,render
from .models import Messages
from .serializers import MessageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

def userregister(request):
    if request.user.is_authenticated:
        return redirect("/post-api/")
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('user created')
            return redirect("/login/")
            # login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            # print('user logged in')
            # messages.success(request, "Registration successful.")
            # return redirect("/post-api/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": form})


def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # print('reached')
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/post-api/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def userlogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

@api_view(['GET'])
def apiOverview(request):
    if request.user.is_authenticated:
        main_contents={
            'to log out user' : '/logout/',
            'Create post': 'post-create/',
            'List or filter posts': 'post-list/',
            'post Details View-Update-Delete': 'post-list/id/',
        }
        return Response(main_contents)
    else:
        user_auth_contents={
            'create a account' : '/',
            'login to account' :'/login/',
        }
        return Response(user_auth_contents)

@api_view(['GET','POST'])
def postcreateandview(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            contents = {
            "user":"enter the user id, your id is "+str(request.user.id),
            "title" : "enter the title of your post",
            "message": "enter your message here",
            "count" : 0,
            }
            return Response(contents)
        elif request.method == 'POST':
            serializer = MessageSerializer(data=request.data)
            # print(type(request.user.id))
            # print(type(request.data['user']))
            if str(request.user.id)==request.data['user']:
                if serializer.is_valid():
                    serializer.save()
                    return redirect("/post-api/post-list/")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('*')
                return redirect("/post-api/post-create/")
    else:
        contents={
            "You need to login first":"/login/",
            "create a user":"/",
            }
        return Response(contents)



@api_view(['GET'])
def postList(request):
    if request.user.is_authenticated:
        List=Messages.objects.order_by('-posted_date')
        for ind in List:
            ind.count=ind.likes.count()
        data=[]
        for content in List:
            data.append(content)
        serializer=MessageSerializer(data,many=True)
        return Response(serializer.data)
    else:
        contents={
            "To login your user account":"/login/",
            "create a user":"/",
            }
        return Response(contents)



@api_view(['GET','POST','DELETE'])
def postDetail(request,pk):
    Data = Messages.objects.get(id=pk)
    Data.count=Data.likes.count()
    if request.user.is_authenticated:
        if request.user==Data.user:
            if request.method=='GET':
                try:
                    serializer = MessageSerializer(Data, many=False)
                    return Response(serializer.data)
                except Messages.DoesNotExist:
                    raise Http404("post does not exist")
            elif request.method =='POST':
                Data = Messages.objects.get(id=pk)
                serializer = MessageSerializer(instance=Data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                return Response(serializer.data, status=status.HTTP_304_NOT_MODIFIED)
            elif request.method == 'DELETE':
                Data = Messages.objects.get(id=pk)
                Data.delete()
                return Response("post removed successfully.")
        else:
            return redirect('/post-api/post-list/'+str(pk)+'/like')
    else:
        contents={
            "To login your user account":"/login/",
            "create a user":"/",
            }
        return Response(contents)

@api_view(['GET','POST'])
def postLike(request,pk):
    if request.user.is_authenticated:        
        if request.method=='GET':
            post=Messages.objects.filter(id=pk).order_by('-posted_date')
            for ind in post:
                ind.count=ind.likes.count()
            data=[]
            for content in post:
                data.append(content)
            serializer=MessageSerializer(data,many=True)
            return Response(serializer.data)
        elif request.method=='POST':
            post = get_object_or_404(Messages, id=pk)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            print('hi')
            return redirect("/post-api/post-list/")
    else:
        contents={
            "To login your user account":"/login/",
            "create a user":"/",
            }
        return Response(contents)



