from flask import Flask, render_template, request, redirect, url_for, flash

import mysql.connector
import time

midb = mysql.connector.connect(
    host="localhost",
    user="ricardo",
    password="Carajo182",
    database="web"
)

cursor = midb.cursor()


app = Flask(__name__)
app.secret_key = 'some_secret' #palabra secreta para mensjes flash


@app.route('/')
@app.route('/inicio')
def index():
    return render_template("index.html")

#********Mostrar****************
@app.route('/mostrar')
def mostrar():
    cursor.execute("select * from Usuario")
    mostrar = cursor.fetchall()
    return render_template("mostrar.html", mostrar_datos=mostrar)

#********Insertar****************
@app.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        edad = request.form['edad']
        # insertar datos en DB
        sql = "insert into Usuario (email,username,edad) values(%s,%s,%s)"
        values = (email, username, edad)

        cursor.execute(sql, values)
        if cursor.rowcount == 1:
            midb.commit()
            flash("Datos grabados exitosamente!")
            return redirect(url_for('mostrar'))
        else:
            flash("Error al registrar los datos")

    return render_template('insertar.html')

#********Actualizar****************
@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    cursor.execute("select * from Usuario")
    mostrar = cursor.fetchall()

    if request.method == "POST":

        email = request.form['email']
        username = request.form['username']
        edad = request.form['edad']
        id = request.form['id']

        sql = "update Usuario set email = %s, username = %s, edad = %s where id = %s"
        values = (email, username, edad, id)

        cursor.execute(sql, values)
        if cursor.rowcount == 1:
            midb.commit()
            flash("Cambios realizados exitosamente!")
            return redirect(url_for('mostrar')) #redireccionar a la plantilla mostrar
        else:
            flash("Error al registrar los datos")

    return render_template('actualizar.html', mostrar_datos=mostrar)

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    if request.method == "POST":
        id = request.form['id']

        sql = "delete from Usuario where id = %s"
        values = (id,)
        cursor.execute(sql, values)

        if cursor.rowcount == 1:
            midb.commit()
            flash("Registro Eliminado Exitosamente")
            return redirect(url_for('mostrar'))
        else:
            flash("Error al registrar los datos")
    return render_template('eliminar.html')



@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == "POST":
        buscar = request.form['buscar']

        sql = "select * from Usuario where username = %s"
        values=(buscar, )

        cursor.execute(sql, values)

        registro = cursor.fetchone()

        if registro != None:
            flash("Usuario encontrado!")
            return render_template('buscar.html',registro=registro)
        else:
            flash("Usuario no encontrado")
            return render_template("mostrar.html")

          




#metodo principal
if __name__ == '__main__':
    app.run(debug=True, port=8000)
