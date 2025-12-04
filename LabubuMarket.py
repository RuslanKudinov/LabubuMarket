from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Простой каталог товаров
products = [
    {"id": 1, "name": "Лабубу классическая", "price": 999, "image": "product1.jpg"},
    {"id": 2, "name": "Лабубу премиум", "price": 1499, "image": "product2.jpg"},
    {"id": 3, "name": "Лабубу мини", "price": 599, "image": "product3.jpg"},
]

# Корзина (временное хранилище)
cart = []

@app.route('/market')
def index():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = None
    for p in products:
        if p['id'] == product_id:
            product = p
    # product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    return "Товар не найден", 404

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart.append(product)
        return redirect(url_for('index'))
    return "Товар не найден", 404

@app.route('/cart')
def view_cart():
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    # Здесь должна быть логика оформления заказа
    cart.clear()
    return "Заказ оформлен! Спасибо за покупку!"

if __name__ == '__main__':
    app.run(debug=True)