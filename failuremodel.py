"""Machine failure prediction"""

# Author: Kyle Marple
# Date: 2017.06.14

import csv
import time
import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

class AlertQueue():
    """A queue for alerts consisting of a time stamp and machine name.
    
    Notes
    -----
    Each alert in the queue is a dictionary with two keys. The 'time' key
    contains a Unix time stamp (in seconds since the epoch) while the 'name' key
    stores the name of the machine for which the alert was generated.
    """
    
    def __init__(self):
        """Initialize the queue."""
        
        self.queue = []
        
    def add_alert(self, name):
        """Add an alert to the queue.
        
        Parameters
        ----------
        name : string
            The name of the machine to queue an alert for.
        """
        
        alert = {}
        alert['time'] = time.time()
        alert['name'] = name
        self.queue.append(alert)
        
    def clear_queue(self):
        """Clear the queue."""
        
        self.queue = []
        
    def empty(self):
        """Return True or False indicating whether or not the queue is empty."""
        
        return len(self.queue) == 0
        
    def pop_alert(self):
        """"Pop the first alert in the queue, removing it and returning it.
        
        Returns
        -------
        rval : dictionary
            A single alert containing 'time' and 'name' entries.
        """
        
        if len(self.queue) > 0:
            rval = self.queue[0]
            self.queue = self.queue[1:]
        else:
            rval = None
        
        return rval
        
    def print_alert(self, alert):
        """Print a single alert.
        
        Parameters
        ----------
        alert : dictionary
            The alert to be printed. Must contain 'time' and 'name' entries.
        """
        
        t = datetime.datetime.fromtimestamp(alert['time'])
        str_t = t.strftime("%c")
        print(str_t + " - Predicted failure of " + alert['name'] + ".")
        
    def print_alerts(self):
        """Pretty-print all alerts in the queue."""
        
        for x in self.queue:
            self.print_alert(x)

class PredictFail():
    """Predicting machine failure, queueing alerts when failure is predicted."""
    
    def __init__(self, file1 = 'compdata.txt',
                 file2 = 'compdata_true_errors.txt'):
        """Read input and build model.
        
        Parameters
        ----------
        file1 : string, default 'compdata.txt'
            Training data file. Each line is expected to contain two integers
            separated by a tab.
        file2 : string, default 'compdata_true_errors.txt'
            Training data results file. Each line is expected to contain a 1 or
            0 indicating if the corresponding entry in file1 resulted in a
            failure.
        """
        
        self.n_features = 2
        self.read_input(file1, file2)
        self.build_model()
        self.queue = AlertQueue()
    
    def build_model(self):
        """Build the model.
        
        Currently, the model used is Nearest Neighbors classification, but this
        can easily be changed as needed.
        """
        
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.model.fit(self.data, self.target)
    
    def check_model(self, temperature, disk_errors):
        """Given temperature and error count, predict if a machine will fail.
        
        Parameters
        ----------
        temperature : int
            The temperature to be tested.
        disk_errors : int
            The disk error count to be tested.
            
        Returns
        -------
        rval[0] : int
            A 1 or 0 indicating whether or not failure is predicted.
        """
        
        test_data = np.empty((1, self.n_features))
        test_data[0] = np.asarray([temperature, disk_errors], dtype=np.int)
        rval = self.model.predict(test_data)
        return rval[0]
        
    def clear_alerts(self):
        """Clear the alert queue."""
        
        self.queue.clear_queue()
        
    def get_alert_queue(self):
        """Return the alert queue for external processing.
            
        Returns
        -------
        self.queue : AlertQueue
            The queue of alerts.
        """
        
        return self.queue
        
    def predict(self, name, temperature, disk_errors):
        """Test a machine. If failure is predicted, queue an alert.
        
        Parameters
        ----------
        name : string
            The name of the machine to be tested.
        temperature : int
            The temperature to be tested.
        disk_errors : int
            The disk error count to be tested.
        """
        
        error = self.check_model(temperature, disk_errors)
        
        if error == 1:
            #Queue an alert
            self.queue.add_alert(name)
        
    def print_alerts(self):
        """Print the queued alerts."""
        
        self.queue.print_alerts()

    def read_input(self, file1 = 'compdata.txt',
                   file2 = 'compdata_true_errors.txt'):
        """Read training data and target info from files.
        
        Parameters
        ----------
        file1 : string, default 'compdata.txt'
            Training data file. Each line is expected to contain two integers
            separated by a tab.
        file2 : string, default 'compdata_true_errors.txt'
            Training data results file. Each line is expected to contain a 1 or
            0 indicating if the corresponding entry in file1 resulted in a
            failure.
        """
        
        # first, get number of samples
        with open('compdata.txt', 'r') as datafile:
            data_reader = csv.reader(datafile, delimiter = '\t')
            self.n_samples = sum(1 for i in data_reader)
        
        self.data = np.empty((self.n_samples, self.n_features))
        self.target = np.empty((self.n_samples,), dtype=np.int)
            
        # next, get the samples
        with open('compdata.txt', 'r') as datafile:
            data_reader = csv.reader(datafile, delimiter = '\t')
            
            for i, x in enumerate(data_reader):
                self.data[i] = np.asarray(x, dtype=np.int)

        # get the error codes    
        with open('compdata_true_errors.txt', 'r') as errorfile:
            error_reader = csv.reader(errorfile, delimiter = '\t')

            for i, x in enumerate(error_reader):
                self.target[i] = np.asarray(x, dtype=np.int)
