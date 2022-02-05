import json
import socket
import subprocess
from typing import Optional
import typer
from schemas.login_schema import LoginSchema
from commands import contact, account
import requests
from store import router_url, path_to_router


app = typer.Typer()

app.add_typer(contact.app, name="contact")
app.add_typer(account.app, name="account")


@app.command()
def login(
    user_name: Optional[str] = typer.Option(None, "--user", "-u", prompt=True),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", prompt=True, hide_input=True
    ),
):
    """
    Login to the privy app
    """

    try:
        response = requests.post(f"{router_url}/api/ping")
    except:
        typer.echo("The Privy Router is not running. You can start it with privy init!")
        raise typer.Exit()
    body = LoginSchema(username=user_name, password=password)
    response = requests.post(
        f"{router_url}/api/auth/login", data=json.dumps(body.dict())
    )
    if response.status_code == 200:
        typer.echo(f"Successfully logged in as {user_name}")
    elif response.status_code == 404:
        typer.echo(
            "No such user was found on this device! Try adding an existing account with privy account add or creating a new one with privy account create!"
        )
    elif response.status_code == 401:
        typer.echo(
            "The credentials did not match. Make sure you typed your credentials correctly!"
        )
    elif response.status_code == 409:
        typer.echo("Already logged in. Log out first then try again!")


@app.command()
def logout():
    """
    Log out from privy
    """
    try:
        requests.post(f"{router_url}/api/auth/logout")
        typer.echo("Successfully logged out!")
    except:
        typer.echo("The Privy Router is not running. You can start it with privy init!")


@app.command()
def init():
    """
    Start the privy router (neccessary for other commands to work)
    """
    try:
        s = socket.socket()
        s.bind(("127.0.0.1", 6130))  # test the port
        s.close()
    except Exception as e:
        typer.echo("Router is already running!")
        raise typer.Exit()
    subprocess.Popen(
        f"{path_to_router} & ",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@app.command()
def whoami():
    """
    Display the username of currently logged in user
    """
    try:
        response = requests.get(f"{router_url}/api/auth/whoami")
        if response.status_code == 404:
            typer.echo(f"No one is logged in at the moment.")
        else:
            typer.echo(f"Logged in as {dict(response.json()).get('username')}")
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")


if __name__ == "__main__":
    app()
