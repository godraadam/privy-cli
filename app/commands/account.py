from typing import Optional
import typer
import requests
from store import router_url

app = typer.Typer(help="Manage accounts on this device")


@app.command()
def add(
    username: Optional[str] = typer.Option(None, "--name", "-n", prompt=True),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", prompt=True, hide_input=True
    ),
):
    """
    Add an existing account on this device
    """
    try:
        response = requests.post(
            f"{router_url}/api/account/add",
            data={"username": username, "password": password},
        )
        if response.status_code == 409:
            # TODO: separate username for pubkey gen from username alias
            typer.echo("An account with given username already exists on this device!")
        else:
            typer.echo("Account addded successfully!")
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")
        
@app.command()
def create(
    username: Optional[str] = typer.Option(None, "--name", "-n", prompt=True),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", prompt=True, hide_input=True
    ),
):
    """
    Create a new account
    """
    try:
        response = requests.post(
            f"{router_url}/api/account/add",
            data={"username": username, "password": password},
        )
        if response.status_code == 409:
            # TODO: separate username for pubkey gen from username alias
            typer.echo("An account with given username already exists on this device!")
        else:
            typer.echo("Account created successfully!")
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")


@app.command()
def remove(username: str = typer.Argument(...)):
    """
    Remove an account from this device
    """
    try:
        response = requests.post(f"{router_url}/api/account/remove/{username}")
        if response.status_code == 404:
            # TODO: separate username for pubkey gen from username alias
            typer.echo(f"No user by the name {username} was found, nothing was deleted.")
        else:
            typer.echo("Account removed successfully!")
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")
