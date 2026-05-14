from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('biblioteca.db')

conexao = sqlite3.connect('biblioteca.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    idade INT NOT NULL,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    data_cadastro DATE DEFAULT CURRENT_DATE
)
''')
conexao.commit()

try:
    cursor.execute('''
    INSERT INTO usuarios (id, idade, nome, email, data_cadastro)
    VALUES (?, ?, ?, ?, ?)
    ''', ('1', '17', 'Maria', 'maria32@gmail.com', '2026-05-05'))
    conexao.commit()
except sqlite3.IntegrityError:
    print("Aviso: Maria já está cadastrada.")

try:
    cursor.execute('''
    INSERT INTO usuarios (id, idade, nome, email, data_cadastro)
    VALUES (?, ?, ?, ?, ?)
    ''', ('2', '18', 'Pedro', 'Pedro45@gmail.com', '2026-03-07'))
    conexao.commit()
except sqlite3.IntegrityError:
    print("Aviso: Pedro já está cadastrado.")
    
    conexao.commit()
    print("Dados inseridos com sucesso!")
except sqlite3.IntegrityError:
    print("Aviso: Alguns dados já existem no cadastro (violação de UNIQUE).")

cursor.execute('UPDATE usuarios SET email= "pedro4321@gmail.com" WHERE id = 2')
conexao.commit()

cursor.execute('DELETE FROM usuarios WHERE id = 1')
conexao.commit()

print("\n--- LISTA DE USUARIOS ---")
cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall() 

for usuario in usuarios:
    id_usuario, idade, nome, email, data_cadastro = usuario
    print(f"ID: {id_usuario}")
    print(f"Nome: {nome}")
    print(f"Idade: {idade}")
    print(f"Email: {email}")
    print(f"Data_cadastro: {data_cadastro}")
    print("-" * 30)

cursor.close()
conexao.close()

@app.route('/')
def index():
    v_conexao = conectar() 
    v_cursor = v_conexao.cursor()
    v_cursor.execute('SELECT id, idade, nome, email, data_cadastro FROM usuarios')
    usuarios_lista = v_cursor.fetchall()
    v_conexao.close()

    return render_template('index.html', usuarios=usuarios_lista)

if __name__ == '__main__':
    app.run(debug=True)