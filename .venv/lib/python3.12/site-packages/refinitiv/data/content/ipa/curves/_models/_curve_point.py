class CurvePoint:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x={self.x}, y={self.y}"

    def __repr__(self):
        return f"CurvePoint(x={self.x}, y={self.y})"
