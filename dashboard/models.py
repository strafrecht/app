from django.db import models
from django.contrib.auth.models import User
from core.models import Submission


"""
Motivation: to encourage Strafrecht users to contribute

Reward Actions:
    Complete MCT session - less reward points (later)
    Wiki (Create/Update) - more reward points
    MCT (Create/Update) - more reward points
    Falltraining (Create/Update) - more reward points

e.g.:

Finishing MCT - 5 point
Trivial contribution - 5/10 points
Significant contribution - 50/100 points
"""


class Reward(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class RewardType(models.Model):
    submission_id = models.ForeignKey(Submission, null=True, on_delete=models.SET_NULL)
    reward_type_id = models.ForeignKey(Reward, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)