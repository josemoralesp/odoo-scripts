import odoorpc
import click


def change_values(fields, values, field, new_val):
    """Used to modify values in list of value import from origin"""
    index = fields.index(field)
    values[index] = new_val
    return values


def get_values(fields, values, field):
    """Used to get a value in list of values import from origin"""
    index = fields.index(field)
    return values[index]


@click.command()
@click.option('-cd', default=,
              prompt='Company ID destiny', help='Company id from destiny')
@click.option('-co', default=,
              prompt='Company ID Origin', help='Company id from origin')
@click.option('-pod', default=,
              prompt='Port Destiny', help='Port of server Destiny')
@click.option('-pd', default=,
              prompt='Password Destiny', help='Password Destiny')
@click.option('-dbd', default=,
              prompt='Database Destiny', help='DB Destiny')
@click.option('-ud', default=,
              prompt='User name Destiny', help='your email or login')
@click.option('-poo', default=,
              prompt='Port Origin', help='Port of origin of data')
@click.option('-po', default=,
              prompt='Password Origin', help='Password Origin')
@click.option('-dbo', default=,
              prompt='Database Origin', help='DB Origin')
@click.option('-uo', default=,
              prompt='User name Origin', help='your email or login')
def import_partners(cd, co, po, dbo, uo, poo, pod, pd, dbd, ud):
    '''
    If you dont know how to execute this script use
    python import_invoice.py --help


    you still need to modify the IP, Protocol, and Portparameters.
    '''
    origin = odoorpc.ODOO('localhost',
                          port=poo,
                          timeout=9999999999999999)
    # destiny = oerplib.OERP(server='',
    destiny = odoorpc.ODOO('localhost',
                           port=pod,
                           timeout=9999999999999999)
    origin.login(login=uo, password=po, db=dbo)
    destiny.login(login=ud, password=pd, db=dbd)
    nrecords = None

    export_fields = ['id', 'name', 'activation', 'website_description',
                     'image_medium', 'debit_limit', 'signup_token',
                     'create_date', 'street', 'debit', 'supplier', 'ref',
                     'email', 'picking_warn', 'street2', 'active', 'zip',
                     'comment', 'sale_warn', 'purchase_warn', 'color', 'image',
                     'city', 'type', 'function', 'picking_warn_msg', 'phone',
                     'customer', 'vat', 'invoice_warn_msg', 'website',
                     'sale_warn_msg', 'invoice_warn', 'is_company',
                     'write_date', 'date', 'lang', 'purchase_warn_msg',
                     'mobile', 'image_small', 'signup_type',
                     'date_partnership', 'partner_longitude',
                     'calendar_last_notif_ack', 'signup_expiration',
                     'website_meta_keywords', 'date_review',
                     'website_meta_description', 'date_review_next',
                     'message_last_post', 'partner_latitude', 'tz', 'employee',
                     'website_meta_title', 'fax', 'country_id/id',
                     'category_id/id', 'title/id', 'ean13', 'l10n_mx_street3',
                     'l10n_mx_street4', 'l10n_mx_city2', 'nacionality_diot',
                     'type_of_third', 'type_of_operation',
                     'property_supplier_payment_term', 'property_payment_term',
                     'regimen_fiscal_id', 'company_id/id', 'website_published',
                     'opt_out', 'notify_email', 'credit_limit']

    import_fields = ['id', 'name', 'activation', 'website_description',
                     'image_medium', 'debit_limit', 'signup_token',
                     'create_date', 'street', 'debit', 'supplier', 'ref',
                     'email', 'picking_warn', 'street2', 'active',
                     # 'email', 'picking_warn', 'l10n_mx_edi_colony', 'active',
                     'zip', 'comment', 'sale_warn', 'purchase_warn', 'color',
                     'image', 'city', 'type', 'function', 'picking_warn_msg',
                     'phone', 'customer', 'vat', 'invoice_warn_msg', 'website',
                     'sale_warn_msg', 'invoice_warn', 'company_type',
                     'write_date', 'date', 'lang', 'purchase_warn_msg',
                     'mobile', 'image_small', 'signup_type',
                     'date_partnership', 'partner_longitude',
                     'calendar_last_notif_ack', 'signup_expiration',
                     'website_meta_keywords', 'date_review',
                     'website_meta_description', 'date_review_next',
                     'message_last_post', 'partner_latitude', 'tz', 'employee',
                     'website_meta_title', 'fax', 'country_id/id',
                     'category_id/id', 'title/id', 'barcode', 'street_number',
                     'street_number2', 'l10n_mx_edi_locality',
                     'l10n_mx_nationality', 'l10n_mx_type_of_third',
                     'l10n_mx_type_of_operation',
                     'property_supplier_payment_term_id',
                     'property_payment_term_id',
                     'property_account_position_id', 'company_id/id',
                     'website_published', 'opt_out', 'notify_email',
                     'credit_limit', 'property_account_payable_id/id',
                     'property_account_receivable_id/id']
    # print export_fields
    partner_ids = origin.execute('res.partner', 'search', [])
    if nrecords:
        partner_ids = partner_ids[:nrecords]
    click.echo("Partners to create " + str(len(partner_ids)))
    partner_data = origin.execute(
        'res.partner', 'export_data', partner_ids, export_fields)
    for (item, partner) in enumerate(partner_data.get('datas', []), 1):
        change_values(import_fields, partner, 'company_id/id', False)
        change_values(import_fields, partner, 'website_published', False)
        change_values(import_fields, partner, 'opt_out', False)
        change_values(import_fields, partner, 'notify_email', 'none')
        change_values(import_fields, partner, 'credit_limit', 0)
        partner.append('l10n_mx.1_cuenta201_01')
        partner.append('l10n_mx.1_cuenta105_01')
        is_company = get_values(import_fields, partner, 'company_type')
        change_values(import_fields, partner, 'company_type',
                      'Company' if is_company else 'Individual')
        dtype = get_values(import_fields, partner, 'type')
        change_values(import_fields, partner, 'type', 'Contact')
        if dtype == u'Invoice':
            change_values(import_fields, partner, 'type', 'Invoice address')
        lang = get_values(import_fields, partner, 'lang')
        if lang in ['es_MX', 'es_VE', 'es_PA']:
            change_values(import_fields, partner,
                          'lang', u'Spanish / Espa\xf1ol')
        vat = get_values(import_fields, partner, 'vat')
        if vat and vat in ['ec', 'es', 'mx', 'pe', 've']:
            change_values(import_fields, partner, 'vat', vat[:2])
        result = destiny.execute(
            'res.partner', 'load', import_fields, [partner])
        if result.get('messages'):
            click.echo(
                'Error importing partner because %s' %
                result.get('messages', {}).get('message'))

if __name__ == '__main__':
    import_partners()
