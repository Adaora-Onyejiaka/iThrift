from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)


class Plan(db.Model):
    plan_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    plan_name=db.Column(db.String(29),nullable=False)
    

    #set relationship
   

class Subscribersplan(db.Model):
    subplan_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    sub_id= db.Column(db.Integer, db.ForeignKey('subscribers.sub_id'),nullable=False)
    plan_id= db.Column(db.Integer, db.ForeignKey('plan.plan_id'),nullable=True)
    datejoined=db.Column(db.Date(), default=datetime.utcnow,nullable=False)
    start_date =db.Column(db.DateTime(), default=datetime.utcnow)
    end_date = db.Column(db.Date())
    plan_amt=db.Column(db.Float())
    

    #set relationship
    subplandeets=db.relationship("Subscribers",backref="subdeets")
    plandeets=db.relationship("Plan",backref="myplan")

class State(db.Model):
    state_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    state_name = db.Column(db.String(255),nullable=False)
   

    #set relationship
   

class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    state_id=db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    lga_name = db.Column(db.String(255), nullable=False)


    #set relationship
    lga_statedeets=db.relationship("State",backref="all_lgas")

class Payrotation(db.Model):
    rot_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sub_id= db.Column(db.Integer, db.ForeignKey('subscribers.sub_id'),nullable=False)
    plan_id= db.Column(db.Integer, db.ForeignKey('plan.plan_id'),nullable=False)
    due_date = db.Column(db.Date())
    
    subpaydeets=db.relationship("Subscribers",backref="payrot.sub")
    payrot_plandeets=db.relationship("Plan",backref="payrot.myplan")





class Subscribers(db.Model):
    sub_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    sub_fname = db.Column(db.String(255),nullable=False)
    sub_lname = db.Column(db.String(255),nullable=False)
    sub_dob = db.Column(db.Date())
    sub_phone =db.Column(db.String(100), nullable=False)
    sub_email = db.Column(db.String(100), nullable=False)
    sub_address = db.Column(db.String(100), nullable=False) 
    sub_empadd =db.Column(db.String(100), nullable=False) 
    sub_regdate=db.Column(db.DateTime(), default=datetime.utcnow)
    sub_state_id= db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)  
    sub_lga_id= db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False)  
    sub_pwd=db.Column(db.String(200),nullable=True)
  
    sub_statedeets=db.relationship("State",backref="sub.state")
    sub_lgadeets=db.relationship("Lga",backref="sub.mylga")
    
    #set relationships
    
class Guarantors(db.Model):
    gu_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    gu_fname = db.Column(db.String(255),nullable=False)
    gu_lname = db.Column(db.String(255),nullable=False)
    gu_email = db.Column(db.String(100), nullable=False)
    gu_dob = db.Column(db.Date())
    gu_phone =db.Column(db.String(100), nullable=True)
    gu_address = db.Column(db.String(100), nullable=False) 
    gu_empadd =db.Column(db.String(100), nullable=False) 
    gu_regdate=db.Column(db.DateTime(), default=datetime.utcnow)
    gu_state_id= db.Column(db.Integer, db.ForeignKey('state.state_id'),nullable=False)  
    gu_lga_id= db.Column(db.Integer, db.ForeignKey('lga.lga_id'),nullable=False)
    sub_id= db.Column(db.Integer, db.ForeignKey('subscribers.sub_id'),nullable=False)   
    
    gu_statedeets=db.relationship("State",backref="gu.state")
    gu_lgadeets=db.relationship("Lga",backref="gu.mylga")

    
    #set relationships
    

class Reviews(db.Model):
    rev_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    rev_title = db.Column(db.String(255),nullable=False)
    rev_msg = db.Column(db.String(255),nullable=False)
    rev_date =db.Column(db.DateTime(), default=datetime.utcnow)
    rev_subid = db.Column(db.Integer, db.ForeignKey('subscribers.sub_id'),nullable=False)  
    
    
    #set relationships
    revdeets=db.relationship("Subscribers",backref="subreview")
    
          
  
    
class Payment(db.Model):
    pay_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    subplan_id = db.Column(db.Integer, db.ForeignKey('subscribersplan.subplan_id'),nullable=True) 
    pay_amt = db.Column(db.Float, nullable=False)  
    sub_id = db.Column(db.Integer,db.ForeignKey("subscribers.sub_id"),nullable=False)
    pay_date = db.Column(db.DateTime(), default=datetime.utcnow)
    pay_email=db.Column(db.String(100),nullable=True)
    pay_refno=db.Column(db.String(20),nullable=True)
    pay_fullname=db.Column(db.String(100),nullable=True)
    pay_status =db.Column(db.Enum('pending','failed','paid'),nullable=False, server_default=("pending"))  

    #set relationship
    pay_subdeets=db.relationship("Subscribers",backref="paysub")
    pay_subplandeets=db.relationship("Subscribersplan",backref="paysubplan")

class Collection(db.Model):
    col_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'),nullable=False)
    subplan_id = db.Column(db.Integer, db.ForeignKey('subscribersplan.subplan_id'),nullable=False)
    pay_id = db.Column(db.Integer, db.ForeignKey('payment.pay_id'),nullable=False)
    col_amt = db.Column(db.Float, nullable=False)  
    sub_id = db.Column(db.Integer,db.ForeignKey("subscribers.sub_id"),nullable=False)
    col_date = db.Column(db.DateTime(), default=datetime.utcnow)
    col_status =db.Column(db.Enum('pending','failed','paid'),nullable=False, server_default=("pending")) 
    pay_evidence = db.Column(db.String(255),nullable=False) 
    pay_method = db.Column(db.String(255),nullable=False)


    #set relationship
    Collectdeets = db.relationship('Subscribers',backref='mycollections')
    col_plandeets = db.relationship('Plan',backref='col.myplan')
    colsubplandeets=db.relationship('Subscribersplan',backref='colsubscibplan')

class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text(), nullable=False)
    date_sent = db.Column(db.DateTime(), default=datetime.utcnow)
