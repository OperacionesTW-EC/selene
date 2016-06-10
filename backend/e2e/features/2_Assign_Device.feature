Feature: Assign devices
  As Tech Ops user
  I want to assign a device
  So Thougthworks can have a list of assigned devices

  @play
  Scenario: Enter the Dashboard
    Given I am on the Selene homepage
    When I press Ingresar
    Then I should be on the "Dashboard" page
  @play
  Scenario: Enter the Device Registration
    Given I am on the "Dashboard" page
    When I choose "Asignar" on the side nav
    Then I should be on the "Asignar dispositivos" page
  @play
  Scenario: Assign a device
    Given I am on the "Asignar dispositivos" page
    When I enter Responsable "Fanny Barco"
    And I select Proyecto "Operations"
    And I enter Fecha de Entrega
    And I select first device
    And I save
    Then I should be on the "Detalle de la asignación" page
  @play
  Scenario: Enter the Device Registration
    Given I am on the "Detalle de la asignación" page
    When I press "Aceptar"
    Then I should be on the "Listados de Dispositivos Asignados" page

