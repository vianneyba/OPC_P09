from itertools import chain
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from review.models import UserFollows, Review, Ticket
from review.forms import SubscriptionForm, TicketForm, ReviewForm
from django.db.models import Value, Q, CharField

def view_my_post(request):
    html_template = './review/accueil.html'
    reviews = Review.objects.filter(user=request.user)
    context = {
        'my_posts': True,
        'reviews': reviews
    }
    return render(request, html_template, context)

@login_required()
def acceuil(request):
    html_template = './review/accueil.html'
    followed_users = list(UserFollows.objects.filter(user=request.user).values_list('followed_user__id', flat=True))
    followed_users.append(request.user.id)
    reviews = Review.objects.filter(
        Q(user__id__in=followed_users) |
        Q(ticket__user=request.user)).order_by('-time_created')
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets= Ticket.objects.filter(
            user__id__in=followed_users).order_by('-time_created')
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    # tickets = Ticket.objects.filter(user__id=request.user.id)

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    context = {
        'posts': posts,
    }

    return render(request, html_template, context)

@login_required()
def create_ticket(request):
    html_template = './review/form_ticket.html'
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('review:accueil-review')
    return render(request, html_template, context={'form': form})

@login_required()
def create_review(request):
    html_template = './review/create_review.html'
    review_form = ReviewForm()
    ticket_form = TicketForm()

    return render(request, html_template,
        {'review_form':review_form, 'ticket_form':ticket_form})

@login_required()
def subscription(request):
    html_template = './review/subscription.html'
    followed_user = UserFollows.objects.filter(user=request.user)
    follower_user = UserFollows.objects.filter(followed_user=request.user)
    form = SubscriptionForm()

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = UserFollows()
            subscription.user = request.user
            subscription.followed_user = User.objects.get(username=form.cleaned_data['username'])
            subscription.save()

    return render(request, html_template,
        {'form': form,
        'followed_user': followed_user,
        'follower_user': follower_user
        })

def unfollow(request, pk):
    html_template = './review/unfollow.html'
    link = UserFollows.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == link.user:
            link.delete()
            return redirect('review:subscription')

    return render(request, html_template, {'link': link})