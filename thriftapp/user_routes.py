import re,random,os,requests,json
from functools import wraps
from flask import render_template, request, redirect, flash,make_response,session,url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta
from thriftapp import app, csrf
from thriftapp.models import db,Reviews,Subscribers,Lga,State,Payment,Payrotation,Plan,Admin,Collection,Guarantors,Subscribersplan,Contact
from thriftapp.forms import SignupForm,ProfileForm,Verform,ContactForm,ContactUs


def login_required(f):
    @wraps(f) #from functools import wraps
    def login_decorator(*args,**kwargs):
        if session.get('subid') and session.get('sub_loggedin'):
           return f(*args,**kwargs)
        else:
            flash("Access Denied, Please Login")
            return redirect("/login")
    return login_decorator


   
@app.route("/dashboard")
@login_required
def dashboard():
    useronline = session.get('subid')    
    userdeets = db.session.query(Subscribers).get(useronline)
    return render_template("user/dashboard.html",userdeets=userdeets)

@app.route("/")
def home():
    return render_template("user/layout.html")

@app.route("/faq")

def faq_page():
    return render_template("/user/faq.html")

@app.route("/aboutus")
def about_page():
    return render_template("/user/aboutus.html")




# @app.route("/explore", methods=['POST','GET'])
# def explore():
#     books = db.session.query(Book).filter(Book.book_status=='1').all()
#     cats = db.session.query(Category).all()
    
#     return render_template('user/explore.html', books=books, cats=cats)  

# @app.route('/search/book')
# def search_book():
#     cate = request.args.get('category')
#     title = request.args.get('title') 
#     search_title = "%"+title+"%" # "%{}%".format(title)
#     #run query
#     if cate =="":
#         result = db.session.query(Book).filter(Book.book_title.ilike(search_title)).all()
#     else:
#         result = db.session.query(Book).filter(Book.book_catid ==cate).filter(Book.book_title.ilike(search_title)).all()

    #result = [<Book 1>, <Book 2>, <Book 3>] 
    # toreturn =""
    # for r in result:
    #     toreturn = toreturn + f"<div class='col'><img src='/static/collections/{r.book_cover}' class='img-fluid bk'><div class='deets'><h6><a href='/review/{r.book_id}'>{r.book_title}</a></h6><p><i>{r.catdeets.cat_name}</i></p><p><button class='btn btn-sm btn-warning'{len(r.bookreviews)}>Reviews</button></p></div></div>"
    
    # return toreturn



# @app.route("/userlog",methods=["POST","GET"])
# def user_log():
#     if request.method=="GET":

#         return render_template("/user/loginpage.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template("user/loginpage.html")
    else:
        username = request.form.get('email') 
        password = request.form.get('password')
        deets = db.session.query(Subscribers). (Subscribers.sub_email==username).first()
        if deets:
            hashedpwd = deets.sub_pwd
            chk = check_password_hash(hashedpwd,password)#returns True/False
            if chk:
                session['sub_loggedin'] = True
                session['subid'] = deets.sub_id
                return redirect("/dashboard")
            else:
                flash("Invalid password")
                return redirect("/login")
        else:
            flash("Invalid username")
            return redirect("/login")


@app.route("/register",methods=["POST","GET"])
def register():
    signupform = SignupForm()
    if request.method =="GET":
        
        s=db.session.query(State).all()
        return render_template("user/signup.html", signupform=signupform,s=s)
    else:
        if signupform.validate_on_submit():
            userpass = request.form.get('password')            
            u = Subscribers(sub_fname=request.form.get('firstname'),
                     sub_email=request.form.get("email"),
                     sub_pwd=generate_password_hash(userpass),
                     sub_lname=request.form.get("lastname"),
                     sub_phone=request.form.get("phone"),
                     sub_dob=request.form.get("dateofbirth"),
                     sub_address=request.form.get("Homeadd"),
                     sub_empadd=request.form.get("empadd"),
                     sub_state_id=request.form.get("state"),
                     sub_lga_id=request.form.get("lgas")
                     )
            db.session.add(u)
            db.session.commit()
            #log the user in and redirect to dashboard u.user_id
            session['subid'] = u.sub_id
            session['sub_loggedin'] =True
            return redirect("/login")
        else:
            return render_template("user/signup.html",signupform=signupform)
@app.route("/verify")
def verification ():
    verform = Verform()
    useronline = session.get('subid')    
    userdeets = db.session.query(Subscribers).get(useronline)
    if request.method =="GET":
        s=db.session.query(State).all()
        return render_template("user/verify.html", verform=verform,userdeets=userdeets,s=s)
    else:
        if verform.validate_on_submit():
            userpass = request.form.get('password')            
            u = Subscribers(sub_fname=request.form.get('firstname'),
                     sub_email=request.form.get("email"),
                     sub_pwd=generate_password_hash(userpass),
                     sub_lname=request.form.get("lastname"),
                     sub_phone=request.form.get("phone"),
                     sub_dob=request.form.get("dateofbirth"),
                     sub_address=request.form.get("Homeadd"),
                     sub_empadd=request.form.get("empadd"),
                     sub_state_id=request.form.get("state"),
                     sub_lga_id=request.form.get("lgas")
                     )
            db.session.add(u)
            db.session.commit()
            #log the user in and redirect to dashboard u.user_id
            session['subid'] = u.sub_id
            session['sub_loggedin'] =True
            return redirect("/login")
        else:
            return render_template("user/verify.html") 
@app.route("/review/<subid>")
def reviews(bookid):
    bookdeets = db.session.query(Reviews).get_or_404(bookid)
    return render_template("user/reviews.html",bookdeets=bookdeets)
      
@app.route("/profile", methods=['POST',"GET"])
@login_required
def profile():
    pform = ProfileForm()
    useronline = session.get('subid') 
    userdeets = db.session.query(Subscribers).get(useronline) 
    if request.method == "GET":        
        return render_template("user/update.html", pform=pform,userdeets=userdeets)
    else:
        if pform.validate_on_submit():
            fullname = request.form.get('fullname') #pform.fullname.data
            picture = request.files.get('pix') #pform.pix.data.filename
            filename= pform.pix.data.filename   
            picture.save("thriftapp/static/images/profile/"+filename) 
            userdeets.user_fullname=fullname
            userdeets.user_pix=filename
            db.session.commit()
            flash("Profile updated")
            return redirect("/dashboard")
        else:
            return render_template("user/update.html", pform=pform,userdeets=userdeets)




@app.route("/signout")  
def signout():
    if session.get('subid') or session.get('sub_loggedin'):
        session.pop('subid',None)
        session.pop('sub_loggedin',None)
    return redirect("/login")

@app.route("/lga")
def load_lga():
    s=db.session.query(State).all()
    return render_template("/user/signup.html",s=s)


@app.route("/show_lga")
def show_lga():
    stateid=request.args.get('stateid')
    lgas=db.session.query(Lga).filter(Lga.state_id==stateid).all()
    toreturn=""
    for t in lgas:
        toreturn=toreturn + f'<option value="{t.lga_id}">'+ t.lga_name+'</option>'

    return toreturn

# @app.route("/dashboard")
# @login_required
# def user_dashboard():
 
#     useronline = session.get('subid')    
#     userdeets = db.session.query(Subscribers).get(useronline)
#     return render_template("user/dashboard.html",userdeets=userdeets)




@app.route("/choose",methods=["POST","GET"])
def choice():
    useronline = session.get('subid')    
    userdeets = db.session.query(Subscribers).get(useronline)
    if request.method == "GET":
        plan = db.session.query(Plan).all()
        users = db.session.query(Subscribers).all()
        return render_template("user/choose.html", plan_id=plan, sub_id=users, userdeets=userdeets)
    else:
        # Retrieve the form data
        subscriber_id = useronline  # Set the subscriber ID
        plan_id = request.form.get('plans')  # Assuming the form field is named 'plan_id'
        plan_amt = request.form.get('plan_amt')  # Assuming the form field is named 'plan_amt'

        # Create a new subscription object
        new_subscription = Subscribersplan(
            sub_id=subscriber_id,
            plan_id=plan_id,
            datejoined=datetime.utcnow(),
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            plan_amt=plan_amt
        )

        # Add the object to the session
        db.session.add(new_subscription)

        # Commit the changes to the database
        db.session.commit()
        return redirect("/makepay")



@app.route("/collections")
def collect():
    return render_template("user/collections.html")

# @app.route("/makepay")
# def payment():
#     return render_template("user/makepay.html")

@app.route("/makepay",methods=["POST","GET"])
def makepay():
    useronline = session.get('subid')    
    userdeets = db.session.query(Subscribers).get(useronline)
    pay_subplandeets=db.session.query(Subscribersplan).all()
    if request.method=="GET":
        return render_template("user/makepay.html",userdeets=userdeets, pay_subplandeets= pay_subplandeets)
    else:
        #retreieve form data
        fullname=request.form.get('fullname')
        email=request.form.get('email')
        plan_amt=request.form.get('plan_amt')
        userid=request.form.get('subid')
        refno=int(random.random()*10000000)
        #create a new donation instance
        pay=Payment(pay_amt=plan_amt,sub_id=userid,pay_fullname=fullname,pay_email=email,pay_refno=refno,pay_status='pending')
        db.session.add(pay)
        db.session.commit()
        #save the freno ina asession so thst we can retrieve the details  on thr next page
        session['ref']= refno

        return redirect("/payment")
@app.route("/payment")
def make_payment():
    userdeets=db.session.query(Subscribers).get(session.get('subid'))
    if session.get('ref') !=None:
        ref=session['ref']
        #display details of transaction to user
        trxdeets=db.session.query(Payment).filter(Payment.pay_refno==ref).first()
        return render_template("user/payment.html",trxdeets=trxdeets,userdeets=userdeets)
    else:
        return redirect("/makepay")
    
@app.route("/paystack",methods=["POST"])
def paystack():
    if session.get('ref') !=None:
        ref=session['ref']
        trx=db.session.query(Payment).filter(Payment.pay_refno==ref).first()
        email=trx.pay_email
        amount=trx.pay_amt
        url="https://api.paystack.co/transaction/initialize"
        headers={"Content-Type":"application/json","Authorization":"Bearer sk_test_67a8c1e9df4a64765feed29282a71fc67af3e4e5"}

        data={"email":email,"amount":amount*100, "reference":ref}
        response=requests.post(url,headers=headers,data=json.dumps(data))
        rspjson=response.json()
        if rspjson['status']==True:
            paygateway=rspjson['data']['authorization_url']
            return redirect(paygateway)
        else:
            return rspjson
    else:
        return redirect("/makepay")
    

@app.route("/landing")
def paystack_landing():
    ref=session.get('ref')
    if ref==None:
        return redirect('/makepay')
    else:
        #connect to paystack verify
        headers={"Content-Type":"application/json","Authorization":"Bearer sk_test_67a8c1e9df4a64765feed29282a71fc67af3e4e5"}
        verifyurl="https://api.paystack.co/transaction/verify/"+str(ref)
       
        response=requests.get(verifyurl,headers=headers)
        rspjson=json.loads(response.text)
        if rspjson['status']==True:
            return rspjson
        else:
            return "payment was not succesful"



@app.route("/setting")
def setst():
    return render_template("user/settings.html")

@app.route("/update")
def update():
    return render_template("user/update.html")








@app.route("/review/<bookid>")
def review(bookid):
    bookdeets = db.session.query(Reviews).get_or_404(bookid)
    return render_template("user/reviews.html",bookdeets=bookdeets)
    


@app.route("/submitreview",methods=['POST'])
@login_required
def submit_review():
    title = request.form.get('review_title')
    text = request.form.get('review')
    bookid = request.form.get('bookid')
    useronline = session.get('subid')
    #insert this review
    review = Reviews(rev_text=text,rev_title=title,rev_bookid=bookid,rev_userid=useronline)
    db.session.add(review)
    db.session.commit()
    flash("Thank you, your review has been submitted")
    return redirect('/dashboard')
    
@app.route("/contact")
def contact_us():
    form=ContactUs()
    return render_template("user/contactform.html",form=form)


@app.route("/submit/contact",methods=["POST"])
def submit_contact_ajax():
    form=ContactUs()
    if form.validate_on_submit():
        fullname=request.form.get('fullname')
        phone=request.form.get('phone')
        email=request.form.get('email')
        message=request.form.get('message')
        f=Contact(name=fullname,email=email,phone=phone,message=message)
        db.session.add(f)
        db.session.commit()
        if f.id:
              
              
              sendback= {"msg":f"Thank you {fullname} for contacting us","msgclass":'alert alert-success'}
        else:
            

            sendback= {"msg":f"Please try again","msgclass": 'alert alert-danger'}

        
      
    else:
        sendback={"msg":f"form validation failed ","msgclass": 'alert alert-danger'}

    return json.dumps(sendback)
    



































# @app.route("/review/<subid>")
# def reviews(bookid):
#     bookdeets = db.session.query(Book).get_or_404(bookid)
#     return render_template("user/reviews.html",bookdeets=bookdeets)
    



    
    






