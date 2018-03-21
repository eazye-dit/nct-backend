<!DOCTYPE html>
<head>
    <title>Login</title>
</head>
<body>
    <form action="/api/login/" method="post">
        <input type="hidden" name="username" value="mechanic">
        <input type="hidden" name="password" value="notsecret">
        <input type="submit" value="Log in as mechanic">
    </form>
    <br />
    <form action="/api/login/" method="post">
        <input type="hidden" name="username" value="administrator">
        <input type="hidden" name="password" value="notsecret">
        <input type="submit" value="Log in as administrator">
    </form>
<body>
