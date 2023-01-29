# Imports

from flask import Flask
from flask_restful import Api
from routes import Index, Login, SignUp, Logout, UpdateAccount, MyAccount, Inventory, Users, UserAdd, \
    UserEdit, UserDelete, InventoryAdd, InventoryEdit, InventoryDelete

# Instantiating

app = Flask(__name__)
app.config.from_object('config.Config')

api = Api(app)

# Adding resources

api.add_resource(Index, '/')
api.add_resource(Logout, '/logout')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(UpdateAccount, '/<string:login>/update')
api.add_resource(MyAccount, '/<string:login>')
api.add_resource(Inventory, '/<string:login>/inventory')
api.add_resource(Users, '/<string:login>/users')
api.add_resource(UserAdd, '/<string:login>/user/add')
api.add_resource(UserEdit, '/<string:login>/user/<int:id>/edit')
api.add_resource(UserDelete, '/<string:login>/user/<int:id>/delete')
api.add_resource(InventoryAdd, '/<string:login>/inventory/add')
api.add_resource(InventoryEdit, '/<string:login>/inventory/<string:id>/edit')
api.add_resource(InventoryDelete, '/<string:login>/inventory/<string:id>/delete')


if __name__ == '__main__':
    app.run(debug=True)  # Run APP
