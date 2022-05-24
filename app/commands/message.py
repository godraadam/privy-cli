from typing import Optional
import requests
import typer
from store import router_url

app = typer.Typer(help="Send or view messages")


@app.command()
def send(
    recipient: Optional[str] = typer.Option(None, "--recipient", "-r", prompt=True),
    message: Optional[str] = typer.Option(None, "--message", "-m", prompt=True),
):
    """
    Send a message to a contact
    """
    try:
        response = requests.post(
            f"{router_url}/api/message/send",
            json={"recipient_alias": recipient, "message": message},
        )
        if response.status_code == 200:
            typer.echo("Message sent successfully!")
        elif response.status_code == 404:
            typer.echo(
                f"Contact with name {recipient} was not found! Try adding it via privy contact add!"
            )
            raise typer.Exit()
        elif response.status_code == 403:
            typer.echo("You need to login before sending a message! Use privy login first!")
            raise typer.Exit()
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")


@app.command()
def ls(contact: Optional[str] = typer.Option(None, "--contact", "-c", prompt=True)):
    """
    Show messages received from a contact
    """
    try:
        response = requests.get(f"{router_url}/api/message/with/{contact}")
        if response.status_code == 200:
            typer.echo(f"Messages with {contact}:")
            messages = response.json()
            for _msg in messages:
                msg = dict(_msg)
                typer.echo(f'{msg["timestamp"]}: {msg["content"]}')
        elif response.status_code == 404:
            typer.echo(
                f"Contact with name {contact} was not found! Try adding it via privy contact add!"
            )
    except requests.exceptions.ConnectionError:
        typer.echo("The privy router is not running! Please start it via privy init!")
