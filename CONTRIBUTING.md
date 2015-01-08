# Contributing to the Gandi CLi

## Topics

* [Reporting Issues](#reporting-issues)
* [Improving documentation](#improving-documentation)
* [Adding features](#adding-features)
* [Contribution Guidelines](#contribution-guidelines)
* [Community Guidelines](#docker-community-guidelines)


## Reporting issues


A great way to contribute to the project is to send a detailed report when you
encounter an issue. We always appreciate a well-written, thorough bug report,
and will thank you for it!

When reporting [issues](https://github.com/docker/docker/issues) on
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

## Contribution Guidelines

### Pull requests are always welcome

Don't hesitate--we appreciate every contribution, no matter how small.

We'll check out your pull requests in the timeliest manner possible. If we can't accept your PR for some reason, we'll give you feedback and you're encouraged to try again!

### Create issues

Any major changes should be documented as [a GitHub issue](https://github.com/Gandi/gandi.cli/issues) before you start working on it.

### Conventions


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


## Community Guidelines


