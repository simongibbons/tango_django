from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import Category, Page

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
    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)
