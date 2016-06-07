Feature: Devices
  As Tech Opss user
  I want to see a device list
  So
  @play
  Scenario: Enter the Dashboard
    Given I am in homepage SELENE
    And I press Ingresar
    Then I should see "Dashboard"
  @play
  Scenario: Device detail
    Given I am in "Dashboard" page
    And I press Dispositivos
    And I select first device detail
    Then I should see "Dispositivo"

  @play
  Scenario: Button Asignar Dispositivo
    Given I am in "Dashboard" page
    And I press Dispositivos
    And I press button "Asignar"
    Then I should see "Asignar dispositivos"

  @play
  Scenario: Button Registrar Dispositivos
    Given I am in "Dashboard" page
    And I press Dispositivos
    And I press button "Registrar"
    Then I should see "Registrar Dispositivo"