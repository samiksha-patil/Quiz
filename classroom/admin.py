from django.contrib import admin
from .models import Quiz,Answer,Question, TakenQuiz,StudentAnswer,Student, Dashboard

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(Student)
admin.site.register(Dashboard)