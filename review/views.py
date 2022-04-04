from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from review.models import UserFollows, Review, Ticket
from review.forms import SubscriptionForm, TicketForm, ReviewForm
from django.db.models import Value, Q, CharField
from datetime import date


def aggregation_tickets_reviews(tickets, reviews):
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    return posts


def save_ticket(form, user, closed_date=False):
    ticket = form.save(commit=False)
    ticket.user = user
    if closed_date:
        ticket.closed_date = date.today()
    ticket.save()
    return ticket


def save_review(form, ticket, user):
    review = form.save(commit=False)
    review.ticket = ticket
    review.user = user
    review.save()
    return review


@login_required()
def view_by_user(request, pk):
    html_template = './review/accueil.html'
    reviews = Review.objects.filter(user=pk).order_by('-time_created')
    tickets = Ticket.objects.filter(
        user=pk).order_by('-time_created')
    context = {
        'my_posts': True,
        'posts': aggregation_tickets_reviews(tickets, reviews)
    }
    return render(request, html_template, context)


@login_required()
def acceuil(request):
    html_template = './review/accueil.html'
    followed_users = list(
        UserFollows.objects.filter(user=request.user)
        .values_list('followed_user__id', flat=True))
    followed_users.append(request.user.id)
    reviews = Review.objects.filter(
        Q(user__id__in=followed_users) |
        Q(ticket__user=request.user)).order_by('-time_created')
    tickets = Ticket.objects.filter(
        user__id__in=followed_users, closed_date=None
        ).order_by('-time_created')

    for user in followed_users:
        print(f'user.username = {user}')
    for review in reviews:
        print(f'review.headline = {review.headline}')
    for ticket in tickets:
        print(f'ticket.title= {ticket.title}')
    context = {
        'posts': aggregation_tickets_reviews(tickets, reviews),
    }

    return render(request, html_template, context)


@login_required()
def create_ticket(request):
    html_template = './review/form_ticket.html'
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            save_ticket(form, request.user)
            return redirect('review:accueil-review')
    return render(request, html_template, context={'form': form})


@login_required()
def update_ticket(request, pk):
    html_template = './review/form_ticket.html'
    ticket = get_object_or_404(Ticket, id=pk)
    form_ticket = TicketForm(instance=ticket)
    if request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES, instance=ticket)
        if form_ticket.is_valid():
            save_ticket(form_ticket, request.user)
            return redirect('review:accueil-review')
    context = {
        'ticket': ticket,
        'form': form_ticket,
        'mod': 'update'
    }
    return render(request, html_template, context=context)


@login_required()
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.delete()

    return redirect('review:view-my-post')


@login_required()
def delete_review(request, pk):
    review = Review.objects.get(pk=pk)
    review.ticket.closed_date = None
    review.ticket.save()
    review.delete()

    return redirect('review:view-my-post')


@login_required()
def update_review(request, pk):
    html_template = './review/create_review.html'
    review = get_object_or_404(Review, id=pk)
    ticket = review.ticket
    form_review = ReviewForm(instance=review)
    if request.method == 'POST':
        form_review = ReviewForm(request.POST, instance=review)
        if form_review.is_valid():
            save_review(form_review, ticket, request.user)
            return redirect('review:accueil-review')

    context = {
        'title_page': 'with_ticket',
        'review_form': form_review,
        'ticket': ticket
    }

    return render(request, html_template, context)


@login_required()
def create_review_by_ticket(request, pk):
    html_template = './review/create_review.html'
    ticket = get_object_or_404(Ticket, id=pk)
    form_review = ReviewForm()

    if request.method == 'POST':
        form_review = ReviewForm(request.POST)
        if form_review.is_valid():
            save_review(form_review, ticket, request.user)
            ticket.closed_date = date.today()
            ticket.save()
            return redirect('review:accueil-review')

    context = {
        'title_page': 'with_ticket',
        'review_form': form_review,
        'ticket': ticket
    }

    return render(request, html_template, context)


@login_required()
def create_review(request):
    html_template = './review/create_review.html'
    review_form = ReviewForm()
    ticket_form = TicketForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if review_form.is_valid() and ticket_form.is_valid():
            ticket = save_ticket(ticket_form, request.user, closed_date=True)
            save_review(review_form, ticket, request.user)

            return redirect('review:accueil-review')

    context = {
        'title_page': 'without_ticket',
        'review_form': review_form,
        'ticket_form': ticket_form
    }

    return render(request, html_template, context)


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
            subscription.followed_user = User.objects.get(
                username=form.cleaned_data['username']
            )
            subscription.save()

    context = {
        'form': form,
        'followed_user': followed_user,
        'follower_user': follower_user
    }

    return render(request, html_template, context)


def unfollow(request, pk):
    html_template = './review/unfollow.html'
    link = UserFollows.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == link.user:
            link.delete()
            return redirect('review:subscription')

    return render(request, html_template, {'link': link})
