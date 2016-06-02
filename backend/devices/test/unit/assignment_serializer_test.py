from nose.tools import assert_equal
from devices.serializers import AssignmentSerializer
from devices import models


class TestAssignmentSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(AssignmentSerializer.Meta.model, models.Assignment)

    def test_should_include_fields_definition(self):
        assert_equal(AssignmentSerializer.Meta.fields, ('id', 'assignee_name', 'project_name', 'project', 'devices', 'expected_return_date'))
