import pandas as pd


class DriftDetectionService:

    def __init__(self, docker=True):
        if docker:
            self.refined_data_path = "./refined"
        else:
            self.refined_data_path = "../../etl/app/refined"

    def detect_drift(self, dataset_name_1, dataset_name_2):
        # load datasets
        dataset1 = self._load_dataset(dataset_name_1)
        dataset2 = self._load_dataset(dataset_name_2)

        # do simple drift detection through descriptive statistics
        dataset1_desc = dataset1.describe()
        dataset2_desc = dataset2.describe()
        results = {
            "any_drift": False
        }
        for column in dataset1.columns:
            dataset1_mean = dataset1_desc[column]['mean']
            dataset2_mean = dataset2_desc[column]['mean']
            mean_diff = abs((dataset1_mean - dataset2_mean) / dataset1_mean * 100)
            dataset1_std = dataset1_desc[column]['std']
            dataset2_std = dataset2_desc[column]['std']
            std_diff = abs((dataset1_std - dataset2_std) / dataset1_std * 100)
            drift = False if mean_diff < 10 and std_diff < 20 else True
            results["any_drift"] = results["any_drift"] or drift
            results[column] = {
                "mean_percentage_diff": mean_diff,
                "std_percentage_diff": std_diff,
                "drift": drift
            }

        return results

    def _load_dataset(self, dataset_name) -> pd.DataFrame:
        return pd.read_csv(f"{self.refined_data_path}/{dataset_name}_data.csv")
