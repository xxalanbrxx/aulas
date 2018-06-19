from tkinter import *
import sqlite3

connect = sqlite3.connect('cadastro.db')
c = connect.cursor()

def inserir():
    login = en1.get()
    senha = en2.get()
    sexo = en3.get()
    if len(login) > 10:
        lglb["bg"] = "red"
    else:
        lglb["bg"] = "green"
    if len(senha) > 8:
        sglb["bg"] = "red"
    else:
        sglb["bg"] = "green"
    if sexo != 'masculino' and sexo != 'feminino':
        sxlb["bg"] = "red"
    else:
        sxlb["bg"] = "green"
    if lglb["bg"] == "green" and sglb["bg"] == "green" and sxlb["bg"] == "green":
        try:
            c.execute('INSERT INTO menu VALUES(?, ?, ?)',(login, senha, sexo))
            connect.commit()
        except Exception as ei:
            print('ERRO: ',ei)
        else:
            print('INSERIDO COM SUCESSO!')

def db():
    
    try:
        c.execute('CREATE TABLE IF NOT EXISTS menu(login text, senha text, sexo text)')
    except Exception as e:
        print("ERRO: ",e)
    else:
        print('TABLE CRIADA!')


janela = Tk()
janela.geometry("200x100")
janela.title("CADASTRO")


en1 = Entry(janela)
en2 = Entry(janela, show="*")
en3 = Entry(janela)

lglb = Label(janela, text="LOGIN: ")
sglb = Label(janela, text="SENHA: ")
sxlb = Label(janela, text="SEXO:   ")

btconf = Button(janela, text="CONFIRMAR", command=inserir)

lglb.grid(row=0, column=0)
en1.grid(row=0, column=1)
sglb.grid(row=1, column=0)
en2.grid(row=1, column=1)
sxlb.grid(row=2, column=0)
en3.grid(row=2, column=1)
btconf.grid(row=3, column=1)

janela.mainloop()

