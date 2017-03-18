from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import click


class SaleTest():

    def __init__(self, **args):
        self.driver = webdriver.Firefox()
        self.driver.get(
            '%(server)s/'
            'login?db=%(db)s&'
            'login=%(user)s&key=%(password)s' % args)
        time.sleep(3)

    def go_to_sale_form(self):
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
        driver = self.driver
        time.sleep(9)
        pickingmenu = "//button[contains(., 'View Delivery Order')]"
        pickingmenu = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(pickingmenu))
        pickingmenu.click()
        time.sleep(3)

    def click_outside(self):
        fieldinput = "html"
        fieldinput = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_xpath(fieldinput))
        fieldinput.click()
        time.sleep(1)

    def fill_form(self):
        driver = self.driver
        partner = ("//span[contains(@class, "
                   "'oe_form_field_many2one')]/div/input")
        partner = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by_xpath(partner))
        partner.clear()
        partner.send_keys('ABA SEGUROS, S.A. DE C.V.')
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
        product.send_keys('3P-CECHB')
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

    def fill_wave(self, product_name, location, qty):
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
        self.fill_wave('3P-CECHB', 'Stock', 13)
        time.sleep(2)
        self.fill_wave('3P-CECHB', 'Stock', 2)
        self.fill_wave('3P-CECHB', 'Stock', 5)
        self.fill_wave('3P-CECHB', 'Stock', 4)
        self.click_outside()
        self.fill_wave('3P-CECHB', 'Stock', 3)
        time.sleep(2)
        driver.execute_script(
            "$('button:contains(Quit)').click()")
        time.sleep(7)
        driver.execute_script(
            "$('button:contains(Done)').click()")
        time.sleep(3)
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

    def validate_pack(self):
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
        for pack in ('0536', '0537', '0538', '0539', '0539'):
            driver.execute_script(
                "$('span.pack_search input').val('%s')" % pack)
            driver.execute_script(
                "$('span.pack_search input').focus()."
                "trigger(jQuery.Event('keyup', { keycode: $.ui.keyCode.ENTER, "
                "which: $.ui.keyCode.ENTER   }))")
            time.sleep(2)
            driver.execute_script(
                """$('textarea[name="scan_data"]').val('3P-CECHB*2')""")
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
def main(server, user, password, db):
    sale = SaleTest(server=server, user=user,
                    password=password, db=db)
    sale.go_to_sale_form()
    sale.fill_form()
    sale.go_to_pickings()
    sale.validate_pick()
    sale.validate_pack()
    sale.validate_out()

if __name__ == '__main__':
    main()
