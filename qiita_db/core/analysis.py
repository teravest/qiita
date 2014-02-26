"""
Objects for dealing with Qiita analyses

This module provides the base object for dealing with Qiita Analysis.
It standardizes the Analysis interface and all the different Qiita-db
backends should inherit from it in order to implement the analysis object.

The subclasses implementing this object should not provide any extra
public function in order to maintain back-end independence.

Classes
-------
- `QiitaAnalysis` -- A Qiita Analysis class
"""
__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Qiita Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from .base_object import QiitaObject
from .exceptions import QiitaDBNotImplementedError


class QiitaAnalysis(QiitaObject):
    """
    Base analysis object to access to the Qiita Analysis information

    Standardizes the QiitaAnalysis interface for all the back-ends.

    Parameters
    ----------
    id:
        The analysis identifier

    Attributes
    ----------
    biom_table
    jobs
    status
    info

    Methods
    -------
    add_jobs(jobs)
        Adds a list of jobs to the analysis

    remove_jobs(jobs)
        Removes a list of jobs from the analysis

    """

    @property
    def biom_table(self):
        """The biom table of the analysis"""
        raise QiitaDBNotImplementedError()

    @property
    def jobs(self):
        """A list of jobs included in the analysis"""
        raise QiitaDBNotImplementedError()

    @jobs.setter
    def jobs(self, jobs):
        """Sets the initial list of jobs to the analysis

        Raises
        ------
        QiitaDBOperationNotPermitedError
            If the analysis already has jobs attached to it
        """
        raise QiitaDBNotImplementedError()

    @property
    def status(self):
        """String with the current status of the analysis"""
        raise QiitaDBNotImplementedError()

    @status.setter
    def status(self, status):
        """Change the status of the analysis"""
        raise QiitaDBNotImplementedError()

    @property
    def info(self):
        """Dict with any other information attached to the analysis"""
        raise QiitaDBNotImplementedError()

    @info.setter
    def info(self, info):
        """Updates the information attached to the analysis

        Parameters
        ----------
            info : dict
        """
        raise QiitaDBNotImplementedError()

    def add_jobs(self, jobs):
        """Adds a list of jobs to the analysis

        Parameters
        ----------
            jobs : list of QiitaJob
        """
        raise QiitaDBNotImplementedError()

    def remove_jobs(self, jobs):
        """Removes a list of jobs from the analysis

        Parameters
        ----------
            jobs : list of QiitaJob
        """
        raise QiitaDBNotImplementedError()
