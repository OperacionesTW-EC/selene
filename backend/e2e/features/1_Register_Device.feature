Feature: Register devices
  As Tech Ops user
  I want to register a device
  So Thougthworks has an inventory of devices

  @play
  Scenario: Register a device
    Given I am on the Selene homepage
    When I press Ingresar
    Then I should be on the "Dashboard" page

    When I choose "Registrar" on the side nav
    Then I should be on the "Registrar Dispositivo" page

    When I select Tipo "Laptop"
    And I select Marca "Apple"
    And I select Activo "Si"
    And I enter Serial "1234-456-WS-33"
    And I enter Modelo "MAC Book-Pro"
    And I select Fecha de Compra "05-13-2016"
    And I select Propiedad "TW"
    And I save
    Then I should see "ha sido registrado satisfactoriamente"
