import oerplib

HOST=''
PORT=
DB=''
USER=''
PASS=''

con_dest = oerplib.OERP(
server=HOST, 
database=DB, 
port=PORT, 
)  

con_dest.login(USER, PASS)

HOST=''
PORT=
DB=''
USER=''
PASS=''

con_orig = oerplib.OERP(
server=HOST, 
database=DB, 
port=PORT, 
)  
print con_orig.db.list()
con_orig.login(USER, PASS)

class import_accountV6(object):
    def create_user_type(self, a_type):
        type_ids = con_dest.search('account.account.type',[('code', '=', a_type.code)])
        if type_ids:
            return type_ids[0]
        else:
            types = {
                    'name': a_type.name,
                    'code': a_type.code,
                    'report_type': a_type.report_type,
                    'close_method': a_type.close_method,
                    }

            type_id = con_dest.create('account.account.type', types)

            return type_id

    def get_code(self, code, company):
        account_ids = con_dest.search('account.account',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code

    def create_account(self, account_brw, company):
        account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                         ('code', '=', account_brw.code),
                                                         ('company_id', '=', company.id)])
        if account_ids:
            return account_ids[0]
        account = {
                'name': account_brw.name,
                'code': self.get_code(account_brw.code, company.id),
                'parent_id': account_brw.parent_id and \
                                                self.create_account(account_brw.parent_id,
                                                                    company) or
                                                False,
                'company_id': company.id, 
                'currency_id': company.currency_id and company.currency_id.id, 
                'user_type': self.create_user_type(account_brw.user_type), 

                }

        print 'Creating acccount %s' % account_brw.name
        account_id = con_dest.create('account.account', account)
        return account_id

    def main(self):
        company_ids = con_orig.search('res.company', [])
        company_id = False
        for company in con_orig.browse('res.company', company_ids):
            company_id = [True for i in company.partner_id.address \
                                                    if i.country_id.code == 'VE'] and company.id
            if company_id:
                break

        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            account_ids = con_orig.search('account.account', [('company_id', '=', company_id)])
            for account in con_orig.browse('account.account', account_ids):
                self.create_account(account, company_dest)




class import_journalV6(object):
    def create_sequence(self, a_type, company):
        if a_type:
            types = {
                    'name': a_type.name,
                    'company_id': company,
                    'prefix': a_type.prefix,
                    'suffix': a_type.suffix,
                    'padding': a_type.padding,
                    'number_increment': a_type.number_increment,
                    }

            type_id = con_dest.create('ir.sequence', types)
            return type_id

        return False

    def get_code(self, code, company):
        account_ids = con_dest.search('account.journal',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code


    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def create_analytic(self, journal_brw, company):
        journal_ids = con_dest.search('account.analytic.journal',[('name', '=', journal_brw.name),
                                                                  ('type', '=', journal_brw.type),
                                                                  ('code', '=', journal_brw.code),
                                                                  ('company_id', '=', company.id)])
        if journal_ids:
            return journal_ids[0]
        journal = {
                'name': journal_brw.name,
                'type': journal_brw.type,
                'code': journal_brw.code,
                'company_id': company.id, 
                }

        print 'Creating journal %s' % journal_brw.name
        journal_id = con_dest.create('account.analytic.journal', journal)
        return journal_id

    def create_journal(self, journal_brw, company):
        journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                         ('code', '=', journal_brw.code),
                                                         ('company_id', '=', company.id)])
        journal_id = False
        if journal_ids:
            return journal_ids[0]
        journal = {
                'name': journal_brw.name,
                'type': journal_brw.type,
                'code': self.get_code(journal_brw.code, company.id),
                'analytic_journal_id': journal_brw.analytic_journal_id and \
                                                self.create_analytic(journal_brw.analytic_journal_id,
                                                               company) or  False,
                'company_id': company.id, 
                'currency_id': company.currency_id and company.currency_id.id, 
                'sequence_id': self.create_sequence(journal_brw.sequence_id, company.id), 
                'default_debit_account_id': self.get_account(journal_brw.default_debit_account_id,
                                                                            company), 
                'default_credit_account_id': self.get_account(journal_brw.default_credit_account_id,
                                                         company), 
                }

        print 'Creating journal %s' % journal_brw.name
        try:
            journal_id = con_dest.create('account.journal', journal)
        except Exception, e:
            print 'Error %s' % e
        return journal_id

    def main(self):
        company_ids = con_orig.search('res.company', [])
        company_id = False
        for company in con_orig.browse('res.company', company_ids):
            company_id = [True for i in company.partner_id.address \
                                if i.country_id.code == 'VE'] and company.id
            if company_id:
                break

        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            journal_ids = con_orig.search('account.journal', [('company_id', '=', company_id)])
            for journal in con_orig.browse('account.journal', journal_ids):
                create_journal(journal, company_dest)

class import_partnerV6(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_address_and_child(self, partner, address, company):
        child = []
        partner_dict = {}
        invoice = False
        for i in address:
            if i.type == 'invoice' and not invoice:
                partner_dict.update({
                    'email': i.email,
                    'phone': i.phone,
                    'country_id': company.country_id and company.country_id.id,
                    'street': i.street,
                    'street2': i.street2,
                    'city': i.street2,
                    'mobile': i.mobile,
                    'fax': i.fax,
                    'type':i.type,
                    })
                invoice = True

            else:
                child.append((0,0, {
                    'name': i.name,
                    'email': i.email,
                    'property_account_payable': self.get_account(partner.property_account_payable,
                                                            company), 
                    'property_account_receivable': self.get_account(partner.property_account_receivable,
                                                               company),
                    'phone': i.phone,
                    'country_id': company.country_id and company.country_id.id,
                    'street': i.street,
                    'street2': i.street2,
                    'city': i.street2,
                    'mobile': i.mobile,
                    'fax': i.fax,
                    'type':i.type,
                    }))

        partner_dict.update({'child_ids': child})

        return partner_dict



    def create_partner(self, partner_brw, company, is_company=True, parent_id=False):
        partner_id = False
        partner = {
                'name': partner_brw.name,
                'vat': partner_brw.vat,
                'customer': partner_brw.customer,
                'is_company': True,
                'supplier': partner_brw.supplier,
                'company_id': company.id, 
                'property_account_payable': self.get_account(partner_brw.property_account_payable,
                                                        company), 
                'property_account_receivable': self.get_account(partner_brw.property_account_receivable,
                                                           company)
                }

        partner.update(get_address_and_child(partner_brw, partner_brw.address, company))

        partner_ids = con_dest.search('res.partner',[('name', '=', partner_brw.name),
                                                     ('vat', '=', partner_brw.vat),
                                                     ('type', '=', partner.get('type'))])
        if partner_ids:
            return partner_ids[0]

        print 'Creating partner %s' % partner_brw.name
        try:
            partner_id = con_dest.create('res.partner', partner)
        except Exception, e:
            print 'Error %s' % e
        return partner_id


    def main(self):
        company_ids = con_orig.search('res.company', [])
        company_id = False
        for company in con_orig.browse('res.company', company_ids):
            company_id = [True for i in company.partner_id.address \
                          if i.country_id.code == 'VE'] and \
                            company.id
            if company_id:
                break

        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            address_ids = con_orig.search('res.partner.address', [('country_id.code', '=', 'VE')])
            partner_ids = []
            for address in address_ids:
                address = con_orig.browse('res.partner.address', address)
                address.partner_id and partner_ids.append(address.partner_id.id)

            list(set(partner_ids))
            for partner in partner_ids:
                partner = con_orig.browse('res.partner', partner)
                self.create_partner(partner, company_dest)

class import_taxV6(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_code_tax(self, a_type, company):
        if not a_type:
            return False

        type_ids = con_dest.search('account.tax.code',[('code', '=', a_type.code),
                                                       ('name', '=', a_type.name),
                                                       ('company_id', '=', company),
                                                       ])
        if type_ids:
            return type_ids[0]
        else:
            types = {
                    'name': a_type.name,
                    'code': a_type.code,
                    'notprintable': a_type.notprintable,
                    'sign': a_type.sign,
                    'company_id': company,
                    'parent_id': self.get_code_tax(a_type.parent_id, company),
                    }

            type_id = con_dest.create('account.tax.code', types)

            return type_id

    def create_tax(self, tax_brw, company):
        tax_ids = con_dest.search('account.tax',[('name', '=', tax_brw.name),
                                                 ('description', '=', tax_brw.description),
                                                 ('company_id', '=', company.id)])
        if tax_ids:
            return tax_ids[0]
        tax = {
                'name': tax_brw.name,
                'base_sign': tax_brw.base_sign,
                'ref_base_sign': tax_brw.ref_base_sign,
                'tax_sign': tax_brw.tax_sign,
                'ref_tax_sign': tax_brw.ref_tax_sign,
                'child_depend': tax_brw.child_depend,
                'include_base_amount': tax_brw.include_base_amount,
                'description': tax_brw.description,
                'sequence': tax_brw.sequence,
                'type_tax_use': tax_brw.type_tax_use,
                'tax_voucher_ok': tax_brw.tax_voucher_ok,
                'price_include': tax_brw.price_include,
                'ret': tax_brw.ret,
                'type': tax_brw.type,
                'amount': tax_brw.amount,
                'account_collected_voucher_id': self.get_account(tax_brw.account_collected_voucher_id, company), 
                'account_paid_voucher_id': self.get_account(tax_brw.account_paid_voucher_id, company), 
                'account_collected_id': self.get_account(tax_brw.account_collected_id, company), 
                'account_paid_id': self.get_account(tax_brw.account_paid_id, company), 
                'base_code_id': self.get_code_tax(tax_brw.base_code_id, company.id), 
                'ref_base_code_id': self.get_code_tax(tax_brw.ref_base_code_id, company.id), 
                'ref_tax_code_id': self.get_code_tax(tax_brw.ref_tax_code_id, company.id), 
                'tax_code_id': self.get_code_tax(tax_brw.tax_code_id, company.id), 
                'company_id': company.id, 
                }



        print 'Creating tax %s' % tax_brw.name
        try:
            tax_id = con_dest.create('account.tax', tax)
        except Exception, e:
            print 'Error %s' % e
        return tax_id


    def main(self):
        company_ids = con_orig.search('res.company', [])
        company_id = False
        for company in con_orig.browse('res.company', company_ids):
            company_id = [True for i in company.partner_id.address if i.country_id.code == 'VE'] and \
                            company.id
            if company_id:
                break

        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            tax_ids = con_orig.search('account.tax', [('company_id', '=', company_id)])
            for tax in tax_ids:
                tax = con_orig.browse('account.tax', tax)
                self.create_tax(tax, company_dest)


class import_account(object):
    def create_user_type(self, a_type):
        type_ids = con_dest.search('account.account.type',[('code', '=', a_type.code)])
        if type_ids:
            return type_ids[0]
        else:
            types = {
                    'name': a_type.name,
                    'code': a_type.code,
                    'report_type': a_type.report_type,
                    'close_method': a_type.close_method,
                    }

            type_id = con_dest.create('account.account.type', types)

            return type_id

    def get_code(self, code, company):
        account_ids = con_dest.search('account.account',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code

    def create_account(self, account_brw, company):
        account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                         ('code', '=', account_brw.code),
                                                         ('company_id', '=', company.id)])
        if account_ids:
            return account_ids[0]
        account = {
                'name': account_brw.name,
                'type': account_brw.type,
                'code': self.get_code(account_brw.code, company.id),
                'parent_id': account_brw.parent_id and \
                                                self.create_account(account_brw.parent_id,
                                                                    company) or
                                                False,
                'company_id': company.id, 
                'currency_id': company.currency_id and company.currency_id.id, 
                'user_type': self.create_user_type(account_brw.user_type), 

                }

        print 'Creating acccount %s' % account_brw.name
        account_id = con_dest.create('account.account', account)
        return account_id

    def main(self):
        company_id = con_orig.search('res.company', ['name','=', 'No me importa'])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            account_ids = con_orig.search('account.account', [('company_id', '=', company_id)])
            for account in con_orig.browse('account.account', account_ids):
                self.create_account(account, company_dest)




class import_journal(object):
    def create_sequence(self, a_type, company):
        if a_type:
            types = {
                    'name': a_type.name,
                    'company_id': company,
                    'prefix': a_type.prefix,
                    'suffix': a_type.suffix,
                    'padding': a_type.padding,
                    'number_increment': a_type.number_increment,
                    }

            type_id = con_dest.create('ir.sequence', types)
            return type_id

        return False

    def get_code(self, code, company):
        account_ids = con_dest.search('account.journal',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code


    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def create_analytic(self, journal_brw, company):
        journal_ids = con_dest.search('account.analytic.journal',[('name', '=', journal_brw.name),
                                                                  ('type', '=', journal_brw.type),
                                                                  ('code', '=', journal_brw.code),
                                                                  ('company_id', '=', company.id)])
        if journal_ids:
            return journal_ids[0]
        journal = {
                'name': journal_brw.name,
                'type': journal_brw.type,
                'code': journal_brw.code,
                'company_id': company.id, 
                }

        print 'Creating journal %s' % journal_brw.name
        journal_id = con_dest.create('account.analytic.journal', journal)
        return journal_id

    def create_journal(self, journal_brw, company):
        journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                         ('code', '=', journal_brw.code),
                                                         ('company_id', '=', company.id)])
        journal_id = False
        if journal_ids:
            return journal_ids[0]
        journal = {
                'name': journal_brw.name,
                'type': journal_brw.type,
                'code': self.get_code(journal_brw.code, company.id),
                'analytic_journal_id': journal_brw.analytic_journal_id and \
                                                self.create_analytic(journal_brw.analytic_journal_id,
                                                               company) or  False,
                'company_id': company.id, 
                'currency_id': company.currency_id and company.currency_id.id, 
                'sequence_id': self.create_sequence(journal_brw.sequence_id, company.id), 
                'default_debit_account_id': self.get_account(journal_brw.default_debit_account_id,
                                                                            company), 
                'default_credit_account_id': self.get_account(journal_brw.default_credit_account_id,
                                                         company), 
                }

        print 'Creating journal %s' % journal_brw.name
        try:
            journal_id = con_dest.create('account.journal', journal)
        except Exception, e:
            print 'Error %s' % e
        return journal_id

    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0] 
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            journal_ids = con_orig.search('account.journal', [('company_id', '=', company_id)])
            for journal in con_orig.browse('account.journal', journal_ids):
                self.create_journal(journal, company_dest)

class import_partner(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_parent_id(self, partner, company):
        if partner:
            partner_id = con_dest.search('res.partner', [('name', '=', partner.name),
                                                         ('vat', '=', partner.vat),
                                                         ('company_id', '=', company.id)])
            if partner_id:
                return partner_id[0]
            else:
                return self.create_partner(partner, company)

        return False
    def get_category(self, categories, company, one=False):
        category_ids = []
        if categories:
            for category in categories:
                category_id = con_dest.search('res.partner.category',
                                              [('name', '=', category.name),
                                               ('active', '=', category.active)])
                if category_id and one:
                    return category_id[0]

                elif category_id and not one:
                    category_ids.append(category_id[0])

                else:
                    category_dict = {
                            'name': category.name,
                            'active': category.active,
                            'parent_id': self.get_category([category.parent_id], company, True)
                            
                            }
                    categ_id = con_dest.create('res.partner.category', category_dict)
                    if one:
                        return categ_id

                    else:
                        category_ids.append(category_id[0])

        return [(6, 0, category_ids)]

    def create_partner(self, partner_brw, company, is_company=True, parent_id=False):
        partner_id = False
        partner_ids = con_dest.search('res.partner',[('name', '=', partner_brw.name),
                                                     ('vat', '=', partner_brw.vat),
                                                     ('type', '=', partner_brw.type)])
        if partner_ids:
            return partner_ids[0]
        partner = {
                'name': partner_brw.name,
                'vat': partner_brw.vat,
                'customer': partner_brw.customer,
                'is_company': partner_brw.is_company,
                'email': partner_brw.email,
                'phone': partner_brw.phone,
                'parent_id': self.get_parent_id(partner_brw.parent_id, company),
                'category_id': self.get_category(partner_brw.category_id),
                'country_id': company.country_id and company.country_id.id,
                'street': partner_brw.street,
                'street2': partner_brw.street2,
                'city': partner_brw.street2,
                'mobile': partner_brw.mobile,
                'fax': partner_brw.fax,
                'type':partner_brw.type,
                'supplier': partner_brw.supplier,
                'company_id': company.id, 
                'property_account_payable': self.get_account(partner_brw.property_account_payable,
                                                        company), 
                'property_account_receivable': self.get_account(partner_brw.property_account_receivable,
                                                           company)
                }



        print 'Creating partner %s' % partner_brw.name
        try:
            partner_id = con_dest.create('res.partner', partner)
        except Exception, e:
            print 'Error %s' % e
        return partner_id


    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'No me importa')])
        company_id = company_id and company_id[0]

        company_dest = con_dest.search('res.company', [('country_id.code', '=', 'VE')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            partner_ids = con_orig.search('res.partner', [('company_id', '=', company_id)])
            for partner in partner_ids:
                partner = con_orig.browse('res.partner', partner)
                self.create_partner(partner, company_dest)

class import_tax(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_code_tax(self, a_type, company):
        if not a_type:
            return False

        type_ids = con_dest.search('account.tax.code',[('code', '=', a_type.code),
                                                       ('name', '=', a_type.name),
                                                       ('company_id', '=', company),
                                                       ])
        if type_ids:
            return type_ids[0]
        else:
            types = {
                    'name': a_type.name,
                    'code': a_type.code,
                    'notprintable': a_type.notprintable,
                    'sign': a_type.sign,
                    'company_id': company,
                    'parent_id': self.get_code_tax(a_type.parent_id, company),
                    }

            type_id = con_dest.create('account.tax.code', types)

            return type_id

    def create_tax(self, tax_brw, company):
        tax_ids = con_dest.search('account.tax',[('name', '=', tax_brw.name),
                                                 ('description', '=', tax_brw.description),
                                                 ('company_id', '=', company.id)])
        if tax_ids:
            return tax_ids[0]
        tax = {
                'name': tax_brw.name,
                'base_sign': tax_brw.base_sign,
                'ref_base_sign': tax_brw.ref_base_sign,
                'tax_sign': tax_brw.tax_sign,
                'ref_tax_sign': tax_brw.ref_tax_sign,
                'child_depend': tax_brw.child_depend,
                'include_base_amount': tax_brw.include_base_amount,
                'description': tax_brw.description,
                'sequence': tax_brw.sequence,
                'type_tax_use': tax_brw.type_tax_use,
                'tax_voucher_ok': tax_brw.tax_voucher_ok,
                'price_include': tax_brw.price_include,
               # 'ret': tax_brw.ret,
                'type': tax_brw.type,
                'amount': tax_brw.amount,
                'account_collected_voucher_id': self.get_account(tax_brw.account_collected_voucher_id, company), 
                'account_paid_voucher_id': self.get_account(tax_brw.account_paid_voucher_id, company), 
                'account_collected_id': self.get_account(tax_brw.account_collected_id, company), 
                'account_paid_id': self.get_account(tax_brw.account_paid_id, company), 
                'base_code_id': self.get_code_tax(tax_brw.base_code_id, company.id), 
                'ref_base_code_id': self.get_code_tax(tax_brw.ref_base_code_id, company.id), 
                'ref_tax_code_id': self.get_code_tax(tax_brw.ref_tax_code_id, company.id), 
                'tax_code_id': self.get_code_tax(tax_brw.tax_code_id, company.id), 
                'company_id': company.id, 
                }



        print 'Creating tax %s' % tax_brw.name
        try:
            tax_id = con_dest.create('account.tax', tax)
        except Exception, e:
            print 'Error %s' % e
        return tax_id


    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            tax_ids = con_orig.search('account.tax', [('company_id', '=', company_id)])
            for tax in tax_ids:
                tax = con_orig.browse('account.tax', tax)
                self.create_tax(tax, company_dest)


class import_product(object):

    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_uom(self, uom_brw):
        if uom_brw:
            uom_ids = con_dest.search('product.uom',[('name', '=', uom_brw.name),
                                                     ('uom_type', '=', uom_brw.uom_type),
                                                     ('rounding', '=', uom_brw.rounding)])
            return uom_ids and uom_ids[0]

        return False

    def get_journal(self, journal_brw, company):
        if journal_brw:
            journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                             ('code', '=', journal_brw.code),
                                                             ('company_id', '=', company.id)])
            return journal_ids and journal_ids[0]

        return False

    def get_location(self, stock_brw, company):
        if stock_brw:
            stock_ids = con_dest.search('stock.location',[('name', '=', stock_brw.name),
                                                          ('usage', '=', stock_brw.usage),
                                                          ('company_id', '=', company.id)])
            return stock_ids and stock_ids[0]

        return False

    def get_taxes(self, tax_brw, company):
        taxes = []
        for tax in tax_brw:
            taxes += con_dest.search('account.tax',[('name', '=', tax.name),
                                                    ('description', '=', tax.description),
                                                    ('company_id', '=', company.id)])

        return [(6, 0, taxes)] 

    def create_category(self, category, company, one=False):
        category_ids = []
        if category:
            category_id = con_dest.search('product.category',
                                          [('name', '=', category.name),
                                           ('type', '=', category.type)])
            if category_id:
                return category_id[0]

            else:
                category_dict = {
                        'name': category.name,
                        'type': category.type,
                        'parent_id': self.create_category(category.parent_id, company),
                       # 'property_account_creditor_price_difference_categ':
                       # self.get_account(category.property_account_creditor_price_difference_categ,
                       #                  company), 
                        'property_account_expense_categ':self.get_account(category.property_account_expense_categ, company), 
                        'property_account_income_categ': self.get_account(category.property_account_income_categ, company), 
                        'property_stock_account_input_caqeg':self.get_account(category.property_stock_account_input_categ, company), 
                        'property_stock_account_output_categ':self.get_account(category.property_stock_account_output_categ, company), 
                        'property_stock_valuation_account_id':self.get_account(category.property_stock_valuation_account_id, company), 
                        'property_stock_journal':self.get_journal(category.property_stock_journal, company), 
                        
                        }
                categ_id = con_dest.create('product.category', category_dict)
                return categ_id

        return False


    def create_product(self, product_brw, company):
        product_ids = con_dest.search('product.product',
                                      [('name', '=', product_brw.name),
                                       ('default_code', '=', product_brw.default_code),
                                       ('company_id', '=', company.id)])
        if product_ids:
            return product_ids[0]
        product = {
                'name': product_brw.name,
                'default_code': product_brw.default_code,
                'ean13': product_brw.ean13,
                'type': product_brw.type,
                'list_price': product_brw.list_price,
                'procure_method': product_brw.procure_method,
                'supply_method': product_brw.supply_method,
                'cost_method': product_brw.cost_method,
                'standard_price': product_brw.standard_price,
                'active': product_brw.active,
                'warranty': product_brw.warranty,
                'sale_delay': product_brw.sale_delay,
                'description_sale': product_brw.description_sale,
                'produce_delay': product_brw.produce_delay,
                'valuation': product_brw.valuation,
                'categ_id': self.create_category(product_brw.categ_id, company),
                'uom_id': self.get_uom(product_brw.uom_id),
                'uom_po_id': self.get_uom(product_brw.uom_po_id),
                'property_stock_procurement':
                                self.get_location(product_brw.property_stock_procurement, company),
                'property_stock_production':
                                self.get_location(product_brw.property_stock_production, company),
                'property_stock_inventory':
                                self.get_location(product_brw.property_stock_inventory, company),
               # 'property_account_creditor_price_difference':
               #            self.get_account(product_brw.property_account_creditor_price_difference,
               #                                             company), 
                'property_account_income': self.get_account(product_brw.property_account_income,
                                                            company), 
                'property_account_expense': self.get_account(product_brw.property_account_expense,
                                                             company), 
                'taxes_id': self.get_taxes(product_brw.taxes_id, company), 
                'supplier_taxes_id': self.get_taxes(product_brw.supplier_taxes_id, company), 
                'company_id': company.id, 
                }



        print 'Creating product %s' % product_brw.name
        try:
            product_id = con_dest.create('product.product', product)
        except Exception, e:
            print 'Error %s' % e
            product_id = False
        return product_id


    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            product_ids = con_orig.search('product.product', [('company_id', '=', company_id)])
            for product in product_ids:
                product = con_orig.browse('product.product', product)
                self.create_product(product, company_dest)

class import_uom(object):

    def get_category(self, uom_brw):
        if uom_brw:
            uom_ids = con_dest.search('product.uom.categ',[('name', '=', uom_brw.name)])
            if uom_ids:
                return uom_ids and uom_ids[0]
            else:
                uom_id = con_dest.create('product.uom.categ',{'name': uom_brw.name})
                return uom_id

        return False

    def create_uom(self, uom_brw, company):
        uom_id = False
        uom_ids = con_dest.search('product.uom',[('name', '=', uom_brw.name),
                                                 ('uom_type', '=', uom_brw.uom_type),
                                                 ('rounding', '=', uom_brw.rounding)])
        if uom_ids:
            return uom_ids[0]

        uom = {
                'name': uom_brw.name,
                'uom_type': uom_brw.uom_type,
                'rounding': uom_brw.rounding,
                'factor': uom_brw.factor,
                'category_id': self.get_category(uom_brw.category_id)
                }



        print 'Creating uom %s' % uom_brw.name
        try:
            uom_id = con_dest.create('product.uom', uom)
        except Exception, e:
            print 'Error %s' % e
        return uom_id


    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            uom_data = con_orig.search('ir.model.data', [('model', '=', 'product.uom')])
            uom_ids = []
            for ids in uom_data:
                data_brw = con_orig.browse('ir.model.data', ids)
                uom_ids.append(data_brw.res_id)
            uom_ids = con_orig.search('product.uom', [])
           # uom_ids_all = con_orig.search('product.uom', [])
           # uom_ids = list(set(uom_ids_all) - set(uom_ids))
            for uom in uom_ids:
                uom = con_orig.browse('product.uom', uom)
                self.create_uom(uom, company_dest)

class import_account_asset(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_journal(self, journal_brw, company):
        if journal_brw:
            journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                             ('code', '=', journal_brw.code),
                                                             ('company_id', '=', company.id)])
            return journal_ids and journal_ids[0]

        return False

    def get_category(self, category, company):
        category_ids = con_dest.search('account.asset.category',[('name', '=', category.name)])
        if category_ids:
            return category_ids[0]
        else:
            categories = {
                    'name': category.name,
                    'method_time': category.method_time,
                    'method_number': category.method_number,
                    'method_period': category.method_period,
                    'method': category.method,
                    'prorata': category.prorata,
                    'note': category.note,
                    'open_asset': category.open_asset,
                    'account_asset_id': self.get_account(category.account_asset_id, company), 
                    'journal_id': self.get_journal(category.journal_id, company), 
                    'account_depreciation_id': self.get_account(category.account_depreciation_id,
                                                                company), 
                    'account_expense_depreciation_id':
                    self.get_account(category.account_expense_depreciation_id,
                                                                company), 
                    }

            category_id = con_dest.create('account.asset.category', categories)

            return category_id

    def get_code(self, code, company):
        account_ids = con_dest.search('account.account',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code

    def get_partner_id(self, partner_brw, company):
        if partner_brw:
            partner_ids = con_dest.search('res.partner',[('name', '=', partner_brw.name),
                                                         ('vat', '=', partner_brw.vat),
                                                         ('company_id', '=', company.id)])
            return partner_ids and partner_ids[0]

        return False

    def get_currency_id(self, currency_brw, company):
        if currency_brw:
            currency_ids = con_dest.search('res.currency',[('name', '=', currency_brw.name),
                                                         ('company_id', '=', company.id)])
            return currency_ids and currency_ids[0]

        return False

    def get_description(self, description):
        lines = []
        for descript in description:
            line = (0, 0, {
                'name': descript.name,
                'sequence': descript.sequence,
                'amount': descript.amount,
                'move_check': descript.move_check,
                'remaining_value': descript.remaining_value,
                'depreciated_value': descript.depreciated_value,
                'depreciation_date': descript.depreciation_date.strftime('%Y-%m-%d'),
                    })
            lines.append(line)

        return lines

    def create_account(self, account_brw, company):
        account_ids = con_dest.search('account.asset.asset',[('name', '=', account_brw.name),
                                                         ('code', '=', account_brw.code),
                                                         ('company_id', '=', company.id)])
        if account_ids:
            return account_ids[0]
        account = {
                'name': account_brw.name,
                'code': account_brw.code,
                'purchase_value': account_brw.purchase_value,
                'salvage_value': account_brw.salvage_value,
                'salvage_value': account_brw.salvage_value,
                'method': account_brw.method,
                'method_time': account_brw.method_time,
                'method_number': account_brw.method_number,
                'method_period': account_brw.method_period,
                'purchase_date': account_brw.purchase_date.strftime('%Y-%m-%d'),
                'prorata': account_brw.prorata,
                'depreciation_line_ids': self.get_description(account_brw.depreciation_line_ids),
                'category_id': self.get_category(account_brw.category_id, company),
                'partner_id': self.get_partner_id(account_brw.partner_id, company),
                'currency_id': self.get_currency_id(account_brw.currency_id, company),
                'parent_id': account_brw.parent_id and \
                                                self.create_account(account_brw.parent_id,
                                                                    company) or False,
                'company_id': company.id, 

                }

        print 'Creating acccount %s' % account_brw.name
        print account
        account_id = con_dest.create('account.asset.asset', account)
        return account_id

    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            account_ids = con_orig.search('account.asset.asset', [('company_id', '=', company_id)])
            for account in con_orig.browse('account.asset.asset', account_ids):
                self.create_account(account, company_dest)



class import_hr_employee(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_journal(self, journal_brw, company):
        if journal_brw:
            journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                             ('code', '=', journal_brw.code),
                                                             ('company_id', '=', company.id)])
            return journal_ids and journal_ids[0]

        return False

    def get_department_id(self, department, company):
        if department:
            department_ids = con_dest.search('hr.department',[('name', '=', department.name),
                                                              ('company_id', '=', company.id)])
            if department_ids:
                return department_ids[0]
            else:
                department = {
                        'name': department.name,
                        'parent_id': self.get_department_id(department.parent_id, company),
                        #'analytic_account_id': self.get_analytic(department.analytic_account_id, company),
                        'manager_id': department.manager_id and self.create_hr(department.manager_id, company),
                        'company_id': company.id,
                        }

                department_id = con_dest.create('hr.department', department)

                return department_id

    def get_job_id(self, job, company):
        if job:
            job_ids = con_dest.search('hr.job',[('name', '=', job.name)])
            if job_ids:
                return job_ids[0]
            else:
                job = {
                        'name': job.name,
                        'description': job.description,
                        'department_id': self.get_department_id(job.department_id, company),
                        }

                job_id = con_dest.create('hr.job', job)

                return job_id

    def get_code(self, code, company):
        account_ids = con_dest.search('account.account',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code

    def get_partner_id(self, partner_brw, company):
        if partner_brw:
            partner_ids = con_dest.search('res.partner',[('name', '=', partner_brw.name),
                                                         ('vat', '=', partner_brw.vat),
                                                         ('company_id', '=', company.id)])
            return partner_ids and partner_ids[0]

        return False

    def get_analytic(self, analytic, company):
        if analytic:
            analytic_ids = con_dest.search('account.analytic.account',
                                          [('name', '=', analytic.name),
                                           ('code', '=', analytic.code),
                                           ('type', '=', analytic.type),
                                           ('company_id', '=', company.id)])
            return analytic_ids and analytic_ids[0]

        return False

    def get_user_id(self, user_brw, company):
        if user_brw:
            user_ids = con_dest.search('res.users',[('name', '=', user_brw.name),
                                                   ('login', '=', user_brw.login)])
            return user_ids and user_ids[0]

        return False

    def get_description(self, description):
        lines = []
        for descript in description:
            line = (0, 0, {
                'name': descript.name,
                'sequence': descript.sequence,
                'amount': descript.amount,
                'move_check': descript.move_check,
                'remaining_value': descript.remaining_value,
                'depreciated_value': descript.depreciated_value,
                'depreciation_date': descript.depreciation_date.strftime('%Y-%m-%d'),
                    })
            lines.append(line)

        return lines

    def create_hr(self, hr_brw, company):
        hr_ids = con_dest.search('hr.employee',[('name', '=', hr_brw.name),
                                                ('work_email', '=', hr_brw.work_email),
                                                ('company_id', '=', company.id)])
        if hr_ids:
            return hr_ids[0]
        hr = {
                'name': hr_brw.name,
                'company_id': company.id, 
                'work_email': hr_brw.work_email,
                'work_phone': hr_brw.work_phone,
                'work_location': hr_brw.work_location,
                'mobile_phone': hr_brw.mobile_phone,
                'visibility': hr_brw.visibility,
                'address_id': self.get_partner_id(hr_brw.address_id, company),
                #'account_analytic_id': self.get_analytic(hr_brw.account_analytic_id, company),
                'user_id': self.get_user_id(hr_brw.user_id, company),
                'department_id': self.get_department_id(hr_brw.department_id, company),
                'parent_id': hr_brw.parent_id and \
                                                self.create_hr(hr_brw.parent_id, company) or False,
                'coach_id': hr_brw.coach_id and self.create_hr(hr_brw.coach_id, company) or False,

                }

        print 'Creating Employee %s' % hr_brw.name
        hr_id = con_dest.create('hr.employee', hr)
        return hr_id

    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            hr_ids = con_orig.search('hr.employee', [('company_id', '=', company_id)])
            print 'hr_ids',hr_ids
            for hrs in hr_ids:
                hr = con_orig.browse('hr.employee', hrs)
                print 'otro'
                self.create_hr(hr, company_dest)



class import_lots(object):
    def get_account(self, account_brw, company):
        if account_brw:
            account_ids = con_dest.search('account.account',[('name', '=', account_brw.name),
                                                             ('code', '=', account_brw.code),
                                                             ('company_id', '=', company.id)])
            return account_ids and account_ids[0]

        return False

    def get_journal(self, journal_brw, company):
        if journal_brw:
            journal_ids = con_dest.search('account.journal',[('name', '=', journal_brw.name),
                                                             ('code', '=', journal_brw.code),
                                                             ('company_id', '=', company.id)])
            return journal_ids and journal_ids[0]

        return False

    def get_department_id(self, department, company):
        if department:
            department_ids = con_dest.search('hr.department',[('name', '=', department.name),
                                                              ('company_id', '=', company.id)])
            if department_ids:
                return department_ids[0]
            else:
                department = {
                        'name': department.name,
                        'parent_id': self.get_department_id(department.parent_id, company),
                        #'analytic_account_id': self.get_analytic(department.analytic_account_id, company),
                        'manager_id': department.manager_id and self.create_lot(department.manager_id, company),
                        'company_id': company.id,
                        }

                department_id = con_dest.create('hr.department', department)

                return department_id

    def get_job_id(self, job, company):
        if job:
            job_ids = con_dest.search('hr.job',[('name', '=', job.name)])
            if job_ids:
                return job_ids[0]
            else:
                job = {
                        'name': job.name,
                        'description': job.description,
                        'department_id': self.get_department_id(job.department_id, company),
                        }

                job_id = con_dest.create('hr.job', job)

                return job_id

    def get_code(self, code, company):
        account_ids = con_dest.search('account.account',[('code', '=', code),
                                                         ('company_id', '=', company)])
        if account_ids:
            new_code = '%s-%s' %(code, 'R')
            return self.get_code(new_code, company)

        else:
            return code

    def get_partner_id(self, partner_brw, company):
        if partner_brw:
            partner_ids = con_dest.search('res.partner',[('name', '=', partner_brw.name),
                                                         ('vat', '=', partner_brw.vat),
                                                         ('company_id', '=', company.id)])
            return partner_ids and partner_ids[0]

        return False

    def get_analytic(self, analytic, company):
        if analytic:
            analytic_ids = con_dest.search('account.analytic.account',
                                          [('name', '=', analytic.name),
                                           ('code', '=', analytic.code),
                                           ('type', '=', analytic.type),
                                           ('company_id', '=', company.id)])
            return analytic_ids and analytic_ids[0]

        return False

    def get_user_id(self, user_brw, company):
        if user_brw:
            user_ids = con_dest.search('res.users',[('name', '=', user_brw.name),
                                                   ('login', '=', user_brw.login)])
            return user_ids and user_ids[0]

        return False

    def get_product_id(self, product_brw, company):
        if product_brw:
            product_ids = con_dest.search('product.product',[('name', '=', product_brw.name),
                                                             ('default_code', '=', product_brw.default_code),
                                                             ('company_id', '=', company.id)])
            return product_ids and product_ids[0]

        return False

    def get_description(self, description):
        lines = []
        for descript in description:
            line = (0, 0, {
                'name': descript.name,
                'sequence': descript.sequence,
                'amount': descript.amount,
                'move_check': descript.move_check,
                'remaining_value': descript.remaining_value,
                'depreciated_value': descript.depreciated_value,
                'depreciation_date': descript.depreciation_date.strftime('%Y-%m-%d'),
                    })
            lines.append(line)

        return lines

    def create_lot(self, lot_brw, company):
        lot_ids = con_dest.search('stock.production.lot',
                                  [('name', '=', lot_brw.name),
                                   ('product_id', '=', lot_brw.product_id.id),
                                   ('company_id', '=', company.id)])
        if lot_ids:
            return lot_ids[0]
        lot = {
                'name': lot_brw.name,
                'company_id': company.id, 
                'product_id': self.get_product_id(lot_brw.product_id, company),
                'prefix': lot_brw.prefix,
                'ref': lot_brw.ref,
                'date': lot_brw.date.strftime('%Y-%m-%d'),
                }

        print 'Creating Lot %s' % lot_brw.name
        lot_id = con_dest.create('stock.production.lot', lot)
        return lot_id

    def main(self):
        company_id = con_orig.search('res.company', [('name', '=', 'Bioderpac')])
        company_id = company_id and company_id[0]
        company_dest = con_dest.search('res.company', [('name', '=', 'Bioderpac')])
        if company_id and company_dest:
            company_dest = con_dest.browse('res.company', company_dest[0])
            lot_ids = con_orig.search('stock.production.lot', [('company_id', '=', company_id)])
            print 'lot_ids',lot_ids
            for lot in con_orig.browse('stock.production.lot', lot_ids):
                self.create_lot(lot, company_dest)



asset = import_lots()
asset.main()
asset = import_hr_employee()
asset.main()
