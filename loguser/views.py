from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.


def registerPage(request):
    # se l'user è autenticato, va alla home
    if request.user.is_authenticated:
        return redirect('home')
    # se l'user non è autenticato, va alla fai la registrazione
    else:
        form = CreateUserForm()
        # richiama la sezione post di admin
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            # se rispetta la procedura allora salva
            if form.is_valid():
                form.save()
                # una volta salvato vai al login
                return redirect('login')
        context = {'form': form}
        return render(request, 'loguser/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            # controllo se l'user è nel database
            user = authenticate(request, username=username, password=password)
            # se è nel database faccio fare il login e poi lo mando alla pagina iniziale
            if user is not None:
                # NOTA LOGIN E' FATTO CON IL METODO DJANGO E NON CON LA MIA FUNZIONE
                login(request, user)
                #login terminato vado alla HOME
                return redirect('home')
            else:
                # se ha sbagliato il login, o l'utente non esiste gli mando un messaggio
                messages.info(request, 'username or password is incorrect')
        context = {}

        return render(request, 'loguser/login.html', context)


# logout utente
def logoutUser(request):
    # uso il metodo logout che ho importato da Django
    logout(request)
    return redirect('home')


# home dell'intero progetto
def home(request):
    #richiedo l'Ip
    ip = get_client_ip(request)
    username = None
    #creo un dizionario per confrontarlo con la query
    proxy = {'ip': ip}
    if request.user.is_authenticated:
        #richiedo il form
        form = IpForm(request.GET or None)
        #richiedo l'username dell'utente che si è già registrato
        username = request.user.username
    # controllo che il queryset Ip non sia vuoto, e che l'utente abbia già effettuato almeno un login
        if Ip.objects.filter() and Ip.objects.filter(user=username):
            #controllo che l'ip dell'utente sia sempre lo stesso
            if Ip.objects.filter(user=username).values('ip').get() != proxy:
                #se l'ha cambiato mando un messaggio all'utente nella home
                messages.info(request, ' Hey,  you changed your IP!!!')
                #cancello l'utente
                instance = Ip.objects.get(user=username)
                instance.delete()
                #ricreo la sezione dell'utente con il nuovo ip (LA RICREO NON LA SOVRASCRIVO)
                new_Ip, created = Ip.objects.get_or_create(user=username, ip=ip)
        else:
            #se l'utente non ha mai fatto un login creo una nuova sezione con il suo username e il suo ip
            new_Ip, created = Ip.objects.get_or_create(user=username, ip=ip)
    return render(request, 'loguser/base.html',)


#funzione per trovare gli ip degli utenti
def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ""
    return ip




