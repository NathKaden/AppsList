class App:
    def __init__(self, name, size=0.0, year=0):
        self.name = name
        self.size = size
        self.year = year

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("nom", ""),
            size=data.get("taille", 0.0),
            year=data.get("année", 0)
        )

    def to_dict(self):
        return {
            "nom": self.name,
            "taille": self.size,
            "année": self.year
        }
