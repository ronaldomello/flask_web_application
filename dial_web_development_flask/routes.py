# Imports

from sqlalchemy import exc
from pymongo.errors import DuplicateKeyError
from flask import request, make_response, render_template, redirect, session, flash
from flask_restful import Resource
from sql_utils import SqlUtils
from mongodb import MongoUtils
from time import sleep


# Resources

class Index(Resource):
    """Index page, Dashboard"""

    def get(self):

        # In session validation

        if not session.get("name"):
            return redirect("/login")  # Log in page redirect

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Render index (dashboard) page html template

            return make_response(render_template('index_dashboard.html', login=login,
                                                 update_my_account=f"{login}/update", my_account=f"{login}",
                                                 inventory_management=f"{login}/inventory",
                                                 users_management=f"{login}/users", user_admin=True))  # Admin
        else:

            # Render index (dashboard) page html template

            return make_response(render_template('index_dashboard.html', login=login,
                                                 update_my_account=f"{login}/update", my_account=f"{login}",
                                                 inventory_management=f"{login}/inventory",
                                                 users_management=f"{login}/users", user_admin=False))  # User


class Login(Resource):
    """Log in page"""

    def get(self):

        # Render log in page html template

        return make_response(render_template('log_in.html'))

    def post(self):

        # Getting data from forms

        input_login = request.form.get("login").strip()
        input_password = request.form.get("password").strip()
        input_password = SqlUtils.encrypt(input_password)  # Encrypting the password to compare with database password
        user = SqlUtils.select_user(login=input_login)  # Query for user by input login

        # Login validation

        if user is None:
            flash("User not found.")
            return redirect("/login")  # Return to sign up page

        user_password = user.password  # user password

        # Password validation

        if input_password != user_password:
            flash("Incorrect password.")
            return redirect("/login")  # Return to log in page

        # Success, join the session

        else:
            session["name"] = input_login  # User login
            return redirect("/")  # Redirect to index page (dashboard) *logged*


class Logout(Resource):
    """Log out"""

    # Leaving the session

    def get(self):
        session["name"] = None
        return redirect("/")  # Redirect to index page (dashboard) *logged off*


class SignUp(Resource):
    """Sign up page"""

    def get(self):
        return make_response(render_template('sign_up.html'))  # Render sign up page html template

    def post(self):

        # Getting data from forms

        input_login = request.form.get("login").strip()
        input_name = request.form.get("name").strip()
        input_email = request.form.get("email").strip()
        input_password = request.form.get("password").strip()
        input_password_confirm = request.form.get("password_confirm").strip()

        # Unique constraint check, define flash_message

        if SqlUtils.select_user(login=input_login):
            flash_message = "Username already exists."
        if SqlUtils.select_user(email=input_email):
            flash_message = "E-mail already exists."

        # Password validation

        if input_password != input_password_confirm:
            flash("Passwords don't match.")
            return redirect("/signup")

        # Success, try to create account

        else:
            try:
                SqlUtils.insert_user(input_login, input_password, input_name, input_email)
                sleep(2)
                return redirect("/")  # Redirect to index page (dashboard) *logged off*

            # Exception username(login)/email // unique

            except exc.IntegrityError:
                flash(flash_message)
                return redirect("/signup")  # Return to sign up page


class MyAccount(Resource):
    """My account page"""

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        user = SqlUtils.select_user(login=login)  # Return user by login

        # Render my account page html template

        return make_response(render_template('my_account.html', login=login, user_name=user.name,
                                             user_email=user.email, update_my_account=f"{login}/update"))


class UpdateAccount(Resource):
    """Update my account page"""

    # In session validation

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # Render my account update page html template

        return make_response(render_template('update_my_account.html'))

    def post(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # Query for current user password

        current_password = SqlUtils.select_user(login=login).password

        # Getting data from forms

        input_new_login = request.form.get("new_login").strip()
        input_new_name = request.form.get("new_name").strip()
        input_new_email = request.form.get("new_email").strip()
        input_current_password = request.form.get("current_password").strip()
        input_new_password = request.form.get("new_password").strip()
        input_new_password_confirm = request.form.get("new_password_confirm").strip()

        # Encrypting the current input password to compare with database password

        input_current_password = SqlUtils.encrypt(input_current_password)

        # Password validation: Current x New

        if current_password != input_current_password:
            flash("Password incorrect.")
            return redirect(f"/{login}/update")  # Returns to the user account update page

        # Password validation: New x New

        if input_new_password != input_new_password_confirm:
            flash("Passwords don't match.")
            return redirect(f"/{login}/update")  # Returns to the user account update page

        # Unique constraint check, define flash_message

        if SqlUtils.select_user(login=input_new_login):
            flash_message = "Username already exists."

        if SqlUtils.select_user(email=input_new_email):
            flash_message = "E-mail already exists."

        # Success, try update user account (my account)

        try:
            data = {"login": input_new_login, "password": input_new_password, "name": input_new_name,
                    "email": input_new_email}  # Grouping the data
            SqlUtils.update_user(login=login, data=data)  # Update user by login
            if input_new_login:
                session["name"] = input_new_login  # New user login
            return redirect("/")  # Redirect to index page (dashboard) *logged*

        # Exception username(login)/email // unique

        except exc.IntegrityError:
            flash(flash_message)
            return redirect(f"/{login}/update")  # Returns to the user account update page


class Users(Resource):
    """Users management page"""
    # id will never be the in-session user id, the id refers to the other users, to be edited or deleted
    # user link -> add new user, delete or edit other users

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Query for all user into database

            users = SqlUtils.select_user(all=True)

            # Render index (dashboard) page html template

            return make_response(render_template('users_management.html', users=users, dashboard="/",
                                                 user_link=f"/{login}/user/", user_admin=True))  # Admin
        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)

    def post(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            search = request.form.get("search").strip()
            user_s = SqlUtils.select_user(forms=True, name=search)  # Query(LIKE) for input username

            if user_s:  # If you find results,list users found

                # Render index (dashboard) page html template

                return make_response(render_template('users_management.html', users=user_s, dashboard="/",
                                                     user_link=f"/{login}/user/", search=True,
                                                     search_return=f"/{login}/users", user_admin=True))  # Admin
            else:
                if user_s is None:  # If you not find results
                    flash('User not found.')
                return redirect(f"/{login}/users")  # Return to users management page

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)


class UserAdd(Resource):
    """Add new user page"""
    # id will never be the in-session user id, the id refers to user to be edited

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Render user add html template

            return make_response(render_template('user_add.html', users_management=f"/{login}/users"))

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)

    def post(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Getting data from forms

            input_login = request.form.get("new_login")
            input_name = request.form.get("new_name")
            input_email = request.form.get("new_email")
            input_user_type = request.form.get("user_type")
            input_password = request.form.get("new_password")
            input_password_confirm = request.form.get("new_password_confirm")

            # Unique constraint check, define flash_message

            if SqlUtils.select_user(login=input_login):
                flash_message = "Username already exists."
            if SqlUtils.select_user(email=input_email):
                flash_message = "E-mail already exists."

            # Password validation

            if input_password != input_password_confirm:
                flash("Passwords don't match.")
                return redirect(f"/{login}/user/add")  # Returns to the user add page
            else:

                # Success, try to add user account

                try:

                    if input_user_type == 'user':  # User Account
                        SqlUtils.insert_user(input_login, input_password, input_name, input_email)

                    elif input_user_type == 'admin':  # Admin Account
                        SqlUtils.insert_user(input_login, input_password, input_name, input_email, admin=True)

                    sleep(2)
                    return redirect(f"/{login}/users")  # Returns to the users page

                # Exception username(login)/email // unique

                except exc.IntegrityError:
                    flash(flash_message)
                    return redirect(f"/{login}/user/add")  # Returns to the user add page

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)


class UserEdit(Resource):
    """User edit page"""
    # id will never be the in-session user id, the id refers to user to be edited

    def get(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Query for user to be edited login, by your id

            to_edit_user = SqlUtils.select_user(id=id)  # User being edited login, by your id

            # Render user edit html template

            return make_response(render_template('user_edit.html', to_edit_user=to_edit_user,
                                                 users_management=f"/{login}/users"))

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)

    def post(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Getting data from forms

            input_new_login = request.form.get("new_login").strip()
            input_new_name = request.form.get("new_name").strip()
            input_new_email = request.form.get("new_email").strip()
            input_user_type = request.form.get("user_type").strip()
            input_new_password = request.form.get("new_password").strip()
            input_new_password_confirm = request.form.get("new_password_confirm").strip()

            # Unique constraint check, define flash_message

            if SqlUtils.select_user(login=input_new_login):
                flash_message = "Username already exists."
            if SqlUtils.select_user(email=input_new_email):
                flash_message = "E-mail already exists."

            # Password validation

            if input_new_password != input_new_password_confirm:
                flash("Passwords don't match.")
                return redirect(f"/{login}/user/{id}/edit")  # Returns to the user edit page
            else:

                # Success, try edit user account

                try:
                    # User editing his own account

                    if id == SqlUtils.select_user(login=login).id:
                        if input_new_login:
                            # New user login
                            session['name'] = input_new_login
                            login = input_new_login

                    # Grouping the data

                    data = {"login": input_new_login, "password": input_new_password, "name": input_new_name,
                            "email": input_new_email, "user_type": input_user_type}
                    SqlUtils.update_user(id=id, data=data)  # Edit user by id

                    return redirect(f"/{login}/users")  # Returns to the users page

                # Exception username(login)/email // unique

                except exc.IntegrityError:
                    flash(flash_message)
                    return redirect(f"/{login}/user/{id}/edit")  # Returns to the user edit page

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)


class UserDelete(Resource):
    """User delete page"""
    # id will never be the in-session user id, the id refers to user to be deleted

    def get(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Query for user to be deleted login, by your id

            to_edit_user_login = SqlUtils.select_user(id=id).login  # User to be deleted login, by your id

            # Render user delete html template

            return make_response(render_template('user_delete.html', to_edit_user_login=to_edit_user_login,
                                                 users_management=f"/{login}/users"))

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)

    def post(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # User editing his own account

            if id == SqlUtils.select_user(login=login).id:
                SqlUtils.delete_user(id)
                session['name'] = None
                return redirect("/")  # Redirect to login page

            # Deleting user by your id

            else:
                SqlUtils.delete_user(id)
                return redirect(f"/{login}/users")  # Returns to the users page

        else:

            # Common users do not have the user management feature

            return redirect("/")  # Redirect to index page (dashboard)


class Inventory(Resource):
    """Inventory management page"""

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # Query for all products

        products = MongoUtils.select_product(all=True)

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            return make_response(render_template('inventory_management.html', dashboard="/",
                                                 products=products, user_admin=True, user_login=login))
        else:

            # Common users do not have the product management feature

            return make_response(render_template('inventory_management.html', dashboard="/",
                                                 products=products, user_admin=False))

    def post(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # Search product feature

        search = request.form.get("search").strip()
        product_s = MongoUtils.select_product(forms=True, name=search)  # Query(LIKE) for input product

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            if product_s:  # If you find results,list products found

                # Render index (dashboard) page html template

                return make_response(render_template('inventory_management.html', dashboard="/",
                                                     search=True, search_return=f"/{login}/inventory",
                                                     products=product_s, user_admin=True))  # Admin
            else:
                if len(product_s) == 0:  # If you not find results
                    flash('Product not found.')
                return redirect(f"/{login}/inventory")  # Return to inventory management page

        else:

            if product_s:  # If you find results,list products found

                # Render index (dashboard) page html template

                return make_response(render_template('inventory_management.html', dashboard="/",
                                                     search=True, search_return=f"/{login}/inventory",
                                                     products=product_s, user_admin=False))  # User
            else:
                if len(product_s) == 0:  # If you not find results
                    flash('Product not found.')
                return redirect(f"/{login}/inventory")  # Return to inventory management page


class InventoryAdd(Resource):
    """Inventory add page"""

    def get(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            return make_response(render_template('inventory_add.html', inventory_management=f"/{login}/inventory"))
        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page

    def post(self, login):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            user_id = SqlUtils.select_user(login=login).id  # User id

            # Getting data from forms

            product_name = request.form.get("product_name").strip()
            product_code = request.form.get("product_code").strip()
            product_quantity = int(request.form.get("product_quantity"))
            product_price = round(float(request.form.get("product_price")), 2)
            product_category = request.form.get("product_category").strip()
            inventory_location = request.form.get("inventory_location").strip()

            # Success, try to add new product

            try:

                MongoUtils.insert_product(user_id, product_name, product_code, product_quantity, product_price,
                                      product_category, inventory_location)
                sleep(2)
                return redirect(f"/{login}/inventory")  # Return to inventory management page

            except DuplicateKeyError:  # Exception product(unique) -> [product_name, product_code, inventory_location]

                flash("Product already exists in this stock.")
                return redirect(f"/{login}/inventory/add")  # Returns to the product add page

        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page


class InventoryEdit(Resource):
    """Inventory edit page"""

    def get(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            to_edit_product = MongoUtils.select_product(id=id)

            return make_response(render_template('inventory_edit.html', inventory_management=f"/{login}/inventory",
                                                 to_edit_product=to_edit_product))
        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page

    def post(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            user_id = SqlUtils.select_user(login=login).id  # User id

            # Getting data from forms

            product_name = request.form.get("product_name").strip()
            product_code = request.form.get("product_code").strip()
            product_quantity = request.form.get("product_quantity")
            product_price = request.form.get("product_price")
            product_category = request.form.get("product_category").strip()
            inventory_location = request.form.get("inventory_location").strip()

            # Success, try to edit product

            try:

                MongoUtils.update_product(id, user_id, product_name, product_code, product_quantity, product_price,
                                      product_category, inventory_location)
                sleep(2)
                return redirect(f"/{login}/inventory")  # Return to inventory management page

            except DuplicateKeyError:  # Exception product(unique) -> [product_name, product_code, inventory_location]

                flash("Product already exists in this stock.")
                return redirect(f"/{login}//inventory/{id}/edit")  # Returns to the product add page

        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page


class InventoryDelete(Resource):
    """Inventory delete page"""
    # id will never be the in-session user id, the id refers to product to be deleted

    def get(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            to_delete_product = MongoUtils.select_product(id=id)

            return make_response(render_template('inventory_delete.html', inventory_management=f"/{login}/inventory",
                                                 to_delete_product=to_delete_product))
        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page

    def post(self, login, id):

        # In session validation

        if not session.get("name"):
            return redirect("/")  # Redirect to index page (dashboard) *logged off*
        else:

            # Valid session validation, if the current user tries to access another user's page

            if login != session.get("name"):
                return redirect("/")  # Redirect to index page (dashboard)

        # Success, join the session

        login = session["name"]  # User login

        # User type validation (user_admin=['admin', 'user'], true if 'admin' else 'false') -> different features

        if SqlUtils.select_user(login=login).user_type == 'admin':

            # Remove product by '_id'

            MongoUtils.delete_product(id)

            return redirect(f"/{login}/inventory")  # Return to inventory management

        else:

            # Common users do not have the product management feature

            return redirect(f"/{login}/inventory")  # Return to inventory management page
