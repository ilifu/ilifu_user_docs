# Ilifu User Documentation

Welcome to the Ilifu user documentation repository.

All the information that a user may need in order
to use the Ilifu systems and services should be made
available here over time.

## Contributing

If you want to contribute to the documentation, follow the steps below:

1. Fork/clone the repository
2. Create a branch for your changes
3. Navigate to the `docs` directory
4. If you want to make a new category, create a directory with it's name, otherwise create a new file such as `<topic_name_here>.md` under the directory which is most appropriate for it.
   - You can fill this `.md` page with the content of the documentation you want to write.
5. Edit the `_sidebar.md` file and add a relative link to your new document, assuming that the `docs` folder is the root.<sup id="a1">[1](#f1)</sup>
6. Submit your changes back to github and create a pull request from your branch to master for review by the site administrators.

To view the rendered site locally while you are making changes:

```bash
docsify serve ilifu_user_docs/docs
```

By default this serves the pages to [http://localhost:3000](http://localhost:3000) in your web browser.

If you wish to do some code linting you can install [markdown linter](https://github.com/markdownlint/markdownlint). Then run the command `mdl -s ./mdl.style docs` to check you code.

```console
$ mdl -s ./mdl.style docs
docs/_coverpage.md:1: MD041 First line in file should be a top level header
docs/_sidebar.md:2: MD007 Unordered list indentation
docs/_sidebar.md:1: MD041 First line in file should be a top level header
docs/about/what_is.md:1: MD002 First header should be a top level header
docs/about/what_is.md:1: MD026 Trailing punctuation in header
docs/about/what_is.md:12: MD026 Trailing punctuation in header
docs/about/what_is.md:1: MD041 First line in file should be a top level header
docs/cluster/running_jobs.md:15: MD009 Trailing spaces
docs/cluster/running_jobs.md:24: MD009 Trailing spaces
docs/cluster/running_jobs.md:33: MD009 Trailing spaces
docs/cluster/running_jobs.md:49: MD009 Trailing spaces
docs/cluster/running_jobs.md:52: MD009 Trailing spaces
docs/cluster/running_jobs.md:54: MD009 Trailing spaces
docs/cluster/running_jobs.md:66: MD009 Trailing spaces
docs/cluster/running_jobs.md:71: MD009 Trailing spaces
docs/cluster/running_jobs.md:75: MD009 Trailing spaces
docs/cluster/running_jobs.md:79: MD009 Trailing spaces
docs/cluster/running_jobs.md:87: MD009 Trailing spaces
...
```

---

<b id="f1">1</b>: The content of `_sidebar.md` should look similar to this (replace everything in and including <\>): [↩](#a1)

```markdown
- **<Category_title>**
    - [<Name_for_documentation_page_you_wrote>](<location_of_.md>)
    ...
```

Refer to `_sidebar.md` in `docs` for examples.
