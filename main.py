import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import font as tkfont
import pandas as pd
from datetime import datetime
import webbrowser

class SistemaFrango:
    def __init__(self, root, imagem_fundo):
        self.root = root
        self.root.title("Sistema de Comércio de Frango")
        self.background_image = ImageTk.PhotoImage(imagem_fundo)
        self.background = tk.Canvas(root, width=1366, height=768)
        self.background.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.background.grid(row=0, column=0, columnspan=10, rowspan=6)
        self.background.configure(bg="goldenrod")

        # Adicionando um quadrado para exibir a data e hora no canto superior direito
        self.quadrado_data_hora = self.background.create_rectangle(1166, 20, 1316, 130, fill='white', outline='black')
        self.label_data = self.background.create_text(1241, 60, text="", font=('Helvetica', 14), fill='black')
        self.label_hora = self.background.create_text(1241, 100, text="", font=('Helvetica', 14), fill='black')
        self.atualizar_data_hora()

###########################################################################################################
#CARREGANDO PLANILHAS
        try:
            self.df = pd.read_excel("vendas_confirmadas.xlsx")
        except FileNotFoundError:
            pass

        try:
            self.df_despesas = pd.read_excel("despesas_registradas.xlsx")
        except FileNotFoundError:
            pass

        try:
            self.df_vendas_fiado = pd.read_excel("vendas_fiado.xlsx")
        except FileNotFoundError:
            pass

        try:
            self.df_vendas_frangovivo = pd.read_excel("vendas_frangovivo.xlsx")
        except FileNotFoundError:
            pass
###############################################################################################

        # Criar um estilo para o botão com a fonte desejada
        estilo = ttk.Style()
        estilo.configure('EstiloBotao.TButton', font=('Helvetica', 14), background='yellow',
                         state='normal',
                         justify='center',
                         borderwidth='3', relief="raised")

        # Adicionando tratador de eventos para fechamento da janela principal
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        # LOGIN
        self.usuarios = {'': ''}
        self.interface_iniciada = False
        self.iniciar_login()

    def atualizar_data_hora(self):
        data_atual = datetime.now().strftime('%Y-%m-%d')
        hora_atual = datetime.now().strftime('%H:%M:%S')

        self.background.itemconfig(self.label_data, text=data_atual)
        self.background.itemconfig(self.label_hora, text=hora_atual)

        self.root.after(1000, self.atualizar_data_hora)

    def iniciar_login(self):
        self.janela_login = tk.Toplevel(self.root)
        self.janela_login.title("Login")
        self.janela_login.geometry("300x150+500+300")
        self.janela_login.transient(self.root)

        ttk.Label(self.janela_login, text="Usuário:").grid(row=0, column=0, padx=10, pady=5)
        self.usuario_entry = ttk.Entry(self.janela_login)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.janela_login, text="Senha:").grid(row=1, column=0, padx=10, pady=5)
        self.senha_entry = ttk.Entry(self.janela_login, show='*')
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)

        botao_login = ttk.Button(self.janela_login, text="Login", command=self.realizar_login)
        botao_login.grid(row=2, column=0, columnspan=2, pady=10)

    def realizar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if usuario in self.usuarios and self.usuarios[usuario] == senha:
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.janela_login.destroy()
            self.interface_iniciada = True
            self.criar_interface()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas. Tente novamente.")

    def criar_interface(self):
        # Frame para os botões
        botoes_frame = ttk.Frame(self.root)
        botoes_frame.grid(row=0, column=0, padx=20, pady=(2, 2), sticky='w')

        # Título Ferramentas
        titulo_texto = "Ferramentas"
        titulo_cor = 'black'
        titulo_fonte = ('Helvetica', 20, 'bold')
        title_label = ttk.Label(botoes_frame, text=titulo_texto, font=titulo_fonte, foreground=titulo_cor)
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # Botões
        botoes = [
            ("Venda", self.abrir_janela_venda),
            ("Vendas - Frango Vivo", self.abrir_janela_venda_frango_vivo),
            ("Despesas", self.abrir_janela_despesas),
            ("Venda Fiado", self.abrir_janela_fiado),
            ("Relatório Diário", self.relatorio_diario),
            ("Verificar Devedores", self.verificar_devedores),
            ("Conferir Resultados", self.abrir_powerbi)
        ]

        for i, (texto, comando) in enumerate(botoes, start=1):
            botao = ttk.Button(botoes_frame, text=texto, command=comando, style='EstiloBotao.TButton')
            botao.grid(row=i, column=0, sticky='w', padx=10, pady=5)

        # Configuração do redimensionamento responsivo
        botoes_frame.grid_rowconfigure((0, len(botoes)), weight=1)
        botoes_frame.grid_columnconfigure(0, weight=1)

    def abrir_powerbi(self):
        webbrowser.open_new_tab(
            "https://app.powerbi.com/view?r=eyJrIjoiZWEwMzIxMTAtYTZiZS00ZjQzLWI1MjQtZjFhNzljMDg0ZGFkIiwidCI6IjljOTQ2MjBlLTUwZWEtNGIzOS04MWZiLWVjOTMwNTBmMjQ4OSJ9")

    def abrir_janela_venda_frango_vivo(self):
        try:
            self.df_vendas_frangovivo = pd.read_excel("vendas_frangovivo.xlsx")
        except FileNotFoundError:
            self.df_vendas_frangovivo = pd.DataFrame(columns=['Data', 'Quilos', 'Forma de Pagamento', 'Valor'])
        # Criar a janela de vendas de frango vivo
        self.janela_venda_frango_vivo = tk.Toplevel(self.root)
        self.janela_venda_frango_vivo.title("Registrar Venda - Frango Vivo")
        self.janela_venda_frango_vivo.geometry("500x300+400+200")
        fonte = tkfont.Font(family="Helvetica", size=12)
        self.janela_venda_frango_vivo.configure(bg="white")

        # Adicionar imagem à janela de vendas de frango vivo
        imagem_vendas = Image.open("fundo10.png")
        imagem_vendas = imagem_vendas.resize((500, 300), Image.LANCZOS)
        imagem_vendas = ImageTk.PhotoImage(imagem_vendas)
        label_imagem_vendas = tk.Label(self.janela_venda_frango_vivo, image=imagem_vendas)
        label_imagem_vendas.image = imagem_vendas
        label_imagem_vendas.place(x=0, y=0, relwidth=1, relheight=1)

        # Label e Entry para Quilos
        ttk.Label(self.janela_venda_frango_vivo, text="Quilos vendidos:", font=fonte, background="white", ).pack(pady=5)
        self.quilos_entry_frango_vivo = ttk.Entry(self.janela_venda_frango_vivo)
        self.quilos_entry_frango_vivo.pack(pady=5)

        # Label e Combobox para Forma de Pagamento
        ttk.Label(self.janela_venda_frango_vivo, text="Forma de pagamento:", font=fonte, background="white").pack(
            pady=5)
        self.forma_pagamento_combobox_frango_vivo = ttk.Combobox(self.janela_venda_frango_vivo,
                                                                 values=["Dinheiro", "Cartão", "Pix"],
                                                                 state="readonly")
        self.forma_pagamento_combobox_frango_vivo.pack(pady=5)

        # Label e Entry para Valor
        ttk.Label(self.janela_venda_frango_vivo, text="Valor:", font=fonte, background="white").pack(pady=5)
        self.valor_entry_frango_vivo = ttk.Entry(self.janela_venda_frango_vivo)
        self.valor_entry_frango_vivo.pack(pady=5)

        # Botão de Confirmar Venda de Frango Vivo
        botao_confirmar_frango_vivo = ttk.Button(self.janela_venda_frango_vivo, text="Confirmar Venda de Frango Vivo",
                                                 command=self.registrar_venda_frango_vivo)
        botao_confirmar_frango_vivo.pack(pady=10)

        # Configurar a fonte para o botão
        botao_confirmar_frango_vivo.configure(style='EstiloBotao.TButton')

    def registrar_venda_frango_vivo(self):
        # Obter os valores das entradas
        quilos_str = self.quilos_entry_frango_vivo.get()
        valor_str = self.valor_entry_frango_vivo.get()

        # Verificar se todos os campos estão preenchidos
        if not quilos_str or not valor_str or not self.forma_pagamento_combobox_frango_vivo.get():
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Substituir vírgula por ponto
        quilos_str = quilos_str.replace(',', '.')
        valor_str = valor_str.replace(',', '.')

        try:
            # Converter strings para float
            quilos = float(quilos_str)
            valor = float(valor_str)
        except ValueError:
            # Se a conversão falhar, mostrar mensagem de erro
            messagebox.showerror("Erro", "Os valores de quilos ou valor não são válidos.")
            return

        forma_pagamento = self.forma_pagamento_combobox_frango_vivo.get()

        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar venda de frango vivo ao DataFrame
        venda_frango_vivo = [data_atual, quilos, forma_pagamento, valor]
        self.df_vendas_frangovivo.loc[len(self.df_vendas_frangovivo)] = venda_frango_vivo

        # Limpar os campos após a venda de frango vivo
        self.quilos_entry_frango_vivo.delete(0, 'end')
        self.forma_pagamento_combobox_frango_vivo.set('')
        self.valor_entry_frango_vivo.delete(0, 'end')

        self.salvar_vendas_frango_vivo_em_excel()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Venda de Frango Vivo registrada com sucesso!")

        # Fechar a janela após a venda ser registrada
        self.janela_venda_frango_vivo.destroy()

    def salvar_vendas_frango_vivo_em_excel(self):
        try:
            # Escolha o local e o nome do arquivo Excel onde deseja salvar as vendas de frango vivo
            nome_arquivo = "vendas_frangovivo.xlsx"

            # Salva o DataFrame de vendas de frango vivo em um arquivo Excel
            self.df_vendas_frangovivo.to_excel(nome_arquivo, index=False)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as vendas de frango vivo em Excel: {e}")

    def abrir_janela_fiado(self):
        try:
            self.df_vendas_fiado = pd.read_excel("vendas_fiado.xlsx")
        except FileNotFoundError:
            self.df_vendas_fiado = pd.DataFrame(columns=['Data', 'Cliente', 'Telefone', 'Tipo', 'Valor', 'Quilos'])

        # Criar a janela de vendas fiado
        janela_fiado = tk.Toplevel(self.root)
        janela_fiado.title("Registrar Venda Fiado")
        janela_fiado.geometry("500x500+400+200")
        fonte = tk.font.Font(family="Helvetica", size=12)
        janela_fiado.configure(bg="white")

        # Adicionar imagem à janela de vendas fiado
        imagem_fiado = Image.open("fundo10.png")
        imagem_fiado = imagem_fiado.resize((500, 500), Image.LANCZOS)
        imagem_fiado = ImageTk.PhotoImage(imagem_fiado)
        label_imagem_fiado = tk.Label(janela_fiado, image=imagem_fiado)
        label_imagem_fiado.image = imagem_fiado
        label_imagem_fiado.place(x=0, y=0, relwidth=1, relheight=1)

        # Label e Entry para Nome do cliente
        ttk.Label(janela_fiado, text="Nome do Cliente:", font=fonte, background="white").pack(pady=5)
        self.nome_cliente_entry = ttk.Combobox(janela_fiado)
        self.nome_cliente_entry.pack(pady=5)
        self.nome_cliente_entry.bind("<<ComboboxFocusOut>>", self.atualizar_telefone)
        self.nome_cliente_entry.bind('<KeyRelease>', self.atualizar_sugestoes_clientes)
        self.nome_cliente_entry.bind("<<ComboboxSelected>>", self.atualizar_telefone)

        # Label e Entry para Telefone do cliente
        ttk.Label(janela_fiado, text="Telefone do Cliente:", font=fonte, background="white").pack(pady=5)
        self.telefone_cliente_entry = ttk.Entry(janela_fiado)
        self.telefone_cliente_entry.pack(pady=5)

        # Label e Combobox para Tipo de venda
        ttk.Label(janela_fiado, text="Tipo de venda:", font=fonte, background="white").pack(pady=5)
        self.tipo_combobox_fiado = ttk.Combobox(janela_fiado, values=["Fiado", "Pagamento"], state="readonly")
        self.tipo_combobox_fiado.pack(pady=5)

        # Label e Entry para Quilos
        ttk.Label(janela_fiado, text="Quilos:", font=fonte, background="white").pack(pady=5)
        self.quilos_entry_fiado = ttk.Entry(janela_fiado)
        self.quilos_entry_fiado.pack(pady=5)

        # Label e Entry para Valor
        ttk.Label(janela_fiado, text="Valor:", font=fonte, background="white").pack(pady=5)
        self.valor_entry_fiado = ttk.Entry(janela_fiado)
        self.valor_entry_fiado.pack(pady=5)

        # Label e Combobox para Origem da venda
        ttk.Label(janela_fiado, text="Origem da Venda:", font=fonte, background="white").pack(pady=5)
        self.origem_combobox_fiado = ttk.Combobox(janela_fiado, values=["Comércio", "Mesa", "Frango Vivo"],
                                                  state="readonly")
        self.origem_combobox_fiado.pack(pady=5)

        # Botão de Confirmar Venda Fiado
        botao_confirmar_fiado = ttk.Button(janela_fiado, text="Confirmar Venda Fiado",
                                           command=lambda: self.registrar_venda_fiado(janela_fiado))
        botao_confirmar_fiado.pack(pady=10)

        # Configurar a fonte para o botão
        botao_confirmar_fiado.configure(style='EstiloBotao.TButton')

        # Adicionando a chamada do método para atualizar o estado do campo de Quilos
        self.tipo_combobox_fiado.bind("<<ComboboxSelected>>", self.atualizar_estado_quilos)

    def atualizar_telefone(self, event):
        # Obter o nome do cliente selecionado
        nome_cliente_selecionado = self.nome_cliente_entry.get()

        # Procurar o telefone correspondente ao cliente selecionado no DataFrame
        telefone_cliente = self.df_vendas_fiado.loc[
            self.df_vendas_fiado['Cliente'] == nome_cliente_selecionado.lower(), 'Telefone'].values

        # Verificar se há algum telefone encontrado
        if telefone_cliente.size > 0:
            # Se o telefone for encontrado, atualizar o campo de entrada de telefone
            self.telefone_cliente_entry.delete(0, tk.END)
            self.telefone_cliente_entry.insert(0, telefone_cliente[0])

    def atualizar_sugestoes_clientes(self, event):
        texto_digitado = self.nome_cliente_entry.get()
        sugestoes = self.obter_sugestoes_clientes(texto_digitado)
        self.nome_cliente_entry['values'] = sugestoes

    def obter_sugestoes_clientes(self, texto_digitado):
        # Usar as informações do DataFrame para sugestões de clientes únicos
        clientes_registrados = self.df_vendas_fiado['Cliente'].unique().tolist()
        sugestoes = []

        # Verificar se o texto digitado corresponde a algum cliente registrado
        for cliente in clientes_registrados:
            if cliente.lower().startswith(texto_digitado.lower()):
                sugestoes.append(cliente.capitalize())  # Manter a primeira letra maiúscula

        return sugestoes

    def registrar_venda_fiado(self, janela_fiado):
        # Obter os valores das entradas
        nome_cliente = self.nome_cliente_entry.get().lower()  # Converter para minúsculas
        telefone_cliente = self.telefone_cliente_entry.get()
        valor_str = self.valor_entry_fiado.get()
        origem = self.origem_combobox_fiado.get()

        # Substituir vírgula por ponto
        valor_str = valor_str.replace(',', '.')

        try:
            # Converter strings para float
            valor = float(valor_str)
        except ValueError:
            # Se a conversão falhar, mostrar mensagem de erro
            messagebox.showerror("Erro", "O valor não é válido.")
            return

        tipo = self.tipo_combobox_fiado.get()

        # Desativar o campo de Quilos se o tipo for "pagamento"
        if tipo == "Pagamento":
            self.quilos_entry_fiado.config(state='disabled')
            self.quilos_entry_fiado.delete(0, 'end')  # Limpar o campo, se houver algo digitado
            quilos = None  # Definir quilos como nulo
        else:
            self.quilos_entry_fiado.config(state='normal')
            quilos_str = self.quilos_entry_fiado.get()
            if not quilos_str:
                messagebox.showerror("Erro", "Por favor, preencha o campo Quilos.")
                return
            # Substituir vírgula por ponto
            quilos_str = quilos_str.replace(',', '.')
            try:
                # Converter string para float
                quilos = float(quilos_str)
            except ValueError:
                # Se a conversão falhar, mostrar mensagem de erro
                messagebox.showerror("Erro", "O valor de Quilos não é válido.")
                return

        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar venda fiado ao DataFrame
        venda_fiado = [data_atual, nome_cliente, telefone_cliente, tipo, valor, quilos, origem]
        self.df_vendas_fiado.loc[len(self.df_vendas_fiado)] = venda_fiado

        # Limpar os campos após a venda fiado
        self.nome_cliente_entry.delete(0, 'end')
        self.telefone_cliente_entry.delete(0, 'end')
        self.tipo_combobox_fiado.set('')
        self.origem_combobox_fiado.set('')  # Limpe a origem após a venda
        self.quilos_entry_fiado.delete(0, 'end')
        self.valor_entry_fiado.delete(0, 'end')

        self.salvar_vendas_fiado_em_excel()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Venda fiado registrada com sucesso!")

        # Fechar a janela após registrar a venda
        janela_fiado.destroy()

    def atualizar_estado_quilos(self, event):
        # Obter o tipo de venda selecionado
        tipo_venda_selecionado = self.tipo_combobox_fiado.get()
        if tipo_venda_selecionado == "Pagamento":
            # Desativar o campo de Quilos e torná-lo readonly
            self.quilos_entry_fiado.config(state='disabled')
            # Desativar o campo de Origem
            self.origem_combobox_fiado.config(state='disabled')
            self.origem_combobox_fiado.set('')  # Limpar o campo de Origem
        elif tipo_venda_selecionado == "Fiado":
            # Ativar o campo de Quilos
            self.quilos_entry_fiado.config(state='normal')
            # Ativar o campo de Origem
            self.origem_combobox_fiado.config(state='normal')

    def salvar_vendas_fiado_em_excel(self):
        try:
            # Escolha o local e o nome do arquivo Excel onde deseja salvar as vendas fiado
            nome_arquivo = "vendas_fiado.xlsx"

            # Salva o DataFrame de vendas fiado em um arquivo Excel
            self.df_vendas_fiado.to_excel(nome_arquivo, index=False)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as vendas fiado em Excel: {e}")

    def verificar_devedores(self):
        try:
            self.df_vendas_fiado = pd.read_excel("vendas_fiado.xlsx")
        except FileNotFoundError:
            self.df_vendas_fiado = pd.DataFrame(columns=['Data', 'Cliente', 'Telefone', 'Tipo', 'Valor'])

        janela_devedores = tk.Toplevel(self.root)
        janela_devedores.title("Verificar Devedores")
        janela_devedores.geometry("500x300+400+200")

        # Carregar a imagem
        imagem_devedores = Image.open("fundo10.png")
        imagem_devedores = imagem_devedores.resize((500, 300), Image.LANCZOS)
        imagem_devedores = ImageTk.PhotoImage(imagem_devedores)

        # Criar um rótulo para a imagem e exibir a imagem
        label_imagem_devedores = tk.Label(janela_devedores, image=imagem_devedores)
        label_imagem_devedores.image = imagem_devedores
        label_imagem_devedores.place(x=0, y=0, relwidth=1, relheight=1)

        # Atualizar a interface gráfica
        janela_devedores.update()

        saldo_clientes = self.calcular_saldo_clientes()

        tabela_devedores = ttk.Treeview(janela_devedores, columns=('Nome', 'Saldo'), show='headings')
        tabela_devedores.heading('Nome', text='Nome do Cliente')
        tabela_devedores.heading('Saldo', text='Saldo Devedor')
        tabela_devedores.pack(fill='both', expand=True)

        for cliente, saldo in saldo_clientes.items():
            tabela_devedores.insert('', 'end', values=(cliente, saldo))

    def calcular_saldo_clientes(self):
        # Filtrar vendas por tipo: "Fiado" e "Pagamento"
        vendas_fiado = self.df_vendas_fiado[self.df_vendas_fiado['Tipo'] == 'Fiado']
        vendas_pagamento = self.df_vendas_fiado[self.df_vendas_fiado['Tipo'] == 'Pagamento']

        # Calcular o saldo para cada cliente
        clientes = vendas_fiado['Cliente'].unique()
        saldo_clientes = {}

        # Calcular o saldo fiado para cada cliente
        for cliente in clientes:
            saldo_fiado = vendas_fiado[vendas_fiado['Cliente'] == cliente]['Valor'].sum()
            saldo_clientes[cliente] = saldo_fiado

        # Subtrair os pagamentos do saldo fiado
        for _, pagamento in vendas_pagamento.iterrows():
            cliente = pagamento['Cliente']
            valor_pagamento = pagamento['Valor']
            saldo_clientes[cliente] -= valor_pagamento

        # Definir saldo como zero se for negativo
        for cliente, saldo in saldo_clientes.items():
            saldo_clientes[cliente] = max(0, saldo)

        return saldo_clientes

    def relatorio_diario(self):
        # Obter a data atual no formato 'YYYY-MM-DD'
        data_atual = datetime.now().strftime('%Y-%m-%d')

        # Ler os dados das planilhas de venda e despesa
        vendas_df = pd.read_excel("vendas_confirmadas.xlsx")
        despesas_df = pd.read_excel("despesas_registradas.xlsx")

        # Ler os dados da planilha de vendas fiado
        try:
            vendas_fiado_df = pd.read_excel("vendas_fiado.xlsx")
        except FileNotFoundError:
            vendas_fiado_df = pd.DataFrame(columns=['Data', 'Cliente', 'Telefone', 'Tipo', 'Valor'])

            # Ler os dados da planilha de vendas de frango vivo
        try:
            vendas_frango_vivo_df = pd.read_excel("vendas_frangovivo.xlsx")
        except FileNotFoundError:
            vendas_frango_vivo_df = pd.DataFrame(columns=['Data', 'Quilos', 'Forma de Pagamento', 'Valor'])



        # Filtrar os dados para incluir apenas as vendas do dia atual
        vendas_frango_vivo_df = vendas_frango_vivo_df[vendas_frango_vivo_df['Data'].str.startswith(data_atual) | vendas_frango_vivo_df['Data'].isnull()]
        vendas_do_dia = vendas_df[vendas_df['Data'].str.startswith(data_atual) | vendas_df['Data'].isnull()]
        despesas_do_dia = despesas_df[despesas_df['Data'].str.startswith(data_atual) | despesas_df['Data'].isnull()]
        # Filtrar as vendas fiado do dia atual excluindo aquelas do tipo "pagamento"
        vendas_fiado_do_dia = vendas_fiado_df[
            (vendas_fiado_df['Data'].str.startswith(data_atual) | vendas_fiado_df['Data'].isnull()) &
            (vendas_fiado_df['Tipo'] != 'Pagamento')]



        # Calcular informações necessárias
        quilos_vendidos = vendas_do_dia['Quilos'].sum() + vendas_fiado_do_dia['Quilos'].sum() + vendas_frango_vivo_df[
            'Quilos'].sum()
        venda_dinheiro = vendas_do_dia[vendas_do_dia['Forma de Pagamento'] == 'Dinheiro']['Valor'].sum()
        venda_cartao = vendas_do_dia[vendas_do_dia['Forma de Pagamento'] == 'Cartão']['Valor'].sum()
        venda_pix = vendas_do_dia[vendas_do_dia['Forma de Pagamento'] == 'Pix']['Valor'].sum()
        despesas_totais = despesas_do_dia['Valor'].sum()
        venda_fiado_total = vendas_fiado_do_dia['Valor'].sum()
        venda_frango_vivo_total = vendas_frango_vivo_df['Valor'].sum()

        # Criar uma nova janela para exibir o relatório diário
        relatorio_window = tk.Toplevel(self.root)
        relatorio_window.geometry("500x500")
        relatorio_window.title("Relatório Diário")

        # Carregar a imagem de fundo
        imagem_fundo_relatorio = Image.open("fundo10.png")
        largura, altura = 500, 500
        imagem_fundo_relatorio = imagem_fundo_relatorio.resize((largura, altura), Image.LANCZOS)
        imagem_fundo_relatorio = ImageTk.PhotoImage(imagem_fundo_relatorio)

        # Configurar a imagem como plano de fundo da janela
        label_fundo_relatorio = tk.Label(relatorio_window, image=imagem_fundo_relatorio)
        label_fundo_relatorio.place(x=0, y=0, relwidth=1, relheight=1)

        # Garantir que a imagem não seja destruída pelo coletor de lixo
        label_fundo_relatorio.image = imagem_fundo_relatorio

        # Adicionar um título
        titulo_label = ttk.Label(relatorio_window, text="Relatório Diário", font=('Helvetica', 24, 'bold'),
                                 background="white", foreground="navy")
        titulo_label.pack(pady=10)

        # Adicionar uma seção para vendas
        ttk.Label(relatorio_window, text="Vendas Comercio e Mesa", font=('Helvetica', 16, 'bold'), background="white").pack(
            pady=5)
        ttk.Label(relatorio_window, text=f"Quilos Vendidos (Total): {quilos_vendidos}", font=('Helvetica', 14),
                  background="white").pack()
        ttk.Label(relatorio_window, text=f"Venda em Dinheiro: R${venda_dinheiro}", font=('Helvetica', 14),
                  background="white").pack()
        ttk.Label(relatorio_window, text=f"Venda em Cartão: R${venda_cartao}", font=('Helvetica', 14),
                  background="white").pack()
        ttk.Label(relatorio_window, text=f"Venda em Pix: R${venda_pix}", font=('Helvetica', 14),
                  background="white").pack()
        tk.Label(relatorio_window, text="Vendas Fiado (Total)", font=('Helvetica', 16, 'bold'),
                 background="white").pack(
            pady=5)
        ttk.Label(relatorio_window, text=f"Vendas Fiado: R${venda_fiado_total}", font=('Helvetica', 14),
                  background="white").pack()
        ttk.Label(relatorio_window, text="Vendas de Frango Vivo", font=('Helvetica', 16, 'bold'),
                  background="white").pack(
            pady=5)
        ttk.Label(relatorio_window, text=f"Venda Frango Vivo: R${venda_frango_vivo_total}", font=('Helvetica', 14),
                  background="white").pack()

        # Adicionar uma linha separadora
        ttk.Separator(relatorio_window, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # Adicionar uma seção para despesas
        ttk.Label(relatorio_window, text="Despesas do Dia", font=('Helvetica', 16, 'bold'), background="white").pack(
            pady=5)
        ttk.Label(relatorio_window, text=f"Despesas Totais: R${despesas_totais}", font=('Helvetica', 14),
                  background="white").pack()

        # Adicionar um botão para fechar a janela
        fechar_button = ttk.Button(relatorio_window, text="Fechar", command=relatorio_window.destroy)
        fechar_button.pack(pady=20)

    def abrir_janela_despesas(self):
        # Criar a janela de despesas
        janela_despesas = tk.Toplevel(self.root)
        janela_despesas.title("Registrar Despesas")
        janela_despesas.geometry("500x300+400+200")
        fonte = tkfont.Font(family="Helvetica", size=12)

        # Carregar a imagem de fundo
        imagem_fundo_despesas = Image.open("fundo10.png")
        imagem_fundo_despesas = imagem_fundo_despesas.resize((500, 300), Image.LANCZOS)
        imagem_fundo_despesas = ImageTk.PhotoImage(imagem_fundo_despesas)

        # Configurar a imagem como plano de fundo da janela
        label_fundo_despesas = tk.Label(janela_despesas, image=imagem_fundo_despesas)
        label_fundo_despesas.place(x=0, y=0, relwidth=1, relheight=1)

        # Garantir que a imagem não seja destruída pelo coletor de lixo
        label_fundo_despesas.image = imagem_fundo_despesas

        # Label e Entry para Valor
        ttk.Label(janela_despesas, text="Valor:", font=fonte).pack(pady=5)
        self.valor_entry_despesa = ttk.Entry(janela_despesas)
        self.valor_entry_despesa.pack(pady=5)

        # Label e Combobox para Tipo de Despesa
        ttk.Label(janela_despesas, text="Tipo de Despesa:", font=fonte).pack(pady=5)
        self.tipo_despesa_combobox = ttk.Combobox(janela_despesas,
                                                  values=["Salário", "Merenda", "Gasolina", "Despesas em Gerais"],
                                                  state="readonly")
        self.tipo_despesa_combobox.pack(pady=5)

        # Botão de Confirmar Despesa
        botao_confirmar_despesa = ttk.Button(janela_despesas, text="Confirmar Despesa",
                                             command=lambda: self.registrar_despesa(janela_despesas))
        botao_confirmar_despesa.pack(pady=10)

        # Configurar a fonte para o botão
        botao_confirmar_despesa.configure(style='EstiloBotao.TButton')

    def registrar_despesa(self, janela_despesas):
        try:
            # Obter os valores das entradas
            valor_str = self.valor_entry_despesa.get()
            tipo_despesa = self.tipo_despesa_combobox.get()

            # Verificar se todos os campos estão preenchidos
            if not valor_str or not tipo_despesa:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            # Substituir vírgula por ponto
            valor_str = valor_str.replace(',', '.')

            # Converter strings para float
            valor = float(valor_str)
        except ValueError:
            # Se a conversão falhar, mostrar mensagem de erro
            messagebox.showerror("Erro", "O valor da despesa não é válido.")
            return

        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar despesa ao DataFrame de despesas
        despesa = [data_atual, tipo_despesa, valor]
        self.df_despesas.loc[len(self.df_despesas)] = despesa

        # Limpar os campos após a despesa
        self.valor_entry_despesa.delete(0, 'end')
        self.tipo_despesa_combobox.set('')

        self.salvar_despesas_em_excel()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Despesa registrada com sucesso!")

        # Fechar a janela de despesas após o registro
        janela_despesas.destroy()

    def salvar_despesas_em_excel(self):
        # Salva o DataFrame de despesas no arquivo

        self.df_despesas.to_excel("despesas_registradas.xlsx", index=False)

    def fechar_janela(self):
        # Antes de fechar, salva as informações
        self.salvar_despesas_em_excel()
        # Fecha a janela
        self.root.destroy()

    def abrir_janela_venda(self):
        # Criar a janela de vendas
        janela_venda = tk.Toplevel(self.root)
        janela_venda.title("Registrar Venda")
        janela_venda.geometry("500x300+400+200")
        fonte = tkfont.Font(family="Helvetica", size=12)
        janela_venda.configure(bg="white")

        # Adicionar imagem à janela de vendas
        imagem_vendas = Image.open("fundo10.png")
        imagem_vendas = imagem_vendas.resize((500, 300), Image.LANCZOS)
        imagem_vendas = ImageTk.PhotoImage(imagem_vendas)
        label_imagem_vendas = tk.Label(janela_venda, image=imagem_vendas)
        label_imagem_vendas.image = imagem_vendas
        label_imagem_vendas.place(x=0, y=0, relwidth=1, relheight=1)

        # Label e Entry para Quilos
        ttk.Label(janela_venda, text="Quilos vendidos:", font=fonte, background="white", ).pack(pady=5)
        self.quilos_entry = ttk.Entry(janela_venda)
        self.quilos_entry.pack(pady=5)

        # Label e Combobox para Tipo de venda
        ttk.Label(janela_venda, text="Tipo de venda:", font=fonte, background="white").pack(pady=5)
        self.tipo_combobox = ttk.Combobox(janela_venda, values=["Comércio", "Mesa"], state="readonly")
        self.tipo_combobox.pack(pady=5)

        # Label e Combobox para Forma de Pagamento
        ttk.Label(janela_venda, text="Forma de pagamento:", font=fonte, background="white").pack(pady=5)
        self.forma_pagamento_combobox = ttk.Combobox(janela_venda, values=["Dinheiro", "Cartão", "Pix"],
                                                     state="readonly")
        self.forma_pagamento_combobox.pack(pady=5)

        # Label e Entry para Valor
        ttk.Label(janela_venda, text="Valor:", font=fonte, background="white").pack(pady=5)
        self.valor_entry = ttk.Entry(janela_venda)
        self.valor_entry.pack(pady=5)

        # Botão de Confirmar Venda
        botao_confirmar = ttk.Button(janela_venda, text="Confirmar Venda",
                                     command=lambda: self.registrar_venda(janela_venda))
        botao_confirmar.pack(pady=10)

        # Configurar a fonte para o botão
        botao_confirmar.configure(style='EstiloBotao.TButton')

    def registrar_venda(self, janela_venda):
        # Obter os valores das entradas
        quilos_str = self.quilos_entry.get()
        valor_str = self.valor_entry.get()

        # Verificar se todos os campos estão preenchidos
        if not quilos_str or not valor_str or not self.tipo_combobox.get() or not self.forma_pagamento_combobox.get():
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        # Substituir vírgula por ponto
        quilos_str = quilos_str.replace(',', '.')
        valor_str = valor_str.replace(',', '.')

        try:
            # Converter strings para float
            quilos = float(quilos_str)
            valor = float(valor_str)
        except ValueError:
            # Se a conversão falhar, mostrar mensagem de erro
            messagebox.showerror("Erro", "Os valores de quilos ou valor não são válidos.")
            return

        tipo = self.tipo_combobox.get()
        forma_pagamento = self.forma_pagamento_combobox.get()

        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Adicionar venda ao DataFrame
        self.df.loc[len(self.df)] = [data_atual, tipo, quilos, forma_pagamento, valor]

        # Limpar os campos após a venda
        self.quilos_entry.delete(0, 'end')
        self.tipo_combobox.set('')
        self.forma_pagamento_combobox.set('')
        self.valor_entry.delete(0, 'end')

        self.salvar_em_excel()

        # Exibir mensagem de sucesso
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")

        # Fechar a janela após a venda
        janela_venda.destroy()

    def salvar_em_excel(self):
        # Salva o DataFrame de vendas no arquivo
        self.df.to_excel("vendas_confirmadas.xlsx", index=False)

    def fechar_programa(self):
        self.root.destroy()

if __name__ == "__main__":
    imagem_fundo = Image.open("logo3.jpeg")
    imagem_fundo = imagem_fundo.resize((1366, 768), Image.LANCZOS)
    root = tk.Tk()
    app = SistemaFrango(root, imagem_fundo)
    root.mainloop()


