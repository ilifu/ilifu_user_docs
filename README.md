Ilifu User Documentation
========================

Welcome to the Ilifu user documentation repository.

All the information that a user may need in order
to use the Ilifu systems and services should be made
available here over time.

## Contributing

If you want to contribute to the documentation, follow the steps below:
1. Fork the repository
2. Navigate to the `docs` directory
3. If you want to make a new category, create a directory with it's name, otherwise create a new file such as `<topic_name_here>.md` under the directory which is most appropriate for it.
    - You can fill this `.md` page with the content of the documentation you want to write.
4. Edit the `_sidebar.md` file and add a relative link to your new document, assuming that the `docs` folder is the root.<sup id="a1">[1](#f1)</sup>

---

<b id="f1">1</b>: The content of `_sidebar.md` should look similar to this (replace everything in and including <\>): [↩](#a1)
```markdown
- **<Category_title>**
    - [<Name_for_documentation_page_you_wrote>](<location_of_.md>)
    ... 
```
Refer to `_sidebar.md` in `docs` for examples.
