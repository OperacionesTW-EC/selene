from django.db import connection
from devices.models import DeviceStatus


class Queries:

    def assigned_devices(self):
        sql = """
        select
          device.id,
          device.code || lpad(device.sequence::text, 4, '0') as full_code,
          type.name as device_type_name,
          brand.name as device_brand_name ,
          assignment.expected_return_date as return_date ,
          assignment.assignee_name,
          project.name as project,"""
        sql += self.assignment_date() + " as assignment_date, "
        sql += self.calculate_end_date() + "  as end_date "
        sql += """ from devices_device as device
        join devices_devicebrand as brand on device.device_brand_id=brand.id
        join devices_devicestatus as status on device.device_status_id=status.id
        join devices_devicetype as type on device.device_type_id=type.id
        join devices_deviceassignment as deviceassignment on device.id = deviceassignment.device_id
        join devices_assignment as assignment on assignment.id = deviceassignment.assignment_id
        left join devices_project as project on project.id = assignment.project_id
        where status.name= '%s'
        order by assignment.assignment_datetime DESC;
        """ % DeviceStatus.ASIGNADO
        cursor = connection.cursor()
        cursor.execute(sql)
        return self.dictfetchall(cursor)

    def assignment_date(self):
        sql = "case when type.code = 'L' then " + self.first_assign_date() + " else " + self.last_assign_date() + " end "
        return sql

    def first_assign_date(self):
        sql = self.assign_date_query()
        sql += """
        ORDER BY  assignment.assignment_datetime
        LIMIT 1 )
        """
        return sql

    def last_assign_date(self):
        sql = self.assign_date_query()
        sql += """
        ORDER BY  assignment.assignment_datetime DESC
        LIMIT 1
        )
        """
        return sql

    def assign_date_query(self):
        return """(SELECT
        assignment.assignment_datetime ::date
        FROM
        devices_deviceassignment as deviceassignment,
        devices_assignment as  assignment
        WHERE
        assignment.id = deviceassignment.assignment_id AND
        deviceassignment.device_id = device.id
        """

    def calculate_end_date(self):
        sql = self.assignment_date() + " + (type.life_time*365)"
        return sql

    def dictfetchall(self, cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]
