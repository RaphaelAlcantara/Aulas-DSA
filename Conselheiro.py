# -*- coding: utf-8 -*-
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from deep_translator import GoogleTranslator

API_URL = "https://api.adviceslip.com/advice"


def traduzir(texto_en):
    try:
        return GoogleTranslator(source="en", target="pt").translate(texto_en)
    except Exception:
        return texto_en  # fallback se a tradução falhar


def pegar_conselho_async(btn, var_texto):
    def tarefa():
        try:
            resp = requests.get(API_URL, timeout=10)
            resp.raise_for_status()
            dados = json.loads(resp.content)
            frase_en = dados["slip"]["advice"]
            frase_pt = traduzir(frase_en)
            var_texto.set(frase_pt)
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Não consegui pegar o conselho.\n\nDetalhes: {e}")
        finally:
            btn.config(state=tk.NORMAL, text="Pegar conselho")
    threading.Thread(target=tarefa, daemon=True).start()


def on_click(btn, var_texto):
    btn.config(state=tk.DISABLED, text="Carregando...")
    var_texto.set("")
    pegar_conselho_async(btn, var_texto)


def main():
    root = tk.Tk()
    root.title("Conselheiro ✨")
    root.geometry("600x320")
    root.minsize(500, 260)

    container = ttk.Frame(root, padding=16)
    container.pack(fill="both", expand=True)

    # fonte maior para todos os elementos
    fonte_titulo = ("Segoe UI", 20, "bold")
    fonte_botao = ("Segoe UI", 14)
    fonte_texto = ("Segoe UI", 14)

    titulo = ttk.Label(
        container, text="Precisa de um conselho?", font=fonte_titulo)
    titulo.pack(anchor="w", pady=(0, 12))

    var_texto = tk.StringVar()

    btn = ttk.Button(container, text="Pegar conselho",
                     command=lambda: on_click(btn, var_texto))
    btn.pack(anchor="w", pady=(0, 12))
    btn.config(width=20)
    btn["style"] = "Botao.TButton"

    # caixa de texto
    caixa = tk.Text(container, wrap="word", height=8, font=fonte_texto)
    caixa.pack(fill="both", expand=True, pady=(0, 0))

    # vincular a StringVar à caixa
    def atualizar_caixa(*_):
        caixa.config(state="normal")
        caixa.delete("1.0", tk.END)
        texto = var_texto.get().strip()
        if texto:
            caixa.insert(tk.END, texto)
        caixa.config(state="disabled")
    var_texto.trace_add("write", atualizar_caixa)

    # estilo do botão
    style = ttk.Style()
    style.configure("Botao.TButton", font=fonte_botao, padding=10)

    root.mainloop()


if __name__ == "__main__":
    main()
