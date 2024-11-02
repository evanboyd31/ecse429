import random
import sys
from behave.runner import Context
from behave.formatter._registry import make_formatters
from behave.runner_util import parse_features

from behave.__main__ import Configuration, run_behave, Runner


class ShuffleRunner(Runner):

    def feature_locations(self):
        locations = super().feature_locations()
        random.shuffle(locations)
        return locations

    def run_with_paths(self):
        self.context = Context(self)
        self.load_hooks()
        self.load_step_definitions()

        # -- STEP: Parse all feature files (by using their file location).
        feature_locations = [
            filename
            for filename in self.feature_locations()
            if not self.config.exclude(filename)
        ]
        features = parse_features(feature_locations, language=self.config.lang)
        for feature in features:
            random.shuffle(feature.scenarios)
        self.features.extend(features)

        # -- STEP: Run all features.
        stream_openers = self.config.outputs
        self.formatters = make_formatters(self.config, stream_openers)
        return self.run_model()


def main():
    config = Configuration()
    return run_behave(config, runner_class=ShuffleRunner)


if __name__ == "__main__":
    sys.exit(main())
