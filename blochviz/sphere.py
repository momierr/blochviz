import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


class BlochSphere:
    def __init__(self, ax, title=""):
        self.ax = ax
        self._arrow = None
        self._trail_line = None
        self._trail_pts = []
        self._setup(title)

    def _setup(self, title):
        ax = self.ax
        ax.set_facecolor("black")
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_zlim(-1.3, 1.3)
        ax.set_box_aspect([1, 1, 1])
        ax.axis("off")
        if title:
            ax.set_title(title, color="white", pad=2, fontsize=10)

        # Wireframe sphere
        u = np.linspace(0, 2 * np.pi, 40)
        v = np.linspace(0, np.pi, 20)
        xs = np.outer(np.cos(u), np.sin(v))
        ys = np.outer(np.sin(u), np.sin(v))
        zs = np.outer(np.ones_like(u), np.cos(v))
        ax.plot_wireframe(xs, ys, zs, color="#334455", linewidth=0.3, alpha=0.4)

        # Axes lines
        for vec, color in [
            ([1, 0, 0], "#ff4444"),
            ([0, 1, 0], "#44ff44"),
            ([0, 0, 1], "#4444ff"),
        ]:
            ax.plot(
                [-vec[0], vec[0]],
                [-vec[1], vec[1]],
                [-vec[2], vec[2]],
                color=color,
                linewidth=0.8,
                alpha=0.6,
            )

        # Pole and axis labels
        ax.text(0, 0, 1.25, "|0⟩", color="white", ha="center", fontsize=9)
        ax.text(0, 0, -1.35, "|1⟩", color="white", ha="center", fontsize=9)
        ax.text(1.35, 0, 0, "x", color="#ff6666", ha="center", fontsize=8)
        ax.text(0, 1.35, 0, "y", color="#66ff66", ha="center", fontsize=8)

        # Equator circle
        phi = np.linspace(0, 2 * np.pi, 100)
        ax.plot(
            np.cos(phi),
            np.sin(phi),
            np.zeros_like(phi),
            color="#445566",
            linewidth=0.5,
            alpha=0.5,
        )

    def update(self, bloch_vec, trail=True):
        x, y, z = bloch_vec
        if self._arrow is not None:
            self._arrow.remove()

        self._arrow = self.ax.quiver(
            0,
            0,
            0,
            x,
            y,
            z,
            color="#00d4ff",
            linewidth=2.5,
            arrow_length_ratio=0.15,
            normalize=False,
        )

        if trail:
            self._trail_pts.append((x, y, z))
            if self._trail_line is not None:
                self._trail_line.remove()
            if len(self._trail_pts) >= 2:
                pts = np.array(self._trail_pts)
                (self._trail_line,) = self.ax.plot(
                    pts[:, 0],
                    pts[:, 1],
                    pts[:, 2],
                    color="#ff9900",
                    linewidth=1.2,
                    alpha=0.7,
                )

    def reset_trail(self):
        self._trail_pts = []
        if self._trail_line is not None:
            self._trail_line.remove()
            self._trail_line = None
