from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)  # 12-значный штрихкод
    image_path = db.Column(db.String(200))
    def __repr__(self):
        return f'<Product {self.name} - {self.price}>'
    image_path = db.Column(db.String(200), nullable=True)

    def delete_image(self):
        if self.image_path:
            try:
                path = os.path.join('app/static', self.image_path)
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                app.logger.error(f"Error deleting image: {str(e)}")
