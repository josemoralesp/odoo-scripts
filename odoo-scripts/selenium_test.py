# pip install selenium==2.53.6
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import click


class BasicFlow(object):

    def __init__(self, **args):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(15)
        self.product = args.get('product')
        self.partner = args.get('partner')
        self.driver.get(
            '%(server)s/'
            'login?db=%(db)s&'
            'login=%(user)s&key=%(password)s' % args)
        time.sleep(3)

    def go_to_sale_form(self):
        """Method used to move us from main window to view for of sale order
        """
        driver = self.driver
        salemenu = "(//a[contains(span, 'Sales')])[1]"
        salemenu = WebDriverWait(driver, 1).until(
            lambda driver: driver.find_element_by_xpath(salemenu))
        salemenu.click()
        time.sleep(2)
        salemenu = "//a[contains(span, 'Sales Orders')]"
        salemenu = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(salemenu))
        salemenu.click()
        time.sleep(2)
        salemenu = "//button[contains(., 'Create')]"
        time.sleep(2)
        salemenu = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(salemenu))
        salemenu.click()

    def go_to_pickings(self):
        """Used to move us from order validated to pickings generated by it"""
        driver = self.driver
        time.sleep(10)
        pickingmenu = "//button[contains(., 'View Delivery Order')]"
        pickingmenu = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(pickingmenu))
        pickingmenu.click()
        time.sleep(3)

    def click_outside(self):
        """Used to do click in somewhere in the window to trigger the
        onchange"""
        self.driver.execute_script(
            "$('div.oe_form_sheet.oe_form_sheet_width').click()")
        time.sleep(1)

    def fill_form(self):
        """Fill the form for a new sale order, testing the onchanges for
        partner and product

        The partner used in this test was: ABA SEGUROS, S.A. DE C.V.
        The product used was: 6002

        The quantity and the price was modified after the product was loaded
        and the fields computed by onchange method returned, this to verify the
        recompute of the price
        """
        driver = self.driver
        partner = ("//span[contains(@class, "
                   "'oe_form_field_many2one')]/div/input")
        partner = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(partner))
        partner.clear()
        partner.send_keys(self.partner or 'ABA SEGUROS, S.A. DE C.V.')
        time.sleep(1)

        self.click_outside()

        line = "//a[contains(., 'Add an item')]"
        line = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(line))
        line.click()
        time.sleep(1)

        product = "//span[@data-fieldname='product_id']/div/input"
        product = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(product))
        product.clear()
        product.send_keys(self.product or '6002')
        time.sleep(1)

        self.click_outside()

        quantity = "//span[@data-fieldname='product_uom_qty']/input"
        quantity = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(quantity))
        quantity.clear()
        quantity.send_keys('10')

        price = "//span[@data-fieldname='price_unit']/input"
        price = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(price))
        price.clear()
        price.send_keys('150')

        self.click_outside()

        savebutton = ("//span[@class='oe_form_buttons_edit']"
                      "/button[contains(., 'Save')]")
        savebutton = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(savebutton))
        savebutton.click()

        buttonconfirm = "(//button[contains(span, 'Confirm Sale')])[1]"
        buttonconfirm = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(buttonconfirm))
        buttonconfirm.click()
        time.sleep(3)

    def validate_pick(self):
        """Validate a picking of type picking. The only picking in the list
        with state Waiting Availability.
        """
        driver = self.driver
        driver.execute_script(
            "$($('.oe_list_content')[3])."
            "find('tr :contains(Waiting Availability)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Check Availability)').click()"
            )
        time.sleep(2)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Transfer)').click()"
            )
        time.sleep(4)
        driver.execute_script(
            "$('div.modal-content button:contains(Apply)').click()")
        time.sleep(4)
        driver.execute_script(
            """$('li a[data-view-type="list"]').click()"""
            )
        time.sleep(4)

    def validate_pack(self, code='0'):
        """Validate the picking of type pack after the pick was validated.
        To validate this picking it is needed to put in package all quants used
        by the previous picking. For this we use the new windows create for
        picking of this type, where we specify the package and the number of
        products used for each package"""
        driver = self.driver
        driver.execute_script(
            "$('div.oe_view_manager.oe_view_manager_current"
            "[data-view-type=list]:not([style])')."
            "find('tr :contains(Ready to Transfer)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Transfer)').click()"
            )
        time.sleep(3)
        codes = ('%(code)s0536,%(code)s0537,%(code)s0538,'
                 '%(code)s0539,%(code)s0539' % {'code': code})
        for pack in codes.split(','):
            driver.execute_script(
                "$('span.pack_search input').val('%s')" % pack)
            driver.execute_script(
                "$('span.pack_search input').focus()."
                "trigger(jQuery.Event('keyup', { keycode: $.ui.keyCode.ENTER, "
                "which: $.ui.keyCode.ENTER   }))")
            time.sleep(2)
            driver.execute_script(
                """$('textarea[name="scan_data"]').val('%s*2')""" %
                (self.product or '6002'))
            time.sleep(1)
            driver.execute_script(
                """$('textarea[name="scan_data"]').focus()."""
                "trigger(jQuery.Event('keyup', { keycode: $.ui.keyCode.ENTER, "
                "which: $.ui.keyCode.ENTER  }))")
            time.sleep(1)
            driver.execute_script(
                "$('button:contains(Save in Cache)').click()")
            time.sleep(2)
        driver.execute_script(
            "$('button:contains(Validate)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('button:contains(Ok)').click()")
        time.sleep(6)

    def validate_out(self):
        """Validate the last picking in the list of pickins generated by the
        sale order. This pickings contains all quants processed from previous
        pickings and the customized new views"""
        driver = self.driver
        time.sleep(3)
        driver.execute_script(
            "$('div.oe_view_manager.oe_view_manager_current"
            "[data-view-type=list]:not([style])')."
            "find('tr :contains(Ready to Transfer)').click()")
        time.sleep(4)
        # driver.execute_script(
        #     "$('button:contains(Delivery Order)').click()")
        # time.sleep(2)
        driver.execute_script(
            "location.reload()")
        time.sleep(10)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Transfer)').click()"
            )
        time.sleep(4)
        driver.execute_script(
            "$('div.modal-content button:contains(Apply)').click()")

    def create_invoice(self):
        """Then the pickings were validated we go ahead to create the invoice
        from the last picking validated and the validate it to complete the
        sale process for this test"""
        driver = self.driver
        time.sleep(6)
        driver.execute_script(
            "$('button.oe_button.oe_form_button.oe_highlight:"
            "contains(Create Invoice):not(.oe_form_invisible)').click()")
        time.sleep(3)
        driver.execute_script(
            "$('div.modal-content button:contains(Create)').click()"
            )
        time.sleep(7)
        driver.execute_script(
            "$('div[data-view-type=list]:not([style])')."
            """find('tr td[data-field="origin"]"""
            ".oe_list_field_cell.oe_list_field_char:contains(OUT/)').click()")
        time.sleep(4)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Validate)').click()"
            )
        time.sleep(8)
        driver.execute_script(
            "$('button.oe_button.oe_form_button.oe_highlight:"
            "contains(Sign)').click()"
            )


class SaleTestApex(BasicFlow):

    def fill_wave(self, product_name, location, qty):
        """Used to fill the needed data in the new window used to pick product
        from a specific location"""
        driver = self.driver
        driver.execute_script(
            "$('#filterbox').val('%s').keyup()" % product_name)
        time.sleep(1)
        driver.execute_script(
            "$('td.location_f input').val('%s').keyup()" % location)
        time.sleep(1)
        driver.execute_script(
            "$('td.quantity_f input').val('%s').keyup()" % qty)
        time.sleep(1)
        driver.execute_script(
            "$('td.quantity_f input').trigger("
            "{type: 'keypress', which: 13, keyCode: 13});")
        time.sleep(2)

    def validate_pick(self):
        """Validate a picking of type picking. The only picking in the list
        with state Waiting Availability. To complete the validation process for
        this picking it is needed to create a new wave and validate the picking
        from it, using the new window created to be used from waves, where you
        specify the location where the quant are taken

        In this process we test som functionalities of wave view, to verify the
        search box and the warning messages showed when you try to reserve more
        than the required by the picking
        """
        driver = self.driver
        driver.execute_script(
            "$($('.oe_list_content')[3])."
            "find('tr :contains(Waiting Availability)').click()")
        time.sleep(2)
        driver.execute_script("$('li a:contains(Additional Info)').click()")
        driver.execute_script("$('.oe_form_button_edit')[1].click()")
        driver.execute_script(
            "$('td.oe_form_group_cell_label:contains(Picking Wave)').next()"
            ".find('.oe_m2o_drop_down_button').click()")
        time.sleep(1)
        driver.execute_script(
            "$('li.oe_m2o_dropdown_option "
            "a:contains(Create and Edit...)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('div.modal-content button:contains(Confirm)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('div.modal-content button:contains(Save)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('span.oe_form_buttons_edit button:contains(Save)')[1].click()")
        time.sleep(1)
        driver.execute_script(
            "$('a:contains(Wave/)').click()")
        time.sleep(3)
        driver.execute_script(
            "$('button:contains(Pick Products)').click()")
        time.sleep(7)
        self.fill_wave('Wrong Product', 'Stock', 13)
        self.click_outside()
        self.fill_wave(self.product or '6002', 'Stock', 13)
        time.sleep(2)
        self.fill_wave(self.product or '6002', 'Stock', 2)
        self.fill_wave(self.product or '6002', 'Stock', 5)
        self.fill_wave(self.product or '6002', 'Stock', 4)
        self.click_outside()
        self.fill_wave(self.product or '6002', 'Stock', 3)
        time.sleep(2)
        driver.execute_script(
            "$('button:contains(Quit)').click()")
        time.sleep(10)
        driver.execute_script(
            "$('button:contains(Done)').click()")
        time.sleep(5)
        driver.execute_script(
            "$('td.oe_list_field_cell:contains(WH/PICK)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('div.modal-content li a:contains(Additional Info)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('div.modal-content a:contains(SO-)').click()")
        time.sleep(3)
        driver.execute_script(
            "$('div.modal-header button.close').click()")
        time.sleep(1)
        driver.execute_script(
            "$('button:contains(Pickings)').click()")
        time.sleep(3)


class SaleTestLodi(BasicFlow):

    def validate_pack(self, code='0'):
        """Validate the picking of type pack after the pick was validated.
        To validate this picking it is needed to put in package all quants used
        by the previous picking. For this we use the new windows create for
        picking of this type, where we specify the package and the number of
        products used for each package"""
        res = super(SaleTestLodi, self).validate_pack('ID')
        return res

    def go_to_pickings(self):
        """Used to move us from order validated to pickings generated by it"""
        time.sleep(10)
        res = super(SaleTestLodi, self).go_to_pickings()
        return res

    def create_invoice(self):
        """Then the pickings were validated we go ahead to create the invoice
        from the last picking validated and the validate it to complete the
        sale process for this test"""
        time.sleep(10)
        res = super(SaleTestLodi, self).create_invoice()
        return res


class SaleTestExim(BasicFlow):

    def validate_out(self):
        """Then the pickings were validated we go ahead to create the invoice
        from the last picking validated and the validate it to complete the
        sale process for this test"""
        driver = self.driver
        time.sleep(3)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Check Availability)').click()"
            )
        time.sleep(2)
        driver.execute_script(
            "$('button.oe_button.oe_form_button."
            "oe_highlight:contains(Transfer)').click()"
            )
        time.sleep(4)
        driver.execute_script(
            "$('div.modal-content button:contains(Apply)').click()")


class SaleTestAbas(BasicFlow):

    def go_to_sale_form(self):
        """Method used to move us from main window to view for of sale order
        """
        driver = self.driver
        time.sleep(2)
        driver.execute_script(
            "$('a.o_app div:contains(Point of Sale)').click()")
        time.sleep(5)
        driver.execute_script(
            "$('div.o_kanban_record:contains(Administrator) "
            "button:contains(Resume)').click()")
        driver.execute_script(
            "$('div.o_kanban_record:contains(Test Admin) "
            "button:contains(New Session)').click()")

    def fill_form(self, partner=False):
        """
        """
        driver = self.driver
        if partner:
            raw_input('Press Enter after the POS is loaded')
            driver.execute_script(
                "$('button:contains(Customer)').click()")
            time.sleep(2)
            driver.execute_script(
                "$('span.searchbox input')."
                "val('AREPAS A LA MEXICANA CON SABOR VENEZOLANO SA DE CV')")
            time.sleep(1)
            driver.execute_script(
                "$('span.searchbox input').trigger("
                "{type: 'keypress', which: 13, keyCode: 13})")
            time.sleep(2)
        products = driver.find_elements_by_xpath(
            "//span[@class='product']/div/span[@class='qty-tag']"
            "[not(contains(., 0 ))]")
        for product in products[:len(products) > 9 and 10 or 1]:
            product.click()
        time.sleep(2)
        driver.execute_script(
            "$('button:contains(Payment)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('div.paymentmethod:contains(Efectivo - GS C2 (MXN)').click()")
        time.sleep(1)
        amount = driver.find_element_by_xpath("//td[@class='col-due']").text
        for val in amount:
            driver.execute_script(
                "$('section.payment-numpad div.numpad button.input-button."
                "number-char:contains(%s)').click()" % val)
            time.sleep(1)
        time.sleep(2)
        driver.execute_script(
            "$('span.next:contains(Validate)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('span:contains(Next Order)').click()")
        if partner:
            time.sleep(2)
            self.fill_form()


    def close_session(self):
        """Close the session used in the POS
        """
        driver = self.driver
        time.sleep(3)
        driver.execute_script(
            "$('div.header-button:contains(Close)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('div.header-button:contains(Confirm)').click()")
        raw_input('Press Enter after the POS is closed')
        driver.execute_script(
            "$('div.o_kanban_record:contains(Administrator) "
            "button:contains(Close)').click()")
        time.sleep(6)
        driver.execute_script(
            "$('button:contains(Validate Closing & Post Entries):"
            """not(".o_form_invisible")').click()""")
        time.sleep(10)
        driver.execute_script(
            "$('li a.dropdown-toggle:contains(Orders)').click()")
        time.sleep(1)
        driver.execute_script(
            "$('li.open ul.dropdown-menu li "
            "a.o_menu_entry_lvl_2:contains(Orders)').click()")
        time.sleep(2)
        driver.execute_script(
            "$('table.o_list_view.table.table-condensed.table-striped "
            "td[data-field=name]')[0].click()")
        time.sleep(3)
        driver.execute_script(
            "$('a:contains(Extra Info)').click()")


@click.command()
@click.option('-server',
              default='',
              prompt='Server',
              help='Url of the server to create connection')
@click.option('-user',
              default='',
              prompt='User',
              help='User to do the login')
@click.option('-password',
              default='',
              prompt='Password',
              help='User to do the login')
@click.option('-db',
              default='',
              prompt='DB',
              help='User to do the login')
@click.option('-com',
              default='',
              prompt='Company',
              help='Company which the test is going  to run the test')
def main(server, user, password, db, com):
    classes_dict = {
        'apex': 'SaleTestApex',
        'lodi': 'SaleTestLodi',
        'exim': 'SaleTestExim',
        'wohlert': 'SaleTestExim',
        'abastotal': 'SaleTestAbas',
    }
    class_obj = globals()[classes_dict.get(com, 'BasicFlow')]
    partner = {
        'lodi': 'Refaccionaria Mario Garcia S.A. De C.V.',
        'apex': 'ABA SEGUROS, S.A. DE C.V.',
        'exim': 'Acabados Rectificados Garcia S.A.',
        'wohlert': 'GENERAL MOTORS CUSTOMER CARE AND AFTERSA',
    }
    product = {
        'lodi': 'A-521',
        'apex': '6002',
        'exim': 'FUN-I0014',
        'wohlert': '3991407',
    }
    values = {
        'server': server,
        'user': user,
        'password': password,
        'db': db,
        'partner': partner.get(com),
        'product': product.get(com)
    }

    sale = class_obj(**values)
    time.sleep(2)
    if com == 'abastotal':
        sale.go_to_sale_form()
        sale.fill_form(True)
        sale.close_session()

    else:
        sale.go_to_sale_form()
        sale.fill_form()
        sale.go_to_pickings()
    if com in ('lodi', 'apex'):
        sale.validate_pick()
        sale.validate_pack()
        sale.validate_out()
        sale.create_invoice()
    elif com in ('exim', 'wohlert'):
        sale.validate_out()
        sale.create_invoice()

if __name__ == '__main__':
    main()
