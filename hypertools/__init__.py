from .align import align, pad, trim_and_pad
from .cluster import cluster
from .core import get_default_options, get, fullfact, eval_dict
from .core.shared import RobustDict
from .io import load, save
from .manip import manip
from .plot import plot, write
from .reduce import reduce

# Convenience functions
def normalize(data, **kwargs):
    """Normalize data using hypertools normalization."""
    return manip(data, model='Normalize', **kwargs)
