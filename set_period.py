# -*- coding: UTF-8 -*-
import oerplib


HOST = raw_input('Por favor ingrese el HOST: ')
PORT = int(raw_input('Por favor ingrese el puerto: '))
DB = raw_input('Por favor ingrese el nombre de la base de datos: ')
USER = raw_input('Por favor ingrese el login del usuario: ')
PASS = raw_input(u'Por favor ingrese la password del usuario: ')

con = oerplib.OERP(
server=HOST, 
database=DB, 
port=PORT, 
)  

con.login(USER, PASS)


def main():
    company_id = con.user.company_id.id
    if company_id:
        invo_read = []

        invo_ids = con.search('account.invoice',[('adminpaq_id', '>', 0),
                                                 ('company_id', '=', company_id)])

        for  i in con.read('account.invoice', invo_ids, ['period_id']):
            i.get('period_id') and invo_read.append(tuple(i.get('period_id')))

        voucher_ids = con.search('account.voucher',[('adminpaq_id', '>', 0),
                                                    ('company_id', '=', company_id)])

        for  i in con.read('account.voucher', voucher_ids, ['period_id']):
            i.get('period_id') and invo_read.append(tuple(i.get('period_id')))

        period_ids = list(set(invo_read))

        for period in period_ids:
            new_p = con.execute('account.period', 'copy_data', period[0])
            new_p.update(({
                'special':True,
                'code': '%s-%s' % ('ADPQ', new_p.get('code')),
                'name': '%s-%s' % ('ADPQ', new_p.get('name')),
                'company_id':company_id,
                'active': False,
                }))
            if not con.search('account.period', [('name', '=', new_p.get('name'))]):
                con.create('account.period', new_p)





main()
