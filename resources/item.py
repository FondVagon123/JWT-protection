from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from models.ItemModel import ItemModel
from db import db

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return {"id": item.id, "name": item.name, "price": item.price}

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    def get(self):
        return [item.name for item in ItemModel.query.all()]
