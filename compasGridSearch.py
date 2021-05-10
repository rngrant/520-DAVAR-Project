# Load all necessary packages
import numpy as np
import sklearn as skl
import six
import tensorflow as tf

# datasets
from aif360.datasets import CompasDataset, BinaryLabelDataset

# metrics
from fklearn.metric_library import UnifiedMetricLibrary, classifier_quality_score

# models
from fklearn.scikit_learn_wrapper import LogisticRegression, KNeighborsClassifier, RandomForestClassifier, SVC
from aif360.algorithms.inprocessing import AdversarialDebiasing

# pre/post-processing algorithms
from aif360.algorithms.preprocessing import DisparateImpactRemover, Reweighing
from aif360.algorithms.postprocessing import CalibratedEqOddsPostprocessing, RejectOptionClassification

# model search
from fklearn.fair_selection_aif import ModelSearch, DEFAULT_ADB_PARAMS

from fklearn.scikit_learn_wrapper import LogisticRegression, KNeighborsClassifier, RandomForestClassifier, SVC
## Re setup data set (sanity check)
dataset = CompasDataset()
# Specific protected group
unprivileged = [{'race': 0, 'sex': 0}]
privileged = [{'race': 1, 'sex': 1}]

## Setup parameters

models = {'LogisticRegression': LogisticRegression, 'RandomForestClassifier': RandomForestClassifier }

metrics = {'UnifiedMetricLibrary': [UnifiedMetricLibrary,
                                    'accuracy_score',
                                    'average_odds_difference',
                                    'statistical_parity_difference',
                                    'equal_opportunity_difference',
                                    'disparate_impact'
                                   ]
          }

hyperparameters = {'LogisticRegression':{'penalty': ['l1', 'l2'], 'C': [0.1, 0.5, 1, 1.5],'solver':['liblinear']},
                   'RandomForestClassifier':{'n_estimators': ['warn', 10, 20, 30, 40, 50, 100]
                  }}

thresholds = [i * 10.0/100 for i in range(5)]

processor_args = {'unprivileged_groups': unprivileged, 'privileged_groups': privileged}

preprocessors=[DisparateImpactRemover()]
postprocessors=[CalibratedEqOddsPostprocessing(**processor_args)]


Search = ModelSearch(models, metrics, hyperparameters, thresholds) 
Search.grid_search(dataset, privileged=privileged, unprivileged=unprivileged, preprocessors=preprocessors, postprocessors=postprocessors)

Search.to_csv("search_output.csv")
