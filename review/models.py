from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    title = models.CharField('Titre', max_length=128)
    description = models.TextField(
        'Description', 
        blank=True, 
        max_length=2048)
    user = models.ForeignKey(
        User,
        related_name='owner',
        on_delete=models.CASCADE,
        verbose_name='Propriétaire ')
    image = models.ImageField(
        null=True,
        upload_to='image')
    closed_date = models.DateTimeField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):

    STAR_CHOICES = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=STAR_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=1)
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Follower')
    followed_user = models.ForeignKey(
        User,
        related_name='followed_by',
        on_delete=models.CASCADE,
        verbose_name='Utilisateur')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )