from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
import models # our custom defined models

# create a Blueprint variable named admin_page.
admin_page = Blueprint('admin_page', __name__, template_folder='templates/admin')


@admin_page.route("/admin/")
def admin():
    if not logged_in():
        return redirect(url_for('login', next='/admin/'))
    # username in session and user has admin role, continue
    return render_template('index.html', title="ADMIN", information="Here you can administer products, services,etc. Click on what you would like to do")


@admin_page.route("/admin/products/")
def products():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session, continue
    # get our registered products from the database
    products = models.Product.query.all()

    # check whether when products route was called using redirect, information was passed.
    # If not passed, use a default message, 'Here you can administer products'
    information = request.args.get('information', 'Here you can administer products')

    # check whether when products route was called using redirect, css was passed.
    # If not passed, use default css 'normal'
    css = request.args.get('css', 'normal')

    return render_template('products.html', title="ADMINISTER PRODUCTS", information=information, css=css, products=products)


def process_product_add():
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue

    if request.method != 'POST':
    # return to products.html page containing add form. Only POST method is allowed
        error = 'Please use the form to add new products'
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent from the form.
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    product_inception_date = request.form['product_inception_date']

    # let's write to the database
    try:
        product = models.Product(name=name, code=code, description=description,
        price_per_unit=price_per_unit,product_inception_date=product_inception_date)
        models.db.session.add(product)
        models.db.session.commit()
    except Exception as e:
        error = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # no error, continue
    return redirect(url_for('admin_page.products', information="Add successful", css="success")


@admin_page.route("/admin/products/edit/<int:id>/", methods=['POST','GET'])
def product_edit(id):
    # check database for the product to edit
    product = models.Product.query.filter_by(id=id).first()
    # send to the edit form
    return render_template('product-edit.html', product=product)


@admin_page.route("/admin/products/process-product-edit/<int:id>/", methods=['POST', 'GET'])
def process_product_edit(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin in role, continue

    if request.method != 'POST':
    # redirect to signup form. Only POST method is allowed
    error = 'Please use the form to edit products'
    return render_template('products.html', title="ADMINISTER PRODUCTS", information=error, css="error")

    # No problem so far, get the request object and the parameters sent.
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price_per_unit = request.form['price_per_unit']
    product_inception_date = request.form['product_inception_date']

    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.Product.query.filter_by(id=id).first()
        # Update the fields
        product.name = name
        product.code = code
        product.description = description
        product.price_per_unit = price_per_unit
        product.product_inception_date = product_inception_date
        # commit
        models.db.session.commit()

    except Exception as e:
        error = 'Could not update product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Update not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Update successful", css="success"))


@admin_page.route("/admin/products/delete/<int:id>/", methods=['POST', 'GET'])
def product_delete(id):
    if not logged_in():
        return redirect(url_for('login', next='/admin/products/'))
    # username in session and admin role, continue


    # No problem so far
    # let's update the database
    try:
        # Get the existing data from database as object
        product = models.Product.query.filter_by(id=id).first()
        # Delete the record
        models.db.session.delete(product)
        # commit
        models.db.session.commit()
    except Exception as e:
        error = 'Could not delete product. The error message is {}'.format(e.__cause__)
        return redirect(url_for('admin_page.products', information="Delete not successful", css="error"))

    return redirect(url_for('admin_page.products', information="Delete successful", css="success"))