import re

bank = r'([BIDV]{4}(?= [+|-]))|([VietinBank]{10}(?=:))|([Agribank]{8}(?=:))|([TPBank]{6}(?=\):))|((?<=VND\. )[Ref]{3})'

rAccountNumber = [r'([0-9]{14})(?= tai)', r'([0-9]{12})(?=[\|]GD:)'
                  , r'([0-9]{13})(?=[-|+|thay doi])', r'[x]{4}[0-9]{7}', r'([0-9]{13})(?=:)']

rIn = [r'([\+|-])([0-9]+[,])+([0-9]+)', r'([\+|-])([0-9]+)'
       , r'([\+|-])([0-9]+[,])+([0-9]+)', r'[\+|-]([0-9]+[\.]?)+', r'([\+|-])([0-9]+[,])+([0-9]+)']

rTime = [r'[0-9]{2}[:][0-9]{2}', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?'
         , r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?', r'[0-9]{2}[:][0-9]{2}([:][0-9]{2})?']

rDate = [r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}'
         , r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}', r'[0-9]{2}[\/|-][0-9]{2}[\/|-][0-9]{2,4}']

rContent = [r'(?<=ND:)(.*)', r'(?<=ND:)(.*)', r'(?<=Ref).*', r'(?<=ND:)(.*)', r'(?<=[\(])(.*)(?=(\)))']

rBalance = [r'(([0-9]+[,])+([0-9]+))(?=VND[\.|;])', r'(([0-9]+[,])+([0-9]+))(?=VND\|ND:)'
            , r'(([0-9]+[,])+([0-9]+))(?=VND[\.])', r'(?<=SD: )(([0-9]+[,|\.])+([0-9]+))', r'(([0-9]+[,])+([0-9]+))(?=VND[\.])']

service = r'((?<=(tai|TAI))ATM)|(ATM(?=.))|(Topup|TOP-UP)|(MOMO(?=.))|(POS)|(BSMS)'

result = {'Bank':'', 'TK':'', 'Time':'', 'Amount':'','Balance':'', 'Content':'', 'Service':''}

def Message(message, i):
    a = re.search(rAccountNumber[i], message)
    if a:
        result['TK'] = a.group()

    I = re.search(rIn[i], message)
    if I:
        result['Amount'] = I.group()

    t = re.search(rTime[i], message)
    if t:
        result['Time'] = t.group()

    d = re.search(rDate[i], message)
    if d:
        result['Time'] = result['Time'] +' ' + d.group()

    c = re.search(rContent[i], message)
    if c:
        result['Content'] = c.group()
        s = re.search(service, c.group())
        print(c.group())
        if s:
            if s.group() == 'ATM': result['Service'] = 'Others'
            elif s.group() == 'MOMO': result['Service'] = 'Bills & Utilities'
            elif s.group() == 'POS': result['Service'] = 'Shopping'
            elif s.group() == 'BSMS': result['Service'] = 'Others'
            elif s.group() == 'Topup' or 'TOP_UP': result['Service'] = 'Bills & Utilities'
            #print(s.group())
            #print(result['Service'] )
        else: result['Service'] = 'Others'

    b = re.search(rBalance[i], message)
    if b:
        result['Balance'] = b.group() + 'VND'

def add_message(request):
    messag = request.POST.get('message', False)
    n = messag.split("\r\n")
    message = ' '.join(n)
    i = -1;
    m = re.search(bank, message)

    if m:
        if m.group() == 'BIDV':
            i = 0
            result['Bank'] = 'BIDV'
        elif m.group() == 'VietinBank':
            i = 1
            result['Bank'] = 'VietinBank'
            #print('i = ', i)
        elif m.group() == 'Ref':
            i = 2
            result['Bank'] = 'Vietcombank'
            #print('i = ', i)
        elif m.group() == 'TPBank':
            i = 3
            result['Bank'] = 'TPBank'
        elif m.group() == 'Agribank':
            i = 4
            result['Bank'] = 'Agribank'
    if i>=0:
        MessageBank(message, i)
        list = [message, result['Bank'], result['TK'], result['Time'], result['Amount'], result['Balance'], result['Content'], result['Service']]
        content = {
            'list':list,
        }
        q = Message(bank_message = message, bank = result['Bank'], tk = result['TK'], time = result['Time']
        , amount = result['Amount'], balance = result['Balance'], content = result['Content'], service = result['Service'])
        q.save();
        for k in result.keys():
            result[k] = ' '
    else:
        list = [message, 'ngan hang chua duoc xac dinh', ' ', ' ', ' ', ' ', ' ', ' ']
        content = {
            'list':list,
        }
