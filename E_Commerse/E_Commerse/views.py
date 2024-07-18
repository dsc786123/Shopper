from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
from .models import Customer,ProductDetail,ProductImage,AddToCart
from django.contrib.auth.hashers import make_password,check_password

import uuid
from .helpers import send_forget_mail
curl = settings.C_URL
media_url=settings.MEDIA_URL

def index(request):
    if request.method == "GET":
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        # print("Product Images:",prod_img)
        prod_details=ProductDetail.objects.all().values("product_brand","product_description","product_price","product_id")
        
        prod_images=[] 
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
        
        print(prod_images)  
        return render(request,'index.html',{'curl':curl,'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})
    
    if request.method == "POST":
        result = request.POST.get('search')
        print("Search data:",result)
        prod_details=ProductDetail.objects.filter(product_brand=result).values()
        print(prod_details)
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        prod_images=[] 
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
        return render(request,'index.html',{'curl':curl,'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})
       


def productdetails(request):
    
    if request.method=="GET":
        product_id=request.GET.get('id')
        print("<=======product_id:========>",product_id)
        prod_img = ProductImage.objects.filter(product_id=product_id).values("product_img")
        print("Product Images:",prod_img)
        
        prod_details=ProductDetail.objects.filter(product_id=product_id).values()
        print(prod_details)
        product_size=prod_details[0]["product_size"]
        print("Product Size:",product_size)
        
        listofsize=product_size.split(",")

        check=True
        if check:  
            redirecting='customer/cart/'
        else:
            print("========login=======")          
            redirecting='login'

        return render(request,'productdetails.html',{'curl':curl,'prod_details':prod_details[0],'prod_images':prod_img,'redirecting':redirecting,'media_url':media_url,"product_id":product_id,'size':listofsize})
    

    elif request.method == 'POST':
        quantity = request.POST.get('quantity')
        print(quantity,"=========")
        product_id=request.POST.get('product_id')
        size=request.POST.get("size")
        print("<=======product_Size:========>",size)
        print("<=======product_id:========>",product_id)
        prod_img = ProductImage.objects.filter(product_id=int(product_id)).values("product_img","product_img_id")
        print("Product Images:",prod_img)
        
        prod_details=ProductDetail.objects.filter(product_id=int(product_id)).values()
        print(prod_details)
        product_quantity=prod_details[0]["product_quantity"]
        print("Product Quantity:",product_quantity)
        print("=======",prod_img[0]["product_img"])
        print("=======",prod_img[1]["product_img_id"])

        single_img=prod_img[0]["product_img"]
        product_img_id=prod_img[0]["product_img_id"]

        product_brand=prod_details[0]["product_brand"]
        product_description=prod_details[0]["product_description"]
        #product_quantity=prod_details[0]["product_quantity"]
        product_price=prod_details[0]["product_price"]

        prod_detail = ProductDetail.objects.get(product_id=product_id)
        cust_detail = Customer.objects.get(customer_id=3)
        prod_img_detail = ProductImage.objects.get(product_img_id=product_img_id)

        product_total_price=int(quantity)*product_price
        print(product_total_price)
        
        check=True
        if check:  
            print("=====customer cart=====")
            addtocart = AddToCart(product_img=single_img,product_brand=product_brand,product_size=size,product_description=product_description,product_quantity=int(quantity),product_price=product_price,product_total_price=product_total_price,product_id=prod_detail,customer_id=cust_detail,product_img_id=prod_img_detail)
            addtocart.save()
            redirecting='customer/cart/'
            return redirect(curl+redirecting)
        else:
            print("========login=======")          
            redirecting='login'
           
        
    return redirect(curl+redirecting)
    # return render(request,'productdetails.html',{'curl':curl,'prod_details':prod_details[0],'prod_images':prod_img,'redirecting':redirecting,'media_url':media_url})
    
    

'''
def login(request):
    fm = CustomerLogin()
    msg=""
    if request.method == "POST":
        fm = CustomerLogin(request.POST)
        if fm.is_valid():
            print("Form Validated")
            print("Email:",fm.cleaned_data['email'])
            print("Password:",fm.cleaned_data['password'])
            gemail=fm.cleaned_data['email']
            gpass=fm.cleaned_data['password']  
        else:
            msg="Please enter correct credentails"
            return render(request,'login.html',{'form':fm,'msg':msg})
        
    elif request.method == "GET":
        print("get request")
        return render(request,'login.html',{'form':fm})  
'''      

def login(request):
    if request.method == "GET":
        return render(request,'login.html',{"curl":curl})
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        qs=Customer.objects.filter(email=email,password=password).values()
        print(qs)
        print(qs[0]["role"])
        role=qs[0]["role"]
        #for session ============================
        request.session["emailid"]=qs[0]["email"]
        request.session["password"]=qs[0]["password"]
        request.session["role"]=qs[0]["role"]
        request.session["customer_id"]=qs[0]["customer_id"]
        #for session ============================

        if role=="customer":
            print("Customer Dashboard!!!")
            #return HttpResponse("<h1>Customer Dashboard!!!</h1>")
            return redirect(curl+'customer/home')
        elif role=="admin":
            print("Admin Dashboard!!!")
            #return HttpResponse("<h1>Admin Dashboard!!!</h1>")
            return redirect(curl+'ecommerseadmin/home')
        else:    
            return render(request,'login.html',{"curl":curl})        


def register(request):
    if request.method == "GET":
        return render(request,'register.html',{"curl":curl})
    
    elif request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        city = request.POST['city']
        pincode = request.POST['pincode']
        # password=make_password(unpassword)

    
    

        print(name,email,password,mobile,address,pincode,city)
        customer = Customer(name=name,email=email,mobile=mobile,address=address,pincode=pincode,city=city ,password=password)
        msg=""
        try:
            
            
            customer.save()
            msg="Customer Register Successfully!!!"
        except Exception as e:
            print("Error Occured at Register Customer:",e)
            msg="Customer Not Register, Please try again"
        return render(request,'register.html',{"curl":curl,"msg":msg})

def email(request):
    if request.method == "GET":
        return render(request,'email.html',{"curl":curl})
    
    if request.method == 'POST':
        email=request.POST.get('email')
        if not Customer.objects.filter(email=email).first():
            print("No User Found with this email")
            return redirect(curl+'login/')
            
        cust_obj = Customer.objects.filter(email=email).first()
        print(type(cust_obj),cust_obj.email)

        #=====Generate a random UUID.
        token = str(uuid.uuid4())
        #===== Save token ====#
        cust = Customer.objects.get(email=cust_obj.email)
        cust.forgot_password_token = token
        cust.save()
        #=========Save token =====#
        send_forget_mail(cust_obj.email,token)
        print("Email is send to your gmail id")
        return render(request,'email.html',{"curl":curl})
    return render(request,'email.html',{"curl":curl,"customer_id":cust_obj.customer_id})


def resetpassword(request,token):
    cust_obj=Customer.objects.filter(forgot_password_token=token).first()
    print(cust_obj.customer_id)

    if request.method == 'POST':
        newpassword=request.POST.get('newpassword')
        confirmpassword=request.POST.get('confirmpassword')
        c_id=request.POST.get('customer_id')
        if c_id is None:
           print("No User Id Found")
           return redirect(curl+'login/')
       
        if newpassword != confirmpassword:
           print("newpassword and confirmpassword is not same")
           return redirect(curl+'/resetpassword/'+token)
        
        Customer.objects.filter(customer_id=c_id).update(password=confirmpassword)
        print("Password Reset Successfully")
        # return redirect(curl+"/login/")
        return render(request,'login.html',{"curl":curl,"msg":"Password Reset Successfully"})
    
    elif request.method == "GET":
        return render(request,'resetpassword.html',{"curl":curl,"customer_id":cust_obj.customer_id})

        
