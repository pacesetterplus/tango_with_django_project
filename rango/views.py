from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

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
def user_login(request):
    #pull out relevant information if it's HTTP POST
    if request.method == 'POST':
    #gather username and password provided by the user.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if valid
        user = authenticate(username=username, password=password)
        #if we have a user object, the details are correct
        if user:
            if user.is_active:
                #send user back to homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # an inactive account
                return HttpResponse("Your Rango account is disabled.")
        else:
            # bad login details provided
            print ("Invalid login details:{0}, {1}".
                format(username,password))
            return HttpResponse("Invalid login details supplied.")

    # request not HTTP POST
    else:
        # no context variable to pass to the template system
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    context_dict = {'message':"Since you are logged in, you can see this text!" }
    return render(request, 'rango/restricted.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    # take user back to homepage
    return HttpResponse(reverse('index'))