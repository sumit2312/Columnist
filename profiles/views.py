from django.shortcuts import render,redirect,HttpResponseRedirect,reverse,get_object_or_404

from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime
# from django.views.generic.simple import direct_to_template

# from .forms import ContactForm,MyUserForm,RegisterForm,LoginForm
# from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from profiles.models import MyUser,Tweet,Comment

from .forms import MyUserCreationForm,TweetForm,ReviewForm


# ----DECORATOR

from django.contrib.auth.decorators import user_passes_test

def is_author(user):
    if user.user_type=="AUTHOR":
        return True
    return False

def is_editor(user):
    if user.user_type=="EDITOR":
        return True
    return False

#  ---- END DECORATOR

class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@user_passes_test(is_author)
def author_base(request):
    return render(request,'author/author.html')


@user_passes_test(is_editor)
def editor_base(request):
    return render(request,'editor/editor.html')



@login_required
def where_next(request):
    """Simple redirector to figure out where the user goes next."""
    if request.user.user_type=="AUTHOR":
        return HttpResponseRedirect(reverse('author-profile'))
    elif request.user.user_type=="EDITOR":
        return HttpResponseRedirect(reverse('editor-profile'))




@user_passes_test(is_author)
def post_tweet(request, tweet_id=None):
    tweet = None
    if tweet_id:
        tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            print("VALID")
            print(request.user)
            new_tweet = form.save(commit=False)
            new_tweet.author = request.user
            new_tweet.state = 'pending'
            new_tweet.save()
            # send_review_email()
            return HttpResponseRedirect(reverse('thank-you'))
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'author/post_tweet.html',{'form': TweetForm(instance=tweet)})


@user_passes_test(is_author)
def thank_you(request):
    tweets_in_queue = Tweet.objects.filter(state='pending').filter(author=request.user)
    tweets_accepted = Tweet.objects.filter(state='published').filter(author=request.user)
    tweets_rejected = Tweet.objects.filter(state='rejected').filter(author=request.user)
    return render(request, 'author/thank_you.html',{'tweets_in_queue': tweets_in_queue ,
                    'tweets_accepted':tweets_accepted,'tweets_rejected':tweets_rejected})


@user_passes_test(is_author)
def tweet_detail(request , tweet_id):
    template_name='author/post-detail.html'
    tweet = get_object_or_404(Tweet , id = tweet_id)
    if tweet.author!=request.user:
        print("NONNONONON")
    comments = tweet.comments.all()
    print(tweet,comments)
    return render(request,template_name,{'tweet':tweet,'comments':comments})


@user_passes_test(is_editor)
def list_tweets(request):
    pending_tweets = Tweet.objects.filter(state='pending').order_by('created_at')
    published_tweets = Tweet.objects.filter(state='published').order_by('-published_at')
    return render(request, 'editor/list_tweets.html',{'pending_tweets': pending_tweets,
                                            'published_tweets': published_tweets})


@user_passes_test(is_editor)
def review_tweet(request, tweet_id):
    reviewed_tweet = get_object_or_404(Tweet, id=tweet_id)
    print(review_tweet)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_comment = form.cleaned_data['new_comment']
            if form.cleaned_data['approval'] == 'approve':
                # publish_tweet(reviewed_tweet)
                # send_approval_email(reviewed_tweet, new_comment)
                reviewed_tweet.published_at = datetime.now()
                reviewed_tweet.state = 'published'
            else:
                # link = request.build_absolute_uri(reverse(post_tweet, args=[reviewed_tweet.id]))
                # send_rejection_email(reviewed_tweet, new_comment,link)
                reviewed_tweet.state = 'rejected'
                reviewed_tweet.save()
                if new_comment:
                    c = Comment(tweet=reviewed_tweet, text=new_comment)
                    c.save()
            return HttpResponseRedirect(reverse('editor-list'))
    else:
        form = ReviewForm()
        return render(request, 'editor/review_tweet.html', {'form': form, 'tweet': reviewed_tweet,
                        'comments': reviewed_tweet.comment_set.all()})



# class HomePageView(ListView):
#     model = MyUser

# def index(request):
#     return render(request,'profile.html')

# def testing(request):
#     if request.method=="POST":
#         form = RegisterForm(request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#             email=form.cleaned_data['email']
#             print(email)
#             print("VALID")
#             form.save()
#             username = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return HttpResponseRedirect(reverse('index'))

#     form=RegisterForm()
#     return render(request,'form.html',{'form':form})



# def user_login(request):
#     if request.method=="POST":
#         form = LoginForm(request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#             username=form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 print("Not --")
            
#     form = LoginForm()
#     return render(request,'register.html',{'form':form})


# class UserProfileView(View):
#     def get(self, request, user_id):

#         try:
#             user = MyUser.objects.get(id=user_id)
#         except:
#             user = None

#         context = {
#             "viewed_user": user
#         }

#         return render(request, "user_profile.html", context)


# def contact(request):
#     if request.method=="POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name=form.cleaned_data['name']
#             email=form.cleaned_data['email ']

#             print(name,email)
#     form=ContactForm()
#     return render(request,'form.html',{'form':form})
