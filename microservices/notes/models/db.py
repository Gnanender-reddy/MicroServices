
from nameko.rpc import rpc


from microservices.users.config.connection import Connection


class DataManagement:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """
    name = "data_service"

    def __init__(self):
        self.c = Connection()
        self.r = self.c.redis_conn()

    @rpc
    def create_entry(self, data):
        print(data)
        query = "INSERT INTO notes (title, description, color, ispinned, isarchived, istrashed,user_id) VALUES ('" + \
                data[
                    'title'] + "', '" + data['description'] + "', '" + data['color'] + "', '" + data[
                    'ispinned'] + "', '" + data[
                    'isarchived'] + "', '" + data['istrashed'] + "','" + data['user_id'] + "') "
        self.c.execute(query)
        # self.mydbobj.execute(query)
        print("Entry create Successfully")

    @rpc
    def update_entry(self, data):
        query = "UPDATE notes SET title = '" + data['title'] + "',description = '" + data[
            'description'] + "',color = '" + data['color'] + "',ispinned = '" + data[
                    'ispinned'] + "', isarchived = '" + data['isarchived'] + "', istrashed = '" + data[
                    'istrashed'] + "' WHERE  user_id = " + data['user_id'] + ""
        self.c.execute(query)
        # self.mydbobj.execute(query)
        print("Data update Successfully")

    @rpc
    def delete_entry(self, data):
        query = "DELETE FROM notes WHERE user_id = " + data['user_id'] + ""
        self.c.execute(query)
        # self.mydbobj.execute(query)
        print("Entry delete Successfully")

    @rpc
    def read_entry(self, data):

        query = "SELECT * FROM notes WHERE user_id = '" + data['user_id'] + "'"
        # self.c.execute(query)
        entry = self.c.run_query(query)

        # entry = self.mydbobj.run_query(query)
        print(entry)

    @rpc
    def put_cache(self, data, data_id):
        self.r.hmset(data_id, data)

    @rpc
    def get_cache(self, data_id):
        x = self.r.hgetall(data_id)
        print(x)
        return x

    @rpc
    def del_cache(self, data_id):
        self.r.hdel(data_id, len(data_id))

    @rpc
    def get_keys(self, data_id):
        return self.r.hkeys(data_id)