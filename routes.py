from flask_restful import Resource

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, API World!'}

class Item(Resource):
    def get(self, item_id):
        # Ejemplo de obtención de un ítem ficticio
        return {'item_id': item_id, 'name': f'Item {item_id}'}

class APIRoutes:
    def init_api(self, api):
        api.add_resource(HelloWorld, '/')
        api.add_resource(Item, '/item/<int:item_id>')