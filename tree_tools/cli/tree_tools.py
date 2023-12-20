
import click
import logging
import json

from src import jtt_tree, jtt_visitor 

@click.group()
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    """TreeTools CLI"""
    
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    
    if debug:
        click.echo('Debug mode is on.')
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    

@cli.command()
@click.pass_context
@click.argument('input_file', type=click.File('r'), required=True)
def load_json(ctx: click.Context, input_file: click.File):
    """Load JSON file"""
    
    data = json.load(input_file)
    logging.debug(data)
    try: 
        tree = jtt_tree.create_tree(data)
        # logging.debug(tree)
        
        query = jtt_visitor.NodeQuery(tree, ['**', 'positions', '0'])
        logging.debug(query.collect_results())
        
    except Exception as e:
        logging.error(e)
        

if __name__ == '__main__':
    cli(obj={})