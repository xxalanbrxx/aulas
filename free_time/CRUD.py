from tkinter import *
import sqlite3

wl = 10
we = 35

bg = "gray"
fg = "black"

c = sqlite3.connect("banco.db")
conn = c.cursor()



try:
    c.execute("""CREATE TABLE IF NOT EXISTS usuarios (id INT AUTO_INCREMENT, nome VARCHAR(20), user VARCHAR(15) UNIQUE NOT NULL, pass VARCHAR(50))""")
except:
	pass


# CLASSE TELA
class Menu(object):
    """docstring for Menu"""

    def __init__(self):
        self.menu = Tk()
        self.menu["bg"] = bg
        self.menu.resizable(False, False)
        self.menu.geometry("220x100")
        self.menu.title("Menu")

        self.lb_login = Label(self.menu, text="User: ", bg=bg, fg=fg)
        self.lb_senha = Label(self.menu, text="Pass: ", bg=bg, fg=fg)

        self.en_login = Entry(self.menu, width=25, bg=bg, fg=fg)
        self.en_senha = Entry(self.menu, width=25, show="*", bg=bg, fg=fg)

        self.bt_tela_login = Button(self.menu, text="CONECTAR", command=self.tela_Login, bg=bg, fg=fg)
        self.bt_tela_cadastro = Button(self.menu, text="CADASTRAR", command=self.tela_cadastro, bg=bg, fg=fg)

        self.lb_login.place(x=10, y=10)
        self.en_login.place(x=50, y=10)

        self.lb_senha.place(x=10, y=35)
        self.en_senha.place(x=50, y=35)

        self.bt_tela_login.place(x=20, y=70)
        self.bt_tela_cadastro.place(x=110, y=70)

        self.lb_erro1 = Label(self.menu, text="*", bg=bg, fg='black')
        self.lb_erro2 = Label(self.menu, text="*", bg=bg, fg='black')

    def __repr__(self):
        return '\n\n\nClasse -> {}\nCor -> {}\nTamanho -> {}'.format('Menu', bg, "300x300")

    def tela_Login(self):
        login = self.en_login.get().lower()
        senha = self.en_senha.get().lower()

        self.lb_erro2.place(x=205, y=35)
        if len(login) <= 5 or login == '':
            self.lb_erro1.place(x=205, y=10)
        else:
            self.lb_erro2.place(x=205, y=35)
            self.lb_erro1.place(x=99999999, y=9999999)

        g = c.execute("SELECT user,pass FROM usuarios WHERE `user`='{}' and `pass`='{}'".format(login, senha))

        for i in g:
            pass
        try:
            print(i[0], i[1])
        except:
            print('Não cadastrado.')
        else:
            if i[0].lower() == 'adminpanel' and i[1].lower() == senha:
                self.menu.destroy()
                Logado('Admin', cargo=1)

            elif i[0].lower() == login and i[1].lower() == senha:
                self.menu.destroy()
                Logado(login).run()


    def tela_cadastro(self):
        self.menu.destroy()
        Cadastrar().run()


    def run(self):
        self.menu.mainloop()


# CLASSE CADASTRAR

class Cadastrar():
    def __init__(self):
        self.cadastro = Tk()
        self.cadastro["bg"] = bg
        self.cadastro.geometry("300x150")
        self.cadastro.title("Cadastrar")
        self.cadastro.resizable(False, False)

        # LABELS
        self.lb_nome = Label(self.cadastro, text="Nome: ", bg=bg, fg=fg)
        self.lb_login = Label(self.cadastro, text="Login: ", bg=bg, fg=fg)
        self.lb_senha = Label(self.cadastro, text="Senha: ", bg=bg, fg=fg)
        self.lb_senha_conf = Label(self.cadastro, text="Confirm: ", bg=bg, fg=fg)

        self.lb_er1 = Label(self.cadastro, text="*", bg=bg, fg='black')
        self.lb_er2 = Label(self.cadastro, text="*", bg=bg, fg='black')
        self.lb_er3 = Label(self.cadastro, text="*", bg=bg, fg='black')

        # ENTRYS
        self.en_nome = Entry(self.cadastro, width=we, bg=bg, fg=fg)
        self.en_login = Entry(self.cadastro, width=we, bg=bg, fg=fg)
        self.en_senha = Entry(self.cadastro, show="*", width=we, bg=bg)
        self.en_senha_conf = Entry(self.cadastro, show="*", width=we, bg=bg)

        # BUTTONS
        self.bt_cadastrar = Button(self.cadastro, text="CONFIRMAR", bg=bg, width=10, command=self.confirmar)
        self.bt_cancelar = Button(self.cadastro, text="CANCELAR", bg=bg, width=10, command=self.cancelar)

        # PLACES
        self.lb_nome.place(x=10, y=10)
        self.en_nome.place(x=60, y=10)

        self.lb_login.place(x=10, y=35)
        self.en_login.place(x=60, y=35)

        self.lb_senha.place(x=10, y=60)
        self.en_senha.place(x=60, y=60)

        self.lb_senha_conf.place(x=10, y=85)
        self.en_senha_conf.place(x=60, y=85)

        self.bt_cadastrar.place(x=80, y=120)
        self.bt_cancelar.place(x=190, y=120)

    def __repr__(self):
        return '\n\n\nClasse -> {}\nCor -> {}\nTamanho -> {}'.format('Cadastrar', bg, "300x150")

    def confirmar(self):
        nome = self.en_nome.get()
        login = self.en_login.get()
        senha = self.en_senha.get()
        senhac = self.en_senha_conf.get()
        count = 0

        if len(nome) > 6 and len(nome) <= 20:
            count += 1
        else:
            self.lb_er1.place(x=275, y=10)

        if len(login) > 5 and len(login) <= 15:
            count += 1
        else:
            self.lb_er2.place(x=275, y=35)

        if len(senha) > 5 and len(senha) < 40 and senha == senhac:
            count += 1
        else:
            self.lb_er3.place(x=275, y=85)

        if count == 3:
            try:
                conn.execute(
                    """INSERT INTO usuarios(`nome`, `user`, `pass`) VALUES('{}','{}','{}')""".format(nome, login, senha))
                c.commit()
            except Exception as erro:
                print('ERRO: ', erro)
                self.lb_er2.place(x=275, y=35)
            else:
                self.cadastro.destroy()
                Menu().run()

    def cancelar(self):
        self.cadastro.destroy()
        Menu().run()

    def run(self):
        self.cadastro.mainloop()


# CLASSE LOGADO
class Logado():
    def __init__(self, user, cargo=0):
        self.logado = Tk()
        self.logado["bg"] = bg
        self.logado.geometry("300x300")
        self.logado.title("{} está Conectado.".format(user))
        self.logado.resizable(False, False)
        self.cargo = cargo

        self.player = user 
        self.LbPesq = Label(self.logado, text=" Pesquisar usuario ", width=20, bg=bg, fg=fg)
        self.EnPesq = Entry(self.logado, bg=bg, fg=fg, width=50)
        self.BtPesq = Button(self.logado, text="    PESQUISAR    ", width=10, bg=bg, fg=fg, command=self.pesq)

        self.LbNomeL = Label(self.logado, text="Nome", bg=bg, fg=fg)
        self.LbUserL = Label(self.logado, text="Usuario", bg=bg, fg=fg)
        self.LbPassL = Label(self.logado, text="Senha", bg=bg, fg=fg)

        self.lista = Listbox(self.logado, width=15, height=2, bg=bg, fg='black')
        self.lista1 = Listbox(self.logado, width=15, height=2, bg=bg, fg='black')
        self.lista2 = Listbox(self.logado, width=15, height=2, bg=bg, fg='black')

        self.limpar = Button(self.logado, text="     LIMPAR     ", bg=bg, fg=fg, command=self.clear)
        self.alterar = Button(self.logado, text="   ALTERAR   ", bg=bg, fg=fg, command=self.alterar)
        self.LbPesq.grid(column=0)
        self.EnPesq.grid(column=0)

        self.LbNomeL.place(x=27, y=40)
        self.LbUserL.place(x=127, y=40)
        self.LbPassL.place(x=227, y=40)

        self.lista.place(x=2, y=60)
        self.lista1.place(x=102, y=60)
        self.lista2.place(x=202, y=60)

        self.BtPesq.place(x=22, y=100)
        self.limpar.place(x=112, y=100)
        self.alterar.place(x=202, y=100)

        self.lb_nome_u = Label(self.logado, text="New Nome: ", bg=bg, fg=fg)
        self.lb_login_u = Label(self.logado, text="New Login: ", bg=bg, fg=fg)
        self.lb_senha_u = Label(self.logado, text="New Senha: ", bg=bg, fg=fg)
        self.lb_encon_u = Label(self.logado, text="", bg=bg, fg=fg)

        self.en_nome_u = Entry(self.logado, bg=bg, fg=fg)
        self.en_login_u = Entry(self.logado, bg=bg, fg=fg)
        self.en_senha_u = Entry(self.logado, bg=bg, fg=fg)
        self.lb_encon_u.place(x=10, y=200)

        self.bt_conf = Button(self.logado, text="confirmar", bg=bg, fg=fg, command=self.conf)
        self.bt_delet = Button(self.logado, text="   deletar  ", bg=bg, fg=fg, command=self.delet)

    def __repr__(self):
        return '\n\n\nClasse -> {}\nCor -> {}\nTamanho -> {}'.format('Logado', bg, "300x300")


    def sair(self):
    	self.logado.destroy()
    	Menu().run()

    def delet(self):
        if cargo == 1:
        	pass
        else:
        	print('Você não tem permissão.')

    def clear(self):
        self.lista.delete(0, END)
        self.lista1.delete(0, END)
        self.lista2.delete(0, END)

    def conf(self):
        pesq = self.EnPesq.get()
        nome = self.en_nome_u.get()
        login = self.en_login_u.get()
        senha = self.en_senha_u.get()
        if len(nome) > 5 and len(login) > 5 and len(senha) > 5:
            try:
                conn.execute(f"UPDATE usuarios SET `nome`='{nome}' WHERE `user`='{pesq}'")
                conn.execute(f"UPDATE usuarios SET `user`='{login}' WHERE `user`='{pesq}'")
                conn.execute(f"UPDATE usuarios SET `pass`='{senha}' WHERE `user`='{pesq}'")
                c.commit()

            except Exception as e:
                print(e)
            else:
                self.logado.destroy()
                Menu().run()


    def alterar(self):
        nome = self.EnPesq.get()
        inff = c.execute(f"""SELECT `user` FROM usuarios WHERE `user`='{nome}'""")
        try:
            for cada in inff:
                pass
            print(cada[0])
            g = 1
        except:
            g = 0
        if g == 1:
            self.lb_encon_u["text"] = f"Usuario '{nome}' encontrado."
            self.lb_encon_u["fg"] = "black"
            self.lb_nome_u.place(x=10, y=222)
            self.lb_login_u.place(x=10, y=242)
            self.lb_senha_u.place(x=10, y=262)

            self.en_nome_u.place(x=80, y=222)
            self.en_login_u.place(x=80, y=242)
            self.en_senha_u.place(x=80, y=262)
            self.bt_conf.place(x=222, y=255)
            self.bt_delet.place(x=222, y=220)
        else:
            self.lb_encon_u["fg"] = "black"
            self.lb_encon_u["text"] = f"Usuario '{nome}' não encontrado."
            self.lb_nome_u.place(x=99999, y=222)
            self.lb_login_u.place(x=99999, y=242)
            self.lb_senha_u.place(x=99999, y=262)

            self.en_nome_u.place(x=99999, y=222)
            self.en_login_u.place(x=99999, y=242)
            self.en_senha_u.place(x=99999, y=262)
            self.bt_conf.place(x=99999, y=255)
            self.bt_delet.place(x=99999,y=222)

    def pesq(self):
        nome = ''
        user = ''
        passw = ''

        nome = self.EnPesq.get()
        if self.cargo == 1:
            info = conn.execute("SELECT * FROM usuarios WHERE `user`='{}'".format(nome))  # ERRO NA PARTE DE IMPRIMRI
            for cadainf in info:
                self.lista.insert(END, cadainf[1])
                self.lista1.insert(END, cadainf[2])
                self.lista2.insert(END, cadainf[3])
        else:
            print('Você não tem permissão.')

    def run(self):
        self.logado.mainloop()

Menu().run()

