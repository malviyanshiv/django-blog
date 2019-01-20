from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from blog.models import Post, Comment
from django.shortcuts import get_object_or_404
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from blog.form import CommentForm, EmailPostForm, SubscribForm
from taggit.models import Tag
from django.core.mail import send_mail

# Create your views here.

def home(requests):
    return HttpResponseRedirect(reverse('blog:blog_home'))

def blog_home(requests):
    object_list = Post.published.all()
    tag_list = requests.GET.getlist('tags[]')
    tag_list = Tag.objects.all().filter(slug__in=tag_list)
    tag_list = [a.id for a in tag_list]
    if tag_list:
        object_list = list(set(object_list.filter(tags__in=tag_list)))
    tags = Tag.objects.all()[:10]
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = requests.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(requests, "blog/index.html", {'posts':posts, 'tags':tags})

def post_detail(requests, day, month, year, slug):
    post = get_object_or_404(Post, slug=slug, status='published',publish__year=year, publish__month=month, publish__day=day)
    if requests.method == 'POST':
        comment_data = CommentForm(requests.POST)
        if comment_data.is_valid():
            new_comment = comment_data.save(commit=False)
            post.comment_count += 1
            post.save()
            new_comment.post = post
            if new_comment.name.strip() == "":
                new_comment.name = "Anonymous"
            if new_comment.email.strip() == "":
                new_comment.email = "user@email.com"
            new_comment.save()
        return redirect( post )
    comments = post.comments.filter(active=True)
    posts = Post.published.all().exclude(id=post.id)[:2]
    return render(requests, "blog/detail.html", {"post": post, "comments": comments, "posts":posts})

def post_share(requests, day, month, year, slug):
    response = {"status": 0}
    post = get_object_or_404(Post, slug=slug, status='published',publish__year=year, publish__month=month, publish__day=day)
    if requests.is_ajax():
        form = EmailPostForm(requests.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rendered = render_to_string('blog/mail.html', {'post':post, 'message':cd['comment']})
            subject = "{} recommends you to read {} blog".format(cd['name'], post.author)
            try:
                send_mail(subject, "", 'thedjangodev@gmail.com', [cd['to']], html_message=rendered, fail_silently=False)
            except:
                return JsonResponse(response)
            response['status'] = 1
            return JsonResponse(response)

def post_download(requests, day, month, year, slug):
    #code to convert the file to pdf to download
    print("Received a download post request")
    return HttpResponseRedirect(reverse('blog:post_detail', args=[day, month, year, slug]))

def post_like(requests, day, month, year, slug):
    data = { 'is_done': 0 }
    try:
        post = get_object_or_404(Post, slug=slug, status='published',publish__year=year, publish__month=month, publish__day=day)
    except:
        return JsonResponse(data)
    if requests.is_ajax():
        post.like_count += 1
        post.save()
        data['is_done'] = post.like_count
        return JsonResponse(data)

def blog_subscribe(requests):
    res = { "status" : 0 }
    if requests.is_ajax():
        new_sub = SubscribForm(requests.POST)
        if new_sub.is_valid():
            new_sub.save()
            print("Got a new use " + new_sub)
            res["status"] = 1
            return JsonResponse(res)
    return HttpResponseRedirect(reverse('blog:blog_home'))
