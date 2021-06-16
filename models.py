
class Livros:
    def __init__(self, livro, autor, editora, id):
        self.livro = livro
        self.autor = autor
        self.editora = editora
        self.id = id

class Usuario:
    def __init__(self, id, nome, senha) :
        self.id = id
        self.nome = nome
        self.senha = senha