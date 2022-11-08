# from flask_sqlalchemy import SQLAlchemy



# db = SQLAlchemy()

# class Person(db.Model):
#     #Every Row in the table is a person; Every Column is a field for the Person
#     id = db.Column(db.Integer, primary_key=True) #db.Integer is a SQL integer type
#     username = db.Column(db.String(80),unique=True,nullable=False)
#     email = db.Column(db.String(120),unique=True,nullable=False)

#     #Return the Person + username
#     def __repr__(self) -> str:
#         return '<Person%r>' % self.username
