# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from dial_basic_nodes.utils.dataset_table import (
    DatasetTableViewFactory,
    DatasetTableWidget,
)

from .test_dataset_table_model import TestDatasetTableModelFactory

TestDatasetTableWidgetFactory = providers.Factory(
    DatasetTableWidget, view=DatasetTableViewFactory, model=TestDatasetTableModelFactory
)
