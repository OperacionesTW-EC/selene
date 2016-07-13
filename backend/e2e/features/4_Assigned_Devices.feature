Feature: Devices
  As Tech Opss user
  I want to see an assigned device list
  So I can see  of each device
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