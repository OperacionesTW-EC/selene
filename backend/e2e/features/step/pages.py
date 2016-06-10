from lettuce import world


class BasePage():
    def __getattr__(self, undeclared_method_name):
        if undeclared_method_name in self.__class__.css_paths:
            css = self.__class__.css_paths[undeclared_method_name]

            def m():
                return world.browser.find_element_by_css_selector(css)

            return m

        if undeclared_method_name in self.__class__.css_plural_paths:
            css = self.__class__.css_plural_paths[undeclared_method_name]

            def mp():
                return world.browser.find_elements_by_css_selector(css)

            return mp

    def button(self, button_name):
        "ultimately runs __getattr__ and reads 'css_paths'"
        return getattr(self, button_name)()


class MainPage(BasePage):

    css_paths = {
                 'device_types': '.main-panel form select[name="device_type"]',
                 'device_brands': '.main-panel form select[name="device_brand"]',
                 'expected_return_date': '.main-panel form input[name="expected_return_date"]',
                 'ownership': '.main-panel form select[name="ownership"]',
                 'project': '.main-panel form select[name="project"]',
                 'serial_number': '.main-panel form input[name="serial_number"]',
                 'purchase_date': '.main-panel form input[name="purchase_date"]',
                 'ingresar_button': '.main-panel form a[type="submit"]',
                 'page_header': '.main-panel .page-header h1',
                 'Guardar': '.main-panel a#save',
                 'Asignar': '.main-panel .panel-heading a[href$="assign_device"]',
                 'Registrar': '.main-panel .panel-heading a[href$="device_form"]',
                 'Aceptar': '.main-panel a[href$="assigned_device_list"]'
        }

    css_plural_paths = {
                 'active_status_buttons': '.main-panel form .btn-group a',
                 'device_detail_buttons': '.main-panel tr.data-row a[href^="#/device/"]',
                 'device_check_boxes': '.main-panel table#device-list input[type="checkbox"]',

        }

    def enter_text(self, field, value):
        input_field = getattr(self, field)()
        input_field.click()
        input_field.clear()
        input_field.send_keys(value)

    def datepicker_day(self, row, day):
        css = 'div.datepicker-days tr:nth-child(%s) td[class="day"]:nth-child(%s)' % (row, day)
        return world.browser.find_element_by_css_selector(css)


class SideNav(BasePage):

    css_paths = {
                 'Dashboard': 'section.sidenav a[href$="dashboard"]',
                 'Asignar': 'section.sidenav a[href$="assign_device"]',
                 'Registrar': 'section.sidenav a[href$="device_form"]',
                 'Dispositivos': 'section.sidenav a[href$="device_list"]',
                 'Asignados': 'section.sidenav a[href$="assigned_device_list"]',
        }


main_page = MainPage()
side_nav = SideNav()
