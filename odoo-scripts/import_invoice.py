import oerplib
import click


def get_destiny_id(destiny, prefix, orig_id, model):
    dest_id = False
    dest_id = destiny.search('ir.model.data',
                             [('name', '=',
                               '{pre}_{model},{id}'.format(pre=prefix,
                                                           model=model,
                                                           id=orig_id))])
    if dest_id:
        dest_id = destiny.read('ir.model.data', dest_id[0],
                               ['res_id']).get('res_id', False)
    return dest_id


def prepare_order_lines(destiny, origin, prefix, line_ids):
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
            'uos_id': get_destiny_id(destiny, prefix, line_read.get('uos_id'),
                                     'product_uom'),
            'partner_id': get_destiny_id(destiny, prefix,
                                         line_read.get('partner_id'),
                                         'res_partner'),
            'account_id': get_destiny_id(destiny, prefix,
                                         line_read.get('account_id'),
                                         'account_account'),
            'analytics_id': get_destiny_id(destiny, prefix,
                                           line_read.get('analytics_id'),
                                           'account_analytic_account'),
            'product_id': get_destiny_id(destiny, prefix,
                                         line_read.get('product_id'),
                                         'product_product'),
            'invoice_line_tax_id': [(6, 0,
                                     [get_destiny_id(destiny, prefix, i,
                                                     'account_tax') for i in
                                      line_read.get('invoice_line_tax_id')])]
        })
        line_read.pop('id', 'no')
        new_lines.append((0, 0, line_read))
    return new_lines


def get_reconcile(destiny, origin, reconcile_id, move, prefix):
    if not reconcile_id:
        return False
    reco_read = origin.read('account.move.reconcile',
                            reconcile_id,
                            ['name', 'opening_reconciliation', 'type']
                            )
    reco_id = destiny.search('account.move.reconcile',
                             [('name', '=', reco_read.get('name'))])
    if not reco_id:
        reco_read.pop('id', 'no')
        reco_id = destiny.create('account.move.reconcile',
                                 reco_read)
        move_ids = origin.search('account.move',
                                 [('line_id.reconcile_partial_id', '=',
                                   reconcile_id),
                                  ('id', '!=', move)])
        for m_id in move_ids:
            lines = origin.search('account.move.line',
                                  [('move_id', '=', m_id),
                                   ('reconcile_partial_id', '=',
                                    reconcile_id)])
            create_acc_move(destiny, origin, prefix, m_id)

    else:
        reco_id = reco_id[0]

    return reco_id


def prepare_move_lines(destiny, origin, prefix, line_ids):
    new_lines = []
    fields = ['analytic_lines', 'statement_id', 'company_id',
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
        line_read.update({
            'product_uom_id': get_destiny_id(destiny, prefix,
                                             line_read.get('product_uom_id'),
                                             'product_uom'),
            'analytic_lines': [],
            'statement_id': get_destiny_id(destiny, prefix,
                                           line_read.get('statement_id'),
                                           'account_bank_statement'),
            'reconcile_partial_id': get_reconcile(destiny, origin,
                                                  line_read.get('reconcile_partial_id'),
                                                  line_read.get('move_id'),
                                                  prefix),
            'reconcile_id': False,
            'analytic_account_id': get_destiny_id(destiny, prefix,
                                                  line_read.
                                                  get('analytic_account_id'),
                                                  'account_analytic_account'),
            'partner_id': get_destiny_id(destiny, prefix,
                                         line_read.get('partner_id'),
                                         'res_partner'),
            'analytics_id': get_destiny_id(destiny, prefix,
                                           line_read.get('analytics_id'),
                                           'account_analytic_account'),
            'journal_id': get_destiny_id(destiny, prefix,
                                         line_read.get('journal_id'),
                                         'account_journal'),
            'tax_code_id': get_destiny_id(destiny, prefix,
                                          line_read.get('tax_code_id'),
                                          'account_tax_code'),
            'account_id': get_destiny_id(destiny, prefix,
                                         line_read.get('account_id'),
                                         'account_account'),
            'currency_id': get_currency(destiny, origin, prefix,
                                        line_read.get('currency_id')),
            'period_id': get_destiny_id(destiny, prefix,
                                        line_read.get('period_id'),
                                        'account_period'),
            'product_id': get_destiny_id(destiny, prefix,
                                         line_read.get('product_id'),
                                         'product_product'),
            'account_tax_id': get_destiny_id(destiny, prefix,
                                             line_read.get('account_tax_id'),
                                             'account_tax'),
            'company_id': 1,
        })
        line_read.pop('id', 'no')
        line_read.pop('invoice', 'no')
        new_lines.append((0, 0, line_read))
    return new_lines


def create_acc_move(destiny, origin, prefix, move_id, lines=None):
    if not move_id:
        return False
    fields = ['partner_id', 'name', 'amount', 'journal_id', 'company_id',
              'line_id', 'state', 'period_id', 'narration', 'date', 'balance',
              'ref', 'to_check']
    move_read = origin.execute('account.move', 'read', move_id, fields, {},
                               '_classic_write')
    move_id = destiny.search('account.move', [('name', '=',
                                               move_read.get('name'))])
    if move_id:
        return move_id[0]
    if lines:
        move_read.update({'line_id': lines})
    move_read.update({
        'partner_id': get_destiny_id(destiny, prefix,
                                     move_read.get('partner_id'),
                                     'res_partner'),
        'journal_id': get_destiny_id(destiny, prefix,
                                     move_read.get('journal_id'),
                                     'account_journal'),
        'period_id': get_destiny_id(destiny, prefix,
                                    move_read.get('period_id'),
                                    'account_period'),
        'line_id': prepare_move_lines(destiny, origin, prefix,
                                      move_read.get('line_id')),
        'company_id': 1,


    })
    move_read.pop('id', 'no')
    move_id = destiny.create('account.move', move_read)
    return move_id


def create_tax_line(destiny, origin, prefix, lines):
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
            'account_id': get_destiny_id(destiny, prefix,
                                         line_read.get('account_id'),
                                         'account_account'),
            'tax_code_id': get_destiny_id(destiny, prefix,
                                          line_read.get('tax_code_id'),
                                          'account_tax_code'),
            'base_code_id': get_destiny_id(destiny, prefix,
                                           line_read.get('base_code_id'),
                                           'account_tax_code'),
        })
        line_read.pop('id', '0')
        new_line.append((0, 0, line_read))
    return new_line


def get_currency(destiny, origin, prefix, currency):
    if not currency:
        return False
    if currency == 1:
        return 34
    elif currency == 2:
        return 3
    else:
        curre = origin.read('res.currency', currency, ['name'])
        curre_d = destiny.search('res.currency', [('name', '=',
                                                   curre.get('name'))])
        if curre_d:
            return curre_d[0]
    return 34


@click.command()
def import_invoices(po, dbo, uo, pre, poo, pod, pd, dbd, ud):
    """
    If you dont know how to execute this script use
    python import_invoice.py --help

    Example:
        python generate_sale.py -po passwordorigin -uo userorigin -dbo
        dborigin -si sale_id

    you still need to modify the IP, Protocol, and Portparameters.
    """
    origin = oerplib.OERP(server='lodi.lodigroup.com',
                          port=poo,
                          timeout=9999999999999999)
    destiny = oerplib.OERP(server='exim.lodigroup.com',
                           port=pod)
    origin.login(user=uo, passwd=po, database=dbo)
    destiny.login(user=ud, passwd=pd, database=dbd)
    invoice_ids = origin.search('account.invoice',
                                [('company_id', '=', 1),
                                 ('state', 'in', ('open',
                                                  'draft'))])

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
        move_id = invo_read.get('move_id')
        state = invo_read.get('state')
        invo_read.update({
            'company_id': 1,
            'partner_id': get_destiny_id(destiny, pre,
                                         invo_read.get('partner_id'),
                                         'res_partner'),
            'account_id': get_destiny_id(destiny, pre,
                                         invo_read.get('account_id'),
                                         'account_account'),
            'fiscal_position': get_destiny_id(destiny, pre, invo_read.
                                              get('fiscal_position'),
                                              'account_fiscal_position'),
            'user_id': get_destiny_id(destiny, pre, invo_read.get('user_id'),
                                      'res_users'),
            'partner_bank_id': get_destiny_id(destiny, pre, invo_read.
                                              get('partner_bank_id'),
                                              'res_partner_bank'),
            'journal_id': get_destiny_id(destiny, pre,
                                         invo_read.get('journal_id'),
                                         'account_journal'),
            'period_id': get_destiny_id(destiny, pre,
                                        invo_read.get('period_id'),
                                        'account_period'),
            'sale_order_date': invo_read.get('sale_order_date'),
            'pay_method_id': get_destiny_id(destiny, pre,
                                            invo_read.get('pay_method'),
                                            'pay_method'),
            'invoice_line': prepare_order_lines(destiny, origin, pre,
                                                invo_read.
                                                get('invoice_line')),
            'move_id': False,
            'state': 'draft',
            'tax_line': create_tax_line(destiny, origin, pre,
                                        invo_read.get('tax_line')),
            'currency_id': get_currency(destiny, origin, pre,
                                        invo_read.get('currency_id')),
        })
        inv_id = destiny.search('account.invoice',
                                [('internal_number', '=',
                                  invo_read.get('internal_number'))])
        if not inv_id:
            inv_id = destiny.create('account.invoice', invo_read)
        else:
            inv_id = inv_id and inv_id[0]

        new_invo_read = destiny.read('account.invoice', inv_id, ['state'])
        if state == new_invo_read.get('state') or state == 'draft':
            continue

        destiny.execute('account.invoice', 'button_reset_taxes', [inv_id])
        if invo_read.get('type') in ('in_invoice', 'in_refund'):
            destiny.execute('account.invoice', 'button_compute', [inv_id],
                            True)
        if move_id:
            try:
                destiny.exec_workflow('account.invoice', 'invoice_open',
                                      inv_id)
            except BaseException, e:
                click.echo('No pude validar %s por %s' %
                           (invo_read.get('name'), e))
                continue
            line_ids = origin.search('account.move.line',
                                     [('move_id', '=', move_id),
                                      ('reconcile_partial_id', '!=', False)])
            if line_ids:
                rec_id = origin.execute('account.move.line', 'read',
                                        line_ids[0],
                                        ['reconcile_partial_id'], {},
                                        '_classic_write')
                rec_id = rec_id['reconcile_partial_id']
                new_rec_id = get_reconcile(destiny, origin, rec_id, move_id,
                                           pre)
                new_move_id = destiny.execute('account.invoice', 'read',
                                              inv_id, ['move_id'], {},
                                              '_classic_write')['move_id']
                line_id = destiny.search('account.move.line',
                                         [('move_id', '=', new_move_id),
                                          ('account_id', '=',
                                           invo_read.get('account_id'))])
                destiny.write('account.move.line', line_id,
                              {'reconcile_partial_id': new_rec_id})

if __name__ == '__main__':
    import_invoices()
