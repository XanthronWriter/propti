import sys
import os
import numpy as np
import copy
import pandas as pd
import shutil as sh
import pickle

import propti as pr

import logging
logging.basicConfig(filename='propti.log', filemode='w', level=logging.DEBUG)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str,
                    help="python input file containing parameter and "
                         "simulation setups")
parser.add_argument("--root_dir", type=str,
                    help="root directory for optimization process", default='.')
parser.add_argument("--prepare_init_inputs",
                    help="prepare input files with initial values",
                    action="store_true")
cmdl_args = parser.parse_args()

setups = None # type: pr.SimulationSetupSet
ops = None
optimiser = None

input_file = cmdl_args.input_file

logging.info("reading input file: {}".format(input_file))
exec(open(input_file).read(), globals())
#TODO: check for correct execution

if ops is None:
    logging.critical("optimisation parameter are not defined")
if setups is None:
    logging.critical("simulation setups are not defined")
if optimiser is None:
    logging.critical("optimiser properties are not defined")

input_file_directory = os.path.dirname(input_file)
logging.info("input file directory: {}".format(input_file_directory))

for s in setups:

    cdir = os.path.join(cmdl_args.root_dir, s.work_dir)

    # create work directories
    if not os.path.exists(cdir): os.mkdir(cdir)

    # copy model template
    sh.copy(os.path.join(input_file_directory, s.model_template), cdir)

    s.model_template = os.path.join(cdir, os.path.basename(s.model_template))

    # copy all exerimental data
    for r in s.relations:
        sh.copy(os.path.join(input_file_directory, r.experiment.file_name),
                cdir)
        r.experiment.file_name = \
            os.path.join(cdir, os.path.basename(r.experiment.file_name))

# check for potential non-unique model input files
in_file_list = []
for s in setups:
    tpath = os.path.join(s.work_dir, s.model_input_file)
    if tpath in in_file_list:
        logging.error("non unique module input file path: {}".format(tpath))
        sys.exit()
    in_file_list.append(tpath)

print(setups, ops, optimiser)

out_file = open('propti.pickle.init', 'wb')
pickle.dump((setups, ops, optimiser), out_file)
out_file.close()

if cmdl_args.prepare_init_inputs:
    logging.info("prepare input files with initial values")
    for s in setups:
        pr.create_input_file(s)
