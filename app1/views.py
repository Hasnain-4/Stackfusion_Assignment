from django.shortcuts import render, redirect
from datetime import date
from django.contrib import messages
import re
from .models import Formsdata
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import EmailMessage


# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def assignment(request):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        date1 = request.POST.get('date')
        email = request.POST.get('email')
        number = request.POST.get('number')

        # logic for calculating age
        date1 = date1.split('-')
        date2 = date1[2] + '-' + date1[1]+'-'+ date1[0] # To convert into 'DD-MM-YYYY' format
        current_date = date.today()
        current_date = str(current_date).split('-')
        age = int(current_date[0]) - int(date1[0])

        # Age and Mobile number validation
        if age > 18:
            
            if(len(number)==10):
                output = re.findall(r"^[6789]\d{9}$",number)
                if(len(output)==1):
                    # Save the form if conditions are valid
                    form_obj = Formsdata(name = name, dob = date2, email=email, number=number)
                    form_obj.save()
                    # Send an email to the user
                    try:
                        subject = 'User Form Submission Successful'
                        text = 'Dear '+name+', <br><br> \
                                Congratulations you have submitted your form successfully! <br> \
                                You can view all the forms submitted by you and by others on given URL <br>\
                                https://stackfusion.pythonanywhere.com/ <br> \
                                Have any further queries, I will be happy to assist you. You can drop a mail to me at ansarihasnain3598@gmail.com <br> \
                                I hope to cater my services to you in the future too! <br><br> \
                                Regards,<br><br> \
                                Hasnain Ansari'
                        
                        mail = EmailMessage(subject, text,settings.EMAIL_HOST_USER , [email])
                        mail.content_subtype = "html"
                        # mail.attach_file()
                        mail.send()
                    except:
                        print('Something went wrong during sending the mail')
                        
                    # Django messages
                    messages.success(request, 'Form posted successfully')
                    return redirect('forms')
                else:
                    messages.warning(request, 'Please enter valid mobile number')
                    return redirect('assignment')
            else:
                messages.warning(request, 'Please enter 10 digits mobile number')
                return redirect('assignment')
        
        else:
            messages.warning(request, 'Please try again when you become 18+')
            return redirect('assignment')
            

    return render(request, 'form.html')

def forms(request):
    obj = Formsdata.objects.all() # Getting all the form objects

    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(obj, 5)  # Only 5 entries at a time
    try:
        application_page = paginator.page(page)
    except PageNotAnInteger:
        application_page = paginator.page(1)
    except EmptyPage:
        application_page = paginator.page(paginator.num_pages)
    # end pagination
    
    context = {
        'formdata':application_page
        }
    return render(request, 'users_list.html', context )
    # Or we can directly use
    # return render(request, 'users_list.html', {'formdata':application_page } )