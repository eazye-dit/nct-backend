from nct.utils import endpoint

public = [
    endpoint(
        "/api/",
        "Fetches an array of available endpoints"
    ),
    endpoint(
        "/api/login/",
        "Sets a cookie to authenticate the user as logged in",
        "POST"
    ),
    endpoint(
        "/api/vehicle/:regnumber/",
        "Fetches information about the vehicle with the specified regnumber"
    )
]


admin = [
    endpoint(
        "/api/admin/appointments/",
        "Returns an array of appointments, sorted by date, from the current date"
    ),
    endpoint(
        "/api/admin/appointment/:id/",
        "Returns the appointment with the associated ID"
    ),
    endpoint(
        "/api/admin/appointment/:id/",
        "Makes changes to the appointment with the associated ID",
        "POST"
    ),
    endpoint(
        "/api/admin/appointment/:id/",
        "Deletes the appointment with the associated ID",
        "DELETE"
    ),
    endpoint(
        "/api/admin/new/appointment/",
        "Adds an appointment to the database",
        "POST"
    ),
    endpoint(
        "/api/admin/new/mechanic/",
        "Adds a mechanic to the database",
        "POST"
    )
]

mechanic = [
    endpoint(
        "/api/mechanic/appointments/",
        "Fetches an array of appointments assigned to the currently logged in mechanic, " +
        "sorted by date, from the current date."
    ),
    endpoint(
        "/api/mechanic/test/:regnumber/",
        "Returns a JSON object with the appropriate tests for the vehicle with the specified regnumber."
    ),
    endpoint(
        "/api/mechanic/test/:regnumber/",
        "Puts a finished test to the server to store.",
        "POST"
    )
]

