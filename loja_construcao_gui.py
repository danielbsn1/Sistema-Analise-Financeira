import sqlite3
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DB_NAME = 'loja_construcao.db'

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def setup_db():
    conn = connect_db()
    c = conn.cursor()
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            cliente_id INTEGER,
            data TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            total REAL NOT NULL,
            pago INTEGER NOT NULL,
            FOREIGN KEY(produto_id) REFERENCES Produtos(id),
            FOREIGN KEY(cliente_id) REFERENCES Clientes(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Loja Material de Construção")
        self.create_widgets()

    def create_widgets(self):
        pad = 10
        self.frame_main = ttk.Frame(self.root, padding=pad)
        self.frame_main.pack(fill='both', expand=True)

        ttk.Label(self.frame_main, text="Sistema Loja de Material de Construção", font=("Arial", 18, "bold")).pack(pady=5)

        buttons = [
            ("Cadastrar Produto", self.produto_window),
            ("Listar Produtos", self.listar_produtos),
            ("Cadastrar Cliente", self.cliente_window),
            ("Listar Clientes", self.listar_clientes),
            ("Registrar Venda", self.venda_window),
            ("Registrar Despesa", self.despesa_window),
            ("Listar Vendas", self.listar_vendas),
            ("Relatório de Renda Mensal", lambda: self.calculo_renda('mes')),
            ("Relatório de Renda Anual", lambda: self.calculo_renda('ano')),
            ("Sair", self.root.quit)
        ]

        for text, cmd in buttons:
            ttk.Button(self.frame_main, text=text, command=cmd).pack(fill='x', pady=3)

    def produto_window(self):
        win = tk.Toplevel(self.root)
        win.title("Cadastrar Produto")
        ttk.Label(win, text="Nome do Produto:").pack(pady=5)
        nome_entry = ttk.Entry(win)
        nome_entry.pack(pady=5)

        ttk.Label(win, text="Preço (ex: 15.50):").pack(pady=5)
        preco_entry = ttk.Entry(win)
        preco_entry.pack(pady=5)

        def salvar():
            nome = nome_entry.get().strip()
            preco_str = preco_entry.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Nome do produto é obrigatório.")
                return
            try:
                preco = float(preco_str)
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido.")
                return
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO Produtos (nome, preco) VALUES (?, ?)", (nome, preco))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso.")
            win.destroy()

        ttk.Button(win, text="Salvar", command=salvar).pack(pady=10)

    def listar_produtos(self):
        win = tk.Toplevel(self.root)
        win.title("Lista de Produtos")
        tree = ttk.Treeview(win, columns=("ID", "Nome", "Preço"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço (R$)")

        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, nome, preco FROM Produtos")
        produtos = c.fetchall()
        conn.close()
        for p in produtos:
            tree.insert('', 'end', values=(p[0], p[1], f"{p[2]:.2f}"))

        tree.pack(fill='both', expand=True)

    def cliente_window(self):
        win = tk.Toplevel(self.root)
        win.title("Cadastrar Cliente")
        ttk.Label(win, text="Nome do Cliente:").pack(pady=5)
        nome_entry = ttk.Entry(win)
        nome_entry.pack(pady=5)

        def salvar():
            nome = nome_entry.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Nome do cliente é obrigatório.")
                return
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO Clientes (nome) VALUES (?)", (nome,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso.")
            win.destroy()

        ttk.Button(win, text="Salvar", command=salvar).pack(pady=10)

    def listar_clientes(self):
        win = tk.Toplevel(self.root)
        win.title("Lista de Clientes")
        tree = ttk.Treeview(win, columns=("ID", "Nome"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")

        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, nome FROM Clientes")
        clientes = c.fetchall()
        conn.close()
        for cli in clientes:
            tree.insert('', 'end', values=(cli[0], cli[1]))

        tree.pack(fill='both', expand=True)

    def venda_window(self):
        win = tk.Toplevel(self.root)
        win.title("Registrar Venda")

        ttk.Label(win, text="Selecione o Produto:").pack(pady=5)
        produtos_cmb = ttk.Combobox(win, state="readonly")
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, nome, preco FROM Produtos")
        produtos = c.fetchall()
        conn.close()
        produtos_dict = {f"{p[1]} (R$ {p[2]:.2f})": p for p in produtos}
        produtos_cmb['values'] = list(produtos_dict.keys())
        produtos_cmb.pack(pady=5)

        ttk.Label(win, text="Quantidade:").pack(pady=5)
        qtd_entry = ttk.Entry(win)
        qtd_entry.pack(pady=5)

        ttk.Label(win, text="Tipo de Venda:").pack(pady=5)
        tipo_var = tk.StringVar(value='V')
        frame_tipo = ttk.Frame(win)
        ttk.Radiobutton(frame_tipo, text="À vista", variable=tipo_var, value='V').pack(side='left', padx=5)
        ttk.Radiobutton(frame_tipo, text="A prazo", variable=tipo_var, value='P').pack(side='left', padx=5)
        frame_tipo.pack()

        cliente_cmb = ttk.Combobox(win, state="readonly")
        cliente_cmb.pack(pady=5)
        cliente_cmb.configure(values=[])
        cliente_cmb_label = ttk.Label(win, text="Selecione o Cliente (para venda a prazo):")
        # Show client selection only if a prazo selected
        def tipo_change(*args):
            if tipo_var.get() == 'P':
                cliente_cmb_label.pack(pady=5)
                cliente_cmb.pack(pady=5)
                # Fill clientes
                conn = connect_db()
                c = conn.cursor()
                c.execute("SELECT id, nome FROM Clientes")
                clientes = c.fetchall()
                conn.close()
                clientes_dict = {f"{cli[1]} (ID: {cli[0]})": cli for cli in clientes}
                cliente_cmb['values'] = list(clientes_dict.keys())
            else:
                cliente_cmb_label.pack_forget()
                cliente_cmb.pack_forget()

        tipo_var.trace_add('write', tipo_change)
        tipo_change()

        def salvar():
            produto_sel = produtos_cmb.get()
            if not produto_sel:
                messagebox.showerror("Erro", "Selecione um produto.")
                return
            try:
                quantidade = int(qtd_entry.get())
                if quantidade <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return
            tipo = tipo_var.get()
            cliente_id = None
            if tipo == 'P':
                cliente_sel = cliente_cmb.get()
                if not cliente_sel:
                    messagebox.showerror("Erro", "Selecione um cliente para venda a prazo.")
                    return
                cliente = clientes_dict.get(cliente_sel)
                if not cliente:
                    messagebox.showerror("Erro", "Cliente selecionado inválido.")
                    return
                cliente_id = cliente[0]
            produto = produtos_dict.get(produto_sel)
            if not produto:
                messagebox.showerror("Erro", "Produto selecionado inválido.")
                return
            produto_id = produto[0]
            preco_unitario = produto[2]
            total = preco_unitario * quantidade
            pago = 1 if tipo == 'V' else 0
            data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = connect_db()
            c = conn.cursor()
            c.execute('''
                INSERT INTO Vendas (produto_id, cliente_id, data, quantidade, preco_unitario, total, pago)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (produto_id, cliente_id, data_venda, quantidade, preco_unitario, total, pago))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Venda registrada: {quantidade}x '{produto_sel}' - Total: R$ {total:.2f} - {'Pago' if pago else 'A prazo'}")
            win.destroy()

        ttk.Button(win, text="Registrar Venda", command=salvar).pack(pady=15)

    def despesa_window(self):
        win = tk.Toplevel(self.root)
        win.title("Registrar Despesa")

        ttk.Label(win, text="Descrição da Despesa:").pack(pady=5)
        desc_entry = ttk.Entry(win)
        desc_entry.pack(pady=5)

        ttk.Label(win, text="Valor da Despesa:").pack(pady=5)
        valor_entry = ttk.Entry(win)
        valor_entry.pack(pady=5)

        def salvar():
            descricao = desc_entry.get().strip()
            valor_str = valor_entry.get().strip()
            if not descricao:
                messagebox.showerror("Erro", "Descrição é obrigatória.")
                return
            try:
                valor = float(valor_str)
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")
                return
            data_despesa = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn = connect_db()
            c = conn.cursor()
            c.execute("INSERT INTO Despesas (descricao, valor, data) VALUES (?, ?, ?)", (descricao, valor, data_despesa))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Despesa '{descricao}' registrada no valor de R$ {valor:.2f}")
            win.destroy()

        ttk.Button(win, text="Registrar Despesa", command=salvar).pack(pady=15)

    def listar_vendas(self):
        win = tk.Toplevel(self.root)
        win.title("Vendas Registradas")
        tree = ttk.Treeview(win, columns=("ID", "Produto", "Cliente", "Data", "Qtd", "Unitário", "Total", "Status"),
                            show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
        tree.column("ID", width=30)
        tree.column("Produto", width=150)
        tree.column("Cliente", width=150)
        tree.column("Data", width=140)
        tree.column("Qtd", width=50, anchor='center')
        tree.column("Unitário", width=80, anchor='e')
        tree.column("Total", width=80, anchor='e')
        tree.column("Status", width=80, anchor='center')

        conn = connect_db()
        c = conn.cursor()
        c.execute('''
            SELECT V.id, P.nome, C.nome, V.data, V.quantidade, V.preco_unitario, V.total, V.pago
            FROM Vendas V
            LEFT JOIN Produtos P ON V.produto_id = P.id
            LEFT JOIN Clientes C ON V.cliente_id = C.id
            ORDER BY V.data DESC
        ''')
        vendas = c.fetchall()
        conn.close()
        for v in vendas:
            id_venda, nome_produto, nome_cliente, data_venda, qtd, preco_unit, total, pago = v
            cliente_display = nome_cliente if nome_cliente else "À vista"
            status = "Pago" if pago else "A prazo"
            tree.insert('', 'end', values=(id_venda, nome_produto, cliente_display, data_venda, qtd,
                                           f"R$ {preco_unit:.2f}", f"R$ {total:.2f}", status))
        tree.pack(fill='both', expand=True)

    def calculo_renda(self, periodo='mes'):
        hoje = date.today()
        conn = connect_db()
        c = conn.cursor()

        if periodo == 'mes':
            data_inicio = f"{hoje.year}-{hoje.month:02d}-01"
            data_fim = f"{hoje.year}-{hoje.month:02d}-31"
            periodo_desc = f"Mês {hoje.month:02d}/{hoje.year}"
        elif periodo == 'ano':
            data_inicio = f"{hoje.year}-01-01"
            data_fim = f"{hoje.year}-12-31"
            periodo_desc = f"Ano {hoje.year}"
        else:
            messagebox.showerror("Erro", "Período inválido.")
            conn.close()
            return

        c.execute("SELECT SUM(total) FROM Vendas WHERE pago=1 AND date(data) BETWEEN ? AND ?", (data_inicio, data_fim))
        total_ganho = c.fetchone()[0] or 0.0

        c.execute("SELECT SUM(total) FROM Vendas WHERE pago=0 AND date(data) BETWEEN ? AND ?", (data_inicio, data_fim))
        total_a_prazo = c.fetchone()[0] or 0.0

        c.execute("SELECT SUM(valor) FROM Despesas WHERE date(data) BETWEEN ? AND ?", (data_inicio, data_fim))
        total_gasto = c.fetchone()[0] or 0.0

        saldo = total_ganho - total_gasto

        texto = (
            f"Relatório de Renda - {periodo_desc}\n\n"
            f"Ganhos à vista: R$ {total_ganho:.2f}\n"
            f"Ganhos a prazo (pendentes): R$ {total_a_prazo:.2f}\n"
            f"Total ganho (à vista + a prazo): R$ {(total_ganho + total_a_prazo):.2f}\n"
            f"Total gasto: R$ {total_gasto:.2f}\n"
            f"Saldo (ganhos à vista - gastos): R$ {saldo:.2f}"
        )
        messagebox.showinfo("Relatório de Renda", texto)
        conn.close()

if __name__ == '__main__':
    setup_db()
    root = tk.Tk()
    app = LojaApp(root)
    root.mainloop()


