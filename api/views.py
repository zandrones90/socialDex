from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.contrib import messages


#creo il file Json che mostra i post nell'ultima ora
def postsjs(request):
    response = []
    now = datetime.now()
    earlier = now - timedelta(hours=1)
    posts = Post.objects.filter(datetime__range=(earlier, now)).order_by('-datetime')
    for post in posts:
        response.append(
            {
                'author': post.user_id,
                'datetime': post.datetime,
                'content': post.content,
                'title': post.title,
                'hash': post.hash,
                'txId': post.txId,
            }
        )
    return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)


#se non hai fatto il login non puoi accedere a file json
@login_required(login_url='login')
#fai vedere tutti i post in ordine cronologico inverso ( da quello più recente a quello più vecchio)
def post_list(request):
    posts = Post.objects.filter().order_by('-datetime')
    return render(request, 'api/post_list.html', {'posts': posts})


@login_required(login_url='login')
#vedi il post singolo
def post_detail(request, pk= None):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'api/post_detail.html', {'post': post})


@login_required(login_url='login')
#crea il post e per ogni post richiama la funzione writeOnChain. Se scrivi hack non puoi pubblicare il post
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            stop = 'hack'
            post = form.save(commit=False)
            #se scrivi hack sul titolo o sul contenuto del post, ritorni a post_new ed esce il messaggio di warning
            if stop in post.title.lower() or stop in post.content.lower():
                messages.warning(request, 'vietato scrivere la parola HACK!!!')
                return redirect('post_new')
            post.user = request.user
            post.datetime = timezone.now()
            post.writeOnChain()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'api/post_edit.html', {'form': form})


@login_required(login_url='login')
#modifica il post
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.datetime = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'api/post_edit.html', {'form': form})
    else:
        return render(request,'api/post_detail.html', {'post': post})


@login_required(login_url='login')
#pagina dove piuò accedere SOLO l'admin (e NON i membri dello staff o gli altri utenti),
#dove mettere il numero dei posts corrispondenti agli users (tra gli users ho considerato anche l'admin)
def admin_page(request):
    if not request.user.is_superuser:
        return render(request, 'api/post_list.html')
    else:
        context =[]
        #faccio la query per richiamare una lista
        user = User.objects.filter()
        for u in range(len(user)):
            context.append(
                {
                    'user': user[u], #metto l'username
                    'number': len(Post.objects.all().filter(user_id=u + 1)) #metto la lunghezza della lista corrispondente al numero di post
                }
            )
        return render(request, 'api/admin_page.html', {'context': context})


@login_required(login_url='login')
#attraverso la ricerca 'url/utente/id' vedo in una pagina i post dell'utente corrispondente all'id
#in questo caso l'id è una parola corrispondente all'username
def post_utente(request, pk=None):
    try:
        #prendo dal modello User l'id corrispondente all'username
        id =User.objects.values().filter(username=pk).values_list('id', flat=True).get()
        #prendo dal modello Post i posts ordinati per data dell'user_id corrispondente a id
        posts = Post.objects.order_by('-datetime').filter(user_id=id)
        return render(request, 'api/post_utente.html', {'posts': posts})
        #se ci sono problemi allora mi da la pagina post_list priva di posts
    except:
        return render(request, 'api/post_list.html')


@login_required(login_url='login')
#inserisci la stringa di input che verrà inviata
def get_input(request):
    q = request.GET.get('q')
    #se q è vuota la pagina si ricarica
    if q is None:
        return render(request, 'api/get_1.html')
    #altrimenti conta il numero di volte che appare q
    else:
        cnt = 0
        posts = Post.objects.filter()
        for post in posts:
            content = post.content
            if q in content:
                cnt += 1

    search_results = cnt
    context = {'search_results': search_results}

    return render(request, 'api/get_1.html', context)



