"""Console script for flake8_django_plugin."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("flake8-django-plugin")
    click.echo("=" * len("flake8-django-plugin"))
    click.echo("Flake8 plugin to enforce good practices.")


if __name__ == "__main__":
    main()  # pragma: no cover
