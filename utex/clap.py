class Config(dict):
    def __init__(self, path: str) -> None:
        from yaml import safe_load

        f = open(path, "r")
        self.__path = path
        d: dict = safe_load(f)
        [self.__setitem__(item[0], item[1]) for item in d.items()]
        f.close()

    def __missing__(self) -> dict:
        return dict()

    @property
    def comport(self) -> dict:
        return self["Comport"]

    @property
    def experimental(self) -> dict:
        return self["Experimental"]

    @property
    def metadata(self) -> dict:
        return self["Metadata"]


class PinoClap(object):
    def __init__(self):
        from argparse import ArgumentParser

        self.__parser = ArgumentParser(
            description="Command line interface for reading the yaml that describes experimental settings."
        )
        self.__parser.add_argument(
            "--yaml", "-y", help="Path to yaml for the experiment.", type=str
        )
        self.__args = self.__parser.parse_args()

    def config(self) -> Config:
        return Config(self.__args.yaml)
