from flask import Flask, render_template, redirect, flash, request, session
import jinja2
from melons import get_melon_list, get_melon_by_id
from forms import LoginForm
from customers import get_by_username

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined # for debugging purposes

### Flask Routes go here. ###
@app.route('/')
def homepage():
    return render_template("base.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    '''Log user into site.'''
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    
        customer = get_by_username(username)
        
        if not customer or customer['password'] != password:
            flash("Invalid username or password")
            return redirect('/login')
        
        session['username'] = customer['username']
        flash('Logged in.')
        return redirect('/melons')    
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    '''Log user out'''
    del session['username']
    flash('User logged out')
    return redirect('/login')
    

@app.route('/melons')
def all_melons():
    '''Return a page showing all melons available for purchase'''
    
    melon_list = get_melon_list()
    return render_template("all_melons.html", melon_list=melon_list)

@app.route('/melon/<melon_id>')
def melon_details(melon_id):
    '''Return a page showing all info about a melon. Also provide a button to buy that melon.'''
    melon = get_melon_by_id(melon_id)
        
    return render_template("melon_details.html", melon=melon)

@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):
    '''Add a melon to the shopping cart'''
    
    #Check if user is logged in
    if 'username' not in session:
        return redirect('/login')
    
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart'] #store cart in local variable
    
    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"{melon_id} added to cart")
    print(cart)
    
    return redirect('/cart')

@app.route('/cart')
def show_shopping_cart():
    '''display contents of shopping cart.'''
    
    #Check if user is logged in
    if 'username' not in session:
        return redirect('/login')
    
    order_total = 0
    cart_melons = []
    
    #Get the cart dictionary from the session (or an empty one if none exists yet)
    cart = session.get("cart", {})
    
    for melon_id, qty in session['cart'].items():
        melon = get_melon_by_id(melon_id)
        melon_type_total = melon.price * qty
        order_total += melon_type_total
        melon.quantity = qty
        melon.type_total = melon_type_total
        
        cart_melons.append(melon)
    
    return render_template('cart.html', cart_melons=cart_melons, order_total=order_total)

@app.route('/empty-cart')
def empty_cart():
    session['cart'] = {}
    
    return redirect('/cart')

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.env = 'development'
    app.run(debug = True, port = 8000, host = 'localhost')