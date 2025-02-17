.. _workflow_executing_submissions_otter_grade:

Grading Locally
===============

The command line interface allows instructors to grade notebooks locally by launching Docker 
containers on the instructor's machine that grade notebooks and return a CSV of grades and 
(optionally) PDF versions of student submissions for manually graded questions.


Configuration Files
-------------------

Otter grades students submissions in individual Docker containers that are based on a Docker image 
generated through the use of a configuration zip file. Before grading assignments locally, an 
instructor should create such a zip file by using a tool such as :ref:`Otter Assign 
<otter_assign>` or :ref:`Otter Generate <workflow_otter_generate>`. This file will be 
used in the construction of a Docker image tagged ``otter-grader:{zip file hash}``. This Docker 
image will then have containers spawned from it for each submission that is graded.

Otter's Docker images can be pruned with ``otter grade --prune``.


Using the CLI
-------------

Before using the command line utility, you should have

* written tests for the assignment, 
* generated a configuration zip file from those tests, and
* downloaded submissions into a directory

The grading interface, encapsulated in the ``otter grade`` command, runs the local grading process 
and defines the options that instructors can set when grading. A comprehensive list of flags is 
provided in the :ref:`cli_reference`.


Basic Usage
+++++++++++

The simplest usage of the Otter Grade is when we have a directory structure as below (and we have 
change directories into ``grading`` in the command line) and we don't require PDFs or additional 
requirements.

.. code-block::

    grading
    ├── autograder.zip
    ├── nb0.ipynb
    ├── nb1.ipynb
    ├── nb2.ipynb  # etc.
    └── tests
        ├── q1.py
        ├── q2.py
        └── q3.py  # etc.

In the case above, our otter command would be, very simply,

.. code-block:: console

    otter grade

Because the submissions are on the current working directory (``grading``), our configuration file 
is at ``./autograder.zip``, and we don't mind output to ``./``, we can use the defualt values of the 
``-a`` and ``-o`` flags.

After grader, our directory will look like this:

.. code-block::

    grading
    ├── autograder.zip
    ├── final_grades.csv
    ├── nb0.ipynb
    ├── nb1.ipynb
    ├── nb2.ipynb  # etc.
    └── tests
        ├── q1.py
        ├── q2.py
        └── q3.py  # etc.

and the grades for each submission will be in ``final_grades.csv``.

If we wanted to generate PDFs for manual grading, we would specify this when making the 
configuration file and add the ``--pdfs`` flag to tell Otter to copy the PDFs out of the containers: 

.. code-block::

    otter grade --pdfs

and at the end of grading we would have

.. code-block::

    grading
    ├── autograder.zip
    ├── final_grades.csv
    ├── nb0.ipynb
    ├── nb1.ipynb
    ├── nb2.ipynb    # etc.
    ├── submission_pdfs
    │   ├── nb0.pdf
    │   ├── nb1.pdf
    │   └── nb2.pdf  # etc.
    └── tests
        ├── q1.py
        ├── q2.py
        └── q3.py    # etc.

To grade submissions that aren't notebook files, use the ``--ext`` flag, which accepts the file 
extension to search for submissions with. For example, if we had the same example as above but with 
Rmd files:

.. code-block:: console

    otter grade --ext Rmd

If you're grading submission export zip files (those generated by ``otter.Notebook.export`` or 
``ottr::export``), your ``otter_config.json`` should have its ``zips`` key set to true, and you
should pass the ``-z`` flag to Otter Grade. You also won't need to use the ``--ext`` flag regardless
of the type of file being graded inside the zip file.


Requirements
++++++++++++

The Docker image used for grading will be built as described in the :ref:`Otter Generatte 
<workflow_otter_generate_container_image>` section. If you require any packages not listed there, 
or among the dependencies of any packages above, you should create a requirements.txt file 
*containing only those packages* and use it when running your configuration generator. 


Support Files
+++++++++++++

Some notebooks require support files to run (e.g. data files). If your notebooks require any such 
files, you should generate your configuration zip file with those files.


Intercell Seeding
+++++++++++++++++

Otter Grade also supports :ref:`intercell seeding <seeding>`. This behavior should be 
configured as a part of your configuration zip file.
