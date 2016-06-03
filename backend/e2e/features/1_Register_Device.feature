Feature: Register devices
  As Tech Opss user
  I want to register a device
  So Thougthworks have an inventory of devices


  Scenario: Enter the Dashboard
    Given I am in homepage SELENE
    And I press Ingresar
    Then I should see "Dashboard"

  Scenario: Enter the Device Registration
    Given I am in Dashboar SELENE
    And I press Registrar Dispositivo
    Then I should see "Registrar Dispositivo"

  Scenario: Register a device
    Given I am in "Registrar Dispositivo" page
    And I select Tipo like "Laptop"
    And I select Marca like "Apple"
    And I select Activo like "Si"
    And I register Serial like "1234-456-WS-33"
    And I register Modelo like "MAC Book-Pro"
    And I select Fecha de Compra like "05-13-2016"
    And I select Propiedad like "TW"
    And I press Guardar
    Then I should see "ha sido registrado satisfactoriamente"

  Scenario: Return to Dashboard
    Given I am in "Listados de Dispositivos Asignados" page
    And I press Dashboard
    Then I should see "Dashboard"
