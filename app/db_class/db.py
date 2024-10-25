from .. import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import  UserMixin, AnonymousUserMixin



class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"))
    text = db.Column(db.String)
    description = db.Column(db.String)
    title = db.Column(db.String)
    lang = db.Column(db.String)

    def to_json(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "text": self.text,
            "description": self.description,
            "title":self.title,
            "lang": self.lang
        }
    
class Documentation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    files = db.relationship('File', backref='documentation', lazy='dynamic', cascade="all, delete-orphan")
    category_id = db.Column(db.Integer, db.ForeignKey('category__doc.id', ondelete="CASCADE"))
    title = db.Column(db.String, unique=True)
    text = db.Column(db.String)
    description = db.Column(db.String)
    last_modif = db.Column(db.DateTime, index=True)
    creation_date = db.Column(db.DateTime, index=True)
    # is_archived = db.Column(db.Boolean, default=False)
    # archived_date = db.Column(db.DateTime, index=True)

    def to_json(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "title": self.title,
            "text": self.text,
            "description": self.description,
            "creation_date": self.creation_date,
            "last_modif": self.last_modif
            # "is_archived": self.is_archived,
            # "archived_date": self.archived_date
        }
    
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('documentation.id', ondelete="CASCADE"))
    uuid = db.Column(db.String(36), index=True)

    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name,
            "doc_id": self.doc_id,
            "uuid": self.uuid
        }
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36))
    name = db.Column(db.String)
    color = db.Column(db.String(), index=True)
    commands = db.relationship('Command', backref='category', lazy='dynamic', cascade="all, delete-orphan")

    def to_json(self):
        json_dict =  {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "color": self.color
        }
        loc = Category.query.join(Category_To_Category, Category_To_Category.parent_id==Category.id).filter_by(child_id=self.id).first()
        json_dict["parent_category"] = {}
        if loc:
            json_dict["parent_category"] = loc.to_json()

        return json_dict
    
class Category_To_Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, index=True)
    child_id = db.Column(db.Integer, index=True)

    def to_json(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "child_id": self.child_id
        }
    
class Category_To_Category_Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, index=True)
    child_id = db.Column(db.Integer, index=True)

    def to_json(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "child_id": self.child_id
        }
    
class Category_Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36))
    name = db.Column(db.String)
    color = db.Column(db.String(), index=True)
    documentations = db.relationship('Documentation', backref='category_doc', lazy='dynamic', cascade="all, delete-orphan")

    def to_json(self):
        json_dict =  {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "color": self.color
        }
        loc = Category_Doc.query.join(Category_To_Category_Doc, Category_To_Category_Doc.parent_id==Category_Doc.id).filter_by(child_id=self.id).first()
        json_dict["parent_category"] = {}
        if loc:
            json_dict["parent_category"] = loc.to_json()

        return json_dict
    




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, index=True)
    password_hash = db.Column(db.String(128))
    api_key = db.Column(db.String(60), index=True)
    
    def is_admin(self):
        r = Role.query.get(self.role_id)
        if r.admin:
            return True
        return False

    def read_only(self):
        r = Role.query.get(self.role_id)
        if r.read_only:
            return True
        return False

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            "id": self.id, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "email": self.email,
            "role_id": self.role_id
        }

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def read_only(self):
        return True
    
login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    read_only = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name,
            "description": self.description,
            "admin": self.admin,
            "read_only": self.read_only
        }
    