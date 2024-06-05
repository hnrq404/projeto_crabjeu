import flet as ft
from flet import Page,View,Theme
import sqlite3
import datetime
import speech_recognition as sr
import time
import random
import pyttsx3

banco=sqlite3.connect("caranguejo4.db",check_same_thread=False)
banco_questoes = sqlite3.connect("questoes.db",check_same_thread=False)
cursor_questoes = banco_questoes.cursor()
cursor = banco.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS usuarios5 (usuario text,senha text,level integer,data text,consecutivos integer,exp integer,icone text,pontos_nivel int)')
def main(page: Page):
    botao_confirmar_icone = ft.ElevatedButton(content=ft.Text("Confirmar",size=20),width=200,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20),))
    icone_usuario_jogando = ft.Image("./assets/carangueijo_sem_fundo.png",width=400,height=130)
    exp_value = ft.Text("0")
    icone_usuario = ft.Image("./assets/carangueijo_sem_fundo.png",height=120,width=80)
    texto_falado_indice = ft.Text("0")
    texto_pontuacao_soma = ft.Text("0")
    texto_pergunta = ft.Text("Questão 1/6",size=50,color="black",weight=ft.FontWeight.BOLD)
    texto_a_ser_falado = ft.Text("BONJOUR PRINCESSE FUDIDA ARROMBADA DO KRAI",size=25,color="white",weight=ft.FontWeight.BOLD)
    text_valor_clickado = ft.Text("0")
    def a_clicked(e):
        text_valor_clickado.value = "0"
        botao_alternativa_A.bgcolor = "orange"
        botao_alternativa_B.bgcolor = "white"
        botao_alternativa_C.bgcolor = "white"
        botao_alternativa_D.bgcolor = "white"
        page.update()
    def b_clicked(e):
        text_valor_clickado.value = "1"
        botao_alternativa_A.bgcolor = "white"
        botao_alternativa_B.bgcolor = "orange"
        botao_alternativa_C.bgcolor = "white"
        botao_alternativa_D.bgcolor = "white"
        page.update()
    def c_clicked(e):
        text_valor_clickado.value = "2"
        botao_alternativa_A.bgcolor = "white"
        botao_alternativa_B.bgcolor = "white"
        botao_alternativa_C.bgcolor = "orange"
        botao_alternativa_D.bgcolor = "white"
        page.update()
    def d_clicked(e):
        text_valor_clickado.value = "3"
        botao_alternativa_A.bgcolor = "white"
        botao_alternativa_B.bgcolor = "white"
        botao_alternativa_C.bgcolor = "white"
        botao_alternativa_D.bgcolor = "orange"
        page.update()
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
    def fechar_alerta_registro(e):
        erro_registro.open = False
        page.update()
    def voltar_pagina_usuario(e):
        errou_audio.open = False
        page.update()
        texto_pergunta.value = 'Questão 1/6'
        page.go("/jogar")
    botao_falar = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="Aperte quando estiver pronto", size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=350,
            height=60
        )
    
    botao_alternativa_A = ft.ElevatedButton(content=ft.Text("a) Bom dia princesa",size=20),width=500,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20)))
    botao_alternativa_B = ft.ElevatedButton(content=ft.Text("b) Bom dia princesa",size=20),width=500,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20),))
    botao_alternativa_C = ft.ElevatedButton(content=ft.Text("c) Bom dia princesa",size=20),width=500,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20),))
    botao_alternativa_D = ft.ElevatedButton(content=ft.Text("d) Bom dia princesa",size=20),width=500,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20),))
    botao_alternativa_A.on_click = a_clicked
    botao_alternativa_B.on_click = b_clicked
    botao_alternativa_C.on_click = c_clicked
    botao_alternativa_D.on_click = d_clicked
    botao_confirmar_alternativa = ft.ElevatedButton(content=ft.Text("CONFIRMAR",size=20),width=200,height=50,color="black",bgcolor="white",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=20)))
    container_botao_falar = ft.Container(
                                        botao_falar,
                                        alignment=ft.alignment.center,
                                        margin=ft.margin.only(top=50),
                                    )
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Tem certeza que deseja voltar?"),
        content=ft.Text("Todo progresso até aqui será perdido!!"),
        actions=[
            ft.TextButton("SIM", on_click=voltar_pagina_usuario),
            ft.TextButton("NÃO", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    def ir_para_proxima_questao(e):
        consulta = cursor_questoes.execute("SELECT * FROM questoes4 WHERE frances=?",(texto_a_ser_falado.value,))
        res = consulta.fetchall()
        botao_alternativa_A.content = ft.Text(res[0][1])
        botao_alternativa_B.content = ft.Text(res[0][2])
        botao_alternativa_C.content = ft.Text(res[0][3])
        botao_alternativa_D.content = ft.Text(res[0][4])
        if texto_pergunta.value != "Questão 6/6":
            texto_pergunta.value = f"Questão {int(texto_pergunta.value[8])+1}/6"
        page.go("/jogando_alternativa")
    def fechar_erro_audio(e):
        consulta = cursor_questoes.execute("SELECT * FROM questoes4 WHERE frances=?",(texto_a_ser_falado.value,))
        res = consulta.fetchall()
        botao_alternativa_A.content = ft.Text(res[0][1])
        botao_alternativa_B.content = ft.Text(res[0][2])
        botao_alternativa_C.content = ft.Text(res[0][3])
        botao_alternativa_D.content = ft.Text(res[0][4])
        if texto_pergunta.value != "Questão 6/6":
            texto_pergunta.value = f"Questão {int(texto_pergunta.value[8])+1}/6"
        page.go("/jogando_alternativa")
        """page.dialog = errou_audio
        errou_audio.open = False
        container_botao_falar.height = 60
        container_texto_falado.height = 0
        page.go("/jogando_alternativa")"""
        page.update()
    errou_audio = ft.AlertDialog(
        modal=True,
        title=ft.Text("Não foi possível compreender o áudio"),
        content=ft.Text("Tente novamente"),
        actions=[
            ft.TextButton("Ok", on_click=fechar_erro_audio),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    errou_questão = ft.AlertDialog(
        modal=True,
        title=ft.Text("Você errou!!"),
        content=ft.Text("Você falou Bonjour princess"),
        actions=[
            ft.TextButton("Próxima Questão", on_click=ir_para_proxima_questao),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    def ir_para_tela_de_login(e):
        page.go("/jogar")
    def fechar_campo(e):
        
            errou_questão.open = False
            container_texto_falado.height = 0
            botao_falar.height = 60
            container_botao_falar.height = 60
            texto = random.randint(0,4)
            texto_falado_indice.value = str(texto)
            consulta = cursor_questoes.execute('SELECT * FROM questoes4')
            res = consulta.fetchall()
            texto_questao = res[texto][0]
            texto_a_ser_falado.value = texto_questao
            page.update()
            page.go("/jogando")
            page.update()
        
            
    def finalizou_jogo(e):
        consulta = cursor.execute("SELECT * FROM usuarios5 WHERE usuario = ?",(text_nome_usuario.value,))
        res = consulta.fetchall()
        exp_value.value = str(int(exp_value.value)+ int(texto_pontuacao_soma.value))
        print(exp_value.value)
        print(res[0][7])
        if int(exp_value.value) >= int(res[0][7]):
            print(int(exp_value.value) - int(res[0][7]))
            exp_value.value = str(int(exp_value.value) - int(res[0][7]))
            
            text_level.value = f"Level {int(text_level.value[6:])+1}"
            print(text_level.value[6:])
            cursor.execute("UPDATE usuarios5 SET pontos_nivel = ? WHERE usuario = ?",(int(res[0][7])+(int(text_level.value[6:])-1)*10,text_nome_usuario.value))
            banco.commit()
        consulta = cursor.execute("SELECT * FROM usuarios5 WHERE usuario = ?",(text_nome_usuario.value,))
        res = consulta.fetchall()
        texto_exp.value = f"{exp_value.value}/{int(res[0][7])}"
        progressobar.value = int(exp_value.value)/int(res[0][7])
        texto_pontuacao_soma.value = "0"
        print(progressobar.value)
        cursor.execute("UPDATE usuarios5 SET exp = ? WHERE usuario = ?",(exp_value.value,text_nome_usuario.value))
        cursor.execute("UPDATE usuarios5 SET level = ? WHERE usuario = ?",(text_level.value[6],text_nome_usuario.value))
        page.go("/jogar")
        print(res)
        banco.commit()
    def confirmou_alternativa(e):
        consulta = cursor_questoes.execute("SELECT * FROM questoes4 WHERE frances=?",(texto_a_ser_falado.value,))
        res = consulta.fetchall()
        if texto_pergunta.value != "Questão 6/6":
            texto_pergunta.value = f"Questão {int(texto_pergunta.value[8])+1}/6"
            if int(text_valor_clickado.value) == res[0][5]:
                page.dialog = errou_questão
                errou_questão.title = ft.Text("Parabéns você acertou")
                errou_questão.content = ft.Text("")
                errou_questão.actions = [ft.TextButton("Próxima questão",on_click=fechar_campo)]
                errou_questão.open = True
                texto_pontuacao_soma.value = str(int(texto_pontuacao_soma.value) + 30)
                page.update()
                
            else:
                page.dialog = errou_questão
                errou_questão.title = ft.Text("Você errou")
                errou_questão.content = ft.Text("")
                errou_questão.actions = [ft.TextButton("Próxima questão",on_click=fechar_campo)]
                errou_questão.open = True
        else:
            if int(text_valor_clickado.value) == res[0][5]:
                texto_pontuacao_soma.value = str(int(texto_pontuacao_soma.value) + 30)
            page.dialog = errou_questão
            errou_questão.open = True
            errou_questão.title = ft.Row([ft.Text(f"Parabéns você ganhou {texto_pontuacao_soma.value}"),ft.Icon(ft.icons.STAR_PURPLE500,color="yellow"),ft.Text("!!")])
            errou_questão.content = ft.Text("")
            errou_questão.actions = [
                ft.TextButton("Sair",on_click=finalizou_jogo)
            ]
        botao_alternativa_A.bgcolor = "white"
        botao_alternativa_B.bgcolor = "white"
        botao_alternativa_C.bgcolor = "white"
        botao_alternativa_D.bgcolor = "white"
        page.update()
    botao_confirmar_alternativa.on_click = confirmou_alternativa
    erro_registro = ft.AlertDialog(
        modal=True,
        title=ft.Text("Preencha todos os campos!!!"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("OK", on_click=fechar_alerta_registro),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_dlg_modal(e):
        errou_audio.open = False
        botao_falar.height = 60
        container_contagem.height = 0
        container_texto_falado.height = 0
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
    botao_clicavel_jogando = ft.ElevatedButton("",opacity=0)
    botao_voltar_jogando = ft.Stack([
        ft.Image("Vector-removebg-preview.png",width=50,color="black"),
        botao_clicavel_jogando
    
    ])
    def triunfo(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "#eaf571"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/arco-do-triunfo.png"
        icone_usuario_jogando.src = "./assets/arco-do-triunfo.png"
        icone_usuario.height = 120
        icone_usuario.width = 80
        page.update()
    botao_icone_triunfo = ft.ElevatedButton("",opacity=0,on_click=triunfo,height=100,width=100)
    icone_arco_triunfo = ft.Container(ft.Stack([
        ft.Image("./assets/arco-do-triunfo.png",width=100),
        botao_icone_triunfo
    
    ]),border_radius=30)
    def bandeira_brasil(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "#eaf571"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/bandeira_brasil.png"
        icone_usuario_jogando.src = "./assets/bandeira_brasil.png"
        page.update()
    botao_bandeira_brasil = ft.ElevatedButton("",opacity=0,on_click=bandeira_brasil,height=100,width=100)
    icone_bandeira_brasil = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/bandeira_brasil.png",width=100,height=50),margin=ft.margin.only(top=25)),
        botao_bandeira_brasil
    
    ]),border_radius=30,alignment=ft.alignment.center)
    def bandeira_frança(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "#eaf571"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/bandeira_frança.png"
        icone_usuario_jogando.src = "./assets/bandeira_frança.png"
        page.update()
    botao_bandeira_frança = ft.ElevatedButton("",opacity=0,on_click=bandeira_frança,height=100,width=100)
    icone_bandeira_frança = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/bandeira_frança.png",width=100),margin=ft.margin.only(top=15)),
        botao_bandeira_frança
    
    ]),border_radius=30)
    def bola_francesa(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "#eaf571"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/bola_francesa.png"
        icone_usuario_jogando.src = "./assets/bola_francesa.png"
        page.update()
    botao_bola_francesa = ft.ElevatedButton("",opacity=0,on_click=bola_francesa,height=100,width=100)
    icone_bola_francesa = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/bola_francesa.png",width=100),margin=ft.margin.only(top=20)),
        botao_bola_francesa
    
    ]),border_radius=30)
    def padrao(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "#eaf571"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/carangueijo_sem_fundo.png"
        icone_usuario_jogando.src = "./assets/carangueijo_sem_fundo.png"
        page.update()
    botao_padrao = ft.ElevatedButton("",opacity=0,on_click=padrao,height=100,width=100)
    icone_padrao = ft.Container(ft.Stack([
        ft.Image("./assets/carangueijo_sem_fundo.png",width=100),
        botao_padrao
    
    ]),border_radius=30)
    def caranguejo_estressado(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "#eaf571"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/caranguejo-puto.png"
        icone_usuario_jogando.src = "./assets/caranguejo-puto.png"
        page.update()
    botao_caranguejo_estressado = ft.ElevatedButton("",opacity=0,on_click=caranguejo_estressado,height=100,width=100)
    icone_caranguejo_estressado = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/caranguejo-puto.png",width=100),margin=ft.margin.only(top=15)),
        botao_caranguejo_estressado
    
    ]),border_radius=30)
    def coelho(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "#eaf571"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/coelho fofinho.png"
        icone_usuario_jogando.src = "./assets/coelho fofinho.png"
        page.update()
    botao_coelho = ft.ElevatedButton("",opacity=0,on_click=coelho,height=100,width=100)
    icone_coelho = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/coelho fofinho.png",width=100),margin=ft.margin.only(top=15)),
        botao_coelho
    
    ]),border_radius=30)
    def dinossauro_verde(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "#eaf571"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/dinossauro-verde.png"
        icone_usuario_jogando.src = "./assets/dinossauro-verde.png"
        page.update()
    botao_dinossauro_verde = ft.ElevatedButton("",opacity=0,on_click=dinossauro_verde,height=100,width=100)
    icone_dinossauro_verde = ft.Container(ft.Stack([
        ft.Image("./assets/dinossauro-verde.png",width=100),
        botao_dinossauro_verde
    
    ]),border_radius=30)
    def dinossauro_laranja(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "#eaf571"
        icone_dinossauro_verde.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/dinossauro_laranja.png"
        icone_usuario_jogando.src = "./assets/dinossauro_laranja.png"
        page.update()
    botao_dinossauro_laranja = ft.ElevatedButton("",opacity=0,on_click=dinossauro_laranja,height=100,width=100)
    icone_dinossauro_laranja = ft.Container(ft.Stack([
        ft.Image("./assets/dinossauro_laranja.png",width=100),
        botao_dinossauro_laranja
    
    ]),border_radius=30)
    def leao(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "#eaf571"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/leão-pixelart.png"
        page.update()
    botao_leao = ft.ElevatedButton("",opacity=0,on_click=leao,height=100,width=100)
    icone_leao = ft.Container(ft.Stack([
        ft.Image("./assets/leão-pixelart.png",width=100),
        botao_leao
    
    ]),border_radius=30)
    def maça(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "#eaf571"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/maça.png"
        icone_usuario_jogando.src = "./assets/maça.png"
        page.update()
    botao_maça = ft.ElevatedButton("",opacity=0,on_click=maça,height=100,width=100)
    icone_maça = ft.Container(ft.Stack([
        ft.Image("./assets/maça.png",width=100),
        botao_maça
    
    ]),border_radius=30)
    def mimico(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "#eaf571"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/mimico.png"
        icone_usuario_jogando.src = "./assets/mimico.png"
        page.update()
    botao_mimico = ft.ElevatedButton("",opacity=0,on_click=mimico,height=100,width=100)
    icone_mimico = ft.Container(ft.Stack([
        ft.Image("./assets/mimico.png",width=100),
        botao_mimico
    
    ]),border_radius=30)
    def napoleao(e):
        icone_usuario_jogando.height = 100
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "#eaf571"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/napoleao.png"
        icone_usuario_jogando.src = "./assets/napoleao.png"
        page.update()
    botao_napoleao = ft.ElevatedButton("",opacity=0,on_click=napoleao,height=100,width=100)
    icone_napoleao = ft.Container(ft.Stack([
        ft.Image("./assets/napoleao.png",width=100),
        botao_napoleao
    
    ]),border_radius=30)
    def neymar(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "#eaf571"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/neymar.png"
        icone_usuario_jogando.src = "./assets/neymar.png"
        page.update()
    botao_neymar = ft.ElevatedButton("",opacity=0,on_click=neymar,height=100,width=100)
    icone_neymar = ft.Container(ft.Stack([
        ft.Image("./assets/neymar.png",width=100),
        botao_neymar
    
    ]),border_radius=30)
    def pizza(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "#eaf571"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/pizza.png"
        icone_usuario_jogando.src = "./assets/pizza.png"
        page.update()
    botao_pizza = ft.ElevatedButton("",opacity=0,on_click=pizza,height=100,width=100)
    icone_pizza = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/pizza.png",width=100),margin=ft.margin.only(top=15)),
        botao_pizza
    
    ]),border_radius=30)
    def tubarao_azul(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "#eaf571"
        icone_tubarao_cinza.bgcolor = "white"
        icone_usuario.src = "./assets/tubarao_azul.png"
        icone_usuario_jogando.src = "./assets/tubarao_azul.png"
        page.update()
    botao_tubarao_azul = ft.ElevatedButton("",opacity=0,on_click=tubarao_azul,height=100,width=100)
    icone_tubarao_azul = ft.Container(ft.Stack([
        ft.Container(ft.Image("./assets/tubarao_azul.png",width=100),margin=ft.margin.only(top=15)),
        botao_tubarao_azul
    
    ]),border_radius=30)
    def tubarao_cinza(e):
        icone_urso.bgcolor = "white"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "#eaf571"
        icone_usuario.src = "./assets/tubarao_cinza.png"
        icone_usuario_jogando.src = "./assets/tubarao_cinza.png"
        page.update()
    botao_tubarao_cinza = ft.ElevatedButton("",opacity=0,on_click=tubarao_cinza,height=100,width=100)
    icone_tubarao_cinza = ft.Container(ft.Stack([
        ft.Image("./assets/tubarao_cinza.png",width=100),
        botao_tubarao_cinza
    
    ]),border_radius=30)
    def urso(e):
        icone_usuario.src = "./assets/urso.png"
        icone_usuario_jogando.src = "./assets/urso.png"
        icone_urso.bgcolor = "#eaf571"
        icone_arco_triunfo.bgcolor = "white"
        icone_bandeira_brasil.bgcolor = "white"
        icone_bandeira_frança.bgcolor = "white"
        icone_bola_francesa.bgcolor = "white"
        icone_caranguejo_estressado.bgcolor = "white"
        icone_coelho.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_dinossauro_verde.bgcolor = "white"
        icone_dinossauro_laranja.bgcolor = "white"
        icone_leao.bgcolor = "white"
        icone_maça.bgcolor = "white"
        icone_mimico.bgcolor = "white"
        icone_napoleao.bgcolor = "white"
        icone_neymar.bgcolor = "white"
        icone_padrao.bgcolor = "white"
        icone_pizza.bgcolor = "white"
        icone_tubarao_azul.bgcolor = "white"
        icone_tubarao_cinza.bgcolor = "white"
        page.update()
    def fechar_confirmou_icone(e):
        page.dialog = confirmou_icone
        confirmou_icone.open = False
        page.update()
    confirmou_icone = ft.AlertDialog(
        modal=True,
        title=ft.Text("Ícone de Usuário alterado com sucesso"),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Ok", on_click=fechar_confirmou_icone),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    def confimar_icone(e):
        cursor.execute("UPDATE usuarios5 SET icone = ? WHERE usuario = ?",(icone_usuario.src,text_nome_usuario.value))
        page.dialog = confirmou_icone
        confirmou_icone.open = True
        page.update()
        banco.commit()
    botao_confirmar_icone.on_click = confimar_icone
    botao_urso = ft.ElevatedButton("",opacity=0,on_click=urso,height=100,width=100)
    icone_urso = ft.Container(ft.Stack([
        ft.Image("./assets/urso.png",width=100),
        botao_urso
    
    ]),border_radius=30)
    
    botao_facil =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="FÁCIL", size=30),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=200,
            height=60,bgcolor="#98f772",
            color="black"
        )
    botao_medio =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="MÉDIO", size=30),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=200,
            height=60,bgcolor="#f1f772",
            color="black"
        )
    botao_dificil =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="DIFÍCIL", size=30),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=200,
            height=60,bgcolor="#f77272",
            color="black"
        )
    text_dias_consecutivos = ft.Text("Você está jogando a 5 dias consecutivos",size=20,color="white")
    botao_clicavel = ft.ElevatedButton("",opacity=0)#botao em cima da seta de voltar
    botao_voltar = ft.Stack([
        ft.Image("Vector-removebg-preview.png",width=50),
        botao_clicavel
    
    ])#botao de voltar
    botao_voltar2 = ft.ElevatedButton("",opacity=0)
    botao_voltar_no_jogo = ft.Stack([
        ft.Image("Vector-removebg-preview.png",width=50,color="white"),
        botao_voltar2
    
    ])#botao de volta
    botao_voltar2.on_click = open_dlg_modal
    def voltar_usuario(e):
        page.go("/jogar")
    botao_clicavel_jogando.on_click = voltar_usuario
    botao_jogar =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="JOGAR", size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=235,
            height=65
        )
    botao_configuracoes =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="CONFIGURAÇÕES", size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=235,
            height=65
        )
    botao_sair =  ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value="SAIR DA CONTA", size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            style=ft.ButtonStyle(#botao para login
            shape=ft.RoundedRectangleBorder(radius=20),color="black"),
            width=235,
            height=65
        )
    progressobar = ft.ProgressBar(value=0,width=250,height=30,color="#ffd600",border_radius=20,semantics_label="13/100")
    texto_exp = ft.Text("0/100",size=20)
    texto_estrela = ft.Container(ft.Icon(ft.icons.STAR_PURPLE500,color="yellow"),alignment=ft.alignment.center,margin=ft.margin.all(0))
    texto_final_exp = ft.Container(ft.Row([texto_exp,texto_estrela],alignment=ft.MainAxisAlignment.CENTER),alignment=ft.alignment.center,padding=0)
    progresso_bar = ft.Container(
        ft.Stack(
            [
            ft.Container(progressobar),
            ft.Container(texto_final_exp,width=250,alignment=ft.alignment.center_right)
            ]
    
                 ),
        alignment=ft.alignment.center
        )
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans": "/fonts/OpenSans-Regular.ttf"
    }
    page.theme = Theme(font_family="Kanit")
    consulta = cursor.execute("SELECT * FROM usuarios5")
    consulta = consulta.fetchall()
    text_consecutivos = ft.Text("0",size=30)#caixa de texto para colocar quantidade de dias consecutivos
    text_mudar_usuario = ft.TextField(label = "Novo nome de usuário...",width=400,color=ft.colors.BLACK,border_color=ft.colors.BLACK)#caixa de seleção para mudar o nome de usuário
    botao_fechar_configuracoes = ft.IconButton(ft.icons.CLOSE,icon_color="black")
    botao_novo_usuario = ft.ElevatedButton("CONFIRMAR",width=200)
    c = ft.Container(#Container da caixa de configurações
        content= ft.Column([ft.Row([ft.Container(botao_fechar_configuracoes,alignment=ft.alignment.top_right,width=900)]),ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                
                tab_content=ft.Container(ft.Text("MUDAR NOME DE USUÁRIO",color="black"),width=260,height=50,alignment=ft.alignment.center),
                content=ft.Container(ft.Column([
                ft.Container(ft.TextField(label="Novo nome de usuário...",text_align=ft.TextAlign.LEFT,width=400,label_style=ft.TextStyle(color="#7F7F7F"),border_color="black"),margin=ft.margin.only(top=20)),
                    ft.Container(content=ft.TextField(label="Confirmar nome de usuário...",text_align=ft.TextAlign.LEFT,width=400,label_style=ft.TextStyle(color="#7F7F7F"),border_color="black"))
                    ]),alignment=ft.alignment.center,margin=ft.margin.only(top=150))
            ),
            ft.Tab(
                tab_content=ft.Container(ft.Text("MUDAR SENHA",color="black"),width=260,height=50,alignment=ft.alignment.center),
                content=ft.Container(ft.Column([
                    ft.Container(ft.TextField(label="Senha atual...",text_align=ft.TextAlign.LEFT,width=400,label_style=ft.TextStyle(color="#7F7F7F")),alignment=ft.alignment.center),
                    ft.Container(content=ft.TextField(label="Nova senha...",text_align=ft.TextAlign.LEFT,width=400,label_style=ft.TextStyle(color="#7F7F7F")),alignment=ft.alignment.center),
                    ft.Container(content=ft.TextField(label="Confirmar nova senha...",text_align=ft.TextAlign.LEFT,width=400,label_style=ft.TextStyle(color="#7F7F7F")),alignment=ft.alignment.center),
                    ft.Container(ft.ElevatedButton("SALVAR",width=200),alignment=ft.alignment.center),
                    ]),alignment=ft.alignment.center,margin=ft.margin.only(top=150))
            ),
            ft.Tab(
                tab_content=ft.Container(ft.Text("MUDAR ÍCONE DE USUÁRIO",color="black"),width=260,height=50,alignment=ft.alignment.center),
                content=ft.Container(ft.Column([
                    ft.Row([
               ft.Container(icone_arco_triunfo,alignment=ft.alignment.center),
               ft.Container(icone_bandeira_brasil,alignment=ft.alignment.center),
               ft.Container(icone_bandeira_frança,alignment=ft.alignment.center),
               ft.Container(icone_bola_francesa,alignment=ft.alignment.center),
               ft.Container(icone_padrao,alignment=ft.alignment.center),
               ft.Container(icone_caranguejo_estressado,alignment=ft.alignment.center)
                ]
                           ,alignment=ft.MainAxisAlignment.CENTER
                           ),
                        
                        
                    ft.Row([
                        ft.Container(icone_coelho,alignment=ft.alignment.center),
                        ft.Container(icone_dinossauro_verde,alignment=ft.alignment.center),
                        ft.Container(icone_dinossauro_laranja,alignment=ft.alignment.center),
                        ft.Container(icone_leao,alignment=ft.alignment.center),
                        ft.Container(icone_maça,alignment=ft.alignment.center),
                        ft.Container(icone_mimico,alignment=ft.alignment.center),
                        
                        
                    ],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.Container(icone_napoleao,alignment=ft.alignment.center),
                        ft.Container(icone_neymar,alignment=ft.alignment.center),
                        ft.Container(icone_pizza,alignment=ft.alignment.center),
                        ft.Container(icone_tubarao_azul,alignment=ft.alignment.center),
                        ft.Container(icone_tubarao_cinza,alignment=ft.alignment.center),
                        ft.Container(icone_urso,alignment=ft.alignment.center),
                    ],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(botao_confirmar_icone,alignment=ft.alignment.center,margin=ft.margin.only(top=20))
                  ],alignment=ft.CrossAxisAlignment.CENTER),alignment=ft.alignment.center,margin=ft.margin.only(top=50),width=700,height=500)
            ),
            
        ],
        expand=1,
        indicator_tab_size=False,
        indicator_color="#E77A52"
    )]),
        width=900,
        height=0,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
        alignment=ft.alignment.bottom_right,
        padding=ft.padding.only(top=0),
        bgcolor="white",
        border=ft.border.all(2,color=ft.colors.BLACK),
        border_radius=20
    )
    page.window_full_screen = True
    page.padding = 0
    page.title = "Routes Example"
    text_username: ft.TextField = ft.TextField(label="Usuário",text_align=ft.TextAlign.LEFT,width=240,label_style=ft.TextStyle(color="#E77A52"),max_length=15)
    text_password: ft.TextField = ft.TextField(label="Senha",text_align=ft.TextAlign.LEFT,width=240,password=True,label_style=ft.TextStyle(color="#E77A52"),can_reveal_password=True)
    button_submit: ft.ElevatedButton = ft.ElevatedButton(text="ENTRAR",width=200,color="white",bgcolor="#E77A52",style=ft.ButtonStyle(#botao para login
                shape=ft.RoundedRectangleBorder(radius=0),))
    
    botao_cadastro = ft.ElevatedButton(text="Cadastre-se",width=150,color="white",bgcolor="#C1846F",style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),))
    text_confirmar_senha: ft.TextField = ft.TextField(label="Confirmar senha",text_align=ft.TextAlign.LEFT,width=240,password=True,label_style=ft.TextStyle(color="#E77A52"),can_reveal_password=True)
    button_registrar: ft.ElevatedButton = ft.ElevatedButton(text="Registrar",width=200,color="white",bgcolor="#E77A52",style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),))
    
    texto_certo_errado = ft.TextField(value=" ", text_align=ft.TextAlign.RIGHT, width=400)
    texto_erro = ft.Text(value="",color=ft.colors.RED_500)
    texto_acerto = ft.Text(value="",color=ft.colors.GREEN_500)
    progresso = ft.Slider(width=400,max=300)
    texto_pontuacao = ft.Text("0",size=30)#pontuacao do usuario
    text_level = ft.Text("0",size=30,color="white")#level do usuario
    text_nome_usuario = ft.Text("",size=30,color="white")
    botao_escutar = ft.IconButton(ft.icons.PLAY_ARROW)
    def escutar(e):
        print(texto_a_ser_falado.value)
        robo = pyttsx3.init()
        rate = robo.getProperty('rate')
        print(pyttsx3.voice.Voice)
        robo.setProperty('rate', rate-100)
        robo.say(texto_a_ser_falado.value)
        robo.runAndWait()
    pontuacao = ft.Text("0",size=30)
    botao_escutar.on_click = escutar
    def jogou(e):
            container_contagem.height = 50
            container_botao_falar.height = 0
            container_botao_falar.margin = ft.margin.only(top=0)
            for i in [3,2,1]:
                texto_contagem.value = f"{i}"
                page.update()
                time.sleep(1)
                
            container_botao_falar.height = 0
            container_contagem.height = 0
            container_texto_falado.height = 80
            page.update()
            page.dialog = errou_questão
            teste = texto_a_ser_falado.value
            r = sr.Recognizer()
            try:
                with sr.Microphone() as fonte:
                        r.adjust_for_ambient_noise(fonte,)
                        audio = r.listen(fonte, phrase_time_limit=3)
                        texto = r.recognize_google(audio, language="fr-FR")
                if texto.lower() == teste.lower():
                    page.dialog = errou_questão
                    texto_pontuacao_soma.value = str(int(texto_pontuacao_soma.value)+10)
                    errou_questão.title = ft.Text("Parabéns você acertou!!")
                    errou_questão.content = ft.Text(f"Você falou {texto}")
                    errou_questão.actions = [ft.TextButton("Próxima Questão", on_click=ir_para_proxima_questao)]
                    errou_questão.open=True
                    page.update()
                else:
                    page.dialog = errou_questão
                    errou_questão.title = ft.Text("Você errou!!")
                    errou_questão.content = ft.Text(f"Você falou {texto}")
                    errou_questão.actions = [botao_escutar,ft.TextButton("Próxima Questão", on_click=ir_para_proxima_questao)]
                    errou_questão.open = True
                    
                    page.update()
            except:
                    page.dialog = errou_audio
                    errou_audio.content = ft.Text("")
                    errou_audio.title = ft.Text("Não foi possível compreender o áudio")
                    errou_audio.open = True
                    texto_certo_errado.value = "não foi possível compreender o áudio"
                    page.update()
            page.update()
            
            page.update()
            page.update()
    botao_falar.on_click=jogou
    def update_usuario(e):#função para atualizar o nome do usuario no banco
        consulta = cursor.execute("SELECT * FROM usuarios5 WHERE usuario=?",(text_mudar_usuario.value,))
        sql = ''' UPDATE usuarios5
                SET usuario = ?
                WHERE usuario = ?'''
        cur = banco.cursor()
        res = consulta.fetchall()
        if len(res) == 0 and text_mudar_usuario.value != "":
            cur.execute(sql, (text_mudar_usuario.value,text_nome_usuario.value))
            banco.commit()
            text_mudar_usuario.value = ""
            page.update()
    botao_novo_usuario.on_click = update_usuario
    def progressoslider(e):
        progresso.value = texto_pontuacao.value
        page.update()
    def registrar_conta(e):#função para registrar uma conta
        consulta_usuarios = cursor.execute("SELECT usuario FROM usuarios5 WHERE usuario=?",(text_username.value,))
        res = consulta_usuarios.fetchall()
        if text_username.value != '' and text_password.value != '':
            if len(res) > 0:
                page.dialog = erro_registro
                erro_registro.open = True
                erro_registro.title = ft.Text("Usuario já cadastrado!!!",color="red")
                page.update()
            elif " " in text_username.value or "!" in text_username.value or "@" in text_username.value or "#" in text_username.value or "$" in text_username.value or "%" in text_username.value or "&" in text_username.value or "*" in text_username.value or " (" in text_username.value or ")" in text_username.value or ";" in text_username.value or "+" in text_username.value or "-" in text_username.value or "?" in text_username.value or "=" in text_username.value or "," in text_username.value or "<" in text_username.value or ">" in text_username.value or "/" in text_username.value:
                page.dialog = erro_registro
                erro_registro.open = True
                erro_registro.title = ft.Text("Crie um usuário sem espaço em branco e sem caracteres especiais",color="red")
                page.update()
            elif len(str(text_password.value)) < 5 or " " in str(text_password.value):
                page.dialog = erro_registro
                erro_registro.open = True
                erro_registro.title = ft.Text("Digite uma senha com no mínimo 5 dígitos!!!",color="red")
                page.update()
            elif text_password.value != text_confirmar_senha.value:
                page.dialog = erro_registro
                erro_registro.open = True
                erro_registro.title = ft.Text("As senhas não são iguais!!!",color="red")
                page.update()
            else:
                cursor.execute("INSERT INTO usuarios5(usuario,senha,level,data,consecutivos,exp,icone,pontos_nivel) VALUES (?,?,?,?,?,?,?,?)",(str(text_username.value),str(text_password.value),1,str(datetime.date.today()),0,0,"./assets/carangueijo_sem_fundo.png",100))
                banco.commit()
                texto_erro.value = ""
                texto_acerto.value = "Usuario cadastrado com sucesso,volte para o início para JOGAR!!"
                text_confirmar_senha.value = ''
                text_username.value = ''
                text_password.value = ''
                page.go("/")
                page.update()
                time.sleep(5)
                texto_acerto.value = ""   
        else:
            page.dialog = erro_registro
            erro_registro.open = True
            erro_registro.title = ft.Text("Preencha todos os campos!!!",color="red")
            page.update()
    def irParaRegistrar(e):
        text_username.value = ""
        text_password.value = ""
        text_confirmar_senha.value = ""
        page.go("/registrar")
    botao_cadastro.on_click = irParaRegistrar
    
    button_registrar.on_click = registrar_conta
    def ir_para_dificuldade(e):
        page.go("/dificuldade")
        page.update()
    """def jogando(e):#função para aumentar a pontuação conforme o usuario vai jogando
        consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
        pontuacao.value = str(int(pontuacao.value)+10)
       
        res = consulta.fetchall()
        if int(pontuacao.value) < 100:
            text_level.value = "level 1"
        elif int(pontuacao.value) < 1000 and int(pontuacao.value) >= 100:
            text_level.value = f"level {int(str(pontuacao.value)[0]) + 1}"
            
        elif int(pontuacao.value) >= 1000 and int(pontuacao.value) < 10000:
            text_level.value = f"level {int(str(pontuacao.value)[:2]) + 1}"
        elif int(pontuacao.value) >= 10000 and int(pontuacao.value) < 100000:
            text_level.value = f"level {int(str(pontuacao.value)[:3]) + 1}"
        else:
            text_level.value = f"level {int(str(pontuacao.value)[:4]) + 1}"
        if progressobar.value < 0.88:
            progressobar.value = progressobar.value + 0.1
            texto_exp.value = f"{str(int(round(progressobar.value*100)))}/100"
        else:
            progressobar.value = 0
            texto_exp.value = f"0/100"
        cursor.execute("UPDATE usuarios3 SET level=? WHERE usuario=?",(text_level.value[6:],text_nome_usuario.value))
        cursor.execute("UPDATE usuarios3 SET pontuaçao=? WHERE usuario=?",(pontuacao.value,text_nome_usuario.value))
        cursor.execute("UPDATE usuarios3 SET exp=? WHERE usuario=?",(progressobar.value,text_nome_usuario.value))
        consulta = cursor.execute("SELECT * FROM usuarios3 WHERE usuario=?",(text_username.value,))
        res = consulta.fetchall()
        data = res[0][4]
        string = data.split("-")
        ano = int(string[0])
        mes = int(string[1])
        dia = int(string[2])
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
        page.update()"""
    botao_jogar.on_click = ir_para_dificuldade
    def jogar(e):#função para entrar na pagina de usuario confirmando o login
        consulta_usuarios = cursor.execute("SELECT * FROM usuarios5 WHERE usuario=?",(text_username.value,))
        res = consulta_usuarios.fetchall()
        if len(res) > 0:
            data = res[0][3]
            string = data.split("-")
            ano = int(string[0])
            mes = int(string[1])
            dia = int(string[2])
            if datetime.date.today() - datetime.timedelta(days=1) > datetime.date(ano,mes,dia):
                cursor.execute("UPDATE usuarios5 SET consecutivos = ? WHERE usuario = ?",(0,str(text_username.value)))
                banco.commit()
        else:
            page.dialog = erro_registro
            erro_registro.open = True
            erro_registro.title = ft.Text("Usuário não cadastrado!!!",color="red")
            page.update()
        
        contagem = len(res)
        if len(res) > 0:
            progresso.value = str(res[contagem-1][3])
            texto_pontuacao.value = f"Pontuação: {str(res[contagem-1][3])}"
            pontuacao.value = f"{str(res[contagem-1][3])}"
            text_level.value = f"Level {res[contagem-1][2]}"
            text_nome_usuario.value = text_username.value
            progressobar.value = float(res[0][5])
            texto_exp.value = f"{int(round(progressobar.value * 100))}/100"
            text_dias_consecutivos.value = f"Você está jogando a {res[0][5]} dias consecutivos"
        if len(res) > 0:
            jogador = str(res[0][1])
            if str(jogador) == str(text_password.value):
                print(res[0][5])
                icone_usuario.src = str(res[0][6])
                text_level.value = f"Level: {res[0][4]}"
                exp_value.value = f"{res[0][5]}"
                texto_exp.value = f"{res[0][5]}/{res[0][7]}"
                progressobar.value = int(exp_value.value)/int(res[0][7])
                icone_usuario_jogando.src = str(res[0][6])
                print(res[0][7])
                if str(res[0][6]) == "./assets/napoleao.png":
                    icone_usuario_jogando.height = 100
                page.go("/jogar")
                page.update()
            else:
                page.dialog = erro_registro
                erro_registro.open = True
                erro_registro.title = ft.Text("Senha incorreta!!!",color="red")
                page.update()
        
        page.update()
    def fechar(e):#função para fechar a pagina
        page.go("/")
        text_username.value = ""
        text_password.value = ""
        page.update()
    botao_sair.on_click = fechar
    button_submit.on_click = jogar
    login = View(
                    "/",
                    [
                        ft.Container(ft.Stack([ #Container com imagem de fundo
                            ft.Image(
                src="./assets/Home Screan (3).png",
                fit="cover",
                height=770
            ),
                        ft.Container(ft.Container( #Container da caixa de login
                            content=ft.Column([
                                ft.Container(ft.Image(
                                                src=f"./assets/MicrosoftTeams-image__1_-removebg-preview.png",
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
                            bgcolor="#EBEAEA",width=600,
                            height=500,
                            opacity=1,
                            border=ft.border.all(3,color="#E77A52"),
                            border_radius=10),alignment=ft.alignment.center,height=page.window_height)]))
                                ]
                        
                )
    login.padding = 0
    opcoes_icones = [ft.Icon(ft.icons.HOME),ft.Icon(ft.icons.ABC),ft.Icon(ft.icons.MONEY_ROUNDED)]
    def animate_container(e):#função para abrir as configurações
        c.height=600
        
        c.update()
        page.update()
    botao_configuracoes.on_click = animate_container
    def fechar_configuracoes(e):#função para fechar as configurações
        c.height = 0
        c.update()
        page.update()
    botao_fechar_configuracoes.on_click = fechar_configuracoes
    
    principal_jogo = View( #Não feita ainda
                    "/jogar",
                    [
                         ft.Container(
           ft.Stack([
                            ft.Image(
                src="./assets/Home Screan (3).png",
                fit="cover",
                height=770
            ),
                ft.Container(ft.Container(
                    ft.Column([
                        ft.Container(
                        ft.Container(ft.Row([
                            ft.Container(icone_usuario,margin=ft.margin.only(left=15)),
                            ft.Container(ft.Container(text_nome_usuario,margin=ft.margin.only(right=50)),width=290,height=65,bgcolor="#E77A52",border_radius=40,margin=ft.margin.only(right=5),alignment=ft.alignment.center_right)
                        ]),bgcolor="white",width=400,height=70,border_radius=40,margin=ft.margin.only(right=0,top=10)),
                                     alignment=ft.alignment.top_right
                        )
                    ,ft.Column([
                        ft.Container(c,alignment=ft.alignment.center),
                    ft.Container( #Container da caixa de login
                        content=botao_jogar,
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(top=(page.window_height-100)/3),
                            opacity=1,
                            border_radius=10),
                     ft.Container( #Container da caixa de login
                        content=botao_configuracoes,
                            alignment=ft.alignment.center,
                            opacity=1,
                            border_radius=10),
                      ft.Container( #Container da caixa de login
                        content=botao_sair,
                            alignment=ft.alignment.center,
                            opacity=1,
                            border_radius=10),
                    ft.Container(text_level,alignment=ft.alignment.center),
                    ft.Container(progresso_bar,alignment=ft.alignment.center),
                    ft.Container(text_dias_consecutivos,alignment=ft.alignment.center),])]),
                    alignment=ft.alignment.center)),
                
                
                    
                
                    ]),
                             
               alignment=ft.alignment.center ),
                    ]
                
    )
                    
                    
                    
    principal_jogo.padding = 0
    
    registrar =  View(
                    "/registrar",
                    [
                        ft.Container(ft.Stack([ #Container com imagem de fundo
                            ft.Container(ft.Image(
                src="./assets/Home Screan (3).png",
                fit="cover",
                height=770
                            )),
                        ft.Container(ft.Container( #Container da caixa de login
                            content=ft.Column([
                                ft.Container(botao_voltar,margin=ft.margin.only(bottom=0,left=15,top=15)),
                                ft.Container(ft.Image(
                                                src=f"./assets/MicrosoftTeams-image__1_-removebg-preview.png",
                                                width=300,
                                                height=200,
                                                fit=ft.ImageFit.CONTAIN,
                                                
                                                )
                                     ,alignment=ft.alignment.center,width=600,margin=ft.margin.only(bottom=0,top=-60)),
                                ft.Container(ft.Column([ft.Container(text_username,alignment=ft.alignment.center,width=300),
                        ft.Container(text_password,alignment=ft.alignment.center,width=300),
                        ft.Container(text_confirmar_senha,alignment=ft.alignment.center,width=300),
                        ft.Container(button_registrar,alignment=ft.alignment.center,width=220,margin=ft.margin.only(bottom=30,left=(300-220)/2),
                                     opacity=1)]),width=600,alignment=ft.alignment.center),
                    ]),
                            alignment=ft.alignment.center,
                            bgcolor="#EBEAEA",width=500,
                            margin=ft.margin.only(top=(page.window_height-400)/2,bottom=(page.window_height-200)/2),
                            opacity=1,
                            border=ft.border.all(3,color="#E77A52"),
                            border_radius=10),alignment=ft.alignment.center)]),
                                     )
                                ]
                        
                )
    selecionar_dificuldade = ft.View(
                "/dificuldade",
                [
                    
                    ft.Container(
           ft.Stack([
                            ft.Image(
                src="./assets/Home Screan (3).png",
                fit="cover",
                height=770
            ),        
                    ft.Container(
                        ft.Container(
                            ft.Container(ft.Row([
                            ft.Container(icone_usuario,margin=ft.margin.only(left=15)),
                            ft.Container(ft.Container(text_nome_usuario,margin=ft.margin.only(right=50)),width=290,height=65,bgcolor="#E77A52",border_radius=40,margin=ft.margin.only(right=5),alignment=ft.alignment.center_right)
                        ]),bgcolor="white",width=400,height=70,border_radius=40),
                            width=400,
                            height=70,
                            alignment=ft.alignment.top_right,
                            bgcolor="white",
                            border_radius=40
                        ),
                        
                        
                        height=100,alignment=ft.alignment.center_right
                        
                        ),
                    ft.Container(
                        ft.Container(
                            ft.Column(
                                [
                                ft.Container(botao_voltar_jogando,margin=ft.margin.only(left=10,top=10)),
                                ft.Row([
                                    ft.Container(ft.Text("SELECIONE A DIFICULDADE",size=30,color="black"),margin=ft.margin.only(top=-50))
                                ],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                ft.Column([
                                    ft.Container(botao_facil,alignment=ft.alignment.center,margin=ft.margin.only(bottom=20)),
                                    ft.Container(botao_medio,alignment=ft.alignment.center,margin=ft.margin.only(bottom=20)),
                                    ft.Container(botao_dificil,alignment=ft.alignment.center)
                                ]),
                                ft.Container(ft.Text("Obs: Quanto maior a dificuldade, mais estrelas você poderá ganhar!!",color="black",weight=ft.FontWeight.BOLD),margin=ft.margin.only(top=10,left=10))
                            ]),
                            width=600,
                            height=360,
                            bgcolor="white",
                            border_radius=20,
                            padding=0
                        ),height=page.window_height,alignment=ft.alignment.center
                       
                    )
             
                ],
            ))])
    
    def ir_para_jogo(e):
        texto_pergunta.value = "Questão 1/6"
        container_texto_falado.height = 0
        container_contagem.height = 0
        botao_falar.height = 60
        container_botao_falar.height = 60
        texto = random.randint(0,4)
        texto_falado_indice.value = str(texto)
        consulta = cursor_questoes.execute('SELECT * FROM questoes4')
        res = consulta.fetchall()
        texto_questao = res[texto][0]
        texto_a_ser_falado.value = texto_questao
        page.update()
        page.go("/jogando")
    botao_facil.on_click = ir_para_jogo
    container_texto_falado = ft.Container(
                                        ft.Row([ft.Container(ft.Text("Fale: ",size=30,color="black",weight=ft.FontWeight.BOLD),margin=ft.margin.only(left=30)),ft.Container(texto_a_ser_falado,height=70,width=680,bgcolor="#E77A52",border_radius=50,alignment=ft.alignment.center)],alignment=ft.MainAxisAlignment.CENTER),
                                        height=0,
                                        border_radius=50,
                                        margin=ft.margin.only(top=50),
                                        bgcolor="white",
                                        alignment=ft.alignment.center_right
                                        
                                        )
    texto_contagem = ft.Text("",size=30,color="white")
    container_contagem = ft.Container(
        texto_contagem,
        height=0,
        alignment=ft.alignment.center
    ) 
    jogando_jogo_falando = ft.View(
                "/jogando",
                [
                    
           ft.Stack([
                            ft.Image(
                src="./assets/Game Screen (write).png",
                fit="cover",
                height=770
            ), 
                            
                    ft.Container(
                        ft.Container(
                            ft.Row([ft.Container(icone_usuario,alignment=ft.alignment.center,margin=ft.margin.only(left=10)),ft.Container(ft.Container(text_nome_usuario,margin=ft.margin.only(right=50)),width=295,height=65,bgcolor="#E77A52",border_radius=40,margin=ft.margin.only(right=5),alignment=ft.alignment.center_right)]),
                            width=400,
                            height=70,
                            alignment=ft.alignment.center_right,
                            bgcolor="white",
                            border_radius=40
                        ),
                        
                        
                        height=100,alignment=ft.alignment.center_right
                        
                        ),
                    
                    ft.Container(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Stack([
                                    ft.Container(
                                        ft.Container(texto_pergunta,alignment=ft.alignment.center,width=500,bgcolor="white"),
                                        height=130,
                                        alignment=ft.alignment.center,
                                        margin=ft.margin.only(top=60)

                                    ),
                                    ft.Container(icone_usuario_jogando,alignment=ft.alignment.center)
                                    ]),
                                    container_contagem,
                                    container_texto_falado
                                    ,
                                    container_botao_falar
                            ]),
                            width=800,
                            height=500,

                            border_radius=0,
                            padding=0
                        ),height=page.window_height,alignment=ft.alignment.center
                       
                    ),
                    ft.Container(botao_voltar_no_jogo,margin=ft.margin.only(left=10,top=10)),
             
                ],
            )])
    jogando_jogo_alternativa = ft.View(
                "/jogando_alternativa",
                [
                    
           ft.Stack([
                            ft.Image(
                src="./assets/Game Screen (write).png",
                fit="cover",
                height=770
            ), 
                            
                    ft.Container(
                        ft.Container(
                            ft.Row([ft.Container(icone_usuario,alignment=ft.alignment.center,margin=ft.margin.only(left=10)),ft.Container(ft.Container(text_nome_usuario,margin=ft.margin.only(right=50)),width=295,height=65,bgcolor="#E77A52",border_radius=40,margin=ft.margin.only(right=5),alignment=ft.alignment.center_right)]),
                            width=400,
                            height=70,
                            alignment=ft.alignment.center_right,
                            bgcolor="white",
                            border_radius=40
                        ),
                        
                        
                        height=100,alignment=ft.alignment.center_right
                        
                        ),
                    
                    ft.Container(
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Stack([
                                    ft.Container(
                                        ft.Container(texto_pergunta,alignment=ft.alignment.center,width=500,bgcolor="white"),
                                        height=130,
                                        alignment=ft.alignment.center,
                                        margin=ft.margin.only(top=60)

                                    ),
                                    ft.Container(ft.Image("./assets/carangueijo_sem_fundo.png",width=400,height=130),alignment=ft.alignment.center)
                                    ]),
                                    ft.Container(
                                        ft.Row([ft.Container(ft.Text("Qual a tradução da frase: ",size=30,color="black",weight=ft.FontWeight.BOLD),margin=ft.margin.only(left=30)),ft.Container(texto_a_ser_falado,height=70,width=680,bgcolor="#E77A52",border_radius=50,alignment=ft.alignment.center)],alignment=ft.MainAxisAlignment.CENTER),
                                        height=75,
                                        border_radius=50,
                                        margin=ft.margin.only(top=50),
                                        bgcolor="white",
                                        alignment=ft.alignment.center_right
                                        
                                        ),
                                    ft.Container(botao_alternativa_A,alignment=ft.alignment.center,margin=ft.margin.only(top=30)),
                                    ft.Container(botao_alternativa_B,alignment=ft.alignment.center),
                                    ft.Container(botao_alternativa_C,alignment=ft.alignment.center),
                                    ft.Container(botao_alternativa_D,alignment=ft.alignment.center),
                                    ft.Container(botao_confirmar_alternativa,alignment=ft.alignment.center),
                                    
                            ]),
                            width=1100,
                            height=800,

                            border_radius=0,
                            padding=0
                        ),height=page.window_height,alignment=ft.alignment.center
                       
                    ),
                    ft.Container(botao_voltar_no_jogo,margin=ft.margin.only(left=10,top=10)),
             
                ],
            )])
    selecionar_dificuldade.padding=0
    registrar.window_full_screen = False
    def voltar_login(e):
        text_username.value = ""
        text_password.value = ""
        text_confirmar_senha.value = ""
        page.go("/")
    botao_clicavel.on_click = voltar_login
    registrar.padding = 0
    jogando_jogo_falando.padding = 0
    jogando_jogo_alternativa.padding = 0
    def route_change(e):
        page.views.clear()

        page.views.append(
            login
        )
        if page.route == "/":
            login.vertical_alignment = ft.MainAxisAlignment.CENTER
            login.horizontal_alignment =ft.CrossAxisAlignment.CENTER
            page.update()
            page.views.append(
                login
            )
        if page.route == "/jogar":
            consulta_usuarios = cursor.execute("SELECT * FROM usuarios5 WHERE usuario=?",(text_nome_usuario.value,))
            res = consulta_usuarios.fetchall()

            pontuacoes = res[0][3]
            levels = res[0][2]
            texto_pontuacao.value = f"Pontuação: {pontuacoes}"
            text_level.value = f"Level {levels}"
            text_level
            page.update()
            page.views.append(
                principal_jogo
            )
        if page.route == "/registrar":
            page.views.append(
                registrar
            )
        if page.route == "/dificuldade":
            page.views.append(
                selecionar_dificuldade
            )
        progresso.on_change = progressoslider
        if page.route == "/jogando":
            page.update()
            page.views.append(
                jogando_jogo_falando
            )
        if page.route == "/jogando_alternativa":
            page.update()
            page.views.append(
                jogando_jogo_alternativa
            )
    
        page.update()
    page.on_route_change = route_change
    page.go(page.route)
ft.app(main)