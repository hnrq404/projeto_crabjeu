import flet as ft
from flet import AppBar,Page, Text, View, colors,Theme
import sqlite3
import datetime
import speech_recognition as sr
import time

banco=sqlite3.connect("caranguejo.db",check_same_thread=False)

cursor = banco.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS usuarios3 (usuario text,senha text,level integer,pontuaçao integer,data text,consecutivos integer)')
def main(page: Page):
    
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }
    page.theme = Theme(font_family="Kanit")
    consulta = cursor.execute("SELECT * FROM usuarios3")
    consulta = consulta.fetchall()
    text_consecutivos = ft.Text("0",size=30)
    text_mudar_usuario = ft.TextField(label = "Novo nome de usuário...",width=400,color=ft.colors.BLACK,border_color=ft.colors.BLACK)
    botao_fechar_configuracoes = ft.IconButton(ft.icons.CLOSE)
    botao_novo_usuario = ft.ElevatedButton("CONFIRMAR",width=200)
    c = ft.Container(
        content= ft.Column([ft.Row([ft.Container(botao_fechar_configuracoes,alignment=ft.alignment.top_right,width=700)]),ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                tab_content=ft.Text("                    MUDAR NOME DE USUÁRIO                    ",color=ft.colors.BLACK),
                content=ft.Container(alignment=ft.alignment.top_left,content=ft.Column([text_mudar_usuario,botao_novo_usuario]),margin=ft.margin.only(top=20))
            ),
            ft.Tab(
                tab_content=ft.Text("                    MUDAR SENHA                    ",color=ft.colors.BLACK),
                content=ft.Column([
                    ft.Container(alignment=ft.alignment.top_left,content=ft.TextField(label = "Nova senha...",width=400),margin=ft.margin.only(top=20)),
                    ft.Container(alignment=ft.alignment.top_left,content=ft.TextField(label ="Confirmar nova senha...",width=400))
                    ])
            ),
        ],
        expand=1,
        divider_color=ft.colors.BLACK45,
    )]),
        width=700,
        height=0,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
        alignment=ft.alignment.bottom_right,
        padding=ft.padding.only(top=0),
        bgcolor=ft.colors.AMBER_50,
        border=ft.border.all(2,color=ft.colors.BLACK),
        border_radius=20
    )
    page.window_full_screen = True
    page.padding = 0
    page.title = "Routes Example"
    text_username: ft.TextField = ft.TextField(label="Usuário",text_align=ft.TextAlign.LEFT,width=200,label_style=ft.TextStyle(color="#E77A52"))
    text_password: ft.TextField = ft.TextField(label="Senha",text_align=ft.TextAlign.LEFT,width=200,password=True,label_style=ft.TextStyle(color="#E77A52"),can_reveal_password=True)
    button_submit: ft.ElevatedButton = ft.ElevatedButton(text="ENTRAR",width=200,color="white",bgcolor="#E77A52",style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),))
    
    botao_cadastro = ft.ElevatedButton(text="Cadastre-se",width=150,color="white",bgcolor="#C1846F",style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),))
    text_confirmar_senha: ft.TextField = ft.TextField(label="Confirmar senha",text_align=ft.TextAlign.LEFT,width=200,password=True)
    button_registrar: ft.ElevatedButton = ft.ElevatedButton(text="REGISTRAR",width=200,color=colors.ORANGE_500)
    texto_ser_falado = ft.TextField(value=" ", text_align=ft.TextAlign.RIGHT, width=400)
    texto_certo_errado = ft.TextField(value=" ", text_align=ft.TextAlign.RIGHT, width=400)
    texto_erro = ft.Text(value="",color=ft.colors.RED_500)
    texto_acerto = ft.Text(value="",color=ft.colors.GREEN_500)
    progresso = ft.Slider(width=400,max=300)
    texto_pontuacao = ft.Text("0",size=30)
    text_level = ft.Text("0",size=30)
    text_nome_usuario = ft.Text("",size=30)
    text_indice = ft.Text("0")
    level = ft.Text("0",size=30)
    pontuacao = ft.Text("0",size=30)
    def update_task(e):
        consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_mudar_usuario.value,))
        sql = ''' UPDATE usuarios3
                SET usuario = ?
                WHERE usuario = ?'''
        cur = banco.cursor()
        res = consulta.fetchall()
        if len(res) == 0 and text_mudar_usuario.value != "":
            cur.execute(sql, (text_mudar_usuario.value,text_nome_usuario.value))
            banco.commit()
            text_mudar_usuario.value = ""
            page.update()
    botao_novo_usuario.on_click = update_task
    def progressoslider(e):
        progresso.value = texto_pontuacao.value
        page.update()
    def registrar_conta(e):
        consulta_usuarios = cursor.execute("SELECT usuario FROM usuarios3 WHERE usuario=?",(text_username.value,))
        res = consulta_usuarios.fetchall()
        if text_username.value != '' and text_password.value != '':
            if len(res) > 0:
                texto_erro.value = "Usuario já cadastrado"
                page.update()
            elif len(str(text_password.value)) < 5 or " " in str(text_password.value):
                texto_erro.value = "Digite uma senha com 5 dígitos ou mais e sem espaços em branco"
                page.update()
            elif text_password.value != text_confirmar_senha.value:
                texto_erro.value =  "Senhas não estão batendo"
                page.update()
            else:
                cursor.execute("INSERT INTO usuarios3(usuario,senha,level,pontuaçao,data,consecutivos) VALUES (?,?,?,?,?,?)",(str(text_username.value),str(text_password.value),1,0,str(datetime.date.today()),0))
                banco.commit()
                texto_erro.value = ""
                texto_acerto.value = "Usuario cadastrado com sucesso,volte para o início para JOGAR!!"
                text_confirmar_senha.value = ''
                text_username.value = ''
                text_password.value = ''
                page.update()
                time.sleep(5)
                texto_acerto.value = ""   
        else:
            texto_erro.value = "Preencha todos os campos"
            page.update()
    def button_clicked(e):
            teste = "criança aprendendo a ler"
            texto_ser_falado.value = f"Diga {teste}"
            texto_certo_errado.value = ""
            page.update()
            r = sr.Recognizer()
            try:
                with sr.Microphone() as fonte:
                        page.update()
                        r.adjust_for_ambient_noise(fonte,)
                        audio = r.listen(fonte, phrase_time_limit=3)
                        texto = r.recognize_google(audio, language="pt-BR")
                if texto.lower() == teste:
                    texto_certo_errado.value = "ACERTOU!!"
                    page.update()
                    
                    page.update()
                else:
                    texto_certo_errado.value = "ERROU!!!"
                    page.update()
            except:
                    texto_certo_errado.value = "não foi possível compreender o áudio"
                    page.update()
            page.update()
    button_registrar.on_click = registrar_conta
    def jogando(e):
        consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
        res = consulta.fetchall()
        if int(level.value) == 1:
            if (int(pontuacao.value) >= 300 and int(pontuacao.value) < 600):
                consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
                res = consulta.fetchall()
                cursor.execute("UPDATE usuarios3 SET pontuaçao = ? WHERE usuario = ?",(int(int(pontuacao.value)+100),str(text_username.value)))
                cursor.execute("UPDATE usuarios3 SET level = ? WHERE usuario = ?",(2,str(text_username.value)))
                pontuacao.value = str(int(pontuacao.value) + 100)
                progresso.value = str(int(pontuacao.value)-300)
                texto_pontuacao.value = str(f"Pontuação: {pontuacao.value}")
                level.value = "2"
                text_level.value = f"Level: {level.value}"
                page.go("/jogar")
                banco.commit()
            else:
                cursor.execute("UPDATE usuarios3 SET pontuaçao = ? WHERE usuario = ?",(int(int(pontuacao.value)+100),str(text_username.value)))
                pontuacao.value = str(int(pontuacao.value) + 100)
                progresso.value = pontuacao.value
                banco.commit()
        if int(level.value) == 2:
                if int(pontuacao.value) >= 600:
                    cursor.execute("UPDATE usuarios3 SET pontuaçao = ? WHERE usuario = ?",(int(int(pontuacao.value)+100),str(text_username.value)))
                    cursor.execute("UPDATE usuarios3 SET level = ? WHERE usuario = ?",(3,str(text_username.value)))
                    pontuacao.value = str(int(pontuacao.value) + 100)
                    texto_pontuacao.value = str(f"Pontuação: {pontuacao.value}")
                    progresso.value = str(int(pontuacao.value)-600)
                    level.value = "3"
                    text_level.value = f"Level: {level.value}"
                    page.go("/jogar")
                    banco.commit()
                else:
                    cursor.execute("UPDATE usuarios3 SET pontuaçao = ? WHERE usuario = ?",(int(int(pontuacao.value)+100),str(text_username.value)))
                    pontuacao.value = str(int(pontuacao.value) + 100)
                    progresso.value = pontuacao.value
                    banco.commit()
        consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
        res = consulta.fetchall()
        data = res[0][4]
        string = data.split("-")
        ano = int(string[0])
        mes = int(string[1])
        dia = int(string[2])
        print(res[0][5])
        if datetime.date.today() - datetime.timedelta(days=1) == datetime.date(ano,mes,dia):
                    sql = ''' UPDATE usuarios3
                SET consecutivos = ?
                WHERE usuario = ?'''
                    consecutivos = int(res[0][5])
                    text_consecutivos.value = f"Dias seguidos:{consecutivos + 1}"
                    cursor.execute(sql,(consecutivos + 1,str(text_username.value)))
                    banco.commit()
        elif datetime.date.today() == datetime.date(ano,mes,dia):
                    consecutivos = int(res[0][5])
                    cursor.execute("UPDATE usuarios3 SET consecutivos = ? WHERE usuario = ?",(consecutivos,str(text_username.value)))
                    banco.commit()
        else:
                    cursor.execute("UPDATE usuarios3 SET consecutivos = ? WHERE usuario = ?",(0,str(text_username.value)))
                    banco.commit()
        cursor.execute("UPDATE usuarios3 SET data = ? WHERE usuario = ?",(str(datetime.date.today()),str(text_username.value)))
        banco.commit()
        page.update()
    
    def jogar(e):
        consulta_usuarios = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
        res = consulta_usuarios.fetchall()
        data = res[0][4]
        string = data.split("-")
        ano = int(string[0])
        mes = int(string[1])
        dia = int(string[2])
        if datetime.date.today() - datetime.timedelta(days=1) > datetime.date(ano,mes,dia):
            cursor.execute("UPDATE usuarios3 SET consecutivos = ? WHERE usuario = ?",(0,str(text_username.value)))
            banco.commit()
        contagem = len(res)
        if len(res) > 0:
            progresso.value = str(res[contagem-1][3])
            texto_pontuacao.value = f"Pontuação: {str(res[contagem-1][3])}"
            text_level.value = f"Level: {res[contagem-1][2]}"
            text_consecutivos.value = f"Dias seguidos: {res[0][5]}"
            text_nome_usuario.value = text_username.value
        if len(res) > 0:
            jogador = str(res[0][1])
            if str(jogador) == str(text_password.value):
                page.go("/jogar")
                page.update()
    def ir_para_jogando(e):
        consulta_usuarios = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_nome_usuario.value,))
        res = consulta_usuarios.fetchall()
        contagem = len(res)
        progresso.value = str(texto_pontuacao.value)[11:]
        pontuacao.value = str(texto_pontuacao.value)[11:]
        level.value = str(text_level.value)[7:]
        
        page.update()
        page.go("/jogando")
    def fechar(e):
        page.window_close()
    botao_sidebar = ft.IconButton(ft.icons.MENU)
    button_submit.on_click = jogar
    principal = View(
                "/",
                [
                    AppBar(title=Text("ÍNICIO"), bgcolor=colors.ORANGE_500),
                    ft.Container(
            content=ft.ElevatedButton("ENTRAR",width=200,on_click=lambda _: page.go("/store"),color=colors.ORANGE_500),
            padding=5,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=200,left=500),
            width=200
        ),
        ft.Container(
            content=ft.ElevatedButton(
                "REGISTRAR",
                width=200,on_click=lambda _: page.go("/registrar"),color=colors.ORANGE_500
            ),
            padding=5,
            alignment=ft.alignment.center,
            width=200,
            margin=ft.margin.only(left=500)
        ),

        ft.Container(
            content=ft.ElevatedButton("SAIR",width=200,on_click=fechar,color=colors.ORANGE_500),
            padding=5,
            alignment=ft.alignment.center,
            width=200,
            margin=ft.margin.only(left=500)
        ),
                ]
            )
    login = View(
                    "/store",
                    [
                        ft.Container(ft.Stack([
                            ft.Image(
                src="Home Screan (3).png",
                fit="cover",
            ),
                        ft.Container(
                            content=ft.Column([
                                ft.Container(ft.Image(
                                                src=f"MicrosoftTeams-image__1_-removebg-preview.png",
                                                width=300,
                                                height=200,
                                                fit=ft.ImageFit.CONTAIN,
                                                )
                                     ,alignment=ft.alignment.center,width=300),
                                ft.Container(text_username,alignment=ft.alignment.center,width=300),
                        ft.Container(text_password,alignment=ft.alignment.center,width=300),
                        ft.Container(button_submit,alignment=ft.alignment.center,width=300),
                        ft.Container(botao_cadastro,alignment=ft.alignment.center,width=220,margin=ft.margin.only(bottom=30,left=(300-220)/2),
                                     opacity=1),
                    ],
                                              ft.MainAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.WHITE,width=600,
                            margin=ft.margin.only(top=(page.window_height-400)/2,left=(page.window_width-400)/2,bottom=(page.window_height-200)/2,right=(page.window_width-400)/2),
                            opacity=1,
                            border=ft.border.all(3,color="#E77A52"),
                            border_radius=10)]))
                                ]
                        
                )
    login.padding = 0
    opcoes_icones = [ft.Icon(ft.icons.HOME),ft.Icon(ft.icons.ABC),ft.Icon(ft.icons.MONEY_ROUNDED)]
    def animate_container(e):
        c.height = 400
        c.margin = ft.margin.only(top=130,bottom=200,left=300)
        c.update()
        page.update()
    def fechar_configuracoes(e):
        c.height = 0
        c.margin = ft.margin.only(top=0,bottom=0,left=0)
        c.update()
        page.update()
    botao_fechar_configuracoes.on_click = fechar_configuracoes
    principal_jogo = View(
                    "/jogar",
                    [
                        AppBar(title=Text(""), bgcolor=colors.ORANGE_500,actions=[ft.IconButton(ft.icons.CONSTRUCTION_SHARP,tooltip="Configurações",on_click=animate_container)]),
                        c,
                ft.Row([
                    ft.CircleAvatar(content=opcoes_icones[0]),
                    ft.Container(
                    content=text_nome_usuario,
                    margin=ft.margin.only(right=10,bottom=0),
                    padding=10,
                    alignment=ft.alignment.bottom_left,
                    width=200,
                    height=60,
                ),
                    ]),
                ft.Column([
                    ft.Row([
                        ft.Container(ft.Image('—Pngtree—transmission tower_744594.png',height=80,fit=ft.ImageFit.CONTAIN),margin=ft.margin.only(right=-50,left=-30)),
                ft.Container(
                    content=text_level,
                    margin=ft.margin.only(left=0,right=10,top=50),
                    padding=10,
                    alignment=ft.alignment.bottom_left,
                    width=200,
                    height=60,
                )]),
               ft.Row([
                        ft.Container(ft.Image('fogo-fotor-bg-remover-2024041415114.png',height=50,fit=ft.ImageFit.CONTAIN),margin=ft.margin.only(right=-30,bottom=30,left=-10)),
                ft.Container(
                    content=texto_pontuacao,
                    margin=ft.margin.only(left=0,right=10,top=0),
                    padding=10,
                    alignment=ft.alignment.center_left,
                    width=500,
                    height=60,
                )]),
                ft.Container(
                    content=text_consecutivos,
                    margin=ft.margin.only(right=10,top=0),
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLUE_50,
                    width=500,
                    height=60,
                    border_radius=10,
                    border=ft.border.all(3, ft.colors.BLACK)),
                
                
                ]),
                ft.Row([ft.ElevatedButton("JOGAR",on_click=ir_para_jogando)])
                    ],
                    
                    
                )
    registrar =  View(
                    "/registrar",
                    [
                        AppBar(title=Text("REGISTRAR"), bgcolor=colors.ORANGE_500),
                        ft.Container(text_username,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500,top=200)),
                        ft.Container(text_password,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500)),
                        ft.Container(text_confirmar_senha,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500)),
                        ft.Container(button_registrar,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500)),
                        ft.Container(texto_erro,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500)),
                        ft.Container(texto_acerto,alignment=ft.alignment.center,width=300,margin=ft.margin.only(left=500))
                    ]
                )
    jogando_jogo = View(
                    "/jogando",
                    [
                        AppBar(title=Text("JOGO"), bgcolor=colors.ORANGE_500),
                        progresso,
                        ft.Row([
                        ft.Container(
                    ft.IconButton(ft.icons.PLAY_ARROW,on_click=jogando)
                    
                ),
                        ft.Container(
                            content=pontuacao
                        ),
                        ft.Container(content=level)])
                    ]
                )
    def route_change(e):
        page.views.clear()

        page.views.append(
            principal
        )
        if page.route == "/store":
            login.vertical_alignment = ft.MainAxisAlignment.CENTER
            login.horizontal_alignment =ft.CrossAxisAlignment.CENTER
            page.update()
            page.views.append(
                login
            )
        if page.route == "/jogar":
            consulta_usuarios = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_nome_usuario.value,))
            res = consulta_usuarios.fetchall()
            print(res)
            pontuacoes = res[0][3]
            levels = res[0][2]
            texto_pontuacao.value = f"Pontuação: {pontuacoes}"
            text_level.value = f"Level: {levels}"
            text_level
            page.update()
            page.views.append(
                principal_jogo
            )
        if page.route == "/registrar":
            page.views.append(
                registrar
            )
        progresso.on_change = progressoslider
        if page.route == "/jogando":
            page.update()
            page.views.append(
                jogando_jogo
            )
    
        page.update()
    page.on_route_change = route_change
    page.go(page.route)
ft.app(main)