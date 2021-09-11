from msilib.schema import ListView

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import date, datetime
from app1 import models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect,csrf_exempt,requires_csrf_token


# Create your views here.
from app1.models import Posts, Likes, Comments, Addfriendnew,Admin,Block,Profilepic


def search(request):

    if request.method=='POST':
        searched = request.POST.get("search")
        s=Posts.objects.filter(username=searched)
        print(s)
        username = request.session['username']
        data = Addfriendnew.objects.filter(username=username, followingusername=searched)
        if (data.count() == 0):
            data="2"
            print(data)
        return render(request, 'search.html',{'search':searched , 's':s ,'data':data})
    return render(request, 'search.html')

# class SearchView(ListView):
#     model = User
#     template_name = 'search.html'
#     context_object_name = 'all_search_results'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_name = self.request.GET.get('username', '')
#         context['all_search_results'] = User.objects.filter(username__icontains=user_name)
#         return context

def addpost(request):
    print("iiiiii")
    username = request.session['username']
    res = render(request,'addpost.html',{'username':username})
    return res

# @csrf_exempt


def like_post(request):
    # if request.is_ajax():
    #     username = request.post.get('like_username')
    #     print(username)
    #     print("working")
    # else:
    #     print("not working")

    if request.method == 'GET':
        post_id = request.GET['post_id']
        post_like_name = request.GET['post_like_name']

        l = models.Likes()

        l.post_id = post_id
        l.like_username = post_like_name

        l.save()

        print(post_id)
        print(post_like_name)


        # likedpost = Posts.obejcts.get(pk=post_id) #getting the liked posts
        # m = Likes(post=likedpost) # Creating Like Object
        # m.save()  # saving it to store in database
        # return HttpResponse(post_id) # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")

    # return HttpResponse(str("shubham"))

def mypost(request):
    username = request.session['username']
    posts=models.Posts.objects.filter(username=username).order_by('time')
    # posts=models.Posts.objects.all()
    res = render(request,'mypost.html',{'username':username,'posts':posts})
    return res

def upload(request):
    if request.method=='POST':
        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)
        img_name=uploaded_file.name

        # res = render(request,'eyebook/addpost',{'img_name':img_name})

        return redirect('/addpost')


def add(request):
    if request.method=='POST':

        post=models.Posts()

        usename = request.session['username']
        today = date.today()

        post_text = request.POST['post_text']

        uploaded_file = request.FILES['document']
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        print(uploaded_file.name)
        print(uploaded_file.size)

        img_name=uploaded_file.name

        # post.post_id =
        post.username = usename
        post.time = today
        post.post_text = post_text
        post.post_img = img_name

        print(post.post_id)

        post.save()

        return HttpResponseRedirect('/mypost')

@login_required(login_url='/login')
def home(request):
    username = request.session['username']
    posts=models.Posts.objects.all()
    likes=models.Likes.objects.all()
    profpic=Profilepic.objects.all()
    res = render(request,'home.html',{'username':username,'posts':posts,'likes':likes,'profpic':profpic})
    return res

def confirm(request):
    res = render(request,'confirmation.html')
    return res


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        role=Admin.objects.get(username=username)
        print(role.roll)
        role1=role.roll
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username

            if role1 == "1":
                user=User.objects.all()
                block=Block.objects.all()
                return render(request,"admin.html",{'user':user,'block':block})
            elif role1 == "2":
                block=Block.objects.filter(username=username)
                if block == "blocked":
                    return render(request,"blocked.html")
                else:
                    return redirect('/home')


        else:
            print("Invalid Credentials")
            msg = "*Invalid Credentials"
            res = render(request,'login.html',{'msg':msg})
    else:
        res = render(request,'login.html')
    return res

def userLogout(request):
    auth.logout(request)
    return redirect('/app/login')

def sign_up_page(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        username = email.split('@')[0]
        password1=request.POST['password1']
        password2=request.POST['password2']
        if len(password1)<8:
            print("Password should be minimum 8 characters")
            msg = "*Password should be minimum 8 characters"
            res = render(request,'sign_up.html',{'msg':msg})
        elif password1==password2:
            if User.objects.filter(username=username).exists():
                print("Email already exists")
                msg = "*Email already exists"
                res = render(request,'sign_up.html',{'msg':msg})
            else:
                user = User.objects.create_user(username=username , password=password1 , email = email,first_name = name)
                user.save()
                ab = Admin()
                ab.username = username
                ab.roll = "2"
                ab.save()
                bk=Block()
                bk.username=username
                bk.status="unblock"
                bk.save()
                print("user created")
                return redirect('/confirmation')
                # res = render(request,'eyebook/home.html')
        else:
            print("Password not matching")
            msg = "*Password not matching"
            res = render(request,'sign_up.html',{'msg':msg})
    else:
        res = render(request,'sign_up.html')
    return res

def newcomment(request,post_id):
    obj=post_id;
    ob=Comments.objects.filter(post_id=post_id)
    return render(request,'comment.html',{'post_id':obj,'ob':ob})

def commentview(request,post_id):
    if request.method=='POST':
        ct = Comments()
        print(post_id)
        ct.post_id = post_id
        ct.username=request.session.get("username")
        ct.comment = request.POST.get("comment")
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y,%H:%M:%S")
        ct.DATE = date_time
        ct.save()
        return redirect('/home')

def follow(request):
    if request.method=='POST':
        ab= Addfriendnew()
        username = request.session['username']
        searched = request.POST.get('follow')
        data = Addfriendnew.objects.filter(username=username, followingusername=searched)
        if (data.count() == 0):
            ab.username=username
            ab.followingusername=searched
            ab.status= request.POST.get('followstatus')
            ab.save()
            return redirect('/home')
        else:
            st= Addfriendnew.objects.get(username=username, followingusername=searched)
            st.status = request.POST.get('followstatus')
            st.save()
            return redirect('/home')

def admin_view(request,username):
    post=Posts.objects.filter(username=username)
    return render(request,"admin_view.html",{'post':post})

def post_view(request,post_id):
    post=Posts.objects.filter(post_id=post_id)
    comment=Comments.objects.filter(post_id=post_id)
    like=Likes.objects.filter(post_id=post_id)
    return render(request,"admin_postview.html",{'post':post,'comment':comment,'like':like})


def block(request,username):
    if request.method=="POST":
        ac=Block()
        ac.username=username
        ac.status=request.POST.get('status')
        ac.save()
        return redirect('/login')

def profile_pic(request):
    return render(request,"profilepic.html")

def prof_pic(request):
    ab = Profilepic()
    ab.username=request.session['username']
    profile_pic= request.FILES['img']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    uploaded_file_url = fs.url(filename)
    ab.profile_pic = uploaded_file_url
    ab.save()
    return redirect('/home')





