from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  

@app.route('/')
def index():
    
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        
        producto_id = request.form['id']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

   
        productos = session.get('productos', [])
        if any(prod['id'] == producto_id for prod in productos):
            flash('El ID del producto debe ser único.', 'error')
            return redirect(url_for('agregar_producto'))

        
        nuevo_producto = {
            'id': producto_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

      
        productos.append(nuevo_producto)
        session['productos'] = productos
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('agregar_producto.html')

@app.route('/eliminar_producto/<string:producto_id>')
def eliminar_producto(producto_id):
    
    productos = session.get('productos', [])
    productos = [prod for prod in productos if prod['id'] != producto_id]
    session['productos'] = productos
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/editar_producto/<string:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    productos = session.get('productos', [])
    producto = next((prod for prod in productos if prod['id'] == producto_id), None)

    if request.method == 'POST':
     
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        flash('Producto editado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('editar_producto.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)