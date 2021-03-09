import tabula
import datetime
from db import engine, data_digital
 
file = "bills/ddd2.pdf"
dir_files = "bills/"

import glob
import pandas as pd

slip = glob.glob('bills/*.pdf', recursive=True)

print(slip)

def create_api():
    lk = []
    for i in slip:
        tables = tabula.read_pdf(file, pages = "all", multiple_tables = True)

        invoice_data = tables[0].to_dict('records')

        pii = tables[1].to_dict('records')

        expenses = tables[2].to_dict('records')

        description = tables[3].to_dict('records')

        taxes_total = tables[4].to_dict('records')

        result = []

        pii.extend(invoice_data)
        pii.extend(taxes_total)
        pii.extend(description)
        for myDict in pii:
            if myDict not in result:
                result.append(myDict)

        res = {} 
        for d in result: 
            res.update(d) 
        
        res['isp_bill'] = str(expenses)

        res['date_add'] = datetime.datetime.now() 

        return res

def redacted():
    for i in slip:
        tables = tabula.read_pdf(file, pages = "all", multiple_tables = True)

        invoice_data = tables[0].to_dict('records')

        expenses = tables[2].to_dict('records')

        description = tables[3].to_dict('records')

        taxes_total = tables[4].to_dict('records')

        result = []

        invoice_data.extend(invoice_data)
        invoice_data.extend(taxes_total)
        for myDict in invoice_data:
            if myDict not in result:
                result.append(myDict)

        res = {} 
        for d in result: 
            res.update(d) 
        
        res['isp_bill'] = str(expenses)

        res['date_add'] = datetime.datetime.now() 

        return res    

def save_data():
    res = create_api()

    name = res['Name']
    email = res['Email']
    telephone = res['Telephone']
    location = res['Location']
    sub_total = res['SUB TOTAL']
    tax_rate = res['TAX RATE']
    tax = res['TAX']
    total = res['TOTAL']
    description = res['Description']
    isp_bill = res['isp_bill']
    date_add = res['date_add']

    data = [(name, email, telephone, location, sub_total, tax_rate, tax, total, description, isp_bill, date_add)]

    ins = data_digital.insert().values(name=name, email=email, telephone=telephone, location=location, sub_total=sub_total, tax_rate=tax_rate, tax=tax, total=total, description=description, isp_bill=isp_bill, date_add=date_add)

    result = engine.execute(ins)

    return result

