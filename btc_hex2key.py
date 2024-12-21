import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bit import Key
from bit.format import bytes_to_wif

# Проверка подключения к интернету
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

# Получение баланса через Mempool API
def get_balance(address):
    try:
        response = requests.get(f"https://mempool.space/api/address/{address}")
        if response.status_code == 200:
            data = response.json()
            funded = data['chain_stats']['funded_txo_sum'] / 1e8
            spent = data['chain_stats']['spent_txo_sum'] / 1e8
            return funded - spent
        else:
            return "Ошибка: проблема с API Mempool"
    except Exception:
        return "Ошибка подключения"

# Обработка и отображение информации о ключах и адресах
def show_info():
    output_text.delete(1.0, tk.END)

    priv_key = priv_key_entry.get()
    key_format = key_format_var.get()

    try:
        if key_format == "WIF":
            try:
                key = Key(priv_key)
                hex_key = key.to_hex()
            except ValueError:
                raise ValueError("Неверный WIF ключ")
        elif key_format == "HEX":
            if len(priv_key) != 64:
                raise ValueError("Приватный ключ должен быть длиной 64 символа в формате HEX")
            key = Key.from_hex(priv_key)
            hex_key = priv_key
        else:
            raise ValueError("Неверный формат ключа")

        wif_key = key.to_wif()
        compressed_address = key.address
        compressed_pubkey = key.public_key.hex()

        uncompressed_key = Key.from_hex(hex_key)
        uncompressed_key._compressed = False
        uncompressed_pubkey = (
            b"04" +
            uncompressed_key.public_point.x.to_bytes(32, "big") +
            uncompressed_key.public_point.y.to_bytes(32, "big")
        ).hex()
        uncompressed_address = uncompressed_key.address

        info = [
            f"Приватный ключ ({key_format}): {priv_key}",
            f"Публичный ключ (сжатый): {compressed_pubkey}",
            f"Публичный ключ (несжатый): {uncompressed_pubkey}",
            f"BTC Адрес (сжатый): {compressed_address}",
            f"BTC Адрес (несжатый): {uncompressed_address}",
            f"Приватный ключ в WIF: {wif_key}",
            f"Приватный ключ в HEX: {hex_key}",
        ]

        if check_internet():
            balance = get_balance(compressed_address)
            if isinstance(balance, float):
                info.append(f"Баланс: {balance} BTC")
            else:
                info.append(balance)
        else:
            info.append("Нет подключения к интернету. Баланс недоступен.")

        output_text.insert(tk.END, "\n".join(info))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")

# Создание окна с темной темой
root = tk.Tk()
root.title("BTC Key Info Viewer")
root.geometry("485x390")
root.resizable(False, False)
root.configure(bg="#2E2E2E")

# Метка для ввода ключа
key_format_var = tk.StringVar(value="WIF")
label = tk.Label(root, text="Введите приватный ключ (64 символа HEX или WIF):", fg="green", bg="#2E2E2E")
label.pack(pady=5)

# Поле ввода приватного ключа
priv_key_entry = tk.Entry(root, width=50, bg="#1E1E1E", fg="green", insertbackground="green")
priv_key_entry.pack(pady=5)

# Переключатель формата ключа
frame = tk.Frame(root, bg="#2E2E2E")
frame.pack()

wif_radio = ttk.Radiobutton(frame, text="WIF", variable=key_format_var, value="WIF")
wif_radio.grid(row=0, column=0, padx=5)

hex_radio = ttk.Radiobutton(frame, text="HEX", variable=key_format_var, value="HEX")
hex_radio.grid(row=0, column=1, padx=5)

style = ttk.Style()
style.configure("TButton", background="#2E2E2E", foreground="green")
style.configure("TLabel", background="#2E2E2E", foreground="green")

# Кнопка для отображения информации
show_button = tk.Button(root, text="Show", command=show_info, bg="#1E1E1E", fg="green", activebackground="#3E3E3E", activeforeground="green")
show_button.pack(pady=10)

# Поле для вывода информации
output_text = tk.Text(root, height=15, width=60, bg="#1E1E1E", fg="green", insertbackground="green")
output_text.pack(pady=10)

# Запуск приложения
root.mainloop()
