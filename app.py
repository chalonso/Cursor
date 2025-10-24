from tkinter import FALSE
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Lista de tarea en memoria
tareas = []

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    texto = request.form.get('tarea')
    if texto:
        nueva_tarea = {
            'id':len(tareas)+1,
            'texto': texto,
            'hecho': False
        }
        tareas.append(nueva_tarea)
    return redirect(url_for('index'))

@app.route('/completar/<int:id>')
def completar(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['hecho'] = True
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

