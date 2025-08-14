from flask import Flask, render_template

import mysql.connector 

class usuario():
    def __init__(self,id,endereco,email,senha,nascimento,genero):
        self.id=id
        self.endereco = endereco
        self.email = email
        self.senha = senha 
        self.genero = genero
        self.nascimento=nascimento
    

class aluno (usuario):
    def __init__ (self,Curso):
        self.Curso=Curso

class professor(usuario):
    

class administrador(usuario):


class Relatorio:
    def __init__(self, aluno.id):


class curso: 