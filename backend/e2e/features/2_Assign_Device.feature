Feature: Assign devices
  As Tech Opss user
  I want to assign a device
    So Thougthworks could have a list of devices assigned
  @play
  Scenario: Enter the Dashboard
    Given I am in homepage SELENE
    And I press Ingresar
    Then I should see "Dashboard"
  @play
  Scenario: Enter the Device Registration
    Given I am in "Dashboard" page
    And I press Asignar
    Then I should see "Asignar dispositivos"
  @play
  Scenario: Assign a device
    Given I am in "Asignar dispositivos" page
    And I register Responsable like "Fanny Barco"
    And I select Proyecto like "Selene"
    And I register Fecha de Entrega
    And I select first device
    And I press Guardar
    Then I should see "Detalle de la asignación"
  @play
  Scenario: Enter the Device Registration
    Given I am in "Detalle de la asignación" page
    And I press Aceptar
    Then I should see "Listados de Dispositivos Asignados"

