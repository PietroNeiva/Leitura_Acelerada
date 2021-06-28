from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
app = Flask(__name__)
app.secret_key = '1234'
from models import Livros, Usuario
import os
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
import PyPDF2
import time
import os

liv1 = Livros('Dom Casmurro', 'Machado de Assis', 'Editora Garnier', '0')
tela = [liv1]

usuario1 = Usuario('pietro', 'Pietro Nazar', '1234')

usuarios = {usuario1.id: usuario1}

@app.route("/")
# app.run(host='0.0.0.0', port=8080)
def index():
    return render_template('tela.html', titulo='Leitura Dinamica', livro=tela)


@app.route('/livros')
def livros():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('livros')))
    return render_template('cadastro.html', titulo='Cadastro de livros')


@app.route('/criar', methods=['POST', ])
def criar():
    id = 1
    arquivo = request.files['arquivo']
    nome = request.form['nome']
    autor = request.form['autor']
    editora = request.form['editora']
    if arquivo is not None:
        upload_path = app.config['UPLOAD_PATH']
        while os.path.exists(f'{upload_path}/livro{id}.pdf'):
            id = id+1

        arquivo.save(f'{upload_path}/livro{id}.pdf')
    else:
        flash('faltou arquivo!')
        return redirect(url_for('criar'))
    livro = Livros(nome, autor, editora, id)
    tela.append(livro)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/leitura/<int:id>')
def leitura(id):
    pdf_file = open(f'uploads/livro{id}.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file, strict=False)
    number_of_pages = read_pdf.getNumPages()
    page = read_pdf.getPage(0)
    page_content = page.extractText()
    parsed = ''.join(page_content)
    lista_de_palavras = parsed.split(" ")
    lista_de_palavras = [line.strip() for line in lista_de_palavras if line.strip() != ""]
    for palavra in lista_de_palavras:
        print(palavra)
        time.sleep(0)
    return render_template('leitura_dinamica.html', arquivo = lista_de_palavras)


if __name__ == "__main__":
    app.run(debug=True)

