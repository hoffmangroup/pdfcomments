# Contributing to pdfcomments

Thank you for taking the time to contribute!

The following is a set of guidelines for contributing to pdfcomments.
These are mostly guidelines, not rules.
Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [michael.hoffman@utoronto.ca](mailto:michael.hoffman@utoronto.ca).

## How can I contribute?

### Reporting bugs

#### How do I submit a good bug report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. When listing steps, don't just say what you did, but explain how you did it.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**

### Suggesting enhancements

#### How do I submit a good enhancement suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most pdfcomments users.

### Pull Requests

We suggest discussing potential pull requests as separate bug reports or enhancement suggestions first.

The process described here has several goals:

- Maintain pdfcomment's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible pdfcomments
- Enable a sustainable system for pdfcomment's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow the style guide
2. After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing <details><summary>What if the status checks are failing?</summary>If a status check is failing, and you believe that the failure is unrelated to your change, please leave a comment on the pull request explaining why you believe the failure is unrelated. A maintainer will re-run the status check for you. If we conclude that the failure was a false positive, then we will open an issue to track that problem with our status check suite.</details>

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewers may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

* Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#summary)
  - Use one of the following commit types (from the [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit):
    - build: Changes that affect the build system or external dependencies
    - ci: Changes to continuous integration configuration files and scripts
    - docs: Documentation-only changes
    - feat: New feature
    - fix: Bug fix
    - perf: Code change that improves performance
    - refactor: Code change that neither fixes a bug nor adds a feature
    - style: Changes that do not affect the meaning of the code (whitespace, formatting, missing semicolons)
    - test: Adding missing tests or correcting existing tests
* Use the present tense (“add feature” not “added feature”)
* Use the imperative mood (“move cursor to…” not “moves cursor to…”)
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python

- Follow PEP 8.
- Code should pass `flake8` checks with default checkers, the `pep8-naming` checker, and `--max-complexity 10` (or less).
- Docstrings should pass the `flake8-docstrings` checker. Note: at present, many functions should either be marked as internal (by adding `_` to the beginning) or have docstrings added, or both.
- See [Long Names Are Long](http://journal.stuffwithstuff.com/2016/06/16/long-names-are-long/) for guidance on how to ensure names are clear and precise
- For command-line interface, follow the [Hoffman Lab application command-line user-interface checklist](https://docs.google.com/document/d/1xJSXHjkgcl77K_-d14YpC5xqY3epQwDYCS_eEYgq6dg)

### Documentation Styleguide

* Use [Markdown](https://daringfireball.net/projects/markdown).
* Where possible use one source line per sentence for better diffs

## Acknowledgments 

Much of these contributing guidelines were modified from the Atom [CONTRIBUTING.md](https://github.com/atom/atom/blob/master/CONTRIBUTING.md), available under a MIT License.
