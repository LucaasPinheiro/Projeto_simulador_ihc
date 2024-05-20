import random
import tkinter as tk
from tkinter import messagebox


# Funções de carregamento
def carregar_perguntas_respostas(nome_arquivo):
    perguntas_respostas = {}
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue

                if linha.endswith('+'):
                    explicacao = linha[:-1]
                elif linha.endswith('$'):
                    personagem, pergunta = linha.split(': ')
                    perguntas_respostas.setdefault(personagem, []).append({
                        "Explicacao":
                        explicacao,
                        "Pergunta":
                        pergunta[:-1],
                        "Respostas": [],
                        "Pontuacoes": [4, 3, 2, 1]
                    })
                elif '_' in linha:
                    respostas = [
                        resposta.strip('_') for resposta in linha.split(';')
                    ]
                    perguntas_respostas[personagem][-1]["Respostas"].extend(
                        respostas)
                else:
                    perguntas_respostas[personagem][-1]["Respostas"].append(
                        linha.strip('_'))

    except FileNotFoundError:
        print("O arquivo especificado não foi encontrado.")

    return perguntas_respostas


def carregar_feedbacks(nome_arquivo):
    feedbacks = {}
    try:
        with open(nome_arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                personagem, feedback = linha.split(";")
                feedbacks.setdefault(personagem, []).append(feedback)
    except FileNotFoundError:
        print("O arquivo de feedbacks especificado não foi encontrado.")
    return feedbacks


# Funções do jogo
def escolher_pergunta_aleatoria(perguntas_respostas):
    personagens = list(perguntas_respostas.keys())
    personagem = random.choice(personagens)
    dados = random.choice(perguntas_respostas[personagem])
    return personagem, dados


def contabilizar_pontos(resposta_escolhida):
    return resposta_escolhida[1]


def escolher_feedback(personagem, pontos, feedbacks):
    if pontos >= 4:
        return random.choice(feedbacks[personagem][:2])
    elif pontos == 3:
        return random.choice(feedbacks[personagem][2:4])
    elif pontos == 2:
        return random.choice(feedbacks[personagem][4:6])
    elif pontos == 1 and len(feedbacks[personagem]) > 6:
        return random.choice(feedbacks[personagem][6:])
    else:
        return ""


# Funções da interface gráfica
def iniciar_jogo():
    global personagem_atual, dados_atual, respostas_embaralhadas

    if not perguntas_respostas:
        messagebox.showinfo("Fim do Jogo", "Não há mais perguntas.")
        return

    personagem_atual, dados_atual = escolher_pergunta_aleatoria(
        perguntas_respostas)
    pergunta_label.config(
        text=f"{personagem_atual}: {dados_atual['Pergunta']}")

    explicacao_text.set(dados_atual.get("Explicacao", ""))

    respostas = dados_atual["Respostas"]
    pontuacoes = [4, 3, 2, 1]
    respostas_embaralhadas = list(zip(respostas, pontuacoes))
    random.shuffle(respostas_embaralhadas)

    for i, (resposta, _) in enumerate(respostas_embaralhadas):
        botoes_respostas[i].config(text=resposta, state=tk.NORMAL)

    atualizar_histórico()


def verificar_resposta(resposta_idx):
    global personagem_atual, dados_atual

    pontos = contabilizar_pontos(respostas_embaralhadas[resposta_idx])

    pontuacoes_personagens[personagem_atual] += pontos

    perguntas_respostas[personagem_atual].remove(dados_atual)
    if not perguntas_respostas[personagem_atual]:
        del perguntas_respostas[personagem_atual]

    feedback = escolher_feedback(personagem_atual, pontos, feedbacks)
    if feedback:
        messagebox.showinfo("Feedback", f"{personagem_atual}: {feedback}")

    for botao in botoes_respostas:
        botao.config(state=tk.DISABLED)

    iniciar_jogo()


def mostrar_menu():
    esconder_todas_frames()
    frame_menu.pack()


def mostrar_jogo():
    esconder_todas_frames()
    frame_jogo.pack()
    iniciar_jogo()


def mostrar_historico():
    atualizar_histórico()
    esconder_todas_frames()
    frame_historico.pack()


def atualizar_histórico():
    personagens_apresentados = sum(
        1 for pontos in pontuacoes_personagens.values() if pontos > 0)
    total_personagens = len(pontuacoes_iniciais)
    perguntas_respondidas = sum(
        len(pontuacoes_iniciais[p]) - len(perguntas_respostas.get(p, []))
        for p in pontuacoes_iniciais)
    total_perguntas = sum(
        len(perguntas) for perguntas in pontuacoes_iniciais.values())

    historico_label.config(
        text=
        f"Personagens apresentados: {personagens_apresentados}/{total_personagens}\n"
        f"Perguntas respondidas: {perguntas_respondidas}/{total_perguntas}")


def esconder_todas_frames():
    frame_menu.pack_forget()
    frame_jogo.pack_forget()
    frame_historico.pack_forget()


def sair():
    root.quit()


# Carregar perguntas e respostas do arquivo
nome_arquivo_perguntas = "perguntas_1.txt"
perguntas_respostas = carregar_perguntas_respostas(nome_arquivo_perguntas)
pontuacoes_iniciais = {
    personagem: perguntas[:]
    for personagem, perguntas in perguntas_respostas.items()
}

# Carregar feedbacks do arquivo
nome_arquivo_feedbacks = "feedback.txt"
feedbacks = carregar_feedbacks(nome_arquivo_feedbacks)

# Inicializar dicionário de pontuações para cada personagem
pontuacoes_personagens = {
    personagem: 0
    for personagem in perguntas_respostas.keys()
}

# Criar interface gráfica
root = tk.Tk()
root.title(
    "JOGO DE HABILIDADES SOCIAIS PARA PESSOAS COM TRANSTORNO DO ESPECTRO AUTISTA(TEA)"
)

# Frames
frame_menu = tk.Frame(root)
frame_jogo = tk.Frame(root)
frame_historico = tk.Frame(root)

# Menu
tk.Label(
    frame_menu,
    text=
    "JOGO DE HABILIDADES SOCIAIS PARA PESSOAS COM TRANSTORNO DO ESPECTRO AUTISTA(TEA)",
    font=("Arial", 16, "bold")).pack(pady=20)
tk.Button(frame_menu, text="Jogar", command=mostrar_jogo).pack(pady=10)
tk.Button(frame_menu, text="Histórico",
          command=mostrar_historico).pack(pady=10)
tk.Button(frame_menu, text="Sair", command=sair).pack(pady=10)

# Jogo
explicacao_text = tk.StringVar()

tk.Label(frame_jogo, text="Situação:").pack()
tk.Label(frame_jogo, textvariable=explicacao_text).pack()

pergunta_label = tk.Label(frame_jogo, text="", wraplength=400)
pergunta_label.pack()

respostas_frame = tk.Frame(frame_jogo)
respostas_frame.pack()

botoes_respostas = []
for i in range(4):
    botao = tk.Button(respostas_frame,
                      text="",
                      command=lambda idx=i: verificar_resposta(idx),
                      state=tk.DISABLED)
    botao.pack(fill=tk.X)
    botoes_respostas.append(botao)

tk.Button(frame_jogo, text="Voltar ao Menu",
          command=mostrar_menu).pack(pady=10)

# Histórico
historico_label = tk.Label(frame_historico, text="", font=("Arial", 12))
historico_label.pack(pady=20)

tk.Button(frame_historico, text="Voltar ao Menu",
          command=mostrar_menu).pack(pady=10)

# Iniciar no menu
mostrar_menu()

root.mainloop()
