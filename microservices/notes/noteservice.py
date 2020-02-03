"""
@Author : P.Gnanender Reddy
@Since : jan'2020.
@:keyword:rpc.
@Description: This class provides services for notes creation, deletion, update and reading data.
"""

import sys
from nameko.rpc import rpc
sys.path.insert(0,'/home/admin1/PycharmProjects/Microservices')

from microservices.notes.models.db import DataManagement


class Note():
    name = "note_service"

    @rpc
    def create_note(self, data):
        print(data)
        db_obj =DataManagement()
        json_keys = list(data.keys())
        if len(json_keys) == 7:
                db_obj.create_entry(data)
                response = {'success': True, 'data': [], 'message': "Entry Create Successfully"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def delete_note(self, data):
        db_obj = DataManagement()

        json_keys = list(data.keys())
        if len(json_keys) == 1:
            db_obj.delete_entry(data)
            response = {'success': True, 'data': [], 'message': "Entry Delete Successfully"}
            return response
        else:

         response = {'success': False, 'data': [], 'message': "some values are missing"}
         return response

        #     if len(db_obj.get_cache(data_id)):
        #         db_obj.del_cache(data_id)
        #         db_obj.delete_entry(data)
        #         response = {'success': True, 'data': [], 'message': "Entry Delete Successfully"}
        #         return response
        #     else:
        #         response = {'success': True, 'data': [], 'message': "Entry not available"}
        #         return response
        # else:
        #     response = {'success': False, 'data': [], 'message': "some values are missing"}
        #     return response

    @rpc
    def update_note(self, data):
        db_obj = DataManagement()
        json_keys = list(data.keys())

        if len(json_keys) == 7:
            db_obj.update_entry(data)
            response = {'success': True, 'data': [], 'message': "data updated successfully"}
            return response
        else:

            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response
        #     if db_obj.get_cache(data_id):
        #         db_obj.put_cache(data, data_id)
        #         db_obj.update_entry(data)
        #         response = {'success': True, 'data': [], 'message': "Data Update Successfully"}
        #         return response
        #     else:
        #         response = {'success': True, 'data': [], 'message': "Entry not available"}
        #         return response
        # else:
        #     response = {'success': False, 'data': [], 'message': "some values are missing"}
        #     return response

    @rpc
    def read_note(self, data):
        db_obj = DataManagement()
        json_keys = list(data.keys())
        if len(json_keys) == 1:
            db_obj.read_entry(data)
            response = {'success': True, 'data': [], 'message': "data read successfully"}
            return response
        else:

            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

        # if len(json_keys) == 2:
        #     if len(db_obj.get_keys(data_id)):
        #         x = db_obj.get_cache(data_id)
        #     response = {'success': True, 'data': [], 'message': "Data read Successfully"}
        #     return response
        # else:
        #     response = {'success': False, 'data': [], 'message': "some values are missing"}
        #     return response