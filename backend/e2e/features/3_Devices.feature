Feature: Devices
  As Tech Opss user
  I want to see a device list
  So 

  Scenario: Enter the Dashboard
    Given I am in homepage SELENE
    And I press Ingresar
    Then I should see "Dashboard"
    
  Scenario: Device detail
    Given I am in Dashboar SELENE
    And I press Dispositivos
    And I select first device detail
    Then I should see "Dispositivo"

  Scenario: Return to Dashboard
    Given I am in "Dispositivo" page
    And I press Dashboard
    Then I should see "Dashboard"

  Scenario: Button Asignar Dispositivo
    Given I am in Dashboar SELENE
    And I press Dispositivos
    And I press button "Asignar Dispositivo"
    Then I should see "Asignar dispositivos"

  Scenario: Return to Dashboard
    Given I am in "Dispositivo" page
    And I press Dashboard
    Then I should see "Dashboard"

  Scenario: Button Registrar Dispositivos
    Given I am in Dashboar SELENE
    And I press Dispositivos
    And I press button "Registrar Dispositivo"
    Then I should see "Registrar Dispositivo"