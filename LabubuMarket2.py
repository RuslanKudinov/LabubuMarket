from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

users = {"1": "1", "2": "2"}

@app.route("/")
def hello_world():
    return """
    <h1>Добро пожаловать на мой сайт! Вы не авторизованы:(</h1>
    <ul>
        <li><a href="/form">Войти в аккаунт</a></li>
        <li><a href="/register">Зарегистрироваться</a></li>
    </ul>
    """


@app.route("/form", methods=["GET", "POST"])
def questions():
    if request.method == "GET":
        return """
        <h1>Заполните данные: </h1>
        <form method="POST">
            Логин: <input type="text" name="login" required><br>
            Пароль: <input type="password" name="password" required><br>
            <input type="submit" value="Войти">
        </form>
        <p>Еще нет аккаунта? <a href="/register">Зарегистрируйтесь</a></p>
        """
    else:
        login = request.form.get("login")
        password = request.form.get("password")
        ok = False
        if login in users:
            if users[login] == password:
                ok = True

        if ok:
            return redirect("/home")

        else:
            return f"""
            <h1>Данные неправильны! </h1>
            <p><a href="/">На главную</a></p>
            <p><a href="/form">Попробовать снова</a></p>
            <p><a href="/register">Зарегистрироваться</a></p>
            """


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return """
        <h1>Регистрация нового пользователя</h1>
        <form method="POST">
            Логин: <input type="text" name="login" required><br>
            Пароль: <input type="password" name="password" required><br>
            Подтвердите пароль: <input type="password" name="confirm_password" required><br>
            <input type="submit" value="Зарегистрироваться">
        </form>
        <p>Уже есть аккаунт? <a href="/form">Войдите</a></p>
        """
    else:
        login = request.form.get("login")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Проверка на существующего пользователя
        if login in users:
            return f"""
            <h1>Ошибка регистрации!</h1>
            <p>Пользователь с логином '{login}' уже существует.</p>
            <p><a href="/register">Попробовать другой логин</a></p>
            <p><a href="/form">Войти в аккаунт</a></p>
            """

        # Проверка совпадения паролей
        if password != confirm_password:
            return f"""
            <h1>Ошибка регистрации!</h1>
            <p>Пароли не совпадают.</p>
            <p><a href="/register">Попробовать снова</a></p>
            """

        # Регистрация пользователя
        users[login] = password
# "34":"345"
        return f"""
        <h1>Регистрация успешна!</h1>
        <p>Пользователь '{login}' успешно зарегистрирован.</p>
        <p><a href="/form">Войти в аккаунт</a></p>
        <p><a href="/">На главную</a></p>
        """

# Простой каталог товаров
products = [
    {"id": 1, "name": "Лабубу классическая", "price": 999, "image": "product1.jpg","about":"Это тот самый друг, с которого все начинается! Классическая Лабубу — плюшевый король уюта. Стандартного размера, чтобы его было удобно обнимать перед сном, но при этом он такой мягкий и милый, что от него невозможно оторваться. Идеальный подарок, который будет дарить тепло и хорошее настроение годами. Просто классика жанра!"},
    {"id": 2, "name": "Лабубу премиум", "price": 1499, "image": "product2.jpg","about":"А это — самый сок! Лабубу Премиум для тех, кто понимает в уюте толк. Сшит из самых качественных плюшевых тканей premium-класса, набивка — супернежная и упругая. Часто с эксклюзивным дизайном, милыми деталями и проработанной мордочкой. Это не просто игрушка, это статусный спутник и предмет коллекционирования. Настоящая роскошь в мире плюша!"},
    {"id": 3, "name": "Лабубу мини", "price": 599, "image": "product3.jpg","about":"Маленький, да удаленький! Лабубу Мини — это карманная порция счастья. Помещается в любую сумку, чтобы всегда быть рядом и поддерживать в любой ситуации. Бери его с собой в путешествия, на учебу или просто чтобы поднять настроение в хмурый день. Несмотря на размер, в нем вся та же доза обаяния, что и у старшего брата!"},
    {"id": 4, "name": "Лабубу ++", "price": 599, "image": "product4.jpg","about":"пупупу"}
]

# Корзина (временное хранилище)
cart = []

@app.route('/home')
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
    return """Заказ оформлен! Спасибо за покупку! <p><a href="/home">На главную</a></p>"""

app.run(debug=True)