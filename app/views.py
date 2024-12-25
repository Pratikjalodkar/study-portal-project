from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import requests
import wikipedia
from .models import Notes, Homework, Todo
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch

# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')


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


def delete_note(request, pk=None):
    note = Notes.objects.get(pk=pk).delete()
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    # context_object_name = 'notes'


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


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    print(homework)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True

    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    homework = Homework.objects.get(pk=pk).delete()
    return redirect('homework')


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


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True

    todo.save()
    return redirect('todo')


def delete_todo_item(request, pk=None):
    todo = Todo.objects.get(pk=pk).delete()
    return redirect('todo')


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


def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/wiki.html', context)


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
            # return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }
    return render(request,'dashboard/register.html',context)


def loginView(request):
    if request.method == 'POST':  # Fix the typo from 'POst' to 'POST'
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Get username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to a dashboard or home page after successful login
                # Replace 'home' with the name of your desired URL pattern
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')

    else:
        form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/login.html', context)







