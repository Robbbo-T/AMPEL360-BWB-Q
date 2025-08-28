"""
MDGPT - Multidimensional Generative Pretrained Transformer
From static 2D images → rich engineering ontologies → parametric 3D

AMPEL360-BWB-Q CQEA Module
UTCS-MI v5.0 Compliant
"""

__version__ = "1.0.0"
__author__ = "AQUA Technologies - MDGPT Team"

from .core import MDGPT
from .perception import PerceptionStack
from .mapping import OntologyMapper
from .reconstruction import Reconstruction

__all__ = [
    "MDGPT",
    "PerceptionStack", 
    "OntologyMapper",
    "Reconstruction"
]