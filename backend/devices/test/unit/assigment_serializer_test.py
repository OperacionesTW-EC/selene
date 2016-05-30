from nose.tools import *
from devices.serializers import *


class TestAssigmentSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(AssignmentSerializer.Meta.model, Assignment)

    def test_should_include_fields_definition(self):
        assert_equal(AssignmentSerializer.Meta.fields, ('id', 'assignee_name', 'project_name', 'project', 'devices', 'assignment_datetime', 'expected_return_date'))
