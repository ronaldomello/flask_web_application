# Imports

from hashlib import md5
from models import User, db_session


# Utility methods

class SqlUtils:
    """Class for all operations with database"""

    # Select

    def select_user(all=False, forms=False, id=None, login=None, name=None, email=None):
        if all is True:
            """Return all users into database"""
            users = User.query.all()
            db_session.remove()
            return users
        if forms is True:
            """Search user by name (LIKE), return user"""
            if name:
                search = f"%{name}%"
                user_s = User.query.filter(User.name.like(search)).all()
                db_session.remove()
                if user_s:
                    return user_s
                else:
                    return None
            else:
                return False
        if id:
            """Search user by id"""
            user = User.query.filter_by(id=id).first()
            db_session.remove()
            if user:
                return user
            else:
                return None
        if login:
            """Search user by login, return user"""
            user = User.query.filter_by(login=login).first()
            db_session.remove()
            if user:
                return user
            else:
                return None
        if email:
            """Search user by email, return user"""
            user = User.query.filter_by(email=email).first()
            db_session.remove()
            if user:
                return user
            else:
                return None
        return False

    # Insert

    def insert_user(login, password, name, email, admin=False):
        if admin is False:
            """Insert user into database"""
            password = md5(password.encode('utf-8')).hexdigest()
            user = User(login=login, password=password, name=name, email=email)
            user.save()
        if admin is True:
            """Insert user(admin) into database"""
            password = md5(password.encode('utf-8')).hexdigest()
            user = User(login=login, password=password, name=name, email=email,
                        user_type="admin")
            user.save()

    # Update

    def update_user(login=None, id=None, data=None):
        if login:
            """Update user by login"""
            user = SqlUtils.select_user(login=login)
            if 'login' in data:
                if data['login'] == "":
                    pass
                else:
                    user.login = data['login']
            if 'password' in data:
                if data['password'] == "":
                    pass
                else:
                    data['password'] = md5(data['password'].encode('utf-8')).hexdigest()
                    user.password = data['password']
            if 'name' in data:
                if data['name'] == "":
                    pass
                else:
                    user.name = data['name']
            if 'email' in data:
                if data['email'] == "":
                    pass
                else:
                    user.email = data['email']
            user.save()
        if id:
            """Edit user by id"""
            user = SqlUtils.select_user(id=id)
            if 'login' in data:
                if data['login'] == "":
                    pass
                else:
                    user.login = data['login']
            if 'password' in data:
                if data['password'] == "":
                    pass
                else:
                    data['password'] = md5(data['password'].encode('utf-8')).hexdigest()
                    user.password = data['password']
            if 'name' in data:
                if data['name'] == "":
                    pass
                else:
                    user.name = data['name']
            if 'email' in data:
                if data['email'] == "":
                    pass
                else:
                    user.email = data['email']
            if 'user_type' in data:
                if data['user_type'] == "":
                    pass
                else:
                    user.user_type = data['user_type']
            user.save()

    # Delete

    def delete_user(id):
        """Delete user by id"""
        user = SqlUtils.select_user(id=id)
        user.delete()

    # Others

    def encrypt(password):
        return md5(str(password).encode('utf-8')).hexdigest()


if __name__ == '__main__':  # For test
    # SqlUtils.insert_user("admin", "admin", "admin", "admin@dial.com", admin=True)  # Create admin
    pass
