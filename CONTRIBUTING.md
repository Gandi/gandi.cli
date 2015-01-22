# Contributing to the Gandi CLi

## Topics

* [Reporting Issues](#reporting-issues)
* [Improving documentation](#improving-documentation)
* [Adding features](#adding-features)
  * [Quickstart](#quickstart)
  * [Code conventions](#code-conventions)
* [Contribution Guidelines](#contribution-guidelines)
  * [Create issues](#create-issues)
  * [Proposing your changes](#proposing-your-changes)
  * [Submission conventions](#submission-conventions)
  * [Tests](#tests)
  * [Documentation](#documentation)


## Reporting issues


A great way to contribute to the project is to send a detailed report when you
encounter an issue. We always appreciate a well-written, thorough bug report,
and will thank you for it!

When reporting [issues](https://github.com/Gandi/gandi.cli/issues) on
GitHub please include your host OS (Ubuntu 12.04, Fedora 19, etc).
Please include:

* The output of `uname -a`.
* The output of `gandi --version`.

Please also include the steps required to reproduce the problem if
possible and applicable.  This information will help us review and fix
your issue faster.


## Improving documentation

Improvements to the Gandi CLI documentation are welcome.

## Adding features

### Quickstart

    <Fork the project on GitHub>
    $ git clone <your fork>
    $ cd gandi.cli
    $ git checkout <name of your feature>
    $ virtualenv .
    $ source bin/activate
    $ pip install .

Make your changes, test them, and submit a PR!

### Code conventions

To add a new command to the CLI:

First, check if there's an existing namespace to either add a command or an option to an already existing one.

Each command is composed of 2 python files, located in the commands/ and modules/ directories:

  * `commands/` contains everything that is related to shell arguments, parameter validation, default values,
  * `modules/` contains code that uses the Gandi API and can be used by other python scripts, or in the python shell,
  * `packages/` contains packaging code (see [packages/README.rst](packages/README.rst))

Code must follow [PEP8 recommendations](http://www.python.org/dev/peps/pep-0008/).

Docstrings should follow [PEP257 recommendations](http://www.python.org/dev/peps/pep-0257/).


## Contribution Guidelines

### Create issues

Any major changes should be documented as [a GitHub issue](https://github.com/Gandi/gandi.cli/issues)
before you start working on it.

### Proposing your changes

Don't hesitate--we appreciate every contribution, no matter how small.

Create a git branch with your new feature or bugfix and either (in order of preference):

* open a Pull Request on GitHub
* mail the patch to feedback@gandi.net,
* send the URL for your branch and we will review/merge it if correct

We'll check your pull requests in the timeliest manner possible. If we can't accept your PR for some reason,
we'll give you feedback and you're encouraged to try again!

### Submission conventions


Fork the repository and make changes on your fork in a feature branch:

- If it's a bug fix branch, name it XXXX-something where XXXX is the number of the
  issue.
- If it's a feature branch, create an enhancement issue to announce your
  intentions, and name it XXXX-something where XXXX is the number of the issue.

#### Tests

Submit unit tests for your changes. Run the full test suite on
your branch before submitting a pull request. #TODO

#### Documentation

Update the documentation when creating or modifying features.
