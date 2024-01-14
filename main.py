"TT"


class TT:
    "TT obj"

    def __init__(self, name) -> None:
        self.name = name
        self.subs = []
        self.cls = []

    @property
    def sub(self) -> list:
        "get all TT sub"
        return self.subs

    @sub.setter
    def sub(self, name: str):
        self.subs.append(name)

    def get_free_period(self):
        "Get all the free period"
        return "not implemented"

    def __repr__(self) -> str:
        return f"name: {self.name} cls: {self.cls}"


def main():
    "Main function"
    t_map = {}  # {<name>: <class list>}
    t_map["T1"] = ["C1", "C2"]
    t_map["T2"] = ["C2", "C3"]
    t1 = TT("T1")
    print(t1)


if __name__ == "__main__":
    main()
