#!/usr/bin/env python
from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------


class QiitaError(Exception):
    """Base clase for all Qiita exceptions"""
    pass


class IncompetentQiitaDeveloperError(QiitaError):
    """Exception for developer errors"""
    pass


class QiitaSearchError(QiitaError):
    """Exception for errors when using search objects"""
    pass


class QiitaUserError(QiitaError):
    """Exception for error when handling with user objects"""
    pass


class QiitaAnalysisError(QiitaError):
    """Exception for error when handling with analysis objects"""
    pass


class QiitaJobError(QiitaError):
    """Exception for error when handling with job objects"""
    pass


class QiitaStudyError(QiitaError):
    """Exception for error when handling with study objects"""
    pass


class IncorrectPasswordError(QiitaError):
    """User passes wrong password"""
    pass


class IncorrectEmailError(QiitaError):
    """Email fails validation"""
    pass


class QiitaEnvironmentError(QiitaError):
    """Exception for error when dealing with the environment"""
    pass
