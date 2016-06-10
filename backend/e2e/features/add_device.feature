Feature: Add a device
    As an Opex user
    I want to add a device to Selene
    To keep the store updated

    @ignore
    Scenario: Add a device
        Given I go to the new device page
        When I submit the form device with valid values
        Then I should see a success message
        And I should see the device in the devices list
