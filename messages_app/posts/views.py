from django.shortcuts import redirect,render
from .models import Messages,comments,User
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
from django.http import HttpResponse

def userregister(request):
    if request.user.is_authenticated:
        return redirect("/postList/")
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('user created')
            return redirect("/login/")
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
                return redirect('/postList/')
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

def postsList(request):
    if request.user.is_authenticated:
        posts=Messages.objects.order_by('-posted_date')
        return render(request=request,template_name='postList.html',context={"posts":posts,"user":request.user})
    else:
        return redirect("/login/")
    
def comment_section(request,post_id):
    post=get_object_or_404(Messages,id=post_id)
    comments_list=comments.objects.filter(post=post).order_by('-posted_date')
    data={
        'post':post,
        'comments': comments_list,
        'length' : len(comments_list),
    }
    return render(request=request,template_name="comment_section.html",context=data)

def add_comment(request,post_id):
    if request.method=="POST":
        if request.user.is_authenticated:
            # print('reached till here')
            comments.add_comment(curr_user_id=request.user.id,post_id=post_id,comment=request.POST['comment'])
            print('posted comment')
            return redirect(f"/postList/{post_id}/comments")
        else:
            redirect("/logout/")
    else:
        return redirect(f"/postList/{post_id}/comments")

def editpost(request,pk,pk1):
    post=get_object_or_404(Messages,id=pk1)
    if request.method=="POST":
        if request.user.is_authenticated:
            post.title=request.POST['Title']
            post.message=request.POST['Content']
            post.image.delete()
            post.image=request.FILES.get('Image')
            print(post.image.url)
            post.save()
            return redirect("/postList/" + pk)
        else:
            return redirect('/')
    else:
        data={
            'title':post.title,
            'message':post.message,
            'id':post.id,
            'image':post.image
        }
        print('reached till here')
        return render(request=request,template_name="editpost.html",context=data)
def deletepost(request,pk,pk1):
    if request.user.is_authenticated:
        try:
            post = get_object_or_404(Messages, id=pk1)
            post.delete()
            return redirect("/postList/" + pk)
        except:
            return HttpResponse("post is already deleted")
def myposts(request,pk):
    if request.user.is_authenticated:
        try:
            posts=Messages.objects.filter(user_id=pk).order_by('-posted_date')
            if request.user==posts[0].user:
                # print(type(posts))
                return render(request=request,template_name='my_posts.html',context={"posts":posts})
        except:
            return HttpResponse("No posts available")
    return redirect("/postList/")

def postCreate(request,pk):
    if request.method=="POST":
        if request.user.is_authenticated:
            data={'title':request.POST['Title'],
                'message':request.POST['Content'],
                'image':request.FILES.get('Image'),}
            data['user']=str(request.user.id)
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect("/postList/")
            else:
                return render(request=request,template_name="postCreate.html")
        else:
            return redirect('/')
    else:
        return render(request=request,template_name="postCreate.html")
    
from django.http import JsonResponse
def postlike(request,pk):
    if request.user.is_authenticated:        
        if request.method=='POST':
            # try:
            print("pk", pk)
            post = get_object_or_404(Messages, id=pk)
            # print("post", post.)
            print("likes", post.likes.count()) 
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            
            data = {'likes': post.likes.count()}
            return JsonResponse(data)
            # except:
            #     print('something went wrong')
        posts=Messages.objects.all().order_by('-posted_date')
        return render(request=request,template_name="postList.html",context={"posts":posts})
    return redirect("/login/")

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
            "title" : "enter the title of your post",
            "message": "enter your message here",
            }
            return Response(contents)
        elif request.method == 'POST':
            data=request.data
            data['user']=str(request.user.id)
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return redirect("/post-api/post-list/")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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



