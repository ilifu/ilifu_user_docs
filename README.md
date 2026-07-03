# Ilifu User Documentation

Welcome to the Ilifu user documentation repository.

All the information that a user may need in order to use the Ilifu systems and services should be included.

## Contributing

If you want to contribute to the documentation, follow the steps below:

1. Fork/clone the repository.
2. Create a branch for your changes.
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

## Conventions

Tag fenced code blocks by intent, so they highlight correctly and get the right copy-button behaviour:

- ` ```bash ` — commands the reader should run. Write them **without** a `$` prompt so the copy button yields a runnable command.
- ` ```console ` — terminal transcripts shown for illustration (prompt **and** output). These get no copy button.
- ` ```text ` — plain output or configuration file contents.
- ` ```python `, ` ```yaml `, ` ```json ` — code or config in that language.

## Checks

Every pull request runs three checks (`.github/workflows/docs.yml`):

- **Internal link check** (blocking) — verifies that every internal link and image resolves the way Docsify would serve it. Run it locally with:

  ```bash
  python3 scripts/check_links.py
  ```

- **Markdown lint** (advisory) — install [markdown linter](https://github.com/markdownlint/markdownlint) and run `mdl -s ./mdl.style docs`. It reports style findings without blocking merges while the pre-existing backlog is worked down; please avoid adding new findings.
- **External link check** (non-blocking) — [lychee](https://github.com/lycheeverse/lychee) checks outbound URLs for link rot.

---

<b id="f1">1</b>: The content of `_sidebar.md` should look similar to this (replace everything in and including <\>): [↩](#a1)

```markdown
- **<Category_title>**
    - [<Name_for_documentation_page_you_wrote>](<location_of_.md>)
    ...
```

Refer to `_sidebar.md` in `docs` for examples.
