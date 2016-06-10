Feature: Devices
  As Tech Opss user
  I want to see a device list
  So
  @play
  Scenario: Enter the Dashboard
    Given I am on the Selene homepage
    When I press Ingresar
    Then I should be on the "Dashboard" page
  @play
  Scenario: Device detail
    Given I am on the "Dashboard" page
    When I choose "Dispositivos" on the side nav
    And I select first device detail
    Then I should be on the "Dispositivo" page

  @play
  Scenario: Button Asignar Dispositivo
    Given I am on the "Dashboard" page
    When I choose "Dispositivos" on the side nav
    Then I should be on the "Lista de dispositivos" page
    And I press "Asignar"
    Then I should be on the "Asignar dispositivos" page

  @play
  Scenario: Button Registrar Dispositivos
    Given I am on the "Dashboard" page
    When I choose "Dispositivos" on the side nav
    And I press "Registrar"
    Then I should be on the "Registrar Dispositivo" page
