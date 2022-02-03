from asyncio import subprocess
import json
import socket
from typing import Optional
import typer
import requests
import subprocess

from schemas.login_schema import LoginSchema

router_url = 'http://127.0.0.1:6130'
path_to_router = '../privy-router/dist/main/main'

app = typer.Typer()

@app.command()
def login(user_name: Optional[str] = typer.Option(..., "--user", "-u", prompt=True), password: Optional[str] = typer.Option(..., "--password", "-p", prompt=True, hide_input=True)):
    try:
        response = requests.post(f"{router_url}/api/ping")
    except:
        typer.echo("The Privy Router is not running. You can start it with privy init!")
        raise typer.Exit()
    body = LoginSchema(username=user_name, password=password)
    response = requests.post(f"{router_url}/api/auth/login", data=json.dumps(body.dict()))
    if response.status_code == 200:
        typer.echo(f"Successfully logged in as {user_name}")
    elif response.status_code == 404:
        typer.echo("No such user was found on this device! Try adding an existing account with privy account add or creating a new one with privy account create!")
    elif response.status_code == 401:
        typer.echo("The credentials did not match. Make sure you typed your credentials correctly!")
    elif response.status_code == 409:
        typer.echo("Already logged in. Log out first then try again!")


@app.command()
def logout():
    try:
        requests.post(f"{router_url}/api/auth/logout")
        typer.echo("Successfully logged out!")
    except:
        typer.echo("The Privy Router is not running. You can start it with privy init!")

@app.command()
def init():
    try:
        s = socket.socket()
        s.bind(("127.0.0.1", 6130))  # test the port
        s.close()
    except Exception as e:
        typer.echo("Router is already running!")
        raise typer.Exit()
    subprocess.Popen(path_to_router, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
if __name__ == "__main__":
    app()