"""3D Bloch sphere renderer using matplotlib."""

from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D as Axes3DType

_GRID = "#1e3a4f"
_RING = "#2a6080"


class BlochSphere:
    """Renders a single Bloch sphere on a 3D matplotlib axes."""

    ax: Axes3DType
    _arrow: Any | None
    _arrow_glow: Any | None
    _trail: Any | None
    _trail_pts: list[tuple[Any, Any, Any]]

    def __init__(self, ax: Axes3DType, title: str = "") -> None:
        self.ax = ax
        self._arrow = None
        self._arrow_glow = None
        self._trail = None
        self._trail_pts = []
        self._setup(title)

    def _setup(self, title: str) -> None:
        ax = self.ax
        ax.set_facecolor("black")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_zlim(-1.3, 1.3)
        ax.set_box_aspect([1, 1, 1])
        ax.axis("off")
        if title:
            ax.set_title(title, color="white", pad=2, fontsize=11)

        # Ghost sphere surface + wireframe
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 30)
        xs = np.outer(np.cos(u), np.sin(v))
        ys = np.outer(np.sin(u), np.sin(v))
        zs = np.outer(np.ones_like(u), np.cos(v))
        ax.plot_surface(
            xs,
            ys,
            zs,
            alpha=0.07,
            color="#0a1a2e",
            linewidth=0,
            shade=False,
        )
        ax.plot_wireframe(
            xs,
            ys,
            zs,
            color=_GRID,
            linewidth=0.4,
            alpha=0.5,
        )

        # Latitude rings at +-30 deg and +-60 deg
        phi = np.linspace(0, 2 * np.pi, 120)
        for lat in (-60, -30, 30, 60):
            z0 = np.sin(np.radians(lat))
            r0 = np.cos(np.radians(lat))
            ax.plot(
                r0 * np.cos(phi),
                r0 * np.sin(phi),
                np.full_like(phi, z0),
                color=_RING,
                linewidth=0.6,
                alpha=0.55,
            )

        # Equator (brighter)
        ax.plot(
            np.cos(phi),
            np.sin(phi),
            np.zeros_like(phi),
            color="#3a80bf",
            linewidth=1.0,
            alpha=0.75,
        )

        # Meridian circles in XZ and YZ planes
        th = np.linspace(0, 2 * np.pi, 120)
        ax.plot(
            np.cos(th),
            np.zeros_like(th),
            np.sin(th),
            color=_RING,
            linewidth=0.6,
            alpha=0.55,
        )
        ax.plot(
            np.zeros_like(th),
            np.cos(th),
            np.sin(th),
            color=_RING,
            linewidth=0.6,
            alpha=0.55,
        )

        # Coordinate axes
        for vec, col in [
            ([1, 0, 0], "#cc3333"),
            ([0, 1, 0], "#33aa33"),
            ([0, 0, 1], "#3355ee"),
        ]:
            ax.plot(
                [-vec[0], vec[0]],
                [-vec[1], vec[1]],
                [-vec[2], vec[2]],
                color=col,
                linewidth=1.0,
                alpha=0.75,
            )

        ax.text(
            0, 0, 1.25, r"$|0\rangle$", color="white", ha="center", fontsize=9
        )
        ax.text(
            0, 0, -1.35, r"$|1\rangle$", color="white", ha="center", fontsize=9
        )
        ax.text(1.35, 0, 0, "x", color="#ff6666", ha="center", fontsize=8)
        ax.text(0, 1.35, 0, "y", color="#66ff66", ha="center", fontsize=8)

        # Equatorial cardinal labels
        ax.text(
            1.40,
            0,
            0,
            r"$|{+}\rangle$",
            color="#ee8888",
            ha="center",
            va="center",
            fontsize=9,
        )
        ax.text(
            -1.40,
            0,
            0,
            r"$|{-}\rangle$",
            color="#ee8888",
            ha="center",
            va="center",
            fontsize=9,
        )
        ax.text(
            0,
            1.40,
            0,
            r"$|R\rangle$",
            color="#88ee88",
            ha="center",
            va="center",
            fontsize=9,
        )
        ax.text(
            0,
            -1.40,
            0,
            r"$|L\rangle$",
            color="#88ee88",
            ha="center",
            va="center",
            fontsize=9,
        )

    def update(
        self,
        bloch_vec: npt.NDArray[np.float64],
        trail: bool = True,
    ) -> None:
        """Redraw the state vector and optionally append to the trail."""
        x, y, z = bloch_vec
        if self._arrow_glow is not None:
            self._arrow_glow.remove()
        if self._arrow is not None:
            self._arrow.remove()

        # Glow layer (wide, dim)
        self._arrow_glow = self.ax.quiver(
            0,
            0,
            0,
            x,
            y,
            z,
            color="#004466",
            linewidth=6.0,
            arrow_length_ratio=0.12,
            normalize=False,
            alpha=0.4,
        )
        # Bright layer
        self._arrow = self.ax.quiver(
            0,
            0,
            0,
            x,
            y,
            z,
            color="#00e5ff",
            linewidth=2.2,
            arrow_length_ratio=0.15,
            normalize=False,
        )

        if trail:
            self._trail_pts.append((x, y, z))
            self._redraw_trail()

    def _redraw_trail(self) -> None:
        if self._trail is not None:
            self._trail.remove()
            self._trail = None
        n = len(self._trail_pts)
        if n < 2:
            return
        pts = np.array(self._trail_pts, dtype=float)
        segments = [pts[i : i + 2] for i in range(n - 1)]
        alphas = np.linspace(0.05, 0.9, len(segments))
        colors = [(1.0, 0.55, 0.0, float(a)) for a in alphas]
        lc = Line3DCollection(segments, colors=colors, linewidths=1.8)
        self.ax.add_collection3d(lc)
        self._trail = lc

    def reset_trail(self) -> None:
        """Clear the trajectory trail."""
        self._trail_pts = []
        if self._trail is not None:
            self._trail.remove()
            self._trail = None
