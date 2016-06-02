from django.core.exceptions import ValidationError
from model_mommy import mommy
from nose.tools import assert_raises, assert_equal, assert_is_none
from devices.models import Assignment
from devices.serializers import AssignmentSerializer


class TestAssignment:

    def setup(self):
        self.assignment = mommy.prepare_recipe('devices.assignment_recipe')

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.assignment.full_clean())

    def test_should_be_invalid_without_name(self):
        self.assignment.assignee_name = None
        assert_raises(ValidationError, self.assignment.full_clean)

    def test_should_be_valid_without_expected_return_date(self):
        self.assignment.expected_return_date = None
        assert_equal(True, AssignmentSerializer(data=self.assignment.__dict__).is_valid())

    def test_should_be_invalid_with_name_too_long(self):
        self.assignment.assignee_name = 'This name is too long and has more than 50 characters, so it is invalid'
        assert_raises(ValidationError, self.assignment.full_clean)

    def test_verbose_name(self):
        assert_equal(str(Assignment._meta.verbose_name), 'Asignación')

    def test_verbose_name_plural(self):
        assert_equal(str(Assignment._meta.verbose_name_plural), "Asignaciones")

    def test_should_be_valid_without_project(self):
        self.assignment.project = None
        assert_equal(True, AssignmentSerializer(data=self.assignment.__dict__).is_valid())


