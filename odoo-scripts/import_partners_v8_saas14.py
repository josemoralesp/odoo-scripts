import odoorpc
import click


@click.command()
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
def import_partners(cd, co, po, dbo, uo, pre, poo, pod, pd, dbd, ud):
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


if __name__ == '__main__':
    import_partners()
