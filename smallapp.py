from app import create_app, db, cli
from app.models import (
    User, Post, Message, Notification, Task, Categories,
    Brands, Products, Stocks, Stores, Orders, Order_items)

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification,
            'Task': Task, 'Categories': Categories, 'Brands': Brands,
            'Products': Products, 'Stocks': Stocks, 'Stores': Stores,
            'Orders': Orders, 'Order_items': Order_items
            }
