#-*- coding:utf-8 -*-
#
import oerplib
import psycopg2

HOST=raw_input('Please insert the server host: ')
DBHOST=raw_input('Please insert the data base host: ')
PORT=int(raw_input('Please insert the server port: '))
DBPORT=int(raw_input('Please insert the database port: '))
DB=raw_input('Please insert the database name: ')
USER=raw_input('Please insert the server user: ')
PASS=raw_input('Please insert the password for server user: ')
DBUSER=raw_input('Please insert the postgres user: ')
DBPASS=raw_input('Please insert the password for postgres user: ')
cur = False
try:
    conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port=%s" % (DB, DBUSER,
                                                                                       DBHOST, 
                                                                                       DBPASS,
                                                                                       DBPORT))
    cur = conn.cursor()
except:
    print "I am unable to connect to the database"

con = oerplib.OERP(
server=HOST, 
database=DB, 
port=PORT, 
)  

con.login(USER, PASS)

def check_partner():
    if len(ids.partner_ids) > 10:
        ids.write({'partner_ids': [(6, 0, [i.id for i in ids.partner_ids[:5]])]})
        cr.commit()
    for partner in ids.partner_ids:
        if partner.vat and partner.is_company:
            ids.write({'dst_partner_id': partner.id})
            cr.commit()
            break

    return True


def do_merge(merge_to='name'):

    merge_obj = con.get('wizard.merge.partner.by.partner')
    if cur:
        vat_cond = """ id NOT IN (SELECT id 
                                  FROM res_partner 
                                  WHERE vat IN ('MXXAXX010101000','MXXEXX010101000') 
                                        OR vat ILIKE '') AND """

        cur.execute("""SELECT min(id), array_agg(id)
                       FROM res_partner 
                       WHERE %s adminpaq_id > 0 
                       GROUP BY %s HAVING COUNT(*) >= 2
                       ORDER BY min(id)""" % (merge_to == 'vat' and vat_cond or 'active=True AND',
                                              merge_to))

        for min_id, aggr_ids in cur.fetchall():
            if len(aggr_ids) < 10:
                merge_id =  merge_obj.create({'partner_id': min_id,
                                              'partner_ids': [(6, 0, aggr_ids)]})
                try:
                    print aggr_ids
                    merge_obj.merge_cb([merge_id])
                except Exception, e:
                    print 'Algo',e 
    return True
do_merge()
