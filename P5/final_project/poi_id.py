#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Remove outliers
data_dict.pop('TOTAL', 0)
data_dict.pop('LOCKHART EUGENE E', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)

### Create new feature
[data_dict[p].pop('email_address', 0) for p in data_dict.keys()]

for p in data_dict.keys():
    
    if data_dict[p]['from_this_person_to_poi'] != 'NaN' and data_dict[p]['from_messages'] != 'NaN' and float(data_dict[p]['from_messages']) > 0:
        #data_dict[p].update({'to_poi_ratio': 'NaN'})
        data_dict[p].update(
            {'to_poi_ratio':
             float(data_dict[p]['from_this_person_to_poi']) / float(data_dict[p]['from_messages'])
            })
    else:
        data_dict[p].update({'to_poi_ratio': 'NaN'})

### Feature Selection
features_list = ['poi',
 'to_messages',
 #'deferral_payments',
 'bonus',
 'total_stock_value',
 'expenses',
 'from_poi_to_this_person',
 #'from_this_person_to_poi',
 #'deferred_income',
 'restricted_stock',
 'long_term_incentive',
 'salary',
 'total_payments',
 'loan_advances',
 #'restricted_stock_deferred',
 'shared_receipt_with_poi',
 'exercised_stock_options',
 #'from_messages',
 'other',
 'to_poi_ratio',
 #'director_fees'
]

### Dataset
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

# Naive Bayes
# Higher precision, lower recall
estimators = [('best', SelectKBest(k=6)),
              ('NB', GaussianNB())]
clf_nb = Pipeline(estimators)

# SVM
# Higher recall, lower precision
estimators = [('norm', MinMaxScaler()),
              ('svm', SVC(C=1, gamma='auto', class_weight='balanced'))]
clf_svm = Pipeline(estimators)


# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

clf_nb.fit(features_train, labels_train)
clf_svm.fit(features_train, labels_train)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf_nb, my_dataset, features_list)
#dump_classifier_and_data(clf_svm, my_dataset, features_list)


