from django.db import connection
from devices.models import DeviceStatus


class Queries():

    def assigned_devices(self):
        sql = """
        select
          device.id,
          device.code || lpad(device.sequence::text, 4, '0') as full_code,
          type.name as device_type_name,
          brand.name as device_brand_name ,
          now()::date as assign_date ,
          now()::date as return_date ,
          now()::date as end_date ,
          assignment.assignee_name,
          project.name as project
        from devices_device as device
        join devices_devicebrand as brand on device.device_brand_id=brand.id
        join devices_devicestatus as status on device.device_status_id=status.id
        join devices_devicetype as type on device.device_type_id=type.id
        join devices_deviceassignment as deviceassignment on device.id = deviceassignment.device_id
        join devices_assignment as assignment on assignment.id = deviceassignment.assignment_id
        join devices_project as project on project.id = assignment.project_id
        where status.name= '%s';
        """ % DeviceStatus.ASIGNADO
        cursor = connection.cursor()
        cursor.execute(sql)
        return self.dictfetchall(cursor)

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]