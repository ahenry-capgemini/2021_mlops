from great_expectations.checkpoint import LegacyCheckpoint
from great_expectations.data_context import DataContext


class GreatExpectationsService:
    """Class with methods to manage great expectations"""

    def __init__(self) -> None:
        self.context = DataContext()

    def validate_refined_data(self, dataset_name):
        # This defines the batch for our data set
        batch_kwargs_2 = {
            "path": f"./refined/{dataset_name}_data.csv",
            "datasource": "refined__dir",
            "data_asset_name": f"{dataset_name}_data",
        }

        # This is where we configure a Checkpoint to validate the batch with our suite
        my_checkpoint = LegacyCheckpoint(
            name="my_checkpoint",
            data_context=self.context,
            batches=[
                {
                    "batch_kwargs": batch_kwargs_2,
                    "expectation_suite_names": ["refined_data.warning"]
                }
            ]
        )

        # And here we just run validation!
        results = my_checkpoint.run()
        return results

    def get_validation_results_uri(self, results, site_name=None, only_if_exists=True):
        validation_result_identifier = results.list_validation_result_identifiers()[0]
        self.context.build_data_docs()
        # self.context.open_data_docs(validation_result_identifier)
        data_docs_urls = self.context.get_docs_sites_urls(
            resource_identifier=validation_result_identifier,
            site_name=site_name,
            only_if_exists=only_if_exists,
        )
        urls_to_open = [site["site_url"] for site in data_docs_urls]

        for url in urls_to_open:
            if url is not None:
                break

        return url.split("local_site", 1)[1]
