from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Product
from werkzeug.utils import secure_filename
import os

# Конфигурация загрузки файлов
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Ограничение 2MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        barcode = request.form['barcode']

        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f'uploads/{filename}'

        product = Product(name=name, price=price, barcode=barcode, image_path=image_path)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('index'))

    # === 🔍 Обработка поиска ===
    search_query = request.args.get('search', '').strip()
    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products)

@app.route('/delete', methods=['POST'])
def delete_product():
    product_id = request.form['id']
    product = Product.query.get(product_id)
    if product:
        if product.image_path:
            try:
                os.remove(os.path.join('app/static', product.image_path))
            except OSError:
                pass
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!')
    return redirect(url_for('index'))

@app.route('/edit-product', methods=['POST'])  # Явно указываем путь
def edit_product():
    try:
        product_id = request.form['id']
        product = Product.query.get_or_404(product_id)

        # Обновление данных
        product.name = request.form.get('name', product.name)
        product.price = float(request.form.get('price', product.price))
        product.barcode = request.form.get('barcode', product.barcode)

        # Обработка изображения
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Удаление старого изображения
                if product.image_path:
                    try:
                        os.remove(os.path.join('app/static', product.image_path))
                    except Exception as e:
                        app.logger.error(f"Error deleting image: {e}")

                # Сохранение нового изображения
                filename = secure_filename(f"{product.id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.image_path = f'uploads/{filename}'

        db.session.commit()
        flash('Товар успешно обновлен!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении: {str(e)}', 'error')

    return redirect(url_for('index'))
