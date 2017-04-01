DROP FUNCTION IF EXISTS get_new_id(cmodel varchar, id_res integer);
CREATE OR REPLACE FUNCTION get_new_id(cmodel varchar, id_res integer)
RETURNS integer AS $$
    DECLARE
        data_name varchar;
        new_id integer;

    BEGIN
        SELECT
            ir_data_name INTO data_name
        FROM
            dblink('con',
                   'SELECT name FROM ir_model_data WHERE model='||
                    quote_literal(cmodel)||' AND res_id='|| id_res) AS
            t1 (ir_data_name varchar);
        SELECT res_id INTO new_id FROM ir_model_data WHERE model=cmodel AND name=data_name LIMIT 1;
    RETURN new_id; END;
    $$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS create_message();
CREATE OR REPLACE FUNCTION create_message()
RETURNS void AS $$
    DECLARE
        msg record;
        ir_data "ir_model_data";
        data_name varchar;
        cmodel varchar;
        new_id integer;
        msg_id integer;
        parent integer;
        uid_write integer;
        rec_id integer;
        uid_create integer;
        id_author integer;
        id_subtype integer;
        chr_subtype varchar;

    BEGIN
        PERFORM dblink_connect('con' ,
            'host=127.0.0.1 dbname=xxxx user=xxxx password=xxxxxx');
        FOR msg IN SELECT * FROM dblink('con',
                   'SELECT id, create_date, create_uid, write_date, write_uid, body, model, record_name, '||
                          'date, subject, message_id, parent_id, res_id, subtype_id, author_id, email_from, '||
                          'mail_server_id, no_auto_thread, reply_to, website_published, path '||
                    'FROM mail_message WHERE '||
                    'model IN ('||quote_literal('product.product')||','||
                                  quote_literal('product.template')||','||
                                  quote_literal('project.project')||','||
                                  quote_literal('project.issue')||','||
                                  quote_literal('sale.order')||','||
                                  quote_literal('project.task')  || ')') AS
                    t1 (id integer, create_date date, create_uid integer, write_date date, write_uid integer, body text,
                        model varchar, record_name varchar, date_val date, subject varchar, message_id varchar,
                        parent_id integer, res_id integer, subtype_id integer, author_id integer,
                        email_from varchar,mail_server_id integer, no_auto_thread boolean, reply_to varchar,
                        website_published boolean, spath char ) LOOP
            IF EXISTS (SELECT res_id FROM ir_model_data WHERE name='mail_message_imported_vx80_'||msg.id) THEN
                EXIT;
            END IF;
            SELECT get_new_id('res.users', msg.write_uid) INTO uid_write;
            SELECT get_new_id('res.users', msg.create_uid) INTO uid_create;
            SELECT get_new_id('res.partner', msg.author_id) INTO id_author;
            cmodel := replace(replace(msg.model, 'project.project', 'sale.order'), 'project.issue', 'helpdesk.ticket');

            IF msg.parent_id IS NOT NULL THEN
                SELECT res_id INTO parent FROM ir_model_data WHERE name='message_imported_vx80_'||msg.parent_id LIMIT 1;
            END IF;

            SELECT
                ir_data_name INTO data_name
            FROM
                dblink('con',
                       'SELECT name FROM ir_model_data WHERE model='||
                        quote_literal(msg.model)||' AND res_id='|| msg.res_id) AS
                t1 (ir_data_name varchar);
            SELECT res_id INTO new_id FROM ir_model_data WHERE model=cmodel AND name=data_name LIMIT 1;
            INSERT INTO mail_message(create_date, create_uid, write_date,
                write_uid, body, model, record_name, date, subject, message_id,
                parent_id, res_id, subtype_id, author_id,
                email_from,mail_server_id, no_auto_thread, reply_to,
                website_published, path, message_type) VALUES
            (msg.create_date, uid_create, msg.write_date, uid_write,
                msg.body, cmodel, msg.record_name, msg.date_val, msg.subject,
                msg.message_id, parent, new_id, msg.subtype_id,
                id_author, msg.email_from, null,
                msg.no_auto_thread, msg.reply_to, msg.website_published,
                msg.spath, 'comment') RETURNING id INTO rec_id;
            INSERT INTO ir_model_data (name, noupdate, date_init, date_update, module, model, res_id) VALUES
            ('message_imported_vx80_'||msg.id, true, NOW(), NOW(), '', 'mail.message', rec_id);
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;

SELECT create_message();

