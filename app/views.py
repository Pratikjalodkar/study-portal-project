from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import requests
import wikipedia
from .models import Notes, Homework, Todo
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'])
            notes.save()
        messages.success(request, f'Note added from {
                         request.user.username} successfully')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    print(notes)
    return render(request, 'dashboard/notes.html', {'notes': notes, 'form': form})

@login_required
def delete_note(request, pk=None):
    note = Notes.objects.get(pk=pk).delete()
    return redirect('notes')

@login_required
class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    # context_object_name = 'notes'


@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(request, f'Homework added from {
                             request.user.username} successfully')
            return redirect('homework')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homework': homework,
        'homework_done': homework_done,
        'form': form,
    }
    print(homework)
    return render(request, 'dashboard/homework.html', context)


@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    print(homework)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True

    homework.save()
    return redirect('homework')


@login_required
def delete_homework(request, pk=None):
    homework = Homework.objects.get(pk=pk).delete()
    return redirect('homework')


@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']

        try:
            video = VideosSearch(text, limit=10)
        except Exception as e:
            messages.error(request, f"Error fetching data: {e}")
            return redirect('youtube')

        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnails': i['thumbnails'][0]['url'],
                'link': i['link'],
                'channel': i['channel']['name'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            des = ''
            if i.get('descriptionSnippet'):
                for j in i['descriptionSnippet']:
                    des += j['text']
            result_dict['description'] = des
            result_list.append(result_dict)

            context = {
                'form': form,
                'results': result_list,
            }
        return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/youtube.html', context)


@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todo.save()
            messages.success(request, f'Todo added from {
                             request.user.username} successfully')
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    context = {
        'form': form,
        'todos': todo,
        'todo_done': todo_done,
    }
    return render(request, 'dashboard/todo.html', context)


@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True

    todo.save()
    return redirect('todo')


@login_required
def delete_todo_item(request, pk=None):
    todo = Todo.objects.get(pk=pk).delete()
    return redirect('todo')


@login_required
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        urls = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(urls)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('averageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            print(result_dict['preview'])
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list,
            }
        return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/books.html', context)


@login_required
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        urls = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
        r = requests.get(urls)
        print(f"Status Code: {r.status_code}")
        print("Response Body:", r.text)

        if r.status_code != 200 or not r.text.strip():
            print("Error: API request failed or returned empty data.")
            context = {
                'form': form,
                'input': text,
                'error': 'No data returned from the API.',
            }
            return render(request, 'dashboard/dictionary.html', context)

        try:
            answer = r.json()
            phenotics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            # example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0].get(
                'synonyms', [])

            context = {
                'form': form,
                'input': text,
                'phenotics': phenotics,
                'audio': audio,
                'definition': definition,
                # 'example': example,
                'synonyms': synonyms,
            }
            print(context)
        except ValueError as e:
            # If JSON decoding fails, log the error and provide a meaningful message
            print("Error decoding JSON:", e)
            print(f"Response Content: {r.text}")
            context = {
                'form': form,
                'input': text,
                'error': 'Error parsing dictionary data.',
            }

        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/dictionary.html',context)


@login_required
def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        try:
            search = wikipedia.page(text)
            context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'details': search.summary,
            }
            return render(request, 'dashboard/wiki.html', context)
        except Exception as e:
            messages.error(request, f"Error fetching data: {e}")
            return redirect('wiki')
        

    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/wiki.html', context)


@login_required
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'yards' and second == 'foot':
                        answer = f'{input} yards = {int(input)*3} foot'
                    if first == 'foot' and second == 'yards':
                        answer = f'{input} foot = {int(input)/3} yards'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >=0:
                    if first == 'pound' and second == 'kilogram':
                         answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                         answer = f'{input} kilogram = {int(input)*0.453592} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        # if form.is_valid():
        #     input = request.POST['input']
        #     measure1 = request.POST['measure1']
        #     measure2 = request.POST['measure2']
        #     if measure1 == 'yards' and measure2 == 'foot':
        #         result = input * 3
        #     elif measure1 == 'foot' and measure2 == 'yards':
        #         result = input / 3
        #     elif measure1 == 'pound' and measure2 == 'kilogram':
        #         result = input / 2.20462
        #     elif measure1 == 'kilogram' and measure2 == 'pound':
        #         result = input * 2.20462
        #     context = {
        #         'form': form,
        #         'input': input,
        #         'measure1': measure1,
        #         'measure2': measure2,
        #         'result': result,
        #     }
            # return render(request, 'dashboard/conversion.html', context)
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'dashboard/conversion.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log in the user
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to 'home' after login
        else:
            form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/login.html', context)


@login_required
def profile(request):
    homework = Homework.objects.filter(user=request.user)
    todo = Todo.objects.filter(user=request.user)
    # notes = Notes.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homeworks': homework,
        'homework_done': homework_done,
        'todos': todo,
        'todo_done': todo_done,
    }
    return render(request, 'dashboard/profile.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'dashboard/logout.html')


