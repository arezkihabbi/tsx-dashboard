class SurfacePoint:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"x={self.x}, y={self.y}, z={self.z}"

    def __repr__(self):
        return f"SurfacePoint(x={self.x}, y={self.y}, z={self.z})"
