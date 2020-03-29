from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from .models import Quiz,Question,Answer,Student,TakenQuiz,Dashboard
from django.contrib import messages
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from .forms import BaseAnswerInlineFormSet, QuestionForm,TakeQuizForm
from django.forms import inlineformset_factory
from django.db import transaction
# Create your views here.


class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/quiz_main.html'

   

class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject', )
    template_name = 'classroom/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('quiz_change', quiz.pk)

class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = 'classroom/quiz_change_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('quiz_change', kwargs={'pk': self.object.pk})

    
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/question_add_form.html', {'quiz': quiz, 'form': form})


def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'classroom/add_answer.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })




class StudentQuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/student_quiz_list.html'





'''

def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    question =Question.objects.all()
    answers = Answer.objects.all()
    student=request.user
    
    if request.method == 'POST':
        print("hi")
        form = TakeQuizForm(question=question, data=request.POST)
        student=request.user
        if form.is_valid():
            student_answer = form.save(commit=False)
            student_answer = request.user
            student_answer.save()
            
            return redirect('quiz_list')

    else:
        form = TakeQuizForm(question=question)


    
    
    return render(request, 'classroom/take_quiz_form.html', {
        'quiz': quiz,
        'questions': questions,
        'answers': answers,
        'form': form
        #'progress': progress
    })
'''

'''
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user

    total_questions = quiz.questions.count()
    unanswered_questions = Student().get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        student=request.user
        if form.is_valid():
                print(form)
                student_answer_instance = form.save(commit=False)
                student_answer_instance = request.user
                print("hi")
                student.user=request.user
                student.save()
                #form.instance. student_answer =request.user
                student_answer_instance.save()
                print("hi")
                if Student().get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
'''

def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions =Question.objects.filter(quiz__id=pk)
    answers = Answer.objects.filter(question__quiz__id=pk)
    
    return render(request, 'classroom/take_quiz_form.html', {
        'quiz': quiz,
        'questions': questions,
        'answers':answers
        
    })


def result(request,pk):
    answers = Answer.objects.filter(question__quiz__id=pk)
    quiz = get_object_or_404(Quiz, pk=pk)
    print("result page")
    if request.method == 'POST':
        data = request.POST
        datas = dict(data)
        print(datas)
        qid = []
        qans = []
        ans = []
        score = 0
        for key in datas:

            try:
               
                qid.append(int(key))
                qans.append(datas[key][0])
            except:
                print("Csrf")
        #for q in qid:
         #   ans.append((Questions.objects.get(id = q)).answer)

        for answer in answers:
            
            if answer.is_correct:

                ans.append(answer.text)
        print(ans)       
        total = len(ans)
        for i in range(total):
            if ans[i] == qans[i]:
                score += 1
        # print(qid)
        # print(qans)
        # print(ans)
        print(score)
        eff = (score/total)*100
        student = request.user
        Dashboard.objects.create(student=student, quiz=quiz, score=score)

   
    return render(request,
        'classroom/result.html',
        {'score':score,
        'eff':eff,
        'total':total,

        })




class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'classroom/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)


    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz_change', kwargs={'pk': question.quiz_id})


class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/quiz_delete_confirm.html'
    success_url = reverse_lazy('quiz_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

#class TakenQuizListView(ListView):
#    model = Dashboard
#    template_name = 'classroom/taken_quiz_list.html'

def TakenQuizListView(request):
     dashboards=Dashboard.objects.all()
     
     
     
     return render(request,'classroom/taken_quiz_list.html',{
        'dashboards' :dashboards
     })  
