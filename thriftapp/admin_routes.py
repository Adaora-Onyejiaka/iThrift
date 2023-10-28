import re,random,os
from functools import wraps
from flask import render_template, request, redirect, flash,make_response,session,url_for
from sqlalchemy.sql import text
from datetime import datetime,timedelta
from thriftapp import app, csrf
from thriftapp.models import *
def login_required(f):
    @wraps(f) #from functools import wraps
    def login_decorator(*args,**kwargs):
        if session.get("admin") and session.get('admin_loggedin'):
           return f(*args,**kwargs)
        else:
            flash("Access Denied, Please Login")
            return redirect("/admin/dashboard")
    return login_decorator


@app.route("/admin/login", methods=["GET","POST"])
def adminlogin():
    if request.method=="GET":
        return render_template("admin/login.html")
    else:
        #retrieve formdata
        username=request.form.get("username")
        pwd=request.form.get("password")
        chk=db.session.query(Admin).filter(Admin.admin_username==username,Admin.admin_pwd==pwd).all
        if chk:
            session['admin_loggedin']=True
            return redirect("/admin/dashboard")
        else:
            flash("incorrect details",category="danger")
            return redirect("/admin/login")
        
@app.route("/admin/home")
def adm_home():
    return render_template("admin/admin_layout.html")        
        
@app.route("/admin/logout")
@login_required
def admin_logout():
    if session.get("admin_loggedin"):
        session.pop("admin_loggedin",None)
        flash("you are logged out successfully",category="success")

    return redirect("/admin/login")




@app.route("/admin/dashboard")
def adminhome():
    if session.get('admin_loggedin')==None:
        flash("Access Denied",category="danger")
        return redirect('/admin/login')
    else:
         return render_template("admin/admin_dashboard.html")

# @app.route("/admin/deletebook/<id>")
# def deletebook(id):
#      if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
#      else:
#         bk=db.session.query(Book).get_or_404(id)
#         os.remove("bookapp/static/collections/"+bk.book_cover)
#         db.session.delete(bk)
#         db.session.commit()
#         flash(f"Book {bk.book_title} has been deleted!", category="success" )
#         return redirect("/admin/books")



# @app.route("/admin/dashboard")
# def adminhome():
#     if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
    
#     return render_template("admin/admin_dashboard.html")


@app.route("/admin/users")
def view_users():
    users = Subscribers.query.all()
    return render_template('admin/users.html', users=users)


    

@app.route("/admin/payment")
def view_payment():
    users = Payment.query.all()
    return render_template('admin/pay.html', users=users)


# @app.route("/admin/sub")
# def manage_sub():
#     if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
#     sub=db.session.query(Subscribers).all()
#     return render_template("admin/allbooks.html",sub=sub)


# @app.route("/admin/newbook",methods=["GET","POST"])
# def add_newbook():
#     if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
    
#     if request.method=="GET":
#         cats=db.session.query(Category).all()
#         return render_template("admin/addbook.html", cats=cats)
#     else:
#         #retrieve all the form data
#         bookcat=request.form.get("bookcat")
#         title=request.form.get("title")
#         year=request.form.get("year")
#         status=request.form.get("status")
#         cover=request.files.get("cover")
#         desc=request.form.get("desc")
#         #validate title and file
#         if title !="" and cover:
#             filename=cover.filename
#             allowed=['.jpg','.png','.jpeg']
#             name,ext=os.path.splitext(filename)
#             newname=str(random.random()*1000000) + ext
#             if ext.lower() in allowed:
#                 cover.save("bookapp/static/collections/"+newname)
#                 b=Book(book_title=title,book_desc=desc,book_cover=newname,book_publication=year,book_catid=bookcat,book_status=status)
#                 db.session.add(b)
#                 db.session.commit()
#                 flash("Book has been added", category="success")
#                 return redirect("/admin/books")
#             else:
#                 flash("Please upload only type jpg, png or jpeg", category="danger")
#                 return redirect("/admin/newbook")
#         else:
#             flash("complete the required field", category="danger")

#             return redirect("/admin/newbook")

































































































































































































      


# @app.route("/admin/books")
# def manage_books():
#     if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
#     books=db.session.query(Book).all()
#     return render_template("admin/allbooks.html",books=books)


# @app.route("/admin/newbook",methods=["GET","POST"])
# def add_newbook():
#     if session.get('admin_loggedin')==None:
#         flash("Access Denied",category="danger")
#         return redirect('/admin/login')
    
#     if request.method=="GET":
#         cats=db.session.query(Category).all()
#         return render_template("admin/addbook.html", cats=cats)
#     else:
#         #retrieve all the form data
#         bookcat=request.form.get("bookcat")
#         title=request.form.get("title")
#         year=request.form.get("year")
#         status=request.form.get("status")
#         cover=request.files.get("cover")
#         desc=request.form.get("desc")
#         #validate title and file
#         if title !="" and cover:
#             filename=cover.filename
#             allowed=['.jpg','.png','.jpeg']
#             name,ext=os.path.splitext(filename)
#             newname=str(random.random()*1000000) + ext
#             if ext.lower() in allowed:
#                 cover.save("bookapp/static/collections/"+newname)
#                 b=Book(book_title=title,book_desc=desc,book_cover=newname,book_publication=year,book_catid=bookcat,book_status=status)
#                 db.session.add(b)
#                 db.session.commit()
#                 flash("Book has been added", category="success")
#                 return redirect("/admin/books")
#             else:
#                 flash("Please upload only type jpg, png or jpeg", category="danger")
#                 return redirect("/admin/newbook")
#         else:
#             flash("complete the required field", category="danger")

#             return redirect("/admin/newbook")