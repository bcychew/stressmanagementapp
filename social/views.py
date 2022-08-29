from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, UserProfile, Thread, UserMessage, Comment
from .forms import PostForm, ThreadForm, MessageForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.models import User 
#import the necessary models, views, mixin, forms, libraries to run the views

#postlistview takes in the loginrequiredmixin and view as input
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs): #define get request
        #define post object from models, sort by the date of creation        
        posts = Post.objects.all().order_by('-created_on')
        #define postform used to retrieve post data
        form = PostForm()
        #define context with the post object, and form
        #the post object contains all the posts posted before, and the form retrieved from the user
        context = {
            'post_list': posts,
            'form': form,
        }
        #return the get request with the following url and context defined above
        return render(request, 'social/post_list.html', context)
    #define post request for postlistview
    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST, request.FILES)
        #request.post for post, request.files for the image file to be processed
        #if the form is valid, save the form in the new post
        #and save the user who posted the form as the author
        #and save the post
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        #define context to return
        context = {
            'post_list': posts,
            'form': form,
        }
        #return the post request with the following url and context defined above
        return render(request, 'social/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
        
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('post-detail', pk=post_pk)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#class profileview for viewing user profile
class ProfileView(View):
    #define get request for profile view, this time including pk as well
    def get(self, request, pk, *args, **kwargs):
        #get user profile objects for the designated pk
        profile = UserProfile.objects.get(pk=pk)
        #get the user from the profile model
        user = profile.user
        #filter the post by the name of the user and sort by the created date
        posts = Post.objects.filter(author=user).order_by('-created_on')
        #get all the friends of the user from the profile model
        friends = profile.friends.all() 
        # if the user has no friends, the person looking at the profile of the user is not friends with the user
        if len(friends) == 0:
            are_friends = False
        #iterate through each friend the profile has
        for friend in friends:
            #if the user who requested the profile is in the friend list of the user of the profile, return are_friends = True and end the loop
            if friend == request.user:
                are_friends = True
                break
            else:   #else they are not friends
                are_friends = False

        #use len method to get the number of friends the profile user has
        friend_count = len(friends)
        #define context with user, profile, posts, friend_count and are_friends
        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'friend_count': friend_count,
            'are_friends': are_friends,
        }
        #return the request in the following url with context above
        return render(request, 'social/profile.html', context)

#define class profileeditview used to edit and update the profile details
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #using UserProfile as the model
    model = UserProfile
    #define the relevant fields for the profile
    fields = ['name', 'bio', 'birth_date', 'location', 'image']
    #define the template of the edit profile page
    template_name = 'social/profile_edit.html'
    #define get_success_url to determine the URL to redirect to when the form is successfully validated.
    def get_success_url (self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
        #return url path of profile with the designated keyword argument of pk
    #define test_func for testing if the user is verified to be the owner of the profile, if yes return true, else return false
    def test_func(self):
        profile = self.get_object() #get current object you're working on in the generic view here
        return self.request.user == profile.user #if the requested user is equal to the user on the profile, return true, otherwise false
        # if true, let them edit view, otherwise cannot access view at all

#define class addfriend that requires the user to be logged in
class AddFriend(LoginRequiredMixin, View):
    #define post request for adding friends
    def post(self, request, pk, *args, **kwargs):
        #get userprofile from the designated pk
        profile = UserProfile.objects.get(pk=pk)
        profile.friends.add(request.user)
        #add the user who requested to add the profile user as a friend of the user

        #redirect to profile, with argument pk = profile.pk
        return redirect('profile', pk=profile.pk)

#define class unfriend that requires the user to be logged in
class Unfriend(LoginRequiredMixin, View):
    #define post request for unfriend
    def post(self, request, pk, *args, **kwargs):
        #get the userprofile objects for the designated pk
        profile = UserProfile.objects.get(pk=pk)
        #removes the requested user from the list of friends in the profile
        profile.friends.remove(request.user)
        #redirect to the profile path, with the pk = pk of profile
        return redirect('profile', pk=profile.pk)

#define class searchuser
class SearchUser(View):
    #define get request for search user
    def get(self, request, *args, **kwargs):
        #save and retrieve the query from the get request
        query = self.request.GET.get('query')
        #filter the userprofile objects by the usernames that contain the query eg admin contains 'a' will show up on search results
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query)
            #Q(filter parameter, find if username matched searched query)   
        )
        #define context
        context = {
            'profile_list': profile_list,
        }
        #return the get request in social/search.html with the profile_list context
        return render(request, 'social/search.html', context)

#define class friendlist that shows the list of friends a user has
class FriendList(View):
    #define get request
    def get(self, request, pk, *args, **kwargs):
        #create profile to store UserProfile objects that match the designated pk for the user
        profile = UserProfile.objects.get(pk=pk)
        #define friends to store in all the friends of the profile user
        friends = profile.friends.all()
        #define context for the class
        context = {
            'profile': profile,
            'friends': friends,
        }
        #return the request in social/friendlist.html with the given context above
        return render(request, 'social/friendlist.html', context)

#define createthread for creating threads based on the form submitted
class CreateThread(View):
    #get request
    def get(self, request, *args, **kwargs):
        #retrieve threadform
        form = ThreadForm()
        #define context
        context = {
            'form': form
        }
        #return request in the following link with given context above
        return render(request, 'social/create_thread.html', context)
    
    #Post request
    def post(self, request, *args, **kwargs):
        #take in threadform with post request
        form = ThreadForm(request.POST)
        #define variable username by deriving the username from the post request
        username = request.POST.get('username')

        #redirects to thread where user is the receiver, or sender
        try:
            receiver = User.objects.get(username=username)
            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = Thread(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')

#class function for writing new message
class WriteNewMessage(View):
    #define post request
    def post(self, request, pk, *args, **kwargs):
        #get threads
        thread = Thread.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        #create new message 
        message = UserMessage(
            thread=thread,
            message_sender=request.user,
            message_receiver=receiver,
            body=request.POST.get('message'),
        )
        #saves the message and redirects to thread
        message.save()
        return redirect('thread', pk=pk)

#class for viewing thread
class ViewThread(View):
    #define get request
    def get(self, request, pk, *args, **kwargs):
        #filter desired thread with list of messages based on pk
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        message_list = UserMessage.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        #render request in thread.html with above context
        return render(request, 'social/thread.html', context)


#class function to show all ongoing threads
class ShowAllThreads(View):
    #get request
    def get(self, request, *args, **kwargs):
        #filter threads when sender is the requested user, or when the receiver the is the requested user, for both directions
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }
        #render request in mail.html with threads context
        return render(request, 'social/mail.html', context)

class Like(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
        #to redirect to previous page

class LikeComments(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
