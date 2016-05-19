# coding=utf8
from django.core.exceptions import ValidationError
from model_mommy import mommy
from nose.tools import *
from devices.models import Assignment

class TestAssignment:

    def setup(self):
        self.assignment = mommy.prepare_recipe('devices.assignment_recipe')

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.assignment.full_clean())

    def test_should_be_invalid_without_name(self):
        self.assignment.assignee_name = None
        assert_raises(ValidationError, self.assignment.full_clean)

    def test_should_be_invalid_with_name_too_long(self):
        self.assignment.assignee_name = 'This name is too long and has more than 50 characters, so it is invalid'
        assert_raises(ValidationError, self.assignment.full_clean)

    def test_verbose_name(self):
        assert_equal(str(Assignment._meta.verbose_name), 'Asignación')

    def test_verbose_name_plural(self):
        assert_equal(str(Assignment._meta.verbose_name_plural), "Asignaciones")

    @raises(ValueError)
    def test_should_be_invalid_without_project(self):
        self.assignment.project = None

    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(Assignment in admin.site._registry)

