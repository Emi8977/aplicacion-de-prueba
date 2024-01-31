from flask import Flask, render_template, request, url_for, redirect
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def paginaprincipal():
    return render_template('index.html')

@app.route('/cargarDatos', methods=['GET','POST'])
def cargarDatos():
    return render_template('cargaDatos.html')

@app.route('/consultarDatos', methods=['GET','POST'])
def consultarDatos():
    return render_template('consultaDatos.html')

@app.route('/lista1', methods=['GET','POST'])
def mostrarlista():
    return render_template('lista.html')
    
@app.route('/editar1', methods=['GET','POST'])
def mostraredicion():
    return render_template('edicion.html')

#CRUD CREATE -Crear ingreso de datos
@app.route('/registrar', methods=['GET','POST'])
def ingreso():
    if request.method == 'POST':
        n1 = request.form['n']
        e1 = request.form['e']
        t1 = request.form['t']
        connection = sqlite3.connect(currentdirectory + '\programacion.db')
        cursor = connection.cursor()
        #el ID debe estar en la base de datos como Primary Key, sino da un error cuando hagamos el query1
        query1 = "INSERT INTO lenguajes (Nombre, Enfoque, Traductor) VALUES ('{nombre}', '{enfoque}', '{traductor}')".format(nombre=n1, enfoque=e1, traductor=t1)
        cursor.execute(query1)
        connection.commit()
        
        msg = "Ingreso creado correctamente"
        
        return render_template('cargaDatos.html', n1=n1, e1=e1, t1=t1, msg=msg)
    
    return render_template('cargaDatos.html')
 
#CRUD: READ -Consultar
@app.route('/preguntar', methods=['GET', 'POST'])
def resultado():
    try:
        if request.method == 'GET':
            n1 = request.args.get('n')
            connection = sqlite3.connect('programacion.db')
            cursor = connection.cursor()
            query1 = "SELECT Nombre, Enfoque, Traductor FROM lenguajes WHERE Nombre = ?"
            cursor.execute(query1, (n1,))
            result = cursor.fetchone()
            
            if result:
                nombre, enfoque, traductor = result
                connection.close()
                return render_template('consultaDatos.html', nombre=nombre, enfoque=enfoque, traductor=traductor)
                return render_template("consultaDatos.html", result=result)
            else:
                return render_template('consultaDatos.html', resultado="No se encontró los datos solicitados")

    except Exception as e:
        return render_template('consultaDatos.html', resultado="Error: {}".format(str(e)))

#Genera la lista de todas las consultas    
@app.route('/lista', methods=['GET', 'POST'])
def lista():
    con = sqlite3.connect("programacion.db")
    
    # Configurar row_factory para utilizar sqlite3.Row
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("SELECT ID, Nombre, Enfoque, Traductor FROM lenguajes")

    rows = cur.fetchall()
    
    con.close()
    
    return render_template("lista.html", rows=rows)

#CRUD -Editar
#Ruta que selecciona un ingreso especifico a traves del ID 
@app.route("/editar", methods=['POST','GET'])
def editar():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("programacion.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT ID, * FROM lenguajes WHERE ID = " + id)

            rows = cur.fetchall()
           
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edicion.html", rows=rows)
   

#Ruta usada para hace la actualizacion en un ingreso especifico
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            nombre = request.form['nombre']
            enfoque = request.form['enfoque']
            traductor = request.form['traductor']


            #QUEDA EDITAR ESTAS LINEA DE CODIGOS PARA QUE SE GUARDE LA EDICION EN LA BASE DE DATOS Y LUEGO MOSTRAR EN LA LISTA

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('programacion.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE lenguajes SET Nombre=?, Enfoque=?, Traductor=? WHERE ID=?", (nombre, enfoque, traductor, id))
                con.commit()
                msg = "Ingreso editado correctamente"
        except:
            con.rollback()
            msg = "Error en la edicion"

        finally:
            con.close()
            # enviar a la pagina de confirmacion -pendiente de hacer dicha pagina por el momento envia a index
            return render_template('mensaje.html',msg=msg)

#CRUD -Borrar
#Ruta para borrar un ingresi especifico de la base de datos   
@app.route("/borrar", methods=['POST','GET'])
def borrar():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('programacion.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM lenguajes WHERE ID="+id)

                    con.commit()
                    msg = "Ingreso borrado correctamente"
        except:
            con.rollback()
            msg = "Error en borrar los datos"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('mensaje.html',msg=msg)


if __name__ == '__main__':
    app.run(debug=True)