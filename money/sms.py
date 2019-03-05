import re
from datetime import datetime
x = datetime.today().strftime("%Y")

bank = r'([BIDV]{4}(?= [+|-]))|([VietinBank]{10}(?=:))|([Agribank]{8}(?=:))|([TPBank]{6}(?=\):))|((?<=VND\. )[Ref]{3})'

rAmountI = r'((?<=\+)[0-9]+([,|\.]?[0-9]+)*)'

rAmountE = r'((?<=-)[0-9]+([,|\.]?[0-9]+)*)'

rDate = r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}'

rNote = [r'(?<=ND:)(.*)[^"]', r'(?<=ND:)(.*)[^"]', r'(?<=Ref).*[^"]', r'(?<=ND:)(.*)[^"]', r'(?<=[\(])(.*)(?=(\)))[^"]']

rCategory = r'((?<=(tai|TAI))ATM)|(ATM(?=.))|(Topup|TOP-UP)|(MOMO(?=.))|(POS)|(BSMS)'

result = {'Time':'', 'Amount':'', 'Note':'', 'Category':''}

def Message(message, i):
    amountE = re.search(rAmountE, message)
    amountI = re.search(rAmountI, message)
    if amountI:
        a = amountI.group()
        b = a.split(",")
        c = ""
        for j in range(len(b)):
            c += b[j]
        result['Amount'] = c
        result['Category'] = 'Others_Income'
    else:
        a = amountE.group()
        b = a.split(",")
        c = ""
        for j in range(len(b)):
            c += b[j]
        result['Amount'] = c
        result['Category'] = 'Others_Expense'

    d = re.search(rDate, message)
    if d:
        e = d.group().split("/")
        e = "-".join(e)
        e = e.split("-")
        if len(e[2])==2:
            e[2] = x[0:2] + e[2]
        result['Time'] = e[2] + "-" + e[1] + "-" + e[0]

    note = re.search(rNote[i], message)
    if note:
        result['Note'] = note.group()
        s = re.search(rCategory, note.group())
        if s:
            if s.group() == 'ATM': result['Category'] = 'Others_Expense'
            elif s.group() == 'MOMO': result['Category'] = 'Bills & Utilities'
            elif s.group() == 'POS': result['Category'] = 'Shopping'
            elif s.group() == 'BSMS': result['Category'] = 'Others_Expense'
            elif s.group() == 'Topup' or 'TOP_UP': result['Category'] = 'Bills & Utilities'
