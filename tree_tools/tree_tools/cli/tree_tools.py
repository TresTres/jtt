import click
import logging
import json


@click.group()
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    """TreeTools CLI"""
    
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    

@cli.command()
@click.pass_context
@click.argument('input_file', type=click.File('r'), required=True)
def load_json(ctx: click.Context, input_file: click.File):
    """Load JSON file"""
    
    if ctx.obj['debug']:
        click.echo("Debug mode is on, will not actually save file to a tree .")
    
    data = json.load(input_file)
    logging.debug(data)


if __name__ == '__main__':
    cli(obj={})