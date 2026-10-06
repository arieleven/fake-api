from behave import then, when


@when('I press the "{route}" button')
def press(context, route):
    context.response = context.client.get(f"/api/{route}")


@then("it does nothing successfully")
def succeeds(context):
    assert context.response.status_code == 200, f"got {context.response.status_code}"
