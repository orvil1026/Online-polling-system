from django.db import models
import secrets
import random
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    quiz_owner=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz_id=models.TextField()
    active=models.BooleanField(default=True)

   

    def generate_quiz_id(self):

        n=6
        id=''
        lower_case="qwertyuiopasdfghjklzxcvnm"
        upper_case='QWERTYUIOPASDFGHKJKLZXCVBNM'
        numbers='1234567890'
        special_characters='!_-.,'
        all=lower_case+upper_case+numbers+special_characters
       
        for i in range(6):
            id+=all[random.randint(0,len(all))]

        return id
    def __str__(self):
        return self.quiz_id




class Poll(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    active=models.BooleanField(default=True)

    def user_can_vote(self,user):

        user_votes=user.vote_set.all()
        qs=user_votes.filter(poll=self)
        if(qs.exists()):
            return False
        return True
    
    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text 

    def get_result_dict(self):
        res=[]
        for choice in self.choice_set.all():
            d={}
            alert_class=['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']
            d['alert_class']=secrets.choice(alert_class)
            d['text']=choice.choice_text
            d['num_votes']=choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res


class Choice(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    
    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]}-{self.choice_text[:25]}"


class Vote(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.poll.text[:25]}-{self.choice.choice_text[:25]} -{self.user.username}"

