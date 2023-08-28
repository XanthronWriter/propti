import logging

#########
# LOGGING
# set up logging to file - see previous section for more details


try:
    # get MPI rank for individual log files
    import mpi4py
    mpi4py.rc.recv_mprobe = False

    from mpi4py import MPI
    my_rank = MPI.COMM_WORLD.Get_rank()
except Exception:
    my_rank = 0


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='propti.{:03d}.log'.format(my_rank),
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)

########
# PROPTI AND SPOTPY

from .spotpy_wrapper import run_optimisation, create_input_file
from .data_structures import Parameter, ParameterSet, \
    SimulationSetupSet, SimulationSetup, Relation, DataSource, \
    OptimiserProperties, Version, Sampler, Job
from .basic_functions import run_simulations, get_save_path
from .propti_post_processing import run_best_para

from .propti_monitor import plot_scatter, plot_scatter2, \
    plot_para_vs_fitness, plot_box_rmse
from .propti_post_processing import run_best_para, plot_hist, \
    calc_pearson_coefficient, collect_best_para_multi, plot_best_sim_exp
from .propti_pre_processing import interpolate_lists

from .fitness_methods import FitnessMethodRMSE, FitnessMethodInterface, \
    FitnessMethodThreshold, FitnessMethodRangeRMSE, FitnessMethodBandRMSE, \
    FitnessMethodIntegrate


###########
# CONSTANTS

# TODO: respect this variable in scripts
pickle_prefix = 'propti.pickle'
