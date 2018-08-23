# coding: utf-8
import time
import itertools

class ModelItemMixIn(object):
    CACHE_TYPE = None

    def load_cache(self, obj):
        raise NotImplementedError, "Need come true"

    def get_database(self):
        return None

    def finish_save(self):
        pass

    def reset(self):
        pass

class ModelConfig(dict, ModelItemMixIn):
    """
    """

    CACHE_TYPE = None
    STORAGE_TYPE = 'mysql'

class ModelChat(ModelItemMixIn):
    """
    """

    STORAGE_TYPE = 'tornadoredis'

    @staticmethod
    def get_database():
        """
        """

        return 'chat'

class ModelDict(dict, ModelItemMixIn):
    """
    """

    CACHE_TYPE = 'string'
    STORAGE_TYPE = 'mysql'

    def __init__(self, defaults, pickler=repr):
        super(dict, self).__init__()

        self.defaults = defaults
        self.changed = False
        self.update(defaults)
        self.reload_cache = False
        self.pickler = pickler

    def __setitem__(self, name, value):
        """
        """

        self.changed = True

        return super(ModelDict, self).__setitem__(name, value)

    def save(self, connection, name, carrier):
        """
        """

        cursor = connection.cursor()

        if not carrier.pk or not cursor.execute(*self.sql_update(name, carrier)):
            cursor.execute(*self.sql_insert(name, carrier))

            carrier.pk = cursor.lastrowid

        connection.commit()

    def reset(self):
        self.update(self.defaults)
        self.changed = True

    def finish_save(self):
        self.changed = False

    def load_cache(self, obj):
        """

        """

        self.update(obj)

    def sql_select(self, name, carrier):
        """
        """

        return "SELECT * FROM %s_%s WHERE id=%s" % (carrier.NAME, name, carrier.pk), []

    def sql_insert(self, name, carrier):
        """
        """

        fields = []
        params = []
        values = []

        for key in self.defaults:
            fill_obj = self.__getitem__(key)
            if not callable(fill_obj):
                params.append(fill_obj)
            else:
                params.append(fill_obj.to_insert())

            fields.append(key)
            values.append('%s')

        sql_fields = "`,`".join(fields)
        sql_values = ",".join(itertools.imap(str, values))
        insert_pk = carrier.pk or 'null'

        query = "INSERT INTO %s_%s(`id`, `%s`, `created_at`) VALUES (%s, %s, %d)" % \
                (carrier.NAME, name,
                 sql_fields, insert_pk, sql_values, int(time.time()))

        return query, params

    def sql_update(self, name, carrier):
        """
        """

        fields = []
        params = []

        for key in self.defaults:
            fill_obj = self.__getitem__(key)
            if not callable(fill_obj):
                fields.append("`%s`=%s" % (key, "%s"))
                params.append(fill_obj)
            else:
                fields.append("`%s`=%s" % (key, fill_obj.to_update()))

        query = "UPDATE %s_%s SET %s, `updated_at`=%d WHERE `id`=%d" % \
                (carrier.NAME, name, ','.join(fields), int(time.time()),
                 carrier.pk)

        return query, params

    def loader(self, stmt):
        """
        """

        row = stmt.fetchone()

        if row:
            self.update(row)

    def cache_loader(self, obj):
        """
        """

        self.update(eval(obj))

    def tocache(self):
        """
        """

        return self.pickler(self)

class ModelList(dict, ModelItemMixIn):
    """
    """

    CACHE_TYPE = 'hash'
    STORAGE_TYPE = 'mysql'

    def __init__(self, defaults, pk_name, major_name='pid', pickler=repr):
        """
        inserts [
        {'pk': 1, 'extra': {'ship': '3'}}
        ]
        modifies: [
        {'pk': 1, 'extra': {'ship': '3'}}
        ]
        removes: [1, 3, 3]
        """

        super(dict, self).__init__()

        self.defaults = defaults
        self.pk_name = pk_name
        self.major_name = major_name
        self.changed = False
        self.inserts = []
        self.modifies = []
        self.removes = []
        self.reload_cache = False
        self.pickler = pickler

    def add(self, pk, **extra):
        """
        """

        data = self.defaults.copy()
        data.update(extra)

        print 'fields, add, ', data

        self.inserts.append({'pk': pk, 'extra': data})
        self.changed = True

    def modify(self, pk, **extra):
        """
        """

        data = self.__getitem__(pk).copy()
        data.update(extra)

        self.modifies.append({'pk': pk, 'extra': data})
        self.changed = True

    def remove(self, pk):
        """
        """

        self.removes.append(pk)
        self.changed = True

    def sql_select(self, name, carrier):
        """
        """

        return "SELECT * FROM %s_%s WHERE %s=%s" % (carrier.NAME, name, 
                                    self.major_name, '%s'), [carrier.pk]

    def reset(self):
        """
        """

        for pk in self.iterkeys():
            self.remove(pk)

    def save(self, connection, name, carrier):
        """
        """

        cursor = connection.cursor()
        table_name = "%s_%s" % (carrier.NAME, name)

        for data in self.inserts:
            cursor.execute(*self.sql_insert(table_name, data, carrier.pk))
            data['extra'][self.major_name] = carrier.pk
            data['extra']['id'] = cursor.lastrowid
            self.__setitem__(data['pk'], data['extra'])

        for data in self.modifies:
            cursor.execute(*self.sql_update(table_name, data))
            self.__getitem__(data['pk']).update(data['extra'])

        cursor.execute(*self.sql_delete(table_name, self.removes))
        connection.commit()

        for pk in self.removes:
            del self[pk]

    def finish_save(self):
        self.inserts = []
        self.modifies = []
        self.removes = []
        self.changed = False

    def sql_insert(self, table_name, data, pid):
        """
        """

        fields = [self.major_name, self.pk_name, 'created_at']
        params = [pid, data['pk'], int(time.time())]
        values = ['%s', '%s', '%s']

        for key in self.defaults:
            fill_obj = data['extra'][key]
            if not callable(fill_obj):
                params.append(fill_obj)
            else:
                params.append(fill_obj.to_insert())

            fields.append(key)
            values.append('%s')

        sql_fields = "`,`".join(fields)
        sql_values = ",".join(values)

        query = "INSERT INTO %s(`%s`) VALUES(%s)" % (
            table_name, sql_fields, sql_values
        )

        print(query, params)

        return query, params

    def sql_update(self, table_name, data):
        """
        """

        fields = ['`updated_at`=%s']
        params = [int(time.time())]

        obj = self.__getitem__(data['pk']).copy()
        obj.update(data['extra'])

        for key in self.defaults:
            fill_obj = data['extra'][key]
            if not callable(fill_obj):
                fields.append("`%s`=%s" % (key, "%s"))
                params.append(fill_obj)
            else:
                fields.append("`%s`=%s" % (key, fill_obj.to_update()))

        params.append(obj['id'])

        query = "UPDATE %s SET %s WHERE `id`=%s" % (table_name,
                                                  ','.join(fields),
                                                  '%s')
        return query, params

    def sql_delete(self, table_name, data):
        """
        """

        removes = []

        for pk in data:
            obj = self.__getitem__(pk)
            removes.append(str(obj['id']))

        if not removes:
            removes.append('0') # safely delete

        query = "DELETE FROM %s WHERE `id` IN (%s)" % (table_name, 
                                                       ','.join(removes))

        return query, []

    def loader(self, stmt):
        """
        """

        for row in stmt:
            pk = row.pop(self.pk_name)
            self.__setitem__(pk, row)

    def cache_loader(self, obj, **kwargs):
        """
        """

        keys = kwargs.get('keys')

        if keys:
            iters = itertools.izip(keys, obj)
        else:
            iters = obj.iteritems()

        for pk, value in iters:
            if isinstance(pk, basestring) and pk.isdigit():
                pk = int(pk)

            self.__setitem__(pk, eval(value))

    def tocache(self):
        """
        """

        data = []

        for key, value in self.iteritems():
            data.append((key, self.pickler(value)))

        return data
