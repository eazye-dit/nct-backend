from nct.utils import endpoint

#base = "https://dev.cute.enterprises"
base = ""

public = [
    endpoint(
        base + "/api/",
        "Fetches an array of available endpoints"
    ),
    endpoint(
        base + "/api/login/",
        "Sets a cookie to authenticate the user as logged in",
        "POST"
    ),
    endpoint(
        base + "/api/vehicle/:regnumber/",
        "Fetches information about the vehicle with the specified regnumber"
    )
]


admin = [
    endpoint(
        base + "/api/admin/appointments/",
        "Returns an array of appointments, sorted by date, from the current date"
    ),
    endpoint(
        base + "/api/admin/appointment/:id/",
        "Returns the appointment with the associated ID"
    ),
    endpoint(
        base + "/api/admin/appointment/:id/",
        "Makes changes to the appointment with the associated ID",
        "POST"
    ),
    endpoint(
        base + "/api/admin/appointment/:id/",
        "Deletes the appointment with the associated ID",
        "DELETE"
    ),
    endpoint(
        base + "/api/admin/new/appointment/",
        "Adds an appointment to the database",
        "POST"
    ),
    endpoint(
        base + "/api/admin/new/mechanic/",
        "Adds a mechanic to the database",
        "POST"
    )
]

mechanic = [
    endpoint(
        base + "/api/mechanic/appointments/",
        "Fetches an array of appointments assigned to the currently logged in mechanic, " +
        "sorted by date, from the current date."
    ),
    endpoint(
        base + "/api/mechanic/test/:regnumber/",
        "Returns a JSON object with the appropriate tests for the vehicle with the specified regnumber."
    ),
    endpoint(
        base + "/api/mechanic/test/:regnumber/",
        "Puts a finished test to the server to store.",
        "POST"
    )
]

