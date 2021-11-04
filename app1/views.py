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


from nltk.corpus import stopwords
import difflib
from app1.RedundentCharacterRemover import RemoveRedundentCharacters
from app1.StemingProcess import steming
from app1.PunctuationRemover import RemovePunctuations
from app1.n_gram_terms_extraction import one_gram,two_gram,three_gram,four_gram
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from difflib import SequenceMatcher
import math
import app1.SynonymsRemover

from .models import ThreadModel, MessageModel
from .forms import ThreadForm, MessageForm
from django.views import View
from django.db.models import Q

# Create your views here.
from app1.models import Posts, Likes, Comments, Addfriend,Admin,Profilepic


def search(request):

    if request.method=='POST':
        searched = request.POST.get("search")
        s=Posts.objects.filter(username=searched)
        print(s)
        username = request.session['username']
        data = Addfriend.objects.filter(username=searched, followingusername=username) | Addfriend.objects.filter(username=username,followingusername=searched)
        if (data.count() == 0):
            data="8"

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
    print(username)
    request1 = Addfriend.objects.filter(followingusername=username,status=1)
    request2 = request1.count
    profilepic = Profilepic.objects.filter(username=username)
    friend=Addfriend.objects.all()
    res = render(request,'home.html',{'username':username,'posts':posts,'likes':likes,'profilepic':profilepic,'request1':request1,
                                      'request2':request2,'friend':friend})
    # res = render(request, 'newhome.html',
    #              {'username': username, 'posts': posts, 'likes': likes, 'profilepic': profilepic, 'request1': request1,
    #               'request2': request2, 'friend': friend})
    return res

def confirm(request):
    res = render(request,'confirmation.html')
    return res


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            role = Admin.objects.get(username=username)
            print(role.roll)
            role1 = role.roll
            auth.login(request, user)
            request.session['username'] = username


            if role1 == "1":
                user = User.objects.all()
                
                return render(request,"admin.html",{'user':user})
            elif role1 == "2":
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


def IncreSTS(vector):
    cluster = ClustersNames.objects.values_list('cluster', flat=True)
    if cluster:
        for c in cluster:
            ratio = SequenceMatcher(None, vector, c).ratio()
            print(ratio)
            if ratio > 0.6:
                return c
            else:
                return vector
    else:
        ClustersNames(cluster=vector).save()
        return vector


def batchSTS1(vector):
    cluster = ClustersNames.objects.values_list('cluster', flat=True)
    if cluster:
        for c in cluster:
            ratio = SequenceMatcher(None, vector, c).ratio()
            print(ratio)
            if ratio > 0.6:
                return c
            else:
                return vector
    else:
        ClustersNames(cluster=vector).save()
        return vector


def batchSTS():
    comments = Comments.objects.values_list('comment', flat=True)
    for comment in comments:

        stopword = set(stopwords.words('english'))
        print ("Removing Punctuations.......")
        a = RemovePunctuations(comment)
        print ("Removing Redundent Characters.......")
        newstring = RemoveRedundentCharacters(a)
        print ("Stemming.........")
        newstring = steming(newstring)
        print ("Onegram.......")
        gram1 = one_gram(newstring)
        print (gram1)
        print ("Twogram.......")
        gram2 = two_gram(newstring)
        print (gram2)
        print ("Threegram.......")
        gram3 = three_gram(newstring)
        print (gram3)
        print ("Fourgram.......")
        gram4 = four_gram(newstring)
        print (gram4)
        print ("Vectoraisation.......")
        v = [i for i in newstring.lower().split() if i not in stopword]
        vector = ""
        for i in v:
            vector = vector + " " + i
        print (vector)

        clustercomment = batchSTS1(vector)
        cluster = ClustersNames.objects.filter(cluster=clustercomment)
        if cluster:
            Clusters(cluster=clustercomment, comment=comment).save()
        else:
            ClustersNames(cluster=clustercomment).save()
            Clusters(cluster=clustercomment, comment=comment).save()


def incrests(request):
    clust = []
    cluster = ClustersNames.objects.values_list('cluster', flat=True)
    clustr = Clusters.objects.values_list('cluster', flat=True)

    for cl in cluster:
        clust.append(cl)
    d = {}
    for i in clust:
        j = 0
        for k in clustr:
            if k == i:
                j = j + 1
        d[i] = j
    print (d)
    val = d.values()
    sorte = []
    big = -1
    for i in val:
        for j in range(0, len(d) - 1):
            if val[j] >= val[j + 1]:
                if j not in sorte:
                    big = j
        sorte.append(big)
    print (sorte, "sorted")

    print (val)
    total = 0
    average = []
    avg = float()
    for i in d.values():
        total = total + i
    print (total)
    for i in d.values():
        avg = round((float(i) / float(total)) * 100, 3)
        print (avg)
        average.append(avg)
    print (average)
    #     temp=average
    #     average.sort()
    #     sorted_average=average
    avg_cluster = []
    for i in d.keys():
        if i not in avg_cluster:
            avg_cluster.append(i)
    print (avg_cluster)
    top_k = 10
    top_avg = []
    print (sorte)
    for i in range(0, top_k):
        print (sorte[i])
        top_avg.append(average[sorte[i]])
    print  (top_avg)
    top_cluster = []
    for i in range(0, top_k):
        top_cluster.append(avg_cluster[sorte[i]])

    return render(request, 'watermark.html', {'clust': top_cluster, 'average': top_avg})


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

        clustersadded = []
        allcom = Comments.objects.all()
        allcomli = []
        for i in allcom:
            allcomli.append(i.comment)
        print(allcomli)
        allcomliremoved = allcomli
        print("Started...")
        for c in allcomli:
            print(c)
            cii = difflib.get_close_matches(c, allcomliremoved)
            print(cii)
            clustersadded.append(cii)
            for ci in cii:
                allcomliremoved.remove(ci)
            print(allcomliremoved)
        print (clustersadded)
        test = difflib.get_close_matches('nic', ['nicc', 'very good', 'very good', 'goood', 'very good', 'very good', 'goood', 'nice', 'nice', 'nice', 'nice', 'nice', 'good', 'nice', 'very good', 'good', 'goood', 'god'])
        print(test)

        return redirect('/home')


def clusteringReq(request):
        comment = request.POST.get("comment")

        # if comment:
        # s = Comments(user=request.session['username'], comment=comment)
        # s.save()
        # print (comment)
        comments = Comments.objects.values_list('comment', flat=True)
        # for comment in comments:

        import nltk
        nltk.download('stopwords')
        # stopword = set(stopwords.words('english'))
        # print ("Removing Punctuations.......")
        a = RemovePunctuations(comment)
        # print ("Removing Redundent Characters.......")
        newstring = RemoveRedundentCharacters(a)
        # print ("Semming.........")
        newstring = steming(newstring)
        # print ("Onegram.......")
        gram1 = one_gram(newstring)
        # print (gram1)
        # print ("Twogram.......")
        gram2 = two_gram(newstring)
        # print (gram2)
        # print ("Threegram.......")
        gram3 = three_gram(newstring)
        # print (gram3)
        # print ("Fourgram.......")
        gram4 = four_gram(newstring)
        print (gram4)
        # print ("Vectoraisation.......")
        v = [i for i in newstring.lower().split() if i not in stopword]
        Sym = SynonymsRemover.synonyms(v)
        v = Sym
        vector = ""
        for i in v:
            vector = vector + " " + i
        print (vector)

        clustercomment = IncreSTS(vector)
        cluster = ClustersNames.objects.filter(cluster=clustercomment)
        if cluster:
            Clusters(cluster=clustercomment, comment=comment).save()
            comments = Comments.objects.values_list('comment', flat=True)
            user = Comments.objects.values_list('user', flat=True)
            c = list(comments)
            u = list(user)
            usercomment = zip(u, c)
            # return render(request, 'upload.html', {'user': usercomment})
        else:
            ClustersNames(cluster=clustercomment).save()
            Clusters(cluster=clustercomment, comment=comment).save()
            comments = Comments.objects.values_list('comment', flat=True)
            user = Comments.objects.values_list('user', flat=True)
            c = list(comments)
            u = list(user)
            usercomment = zip(u, c)
            # return render(request, 'upload.html', {'usercomment': usercomment})
        # else:
        #     comments = Comments.objects.values_list('comment', flat=True)
        #     user = Comments.objects.values_list('user', flat=True)
        #     c = list(comments)
        #     u = list(user)
        #     usercomment = zip(u, c)
        #     return render(request, 'upload.html', {'usercomment': usercomment})



def follow(request):
    if request.method=='POST':
        print("hello")
        username = request.session['username']
        searched = request.POST.get('follow')

        status=request.POST.get('followstatus')
        print(username)
        print(searched)
        print(status)
        ab = Addfriend()
        if (status == "1"):
            ab.username=username
            ab.followingusername=searched
            ab.status= request.POST.get('followstatus')
            ab.notification="request send"
            ab.save()
            return redirect('/home')
        else:
            st= Addfriend.objects.get(username=searched, followingusername=username)
            st.status = request.POST.get('followstatus')
            st.notification="unfriend"
            st.save()
            return redirect('/home')

def accept(request):
    if request.method=='POST':
        followingusername = request.session['username']
        username = request.POST.get('acceptusername')
        print(followingusername)
        print(username)
        ab = Addfriend.objects.get(username=username, followingusername=followingusername)
        ab.status=request.POST.get('followstatus')
        ab.notification="accepted"
        ab.save()
        return redirect('/home')

def decline(request):
    if request.method=='POST':
        followingusername = request.session['username']
        username = request.POST.get('declineusername')
        ab = Addfriend.objects.get(username=username, followingusername=followingusername)
        ab.status = request.POST.get('followstatus')
        ab.notification="deleted"
        ab.save()
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
    ac=User.objects.get(username=username)
    ac.username=username
    ac.is_active=request.POST.get("status")
    ac.save()
    user=User.objects.all()
    return render(request,"admin.html",{'user':user})

def adminHome(request):
    user = User.objects.all()
    return render(request, "admin.html", {'user': user})

def profile_pic(request):
    return render(request,"profilepicnew.html")

def prof_pic(request):
    username = request.session['username']
    data = Profilepic.objects.filter(username=username)
    # print(data.count)
    # if (data.count == 0):
    if not data:
        ab = Profilepic()
        ab.username = request.session.get('username')
        profile_pic = request.FILES['img']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        ab.profile_pic = uploaded_file_url
        ab.save()
        return redirect('/home')
    else:
        ab = Profilepic.objects.get(username=username)
        ab.username = request.session.get('username')
        profile_pic = request.FILES['img']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        uploaded_file_url = fs.url(filename)
        ab.profile_pic = uploaded_file_url
        ab.save()
        return redirect('/home')

def landingPage(request):
    return redirect('/home')

def findfriend(request):
    user = Profilepic.objects.all()
    return render(request, "findfrients.html", {'user': user})
    # return render(request, "newTemplate.html", {'user': user})

def addFriendclick(request, username):
    print(username)
    user = Profilepic.objects.all()
    return render(request, "findfrients.html", {'user': user})

def viewCluster(request,post_id):

    comment = Comments.objects.filter(post_id=post_id)

    clustersadded = []
    allcom = comment
    allcomli = []
    for i in allcom:
        allcomli.append(i.comment)
    print(allcomli)
    allcomliremoved = allcomli
    print("Started...")
    for c in allcomli:
        print(c)
        cii = difflib.get_close_matches(c, allcomliremoved)
        print(cii)
        clustersadded.append(cii)
        for ci in cii:
            allcomliremoved.remove(ci)
        print(allcomliremoved)
    print (clustersadded)
    clustersadded.append(allcomliremoved)
    return render(request, "clusters.html", {'clusters': clustersadded})

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'inbox.html', context)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return redirect('thread', pk=pk)
