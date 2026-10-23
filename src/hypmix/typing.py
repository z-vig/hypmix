# Standard Libraries
from dataclasses import dataclass
from typing import TypeVar, Literal, TypeAlias, TypeGuard
from typing_extensions import Annotated
import os
from pathlib import Path

# Dependencies
import numpy.typing as npt
import numpy as np

PathLike = str | os.PathLike | Path

DType = TypeVar("DType", bound=np.generic)
SpectrumLike = Annotated[npt.NDArray[DType], (1,)]
ImageCubeLike = Annotated[npt.NDArray[DType], (3,)]
ImageLike = Annotated[npt.NDArray[DType], (2,)]


@dataclass
class Spectrum:
    data: SpectrumLike
    wvl: SpectrumLike


@dataclass
class ImageCube:
    data: ImageCubeLike
    wvl: SpectrumLike
    bands_first: bool = False

    def __post_init__(self):
        bands_dim = np.argmin(self.data.shape)
        self.data = np.moveaxis(self.data, bands_dim, -1)


ResidualMode: TypeAlias = Literal["Band-by-Band", "Total R\u00b2"]
residual_modes: list[ResidualMode] = ["Band-by-Band", "Total R²"]


def is_valid_residual_mode(value: str) -> TypeGuard[ResidualMode]:
    return value in residual_modes
