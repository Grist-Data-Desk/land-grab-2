#!/usr/bin/env python
import typer

from land_grab_2.stl_dataset.step_1 import build_dataset, compute_summary
from land_grab_2.stl_dataset.step_2.land_activity_search import activity_match
from land_grab_2.uni_holdings_dataset import check_overlap, reverse_search
import land_grab_2.stl_dataset.step_3.cession_purchase_price as cession_purchase_price
app = typer.Typer()


# @app.command()
# def all():
#     'install clean-all stl-dataset stl-summary stl-activity-match private-holdings-by-geo-overlap
#     private-holdings-by-reverse-search'


@app.command()
def stl_dataset():
    build_dataset.run()
    # compute_summary.run() # TODO
    activity_match.run()
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


#
# @app.command()
# def clean_all():
#     'clean_stl_dataset clean-stl-summary clean-geo-overlap clean-reverse-search'
#
#
# @app.command()
# def clean_stl_dataset():
#     # rm -rf $(DATA)/stl_dataset/step_1/input/state_trust/cleaned
#     # rm -rf $(DATA)/stl_dataset/step_1/input/state_trust/merged
#     'rm -rf $(DATA)/stl_dataset/step_1/input/state_trust/queried'
#
#
# @app.command()
# def clean_stl_summary():
#     'rm -rf $(DATA)/stl_dataset/step_1/input/state_trust/summary_statistics'
#
#
# @app.command()
# def clean_stl_activity_match():
#     'rm -rf $(DATA)stl_dataset/step_2/output'
#
#
# @app.command()
# def clean_geo_overlap():
#     'rm -rf $(DATA)/uni_holdings/overlap_check/output'
#
#
# @app.command()
# def clean_reverse_search():
#     'rm -rf $(DATA)/uni_holdings/reverse_search/output'


if __name__ == '__main__':
    app()
