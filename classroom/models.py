from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    subject= models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text=models.CharField('Answer', max_length=255)

    def __str__(self):
        return self.text
class Answer(models.Model):
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text= models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username



class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class Dashboard(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='+')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return str(self.student)


