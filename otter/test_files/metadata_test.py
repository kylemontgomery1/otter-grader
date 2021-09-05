"""Support for notebook metadata test files"""

import base64
import doctest
import io
import json
import os
import pathlib
import dill
import warnings

from contextlib import redirect_stderr, redirect_stdout
from textwrap import dedent

from .abstract_test import TestCase
from .exception_test import ExceptionTestFile
from .ok_test import OKTestFile


NOTEBOOK_METADATA_KEY = "otter"


class NotebookMetadataExceptionTestFile(ExceptionTestFile):
    """
    A single notebook metadata test file for Otter.

    Tests are defined in the metadata of a jupyter notebook as a JSON object with the ``otter`` key.
    The tests themselves are assumed to be base-64-encoded compiled ``code`` objects from test files.

    .. code-block:: json

    {
        "metadata": {
            "otter": {
                "tests": {
                    "q1": ""
                }
            }
        }
    }

    Args:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``, optional): the point value of this test, defaults to 1
        all_or_nothing (``bool``, optional): whether the test should be graded all-or-nothing across
            cases

    Attributes:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``): the point value of this test, defaults to 1
        all_or_nothing (``bool``): whether the test should be graded all-or-nothing across
            cases
        passed_all (``bool``): whether all of the test cases were passed
        test_case_results (``list`` of ``TestCaseResult``): a list of results for the test cases in
            ``test_cases``
        grade (``float``): the percentage of ``points`` earned for this test file as a decimal
    """

    @staticmethod
    def encode_test_file(path):
        """
        Compile a test file and return the compiled code as a base-64-encoded string.

        Args:
            path (``str``): the path to the test file

        Returns:
            ``str``: the compiled code encoded in base-64
        """
        code = ExceptionTestFile.compile_test_file(path)
        return base64.b64encode(dill.dumps(code)).decode("utf-8")

    @staticmethod
    def encode_string(s, path="<string>"):
        """
        Compile a string and return the compiled code as a base-64-encoded string.

        Args:
            s (``str``): the string to compile
            path (``str``, optional): the path to the test file

        Returns:
            ``str``: the compiled code encoded in base-64
        """
        code = ExceptionTestFile.compile_string(s, path=path)
        return base64.b64encode(dill.dumps(code)).decode("utf-8")

    @staticmethod
    def decode_test_file(code):
        """
        Decode and unpickle the compiled code from a base-64-encoded string.

        Args:
            code (``str``): the compiled code encoded in base-64

        Returns:
            ``code``: the compiled code from the test file
        """
        return dill.loads(base64.b64decode(code.encode("utf-8")))

    @classmethod
    def from_file(cls, path, test_name):
        """
        Parse an exception-based test from a Jupyter notebook's metadata and return an 
        ``ExceptionTestFile``.

        Args:
            path (``str``): the path to the notebook
            test_name (``str``): the name of the test to extract from the metadata

        Returns:
            ``ExceptionTestFile``: the new ``ExceptionTestFile`` object created from the given file
        """
        with open(path) as f:
            nb = json.load(f)
        
        test_spec = nb["metadata"][NOTEBOOK_METADATA_KEY]["tests"]
        if test_name not in test_spec:
            raise ValueError(f"Test {test_name} not found")
        
        test_spec = test_spec[test_name]
        test_code = cls.decode_test_file(test_spec)

        return cls.from_spec(test_code, path=path)


class NotebookMetadataOKTestFile(OKTestFile):
    """
    A single notebook metadata test file for Otter.

    Tests are defined in the metadata of a jupyter notebook as a JSON object with the ``otter`` key.
    The tests themselves are OK-formatted.

    .. code-block:: json

    {
        "metadata": {
            "otter": {
                "tests": {
                    "q1": {}
                }
            }
        }
    }

    Args:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``, optional): the point value of this test, defaults to 1
        all_or_nothing (``bool``, optional): whether the test should be graded all-or-nothing across
            cases

    Attributes:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``): the point value of this test, defaults to 1
        all_or_nothing (``bool``): whether the test should be graded all-or-nothing across
            cases
        passed_all (``bool``): whether all of the test cases were passed
        test_case_results (``list`` of ``TestCaseResult``): a list of results for the test cases in
            ``test_cases``
        grade (``float``): the percentage of ``points`` earned for this test file as a decimal
    """

    @classmethod
    def from_file(cls, path, test_name):
        """
        Parse an OK-formatted test from a Jupyter notebook's metadata and return an ``OKTestFile``.

        Args:
            path (``str``): the path to the notebook
            test_name (``str``): the name of the test to extract from the metadata

        Returns:
            ``OKTestFile``: the new ``OKTestFile`` object created from the given file
        """
        with open(path) as f:
            nb = json.load(f)
        
        test_spec = nb["metadata"][NOTEBOOK_METADATA_KEY]["tests"]
        if test_name not in test_spec:
            raise ValueError(f"Test {test_name} not found")
        
        test_spec = test_spec[test_name]

        return cls.from_spec(test_spec, path=path)
