"""Load data from AWS dataset."""

import json
import sys
from urllib.request import urlopen

from progress.bar import Bar

import pandas as pd

# import pdal


class LoadData:
    def __init__(self) -> None:
        """Initialize loaddata class."""
        try:
            self.data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
            self.df = pd.DataFrame(
                columns=[
                    "region",
                    "year",
                    "xmin",
                    "xmax",
                    "ymin",
                    "ymax",
                    "zmin",
                    "zmax",
                    "points",
                ]
            )
        except Exception:
            sys.exit(1)

    def get_regions(self) -> None:
        """Get the regions data from a json file."""
        with open("regions.json", "r") as f:
            self.regions = json.load(f)
            self.bar = Bar("Loading MetaData", max=len(self.regions))

    def get_data(self) -> None:
        """Get boundaries of the data."""
        # Get the regions
        self.get_regions()
        # print(len(self.regions))
        data = []
        for ind in range(len(self.regions)):
            try:
                # print(self.regions[str(ind + 1)])
                end_pt = self.data_path + self.regions[str(ind + 1)] + "/ept.json"
                res = json.loads(urlopen(end_pt).read())
            except Exception as e:
                print("The status: ", res)
                print(e)
            if res:
                x = {
                    "region": "".join(self.regions[str(ind + 1)].split("_")[:-1]),
                    "year": self.regions[str(ind + 1)].split("_")[-1],
                    "xmin": res["bounds"][0],
                    "xmax": res["bounds"][3],
                    "ymin": res["bounds"][1],
                    "ymax": res["bounds"][4],
                    "zmin": res["bounds"][2],
                    "zmax": res["bounds"][5],
                    "points": res["points"],
                }

                data.append(x)
                self.bar.next()
            else:
                pass
        self.df = pd.DataFrame(data)
        self.bar.finish()
        self.save_csv("../data/metadata.csv")

    def save_csv(self, path) -> None:
        """Save dataframe as a csv.
        Args:
            path (str): path of the csv file
        """
        try:
            self.df.to_csv(path, index=False)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    LoadData().get_data()