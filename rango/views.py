from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

from rango.forms import UserForm, UserProfileForm

def encode_url( name ):
    return name.replace(' ', '_')

def decode_url( url ):
    return url.replace('_', ' ')

def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    for category in category_list:
        category.url = encode_url( category.name )

    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': page_list,
                   }

    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    return render_to_response('rango/about.html', {}, context )

def category(request, category_name_url):
    context = RequestContext(request)

    #Encode spaces in Categories with underscores
    category_name = decode_url( category_name_url )
    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url,
                   }

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)

@login_required
def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm( request.POST )

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect( reverse('index') )
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)

@login_required
def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)

            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)

            page.views = 0

            page.save()

            return HttpResponseRedirect( reverse( 'category', args=(category_name_url,) ) )
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)        

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form,'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)

    context_dict = {}
    requested_page = request.GET.get('next', reverse('index'))
    context_dict['requested_page'] = requested_page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect( requested_page )
            else:
                context_dict['error_text'] = "User is disabled"
                return render_to_response('rango/login.html', context_dict, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['error_text'] = "Invalid Username or Password"
            return render_to_response('rango/login.html', context_dict, context)

    else:
        return render_to_response('rango/login.html', context_dict, context)

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect( reverse('index') )
