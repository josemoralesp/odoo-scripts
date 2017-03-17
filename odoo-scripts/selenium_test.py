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

if __name__ == '__main__':
    main()
