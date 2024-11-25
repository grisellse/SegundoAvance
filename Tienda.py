import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFormLayout, QLineEdit, QStackedWidget, QMainWindow, QHBoxLayout,QTableWidget,QSizePolicy, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QIcon
import sqlite3

# Ventana para gestionar productos----

class VProductos(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Gestionar Productos')
        label.setAlignment(Qt.AlignCenter)  # esto es para  centrar el texto
        layout.addWidget(label)# esto es para agregar el label a la ventana

        # Formulario con campos de la ventana productos
        form_layout = QFormLayout()
        self.nombre_input = QLineEdit() # esto es para  crear un campo de texto
        self.nombre_input.setFixedSize(500, 40)# esto es para darle un tamaño a la caja de texto
        form_layout.addRow('Nombre del Producto:', self.nombre_input)# esto es para agragar el campo de texto al formulario
        self.precio_input = QLineEdit()
        self.precio_input.setFixedSize(500, 40)
        form_layout.addRow('Precio: $', self.precio_input)
        layout.addLayout(form_layout)# esto es para agregar el formulario a la ventana
        self.id_input = QLineEdit()
        self.id_input.setFixedSize(500, 40)
        form_layout.addRow('ID del Producto:', self.id_input)
        layout.addLayout(form_layout)

        # Layout para los botones
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)# esto centra los botones
        self.btn_add_product = QPushButton('Agregar') # esto es para crear un boton
        self.btn_add_product.setFixedSize(150, 40)# esto es para darle un tamaño al boton
        self.btn_edit_product = QPushButton('Editar')
        self.btn_edit_product.setFixedSize(150, 40)
        self.btn_del_product = QPushButton('Eliminar')
        self.btn_del_product.setFixedSize(150, 40)
        btn_layout.addWidget(self.btn_add_product)# esto es para  agregar el boton a la ventana
        btn_layout.addWidget(self.btn_edit_product)
        btn_layout.addWidget(self.btn_del_product)# 
        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.setSpacing(60)#  esto es para darle un espacio entre los botones
        layout.addLayout(btn_layout)
         # Tabla para mostrar productos
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Precio'])
        layout.addWidget(self.table)

        self.setLayout(layout)# 

        # Definir los estilos la ventana
        self.setStyleSheet("""
            QWidget {
                background-color:;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #918dd0 ;
                font-size: 16px;
            }               
            QPushButton {
                background-color: #918dd0;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #908af2;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
        """)

        self.btn_add_product.clicked.connect(self.agregar_producto)
        self.btn_edit_product.clicked.connect(self.editar_producto)
        self.btn_del_product.clicked.connect(self.eliminar_producto)
        self.table.cellClicked.connect(self.seleccionar_producto)

        self.cargar_productos()
    def cargar_productos(self):
        """Cargar productos desde la base de datos en la tabla."""
        conn = sqlite3.connect('Latiendita.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)  # Limpiar la tabla
        for producto in productos:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(producto):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def seleccionar_producto(self, row, column):
        """Seleccionar producto de la tabla y llenar los campos de entrada."""
        self.id_input.setText(self.table.item(row, 0).text())
        self.nombre_input.setText(self.table.item(row, 1).text())
        self.precio_input.setText(self.table.item(row, 2).text())

    def mostrar_mensaje(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def agregar_producto(self):
        nombre = self.nombre_input.text()
        precio = self.precio_input.text()


        if nombre and precio:
            try:
                precio = float(precio)  # Convertir a float
                conn = sqlite3.connect('Latiendita.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)', (nombre, precio, 0))
                conn.commit()
                conn.close()

                self.mostrar_mensaje("Producto agregado")
                self.cargar_productos()
                self.nombre_input.clear()
                self.precio_input.clear()
            except Exception as e:
                print("Error al agregar producto:", e)
          
                self.mostrar_mensaje("Error al agregar producto:", e)
        else:
            self.mostrar_mensaje("Por favor, complete todos los campos.")

    def mostrar_mensaje(self, mensaje):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(mensaje)
            msg.setWindowTitle("Notificacion")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def editar_producto(self):
        nombre = self.nombre_input.text()
        precio = self.precio_input.text()
        id_producto = self.id_input.text()

        if nombre and precio and id_producto:
            try:
                precio_f = float(precio)
                conn = sqlite3.connect('Latiendita.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE productos SET nombre = ?, precio = ? WHERE id = ?', (nombre, precio_f, id_producto))
                conn.commit()
                conn.close()
                self.mostrar_mensaje("Producto editado correctamente.")
                self.cargar_productos()
                self.nombre_input.clear()
                self.precio_input.clear()
                self.id_input.clear()
            except ValueError:
                self.mostrar_mensaje("Por favor, ingrese un precio válido.")
            except Exception as e:
                print("Error al editar producto:", e)
                self.mostrar_mensaje("Error al editar el producto.")
        else:
            self.mostrar_mensaje("Por favor, complete todos los campos.")

    def eliminar_producto(self):
            id_producto = self.id_input.text()

            if id_producto:
                try:
                    conn = sqlite3.connect('Latiendita.db')
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM productos WHERE id = ?', (id_producto,))
                    conn.commit()
                    conn.close()
                    self.mostrar_mensaje("Producto eliminado correctamente.")
                    self.cargar_productos()
                    self.id_input.clear()
                except Exception as e:
                    print("Error al eliminar producto:", e)
                    self.mostrar_mensaje("Error al eliminar el producto.")
            else:
                self.mostrar_mensaje("Por favor, ingrese el ID del producto a eliminar.")


class VVentas(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #ceb2f9;  
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #918dd0;
                font-size: 16px;
            }               
            QPushButton {
                background-color: #918dd0;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #908af2;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
            
            QTableWidget {
            background-color: #ceb2f9 ;  
            color: white;  
            font-size: 16px;
            }
            QHeaderView::section {
            background-color: #918dd0;  
            color: white;  
            font-size: 16px;
            font-weight: bold;
            }
            QScrollBar:vertical {
            background: #918dd0;  
            width: 10px;
            }
            QScrollBar::handle:vertical {
            background: #918dd0; 
            min-height: 20px;
            border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
            }
            """)

        l_principal = QHBoxLayout(self)

        seccion_venta = QVBoxLayout()
        
        titulo = QLabel("Punto de Venta")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        seccion_venta.addWidget(titulo)

        # tabla para los productos agregados a la venta
        self.tab_productos = QTableWidget(0, 4)
        self.tab_productos.setHorizontalHeaderLabels(["Id", "Nombre", "Descripcion", "Precio", "Cantidad"])
        self.tab_productos.setFixedHeight(200)
        seccion_venta.addWidget(self.tab_productos)
        l_precio = QHBoxLayout()
        
      
        self.btn_agr_producto = QPushButton("Agregar Producto")
        self.btn_agr_producto.setFixedSize(150, 40)
        l_precio.addWidget(self.btn_agr_producto)

   
        self.l_total = QLabel("Total: S/ 0.00")
        self.l_total.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")
        self.l_total.setAlignment(Qt.AlignRight)
        l_precio.addWidget(self.l_total)

        
        seccion_venta.addLayout(l_precio)

        l_principal.addLayout(seccion_venta)

       
        seccion_detalles = QVBoxLayout()

     
        self.b_busqueda = QLineEdit()
        self.b_busqueda.setPlaceholderText("Buscar producto...")
        self.b_busqueda.setFixedHeight(40)  # aumenta la altura
        self.b_busqueda.setMinimumWidth(250)  
        self.b_busqueda.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        seccion_detalles.addWidget(self.b_busqueda)
        l_botones = QHBoxLayout()
        
        # boton para generar factura
        self.btn_g_factura = QPushButton("Generar Factura")
        self.btn_g_factura.setFixedSize(150, 40)
        l_botones.addWidget(self.btn_g_factura)

        # botpn para finalizar la venta
        self.btn_f_venta = QPushButton("Finalizar Venta")
        self.btn_f_venta.setFixedSize(150, 40)
        l_botones.addWidget(self.btn_f_venta)
        seccion_detalles.addLayout(l_botones)
        l_principal.addLayout(seccion_detalles)

       # cargar base de datos 
    def cargar_productos(self):
        conn = sqlite3.connect('Latiendita.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        self.tab_productos.setRowCount(len(productos))
        
        for row_index, row_data in enumerate(productos):
            for column_index, item in enumerate(row_data):
                self.tab_productos.setItem(row_index, column_index, QTableWidgetItem(str(item)))

        conn.close()

# inicio----
class Inicio(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel('Bienvenido a la Administración de la Tienda')
        label.setAlignment(Qt.AlignCenter)  
        layout.addWidget(label)
        self.setLayout(layout)
        layout.addStretch()



class VPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('La Tiendita')
        self.setGeometry(100, 100, 800, 400)  # tamaño de la ventana

      

        self.setWindowIcon(QIcon("c:/Users/lenovo/Downloads/SVG/store.png"))  # Ruta al ícono

        # Inicializar la base de datos
        self.inicializar_bd_()

        layout = QVBoxLayout()    
        self.st_widget = QStackedWidget()
      
        #vistas
        self.v_inicio = Inicio()
        self.v_productos = VProductos()
        self.v_ventas = VVentas()

        
        self.st_widget.addWidget(self.v_inicio)
        self.st_widget.addWidget(self.v_productos)
        self.st_widget.addWidget(self.v_ventas)

        # layout para los botones
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(10, 10, 10, 10)  # margenes internos del layout (izquierda, arriba, derecha, abajo)
        botones_layout.setSpacing(90)  #

        self.setStyleSheet("background-color:  #dfddff;")
        self.btn_inicio = QPushButton('Inicio')
        self.btn_inicio.setFixedSize(150, 40)
        self.btn_inicio.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_inicio.clicked.connect(self.vista_inicio)        
        self.btn_productos = QPushButton('Productos')
        self.btn_productos.setFixedSize(150, 40)
        self.btn_productos.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_productos.clicked.connect(self.vista_productos)
        self.btn_ventas = QPushButton('Ventas')
        self.btn_ventas.setFixedSize(150, 40)
        self.btn_ventas.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_ventas.clicked.connect(self.vista_ventas)

        # añadir los botones al layout
        botones_layout.addStretch(1)
        botones_layout.addWidget(self.btn_inicio)
        botones_layout.addWidget(self.btn_productos)
        botones_layout.addWidget(self.btn_ventas)
        botones_layout.addStretch(1)

        # añadir el stacked_widget y el layout de botones al layout principal
        layout.addWidget(self.st_widget)
        layout.addLayout(botones_layout)

        # crear un widget central para la ventana principal
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # muetrar la pantalla de inicio por defecto
        self.vista_inicio()

    def inicializar_bd_(self):
        self.conn = sqlite3.connect('Latiendita.db')
        self.cursor = self.conn.cursor()

        # Crear tabla de productos 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )
        ''')
        self.conn.commit()



    # funciones para mostrar las vistas
    def vista_inicio(self):
        self.st_widget.setCurrentIndex(0)

    def vista_productos(self):
        self.st_widget.setCurrentIndex(1)

    def vista_ventas(self):
        self.v_ventas.cargar_productos() 
        self.st_widget.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # se crea y se muestra la ventana principal
    ventana = VPrincipal()
    ventana.show()

    sys.exit(app.exec_())
