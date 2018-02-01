from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    print (page_list)
    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {'categories':category_list, 'pages': page_list}

    #return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages']= pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages']= None
        context_dict['category'] = None
    return render(request, 'rango/category.html',context_dict)

def about(request):
    return render(request, 'rango/about.html',context=None)

def add_category(request):
    form = CategoryForm()

    # A HTTP Method
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
           print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

# view for add_page.html
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                return show_category(request, category_name_slug) 
            else:
                print (form.errors)
    
    context_dict = {'form':form, 'category':category} 
    return render(request,'rango/add_page.html', context_dict)

def register(request):

    #is registeration successful?
    registered = False

    #if it is a HTTP POST, we are interested in processing data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            #save user's form data to dbase
            user = user_form.save()

            #hash password
            user.set_password(user.password)
            user.save()

            #sort out the UserProfile instance
            #we set commit = false. This delays saving the model
            #until we are ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            #get picture if provided
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            #now save the UserProfile model instance
            profile.save()
            #registration successful
            registered = True
        else:
            #Invalid forms
            print(user_form.errors, profile_form.errors)
    else:
        #not a HTTP POST

        # this form will be blank
        user_form = UserForm()
        profile_form = UserProfileForm()
    # render template depending on the context
    return render(request, 'rango/register.html', {'user_form': user_form, 
                                                    'profile_form': profile_form,
                                                    'registered': registered})
