import oerplib
import click


def get_account(destiny, origin, account_id, company_id):
    account = origin.read('account.account', account_id, ['code'])
    account_id = destiny.search('account.account',
                                [('code', '=', account.get('code')),
                                 ('company_id', '=', company_id)])
    return account_id and account_id[0]


def get_destiny_id(destiny, origin, re_id, model, company_id):
    destiny_id = False
    if not re_id:
        return False
    if model == 'product.uom':
        uom = origin.read(model, re_id, ['name'])
        uom_id = destiny.search(model,
                                [('name', '=', uom.get('name'))])
        return uom_id and uom_id[0]
    if model == 'res.users':
        user = origin.read(model, re_id, ['login'])
        user_id = destiny.search(model,
                                 [('login', '=', user.get('login'))])
        return user_id and user_id[0]
    if model == 'account.payment.term':
        term = origin.read(model, re_id, ['name'])
        term_id = destiny.search(model,
                                 [('name', '=', term.get('name'))])
        return term_id and term_id[0]
    if model == 'account.tax.code':
        code = origin.read(model, re_id, ['name'])
        code_id = destiny.search(model,
                                 [('name', '=', code.get('name')),
                                  ('company_id', '=', company_id)])
        return code_id and code_id[0]
    if model == 'account.tax':
        tax = origin.read(model, re_id, ['name'])
        tax_id = destiny.search(model,
                                [('name', '=', tax.get('name')),
                                 ('company_id', '=', company_id)])
        return tax_id and tax_id[0]
    if model == 'account.fiscal.position':
        fiscal = origin.read(model, re_id, ['name'])
        fiscal_id = destiny.search(model,
                                   [('name', '=', fiscal.get('name')),
                                    ('company_id', '=', company_id)])
        return fiscal_id and fiscal_id[0]
    if model == 'account.analytic.account':
        analytic = origin.read(model, re_id, ['name'])
        analytic_id = destiny.search(model,
                                     [('name', '=', analytic.get('name')),
                                      ('company_id', '=', company_id)])
        return analytic_id and analytic_id[0]
    if model == 'res.partner.bank':
        acc = origin.read(model, re_id, ['acc_number'])
        acc_id = destiny.search(model,
                                [('acc_number', '=', acc.get('acc_number')),
                                 ('company_id', '=', company_id)])
        return acc_id and acc_id[0]
    if model == 'account.period':
        period = origin.read(model, re_id, ['code'])
        period_id = destiny.search(model,
                                   [('code', '=', period.get('code')),
                                    ('company_id', '=', company_id)])
        return period_id and period_id[0]
    if model == 'pay.method':
        pay = origin.read(model, re_id, ['name'])
        pay_id = destiny.search(model,
                                [('name', '=', pay.get('name'))])
        return pay_id and pay_id[0]
    return destiny_id


def get_partner(destiny, origin, partner_id, company_id):
    if not partner_id:
        return False

    partner = origin.read('res.partner', partner_id, ['name', 'vat'])
    partner_id = destiny.search('res.partner',
                                [('vat', '=', partner.get('vat'))])
    if len(partner_id) == 1:
        return partner_id[0]
    partner_id = destiny.search('res.partner',
                                [('name', '=', partner.get('name'))])
    if partner_id:
        return partner_id[0]
    else:
        partner_id = destiny.create('res.partner',
                                    {'name': partner.get('name'),
                                     'vat': partner.get('vat')})
    return partner_id


def get_product(destiny, origin, product_id, company_id):
    if not product_id:
        return False
    product = origin.read('product.product', product_id, ['name'])
    product_id = destiny.search('product.product',
                                [('name', '=', product.get('name'))])
    if product_id:
        return product_id[0]
    else:
        product_id = destiny.create('product.product',
                                    {'name': product.get('name')})
    return product_id


def get_journal(destiny, origin, journal_id, company_id):
    journal = origin.execute('account.journal', 'read', journal_id,
                             ['name', 'code', 'type', 'currency',
                              'default_credit_account_id',
                              'default_debit_account_id'],
                             {}, '_classic_write')
    journal_id = destiny.search('account.journal',
                                ['|',
                                 ('code', '=', journal.get('code')),
                                 ('name', '=', journal.get('name')),
                                 ('company_id', '=', company_id)])
    if journal_id:
        return journal_id[0]
    else:
        journal_id = destiny.create('account.journal',
                                    {'name': journal.get('name'),
                                     'code': journal.get('code'),
                                     'company_id': company_id,
                                     'type': journal.get('type'),
                                     'default_credit_account_id': get_account(destiny, origin, journal.get('default_credit_account_id'), company_id),
                                     'default_debit_account_id': get_account(destiny, origin, journal.get('default_debit_account_id'), company_id),
                                     #'currency': get_currency(destiny, origin, journal.get('currency'), company_id),
                                     })

    return journal_id


def prepare_order_lines(destiny, origin, prefix, line_ids, company_id):
    new_lines = []
    fields = ['origin', 'uos_id', 'sequence', 'price_unit', 'price_subtotal',
              'partner_id', 'analytics_id', 'company_id', 'account_id',
              'invoice_line_tax_id', 'discount', 'name', 'product_id',
              'quantity']
    for line in line_ids:
        line_read = origin.execute('account.invoice.line', 'read', line,
                                   fields,
                                   {}, '_classic_write')
        line_read.update({
            'uos_id': get_destiny_id(destiny, origin, line_read.get('uos_id'), 'product.uom', company_id),
            'company_id': company_id,
            'partner_id': get_partner(destiny, origin, line_read.get('partner_id'), company_id),
            'account_id': get_account(destiny, origin, line_read.get('account_id'), company_id),
            'analytics_id': get_destiny_id(destiny, origin, line_read.get('analytics_id'), 'account.analytic.account', company_id),
            'product_id': get_product(destiny, origin, line_read.get('product_id'), company_id),
            'invoice_line_tax_id': [(6, 0,
                                     [get_destiny_id(destiny, origin, i,
                                                     'account.tax', company_id)
                                      for i in line_read.
                                      get('invoice_line_tax_id')])]
        })
        line_read.pop('id', 'no')
        new_lines.append((0, 0, line_read))
    return new_lines


def get_reconcile(destiny, origin, reconcile_id, move, prefix, year, company_id):
    if not reconcile_id:
        return False
    reco_read = origin.read('account.move.reconcile',
                            reconcile_id,
                            ['name', 'opening_reconciliation', 'type']
                            )
    dest_id = get_id_from_ir_data(destiny, prefix, 'account_move_reconcile', reconcile_id)
    if dest_id:
        return dest_id
    reco_read.pop('id', 'no')
    reco_id = destiny.create('account.move.reconcile',
                                reco_read)

    destiny.create('ir.model.data',
                {'name': '{pre}_{model},{mid}'. format(pre=prefix, model='account_move_reconcile', mid=reconcile_id),
                    'res_id': reco_id,
                    'model': 'account.move.reconcile'})
    move_ids = origin.search('account.move',
                                ['|',
                                ('line_id.reconcile_partial_id', '=',
                                reconcile_id),
                                ('line_id.reconcile_id', '=', reconcile_id)])
    for m_id in move_ids:
        create_acc_move(destiny, origin, prefix, m_id, year, company_id)

    return reco_id


def prepare_move_lines(destiny, origin, prefix, line_ids, move_id, company_id, year):
    new_lines = []
    fields = ['analytic_lines', 'company_id',
              'currency_id', 'date_maturity', 'invoice', 'narration',
              'reconcile_partial_id', 'blocked', 'analytic_account_id',
              'credit', 'partner_id', 'analytics_id', 'journal_id',
              'tax_code_id', 'state', 'amount_residual_currency', 'debit',
              'ref', 'account_id', 'period_id', 'amount_currency', 'date',
              'product_id', 'reconcile_id', 'tax_amount', 'name',
              'account_tax_id', 'product_uom_id', 'amount_residual', 'move_id',
              'date_created', 'balance', 'quantity']
    for line in line_ids:
        line_read = origin.execute('account.move.line', 'read', line,
                                   fields,
                                   {}, '_classic_write')
        dest_id = get_id_from_ir_data(destiny, prefix, 'account_move_line',
                                      line_read.get('id'))
        if dest_id:
            return dest_id

        line_read.update({
            'product_uom_id': get_destiny_id(destiny, origin,
                                             line_read.get('product_uom_id'),
                                             'product.uom', company_id),
            'analytic_lines': [],
            'move_id': move_id,
            'reconcile_partial_id': get_reconcile(destiny, origin, line_read.get('reconcile_partial_id'), line_read.get('move_id'), prefix, year, company_id),
            'reconcile_id': get_reconcile(destiny, origin, line_read.get('reconcile_id'), line_read.get('move_id'), prefix, year, company_id),
            'analytic_account_id': get_destiny_id(destiny, origin,
                                                  line_read.get('analytic_account_id'),
                                                  'account.analytic.account',
                                                  company_id),
            'partner_id': get_partner(destiny, origin,
                                      line_read.get('partner_id'), company_id),
            'analytics_id': get_destiny_id(destiny, origin,
                                           line_read.get('analytics_id'),
                                           'account.analytic.account',
                                           company_id),
            'journal_id': get_journal(destiny, origin,
                                      line_read.get('journal_id'), company_id),
            'tax_code_id': get_destiny_id(destiny, origin,
                                          line_read.get('tax_code_id'),
                                          'account.tax.code', company_id),
            'account_id': get_account(destiny, origin,
                                      line_read.get('account_id'), company_id),
            'currency_id': get_currency(destiny, origin,
                                        line_read.get('currency_id'),
                                        company_id),
            'period_id': get_destiny_id(destiny, origin,
                                        line_read.get('period_id'),
                                        'account.period', company_id),
            'product_id': get_product(destiny, origin,
                                      line_read.get('product_id'), company_id),
            'account_tax_id': get_destiny_id(destiny, origin,
                                             line_read.get('account_tax_id'),
                                             'account.tax', company_id),
            'company_id': company_id,
        })
        old_id = line_read.pop('id', 'no')
        if line_read.get('currency_id') == 193:
            line_read.pop('currency_id')
        line_read.pop('invoice', 'no')
        line_id = destiny.create('account.move.line', line_read)
        destiny.create('ir.model.data',
                       {'name': '{pre}_{model},{mid}'.format(pre=prefix,
                                                             model='account_move_line',
                                                             mid=old_id),
                        'res_id': line_id,
                        'model': 'account.move.line'})
    return new_lines


def create_tax_line(destiny, origin, prefix, lines, company_id):
    new_line = []
    fields = ['tax_amount', 'account_id', 'sequence', 'manual', 'company_id',
              'base_amount', 'amount', 'base', 'tax_code_id', 'base_code_id',
              'name']
    for line in lines:
        line_read = origin.execute('account.invoice.tax',
                                   'read',
                                   line,
                                   fields,
                                   {},
                                   '_classic_write')
        line_read.update({
            'account_id': get_account(destiny, origin, line_read.get('account_id'), company_id),
            'tax_code_id': get_destiny_id(destiny, origin, line_read.get('tax_code_id'), 'account.tax.code', company_id),
            'base_code_id': get_destiny_id(destiny, origin, line_read.get('base_code_id'), 'account.tax.code', company_id),
        })
        line_read.pop('id', '0')
        new_line.append((0, 0, line_read))
    return new_line


def get_id_from_ir_data(destiny, prefix, model, old_id):
    new_id = destiny.search('ir.model.data',
                            [('name', '=', '{pre}_{model},{mid}'. format(pre=prefix, model=model, mid=old_id))])
    if not new_id:
        return False
    new_id = destiny.read('ir.model.data', new_id[0], ['res_id'])
    return new_id.get('res_id')


def create_acc_move(destiny, origin, prefix, move_id, year, company_id):
    if not move_id:
        return False
    fields = ['partner_id', 'name', 'amount', 'journal_id', 'company_id',
              'line_id', 'state', 'period_id', 'narration', 'date', 'balance',
              'ref', 'to_check']
    move_read = origin.execute('account.move', 'read', move_id, fields, {},
                               '_classic_write')
    dest_id = get_id_from_ir_data(destiny, prefix, 'account_move', move_read.get('id'))
    if dest_id:
        return dest_id
    move_id = destiny.search('account.move', [('name', '=',
                                               move_read.get('name'))])
    lines = move_read.get('line_id')
    move_read.update({
        'name': year + '_' + move_read.get('name'),
        'partner_id': get_partner(destiny, origin, move_read.get('partner_id'), company_id),
        'journal_id': get_journal(destiny, origin, move_read.get('journal_id'), company_id),
        'period_id': get_destiny_id(destiny, origin, move_read.get('period_id'), 'account.period', company_id),
        'line_id': False,
        'company_id': company_id,


    })
    old_id = move_read.pop('id', 'no')
    move_id = destiny.create('account.move', move_read)
    destiny.create('ir.model.data',
                   {'name': '{pre}_{model},{mid}'. format(pre=prefix, model='account_move', mid=old_id),
                    'res_id': move_id,
                    'model': 'account.move'})
    prepare_move_lines(destiny, origin, prefix, lines, move_id, company_id, year),
    return move_id


def get_currency(destiny, origin, currency, company_id):
    if not currency:
        return False
    curre = origin.read('res.currency', currency, ['name'])
    curre_d = destiny.search('res.currency', [('name', '=',
                                               curre.get('name')),
                                              ('company_id', '=', company_id)])
    if curre_d:
        return curre_d[0]
    return False


@click.command()
@click.option('-year', default='2012',
              prompt='Year', help='Year')
@click.option('-cd', default=4,
              prompt='Company ID destiny', help='Company id from destiny')
@click.option('-co', default=5,
              prompt='Company ID Origin', help='Company id from origin')
@click.option('-pod', default=7000,
              prompt='Port Destiny', help='Port of server Destiny')
@click.option('-pd', default='',
              prompt='Password Destiny', help='Password Destiny')
@click.option('-dbd', default='',
              prompt='Database Destiny', help='DB Destiny')
@click.option('-ud', default='',
              prompt='User name Destiny', help='your email or login')
@click.option('-poo', default='',
              prompt='Port Origin', help='Port of origin of data')
@click.option('-po', default='',
              prompt='Password Origin', help='Password Origin')
@click.option('-dbo', default='',
              prompt='Database Origin', help='DB Origin')
@click.option('-uo', default='',
              prompt='User name Origin', help='your email or login')
@click.option('-pre', default='', prompt='Prefix to ir_model_data',
              help='Prefix used to id of records imported e.g '
              'prefix_product_product,id')
def import_invoices(year, cd, co, po, dbo, uo, pre, poo, pod, pd, dbd, ud):
    '''
    If you dont know how to execute this script use
    python import_invoice.py --help


    you still need to modify the IP, Protocol, and Portparameters.
    '''
    origin = oerplib.OERP(server='',
                          port=poo,
                          timeout=9999999999999999)
    # destiny = oerplib.OERP(server='',
    destiny = oerplib.OERP(server='www.vauxoo.com',
                           port=pod)
    origin.login(user=uo, passwd=po, database=dbo)
    destiny.login(user=ud, passwd=pd, database=dbd)
    invoice_ids = origin.search('account.invoice',
                                [('company_id', '=', co),
                                 ('period_id.fiscalyear_id.name', '=', year)])

    fields = ['origin', 'comment', 'date_due', 'check_total', 'reference',
              'payment_term', 'number', 'company_id', 'currency_id',
              'partner_id', 'account_id', 'fiscal_position', 'user_id',
              'partner_bank_id', 'reference_type', 'journal_id', 'tax_line',
              'amount_tax', 'sale_date', 'state', 'type', 'invoice_line',
              'internal_number', 'reconciled', 'residual', 'move_name',
              'date_invoice',  'period_id', 'amount_untaxed', 'move_id',
              'amount_total', 'name', 'pay_method']
    for invoice in invoice_ids:
        invo_read = origin.execute('account.invoice',
                                   'read',
                                   invoice,
                                   fields,
                                   {},
                                   '_classic_write')
        invo_read.update({
            'company_id': cd,
            'internal_number': year + '-' + invo_read.get('internal_number', '') or '',
            'number': year + '-' + invo_read.get('number', '') or '',
            'name': year + '-' + str(invo_read.get('name', '')) or '',
            'move_name': year + '-' + invo_read.get('move_name'),
            'partner_id': get_partner(destiny, origin, invo_read.get('partner_id'), cd),
            'account_id': get_account(destiny, origin, invo_read.get('account_id'), cd),
            'journal_id': get_journal(destiny, origin, invo_read.get('journal_id'), cd),
            'user_id': get_destiny_id(destiny, origin, invo_read.get('user_id'), 'res.users', cd),
            'fiscal_position': get_destiny_id(destiny, origin, invo_read.get('fiscal_position'), 'account.fiscal.position', cd),
            'payment_term': get_destiny_id(destiny, origin, invo_read.get('payment_term'), 'account.payment.term', cd),
            'partner_bank_id': get_destiny_id(destiny, origin, invo_read.get('partner_bank_id'), 'res.partner.bank', cd),
            'period_id': get_destiny_id(destiny, origin, invo_read.get('period_id'), 'account.period', cd),
            'pay_method_id': get_destiny_id(destiny, origin, invo_read.get('pay_method'), 'pay.method', cd),
            'sale_order_date': invo_read.get('sale_order_date'),
            'invoice_line': prepare_order_lines(destiny, origin, pre, invo_read. get('invoice_line'), cd),
            'tax_line': create_tax_line(destiny, origin, pre, invo_read.get('tax_line'), cd),
            'currency_id': get_currency(destiny, origin, invo_read.get('currency_id'), cd),
            'move_id': create_acc_move(destiny, origin, pre, invo_read.get('move_id'), year, cd),
        })
        inv_id = destiny.search('account.invoice',
                                [('internal_number', '=',
                                  invo_read.get('internal_number')),
                                 ('company_id', '=', cd),
                                 ('type', '=', invo_read.get('type'))])
        if not inv_id:
            inv_id = destiny.create('account.invoice', invo_read)
            click.echo('Created the invoice %s ' % invo_read.get('name'))

if __name__ == '__main__':
    import_invoices()
