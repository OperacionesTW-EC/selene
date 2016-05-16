from django.core.exceptions import ValidationError
from nose.tools import *
from devices.models import Project

class TestProject:

    def setup(self):
        self.project = Project(name='SomeName')

    def test_should_be_valid_with_valid_fields(self):
        assert_is_none(self.project.full_clean())

    def test_should_be_invalid_without_name(self):
        self.project.name = None
        assert_raises(ValidationError, self.project.full_clean)

    def test_should_be_invalid_with_name_too_long(self):
        self.project.name = 'This name is too long and has more than 50 characters, so it is invalid'
        assert_raises(ValidationError, self.project.full_clean)

    def test_should_return_the_project_name(self):
        assert_equals(self.project.name, str(self.project))

    def test_verbose_name(self):
        assert_equal(str(Project._meta.verbose_name), "Proyecto")

    def test_verbose_name_plural(self):
        assert_equal(str(Project._meta.verbose_name_plural), "Proyectos")

    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(Project in admin.site._registry)