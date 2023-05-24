from .kafka_parser import KafkaOutput, KafkaParser
from lc_classification.predictors.predictor.predictor_parser import PredictorOutput
import numpy as np
import pandas as pd


class StepParser(KafkaParser):
    def parse(self, model_output: PredictorOutput, **kwargs) -> KafkaOutput[list]:
        messages = kwargs.get("messages", [])
        features = kwargs.get("features", pd.DataFrame())
        step_metrics = kwargs.get("step_metrics", {})
        parsed = []
        step_metrics["class"] = model_output.classifications["class"].tolist()
        features.drop(columns=["candid"], inplace=True)
        features.replace({np.nan: None}, inplace=True)
        messages_df = pd.DataFrame(
            [
                {"aid": message.get("aid"), "candid": message.get("candid", np.nan)}
                for message in messages
            ]
        )
        messages_df.sort_values("candid", ascending=False, inplace=True)
        messages_df.drop_duplicates("aid", inplace=True)
        for _, row in messages_df.iterrows():
            aid = row.aid
            candid = row.candid
            features_aid = features.loc[aid].to_dict()

            tree_aid = self._get_aid_tree(model_output.classifications, aid)
            write = {
                "aid": aid,
                "candid": candid,
                "features": features_aid,
                "lc_classification": tree_aid,
            }
            parsed.append(write)

        return KafkaOutput(parsed)

    def _get_aid_tree(self, tree, aid):
        tree_aid = {}
        for key in tree:
            data = tree[key]
            if isinstance(data, pd.DataFrame):
                tree_aid[key] = data.loc[aid].to_dict()
            elif isinstance(data, pd.Series):
                tree_aid[key] = data.loc[aid]
            elif isinstance(data, dict):
                tree_aid[key] = self._get_aid_tree(data, aid)
        return tree_aid
