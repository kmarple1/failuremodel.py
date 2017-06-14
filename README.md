Machine Failure Prediction
==========================

## 1. Description

Model and predict machine failure based on temperatures and disk error counts.

## 2. Contents

This README should be part of a distribution containing the following files:

 * compdata.txt -- Training data file.
 * compdata_true_errors.txt -- Error results corresponding to compdata.txt.
 * driver.py -- A sample driver file.
 * failuremodel.py -- The main source code file.
 * README.md -- This file.

## 3. Requirements

The API relies on scikit-learn (http://scikit-learn.org), which requires SciPy 
and NumPy. Assuming that these are installed, scikit-learn can be installed
using pip:

    pip install -U scikit-learn

## 4. Usage

To use the API, failuremodel must be imported and a failuremodel.PredictFail
object created:

    import failuremodel
    
    pf = failuremodel.PredictFail()

Tests can then be run against the model using the predict method
as follows:

    pf.predict("test01", 100, 0)

Two methods can be used to access the alerts. First, print_alerts() will
pretty-print all alerts in the queue in the order in which they were generated.
Alternatively, get_alert_queue() will return the AlertQueue, allowing manual
manipulation. Note that neither method clears the queue. This can be done by
calling clear_alerts().
    
A sample driver file (driver.py) has been provided which demonstrates the above
methods as well as manual manipulation of the AlertQueue. 
