#!/usr/bin/env python
import typer

from land_grab_2.stl_dataset.step_1 import build_dataset, compute_summary
from land_grab_2.stl_dataset.step_2.land_activity_search import activity_match
from land_grab_2.uni_holdings_dataset import check_overlap, reverse_search
import land_grab_2.stl_dataset.step_3.cession_purchase_price as cession_purchase_price

app = typer.Typer()


@app.command()
def stl_dataset_step_1():
    build_dataset.run()
    activity_match.run()


@app.command()
def stl_dataset_step_2():
    # below needs session
    # compute_summary.run() # TODO
    cession_purchase_price.run()


@app.command()
def stl_summary():
    compute_summary.run()


@app.command()
def stl_activity_match():
    activity_match.run()


@app.command()
def private_holdings_by_geo_overlap(states=None):
    check_overlap.run(states)


@app.command()
def private_holdings_by_reverse_search():
    reverse_search.run()


if __name__ == '__main__':
    app()
