from typing import Optional
import typer
import requests
from schemas.contact import PrivyContactCreate
from store import router_url

app = typer.Typer(help="Manage contacts of currently logged in user")


@app.command()
def add(
    alias: str = typer.Option(..., "--alias", "-a", prompt=True),
    public_key: str = typer.Option(..., "--pubkey", "-p", prompt=True),
    trusted: Optional[bool] = typer.Option(False, "--trusted", prompt=True),
):
    """
    Add a new contact
    """
    try:
        contact = PrivyContactCreate(alias=alias, pubkey=public_key, trusted=trusted)
        response = requests.post(f"{router_url}/api/contact/add", json=contact.dict())
        if response.status_code != 200:
            typer.echo(f"Something went wrong... Error code {response.status_code}")
            raise typer.Exit()
        typer.echo(
            f"New contact created: {alias} -> {public_key} (trusted: {'Yes' if trusted else 'No'})"
        )
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")


@app.command()
def ls():
    """
    List contacts
    """
    try:
        response = requests.get(f"{router_url}/api/contact/ls")
        if response.status_code != 200:
            typer.echo(f"Something went wrong... Error code {response.status_code}")
            raise typer.Exit()
        contacts = response.json()
        typer.echo(f"alias {' ' * 28} public key")
        typer.echo("-" * 45)
        for _contact in contacts:
            contact = dict(_contact)
            typer.echo(
                f"{contact['alias']} -> {' ' * (30 - len(contact['alias']))} {contact['pubkey']} {typer.style('trusted' if contact['trusted'] else '', fg=typer.colors.GREEN)}"
            )
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")


@app.command()
def rm(
    alias: str = typer.Argument(...),
):
    """
    Remove a contact
    """
    try:
        response = requests.delete(f"{router_url}/api/contact/rm/{alias}")
        if response.status_code == 404:
            typer.echo(f"No contact with alias {alias} was found, nothing was deleted.")
            raise typer.Exit()
        if response.status_code != 200:
            typer.echo(f"Something went wrong... Error code {response.status_code}")
            raise typer.Exit()
        typer.echo(
            f"{alias} removed from contacts"
        )
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")
