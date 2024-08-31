# Write in views method
from django.http import HttpResponseRedirect
# redirect
from django.shortcuts import render,redirect,get_object_or_404
# import signup model
from Login.models import Signup
# import Category model
from Category.models import Category
#import Bussiness Model
from AddBussiness.models import Business,Search,Message,Lead,Adv,Gallery
# import Appointment
from Appointment.models import Appointment
# Message with redirect
from django.contrib import messages
# for Random data
from django.db.models.functions import Random
# Jquery Data 
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
# Math
from math import ceil
from django.db.models import Avg
from django.db.models import Count
import json
# Paginatin
from django.core.paginator import Paginator

# main Index page
def home(request):
    user = request.COOKIES.get('user')
    category = Category.objects.all().order_by(Random())
    
    data = {
        'user': user,
        "cat" : category
    }
    return render(request, 'index.html', data)

# main Login page
def login(request):
    user_cookie = request.COOKIES.get('user')
    username_session = request.session.get(user_cookie)
    
    if user_cookie is not None or username_session is not None:
        return redirect('/') 
    user = request.COOKIES.get('user')
    data = {
        'user': user
    }
    return render(request,"login.html",data)

# main Signup page
def signup(request):
    user_cookie = request.COOKIES.get('user')
    username_session = request.session.get(user_cookie)
    
    if user_cookie is not None or username_session is not None:
        return redirect('/') 
    user = request.COOKIES.get('user')
    data = {
        'user': user,
    }
    return render(request,"signup.html",data)

# main Logout page
def logout(request):
    user = request.COOKIES.get('user')
    
    if user is not None:
        response = redirect("/")
        response.delete_cookie("user")
        if user in request.session:
            del request.session[user]
        return response
    else:
        return redirect('/')

# Authentication for login
def actionsignup(request):
    if request.method == "POST" :
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        bussiness = request.POST.get("bussiness")
        if name == "" or email == "" or password == "" or phone == "":
            return render(request, 'signup.html', {'error': 'All fields are required'})
        if bussiness is None:
            return render(request, 'signup.html', {'error': 'All fields are required'})
        
        if Signup.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        stud = Signup(name=name,email=email,password=password,phone=phone,bussiness=bussiness)
        stud.save()
        response = HttpResponseRedirect("/")
        response.set_cookie("user",email)
        request.session[email] = password
        return response
    
# Authentication for Signup
def actionlogin(request):
    if request.method == "POST" :
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if email=="" or password=="":
            return render(request, 'login.html', {'error': 'All fields are required'})
        
        if Signup.objects.filter(email=email).exists():
            user = Signup.objects.get(email=email)
            
            if user.password == password:
                response = redirect('/')
                response.set_cookie('user', email)
                request.session[email] = password
                return response
            else:
                return render(request, 'login.html', {'error': 'Password not match'})
        else:
            return render(request, 'login.html', {'error': 'Email not exists'})

# Bussinesses in Main Category Page
def category(request,id):
    if Category.objects.filter(id=id).exists():
        category = Category.objects.get(id=id)
        businesses = Business.objects.filter(category=category).order_by("id")
        user = request.COOKIES.get('user')
        advertisement  = Adv.objects.all()
        cookie = {
            'catname':category,
            'user': user,
            "businesses":businesses,
            "advertisement":advertisement
        }
        return render(request, 'category.html', cookie)    
    else:
        return redirect("/")
    #return HttpResponse(businesses)

# Bussiness in Main page
def bussiness(request,id):
    if Business.objects.filter(id=id).exists():
        addbussiness = Business.objects.get(id=id)
        user = request.COOKIES.get('user')
        rating = Message.objects.filter(business_id=id).aggregate(Avg('rating'))['rating__avg']
        business_rating = ceil(rating) if rating is not None else 0
        ratingss = "{:.2f}".format(rating) if rating is not None else 0
        messages = Message.objects.filter(business_id=id)
        paginator = Paginator(messages, 2)
        page = request.GET.get("page")
        studs = paginator.get_page(page)
        canreply = ""
        if Message.objects.filter(email=user,business_id=id).exists():
            canreply = "no"

        gallery = ""
        if Gallery.objects.filter(business_id=id).exists():
            gallery = Gallery.objects.filter(business_id=id)

        advertisement  = Adv.objects.all()

        bussinesscategory1 = addbussiness.category
        bussinesscategory = str(bussinesscategory1)
        if bussinesscategory=="Dentists":
            bussinesscategory = "Dentists"
        else:
            bussinesscategory = ""

        appointmentsbook = "yes"
        if Appointment.objects.filter(email=user,business_id=id).exists():
            appointmentsbook = ""
        
        data = {
            'user': user,
            'bus':addbussiness,
            'rating':business_rating,
            'prating':ratingss,
            "messages": studs,
            "reply":canreply,
            'star_range': range(5),
            'gallery':gallery,
            "advertisement":advertisement,
            "bussinesscategory":bussinesscategory,
            "appointmentsbook":appointmentsbook
        }
        if request.GET.get('dis'):
            dis = request.GET.get('dis')
            search = Search(
                business_id=id,
                city=dis
            )
            search.save()
        return render(request, 'bussiness.html', data)
    else:
        return redirect("/")

# Add District
@csrf_protect
def adddistrict(request):
    if request.method == "POST":
        city = request.POST.get("city")
        business_id = request.POST.get("business_id")

        if city:
            search = Search(
                business_id=business_id,
                city=city
            )
            search.save()
            return JsonResponse({'message': 'Data saved successfully'})
    return JsonResponse({'error': 'Invalid request'})

# Edit Profile
def edit(request):
    user = request.COOKIES.get("user")
    bussiness = "no"
    if user:
        details = Signup.objects.get(email=user)
        bussiness = Signup.objects.get(email=user).bussiness
        if bussiness=="yes":
            if Business.objects.filter(email=user).exists():
                bussiness="no"
        data = {
            'user': user,
            'bussiness': bussiness,
            'details':details
        }
        return render(request, 'edit.html', data)
          
    else:
        return redirect("/")
    
def editprofile(request):
    if request.method == "POST":
        user = request.COOKIES.get("user")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        
        if name=="" or phone=="":
            messages.warning(request, 'All fields are required')
            return redirect("/edit")
        stud = Signup.objects.get(email=user)
        stud.name = name
        stud.phone = phone
        stud.save()
        messages.success(request, 'Profile Edit Successfully!')
        return redirect("/edit")
    else:
        messages.warning(request, 'Invalid request method')
        return redirect("/edit")
    
# Change Password
def changepassword(request):
    user = request.COOKIES.get("user")
    bussiness = "no"
    if user:
        bussiness = Signup.objects.get(email=user).bussiness
        if bussiness=="yes":
            if Business.objects.filter(email=user).exists():
                bussiness="no"
        data = {
            'user': user,
            'bussiness': bussiness
        }
        return render(request, 'password.html', data)
          
    else:
        return redirect("/")
    
def passwordchange(request):
    if request.method == "POST":
        user = request.COOKIES.get("user")
        cp = request.POST.get("cp")
        np = request.POST.get("np")
        rp = request.POST.get("rp")
        
        if cp=="" or np=="" or rp=="":
            messages.warning(request, 'All fields are required')
            return redirect("/changepassword")
        
        details = Signup.objects.get(email=user)
        if details.password==cp:
            if np==rp:
                stud = Signup.objects.get(email=user)
                stud.password = np
                stud.save()
                messages.success(request, 'Password Changed Successfully!')
                return redirect("/changepassword")
            else:
                messages.warning(request, 'New and retype password not match')
                return redirect("/changepassword")
        else:
            messages.warning(request, 'Current Password Incorrect')
            return redirect("/changepassword")
    else:
        messages.warning(request, 'Invalid request method')
        return redirect("/changepassword")
    

# Search Bussiness
def search(request):
    if request.method == "POST":
        location = request.POST.get("location")
        business = request.POST.get("business")
        businesses = Business.objects.filter(district__icontains=location, title__icontains=business)
        user = request.COOKIES.get('user')
        if user :
            userdetails = Signup.objects.get(email=user)
            leadbussiness = Business.objects.filter(title__icontains=business)
            for lead in leadbussiness:
                new_lead = Lead(
                    business_id=lead.id,
                    user=userdetails.name,
                    email = user,
                    search = business,
                    location = location
                )
                new_lead.save()

        advertisement  = Adv.objects.all()
        data = {
            'user': user,
            "location" : location,
            "business" : business,
            "businesses" : businesses,
            "advertisement":advertisement
        }
        return render(request,"search.html",data)
        
    else:
        return redirect("/")

# Comment and rating url 
@csrf_protect
def sharereply(request):
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        message_content = request.POST.get("message")
        business_id = int(request.POST.get("business_id"))
        
        user_email = request.COOKIES.get("user")
        if user_email:
            user_details = get_object_or_404(Signup, email=user_email)
            username = user_details.name
            
            message = Message(
                business_id=business_id,
                user=username,
                email=user_email,
                rating=rating,
                message=message_content
            )
            message.save()
            
            response_data = {
                'status': 'success'
            }
            
            return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'error'
            }
            return JsonResponse(response_data, status=401)
    
    return JsonResponse({'error': 'Method not allowed.'})

# Comment and rating url 
@csrf_protect
def updatereply(request):
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        message_content = request.POST.get("message")
        business_id = int(request.POST.get("business_id"))
        cid = int(request.POST.get("cid"))
        user_email = request.COOKIES.get("user")
        if user_email:
            user_details = get_object_or_404(Signup, email=user_email)
            username = user_details.name
            
            message = get_object_or_404(Message, id=cid, business_id=business_id, email=user_email)
                
                # Update the message record
            message.rating = rating
            message.message = message_content
            message.save()
            
            response_data = {
                'status': 'success'
            }
            
            return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'error'
            }
            return JsonResponse(response_data, status=401)
    
    return JsonResponse({'error': 'Method not allowed.'})


# Dashboard Bussiness
def dashboard(request):
    user = request.COOKIES.get('user')
    if user:
        bussiness = "no"
        bussiness = Signup.objects.get(email=user).bussiness
        if bussiness=="yes":
            userdetails = Signup.objects.get(email=user)
            bussinessdetails=""
            if Business.objects.filter(email=user).exists():
                bussinessdetails = Business.objects.get(email=user)
            category = Category.objects.all()
            appointments=""
            if Appointment.objects.filter(business_id=bussinessdetails.id).exists():
                appointments = Appointment.objects.filter(business_id=bussinessdetails.id).order_by("-id")
            data = {
                "userdetails":userdetails,
                "bussinessdetails":bussinessdetails,
                "cat":category,
                "appointments":appointments
            }
            return render(request,"profile.html",data)
            
        else:
            userdetails = Signup.objects.get(email=user)
            message = ""
            bussiness = ""
            if Message.objects.filter(email=user).exists():
                message = Message.objects.filter(email=user)
                business_ids = message.values_list('business_id', flat=True)
                bussiness = Business.objects.filter(id__in=business_ids)
            data = {
                "userdetails":userdetails,
                "bussiness" : bussiness
            }
            return render(request,"user.html",data)
    else:
        return redirect("/")
    
# Add Bussines Details
def addbussinessdata(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        address = request.POST.get('address')
        category_id = request.POST.get('category') 
        state = request.POST.get('state')
        district = request.POST.get('district')
        contact_number = request.POST.get('contact_number')
        open_until = request.POST.get('open_until')
        experience = request.POST.get('experience')
        timing = request.POST.get('timing')
        service = request.POST.get('service')
        overview = request.POST.get('overview')
        image = request.FILES.get('image')

        user = request.COOKIES.get('user')

        if not (title and address and category_id and state and district and contact_number and open_until and experience and timing and service and overview and image):
            messages.warning(request, 'All fields are required.')
            return redirect("/dashboard")
        
        category = get_object_or_404(Category, id=category_id) 
        yt = ""
        if request.POST.get('yt'):
            yt = request.POST.get('yt')
        business = Business(
            title=title,
            address=address,
            category=category,
            email=user,
            state=state,
            district=district,
            contact_number=contact_number,
            open_until=open_until,
            experience=experience,
            timing=timing,
            service=service,
            overview=overview,
            youtube = yt,
            image=image
        )
        business.save()
        messages.success(request, 'Business data added successfully!')
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")

# Dashboard Bussiness Views
def views(request):
    user = request.COOKIES.get('user')
    if user:
        if Business.objects.filter(email=user).exists():
            business = Business.objects.get(email=user)
            business_id = business.id

            search = Search.objects.filter(business_id=business_id)
            
            city_view_counts = list(search.values('city').annotate(count=Count('city')))
            city_view_counts_json = json.dumps(city_view_counts) 
            
            messages = Message.objects.filter(business_id=business_id)
            paginator = Paginator(messages, 2)
            page = request.GET.get("page")
            studs = paginator.get_page(page)
            data = {
                "id":business_id,
                "messages": studs,
                "search": search,
                'star_range': range(5),
                'cityview': city_view_counts_json
            }
            return render(request,"views.html",data)
        else:
            return redirect("/dashboard")
    else:
        return redirect("/")


@csrf_protect
def loadmore(request):
    if request.method == "POST":
        business_id = int(request.POST.get("id"))
        messages = Message.objects.filter(business_id=business_id)
        points = int(request.POST.get("points", 1))
        paginator = Paginator(messages, 2)
        page_obj = paginator.get_page(points)
        data = []
        for msg in page_obj.object_list:
            data.append({
                'id': msg.id,
                'name': msg.user,
                'rating': msg.rating,
                'message': msg.message,
                'email': msg.email,
            })

        return JsonResponse({"data": data, "has_next": page_obj.has_next()})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

#Edit Dashboard Profile
def EditProfile(request):
    user = request.COOKIES.get('user')
    if user:
        userdetails = Signup.objects.get(email=user)
        data = {
            "userdetails":userdetails
        }
        return render(request,"EditProfile.html",data)
        
    else:
        return redirect("/")
    
def DashEditProfile(request):
    if request.method == "POST":
        user = request.COOKIES.get("user")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        
        if name=="" or phone=="":
            messages.warning(request, 'All fields are required')
            return redirect("/EditProfile")
        stud = Signup.objects.get(email=user)
        stud.name = name
        stud.phone = phone
        stud.save()
        messages.success(request, 'Profile Edit Successfully!')
        return redirect("/EditProfile")
    else:
        messages.warning(request, 'Invalid request method')
        return redirect("/EditProfile")
    
# Change Password Dashboard Profile
def ChangePassword(request):
    user = request.COOKIES.get('user')
    if user:
        userdetails = Signup.objects.get(email=user)
        data = {
            "userdetails":userdetails
        }
        return render(request,"ChangePassword.html",data)
        
    else:
        return redirect("/")
    
def DashChangePassword(request):
    if request.method == "POST":
        user = request.COOKIES.get("user")
        cp = request.POST.get("cp")
        np = request.POST.get("np")
        rp = request.POST.get("rp")
        
        if cp=="" or np=="" or rp=="":
            messages.warning(request, 'All fields are required')
            return redirect("/ChangePassword")
        
        details = Signup.objects.get(email=user)
        if details.password==cp:
            if np==rp:
                stud = Signup.objects.get(email=user)
                stud.password = np
                stud.save()
                messages.success(request, 'Password Changed Successfully!')
                return redirect("/ChangePassword")
            else:
                messages.warning(request, 'New and retype password not match')
                return redirect("/ChangePassword")
        else:
            messages.warning(request, 'Current Password Incorrect')
            return redirect("/ChangePassword")
    else:
        messages.warning(request, 'Invalid request method')
        return redirect("/ChangePassword")
    
# UpdateBussiness Bussiness
@csrf_protect
def UpdateBusiness(request):
    if request.method == "POST":
        id = request.POST.get('id')
        address = request.POST.get('address')
        state = request.POST.get('state')
        district = request.POST.get('district')
        number = request.POST.get('number')
        open = request.POST.get('open')
        experience = request.POST.get('experience')
        timing = request.POST.get('timing')
        service = request.POST.get('service')
        overview = request.POST.get('overview')
        business = get_object_or_404(Business, id=id)
        business.id = id
        business.address = address
        business.state = state
        business.district = district
        business.contact_number = number
        business.open_until = open
        business.experience = experience
        business.timing = timing
        business.service = service
        business.overview = overview
        business.save()
        return JsonResponse({'status': 'success'})
        
    else:
        return JsonResponse({'status': 'error', 'message': 'Method Not Allowed'}, status=405)
    
# Advertisement 
def advertisement(request):
    user = request.COOKIES.get('user')
    if user: 
        advertisements = ""
        if Adv.objects.filter(business_email=user).exists():
            advertisements = Adv.objects.filter(business_email=user)
        return render(request, 'advertisement.html', {'advertisements': advertisements})
    
def advdata(request):
    user = request.COOKIES.get('user')
    if user:
        if request.method == "POST":
        
            option = request.POST.get("options")
            image = request.FILES.get("image")

            advertisement = Adv()
            if option == "option1":
                advertisement.option1 = "800 x 800 pixels"
            elif option == "option2":
                advertisement.option2 = "500 x 900 pixels"
            elif option == "option3":
                advertisement.option3 = "900 x 500 pixels"
            elif option == "option4":
                advertisement.option4 = "1000 x 200 pixels"
            advertisement.business_email=user
            advertisement.image = image
            advertisement.save()
            messages.success(request, 'Advertisement Added Successfully!')
            return redirect("/advertisement")
        messages.warning(request, 'Method Not Supported')
        return redirect("/advertisement")
    return redirect("/")

def gallery(request):
    user = request.COOKIES.get('user')
    if user:
        bussinessid = Business.objects.get(email=user).id
        bussiness = Business.objects.get(email=user)
        gallery = ""
        if Gallery.objects.filter(business_id=bussinessid).exists():
            gallery = Gallery.objects.filter(business_id=bussinessid)
        data = {
            "gallery":gallery,
            "bus":bussiness
        }
        return render(request,"gallery.html",data)

# Gallery Of Bussiness
def galleryimg(request):
    user = request.COOKIES.get('user')
    if user:
        if request.method == "POST":
            
            image = request.FILES.get("image")
            bussinessid = Business.objects.get(email=user).id
            if Gallery.objects.filter(business_id=bussinessid).count() >= 3:
                messages.warning(request, 'You can upload only 3 images.')
                return redirect("/Gallery")
            gallery = Gallery(
                business_id = bussinessid,
                image = image
            )
            gallery.save()
            messages.success(request, 'Image Added Successfully!')
            return redirect("/Gallery")
        messages.warning(request, 'Method Not Supported')
        return redirect("/Gallery")
    return redirect("/")

# Delete Gallery Image
def galdelete(request,id):
    image = get_object_or_404(Gallery, id=id)
    image.delete()
    messages.warning(request, 'Image Delete Succesfully.')
    return redirect("/Gallery")

# Lead Bussiness
def leadbussiness(request):
    user = request.COOKIES.get("user")
    if user:
        bussinessid = Business.objects.get(email=user).id
        studs = ""
        if Lead.objects.filter(business_id=bussinessid).exists():
            leadbussiness = Lead.objects.filter(business_id=bussinessid).order_by("-id")
            paginator = Paginator(leadbussiness,5)
            page = request.GET.get("page")
            studs= paginator.get_page(page)
        data = {
            "leadbussiness":studs
        }
        return render(request,"leadbussiness.html",data)
    else:
        return redirect("/")

# Appointments

def appointments(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        id = request.POST.get('id')
        user = request.COOKIES.get('user')
        userdetails = Signup.objects.get(email=user)
        appoint = Appointment(
            business_id = id,
            user = userdetails.name,
            email = userdetails.email,
            date = date,
            time = time 
        )
        appoint.save()
        response_data = {
                'status': 'success'
            }
            
        return JsonResponse(response_data)
    else:
        return redirect("/dashboard")
