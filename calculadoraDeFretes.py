import os
import sqlite3 as sql
from tkinter import *
from tkinter import ttk
from tkentrycomplete import *

uf = None
product_names = ["Comfort", "3 em 1", "Vira Mesa", "Premium"]
wComfort = 36.48
wPremium = 36.48
w3em1 = 29.20
wViramesa = 19.2
rsAg = ["POAP", "CXSP", "LAJP", "POAR", "LAJR", "OSOP", "CXSR", "PELP", "PFUP", "IJUP", "STMP", "POAI", "CXSI", "LAJI", "IJUR", "OSOR", "PFUR", "STMR", "PELR", "IJUI", "PFUI", "STMI", "PELI", "OSO", "BGEP", "BGER", "BGEI"]
scAg = ["ITJP", "ITJR", "FLNI", "FLNP", "FLNR", "RDLP", "RDLR", "RDLI", "ITJI"]
prAg = ["CTBP", "CTBR", "CTBI"]
spAg = ["SPOP", "SPOR", "SPOI", "CAPP", "CAPR", "CAPI", "SJCP", "SJCR", "SJCI"]



def identifyProd():
    amount = quantity.get()   
    product = selected_product.get()
    match product:
        case "Comfort":
            prodWeight = wComfort
        case "Premium":
            prodWeight = wPremium
        case "3 em 1":
            prodWeight = w3em1
        case "Vira Mesa":
            prodWeight = wViramesa
    prodWeight *= amount
    return prodWeight

def getUf(Ag):
    global uf
    if Ag in rsAg:
        uf = "rs"
    elif Ag in scAg:
        uf = "sc"
    elif Ag in prAg:
        uf = "pr"
    elif Ag in spAg:
        uf = "sp"
    else:
        raise ValueError(f"Agencia '{Ag}' não pertence a nenhuma UF conhecida.")
    return uf

def getShippingPrice():
    prodWeight = identifyProd()
    city = selected_city.get()
    print(city)
    cur3.execute(f"SELECT agencia FROM cidades WHERE cidade = ?", (city,))
    AgB = cur3.fetchone()
    Ag = f"{AgB}".strip("'[()], ")
    getUf(Ag)
    print(Ag)
    c = sql.connect("dadosTransporte.db")
    cur = c.cursor()
    match prodWeight:
        case prodWeight if prodWeight <= 10:
            sqlvalor = "valor10"
        case prodWeight if prodWeight <= 20:
            sqlvalor = "valor20"
        case prodWeight if prodWeight <= 30:
            sqlvalor = "valor30"
        case prodWeight if prodWeight <= 60:
            sqlvalor = "valor60"
        case prodWeight if prodWeight <= 80:
            sqlvalor = "valor80"
        case prodWeight if prodWeight <= 100:
            sqlvalor = "valor100"
        case prodWeight if prodWeight <= 120:
            sqlvalor = "valor120"
        case prodWeight if prodWeight <= 140:
            sqlvalor = "valor140"
        case prodWeight if prodWeight <= 160:
            sqlvalor = "valor160"
        case prodWeight if prodWeight <= 180:
            sqlvalor = "valor180"
        case prodWeight if prodWeight <= 200:
            sqlvalor = "valor200"
    print(AgB, ",\n", Ag)
    cur.execute(f"SELECT {sqlvalor} FROM cidades_atendidas WHERE cidade = ?", (Ag,))
    valorfretebruto = cur.fetchall()
    sValorfretebruto = str(valorfretebruto).strip("[]()', ")
    print(sValorfretebruto)
    cur.close()
    return sValorfretebruto

def showPriceClean(showPrice):
    global redefineShowPrice 
    redefineShowPrice = showPrice.configure(text="")

def calculate():
    prodWeight = identifyProd()
    sValorfretebruto = getShippingPrice()
    match uf:
            case "rs":
                ufTax = 39
            case "sc":
                ufTax = 49
            case "pr":
                ufTax = 59
            case "sp":
                ufTax = 69

    fValorfretebruto = float(sValorfretebruto)
    valorfreteliquido = fValorfretebruto + ufTax + 30
    sValorfreteliquido = f"{valorfreteliquido:.2f}"
    city = selected_city.get()
    amount = quantity.get()   
    product = selected_product.get()

    showPrice =ttk.Label(
    frm,
    text=f"R$ {sValorfreteliquido}"
    )
    showPrice.grid(column=0, row=8)
    
    print(product, ";\n", prodWeight, sValorfretebruto, valorfreteliquido, ";\n", city, ";\n", amount)
    return showPrice

def reset():
    showPrice = calculate()
    showPriceClean(showPrice)

def buttonFunctions():
    reset()
    calculate()





con2 = sql.connect("dadosTransporte.db")
cur2 = con2.cursor()
getAgValue = cur2.execute("SELECT cidade FROM cidades_atendidas")


con3 = sql.connect("cidadesAgencias.db")
cur3 = con3.cursor()
getCid = cur3.execute("SELECT cidade FROM cidades")
cidadesAtendidasBrute = cur3.fetchall()
cidadesAtendidasList = [row[0] for row in cidadesAtendidasBrute]


root = Tk()
root.title("calculadora de fretes")
root.resizable(False, False)

selected_product = StringVar()
selected_city = StringVar()
quantity = IntVar(value=1)





bgstyle = ttk.Style(
)
bgstyle.configure("customColor.TFrame", background="#171717")
sepstyle = ttk.Style(
)
bgstyle.configure("sepColor.TFrame", background="#ffffff")

frm = ttk.Frame(root, style="customColor.TFrame", padding=70)
frm.grid()


ttk.Label(
    frm, 
    text="produto 1"
    ).grid(column=0, row=1)

ttk.Combobox(
    frm, 
    values=product_names, 
    textvariable=selected_product,
    placeholder="produto",
    state="readonly"
    ).grid(column=0, row=2, pady=2)
combo = ttk.Combobox(
    frm, 
    values=cidadesAtendidasList,
    textvariable=selected_city,
    placeholder="cidade", 
    state="normal")
combo.grid(column=0, row=3, pady=2)


ttk.Spinbox(
    frm, 
    from_=1,
    to=10, 
    textvariable=quantity,
    placeholder="n°", 
    state="readonly").grid(column=0, row=4, pady=2)
ttk.Button(
    frm, 
    text="Calcular",
    command=buttonFunctions
    ).grid(column=0, row=5, pady=4)

separator = ttk.Separator(
    frm,
    style="sepColor.TFrame",
    orient="horizontal"
)

separator.grid(row=7, pady=13, sticky='ew')


 
root.mainloop()