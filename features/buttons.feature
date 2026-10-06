Feature: Fake Doing Bullshit buttons
  Every button should do nothing, successfully.

  Scenario: Do nothing
    When I press the "ok" button
    Then it does nothing successfully

  Scenario: Do nothing, maybe
    When I press the "flaky" button
    Then it does nothing successfully

  Scenario: Do nothing, badly
    When I press the "broken" button
    Then it does nothing successfully

  Scenario: Do nothing, slowly
    When I press the "slow" button
    Then it does nothing successfully
