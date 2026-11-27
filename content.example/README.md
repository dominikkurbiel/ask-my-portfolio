# Sample content

Fictional content used by tests, CI and anyone running the project locally. The real portfolio
content lives in `content/`, which is git-ignored and deployed to the server separately.

To use your own: copy this folder to `content/` and edit the markdown files, or point `CONTENT_DIR`
at another folder.

How to write content that the assistant can search well:

- Use headings for structure. Each section is indexed with its heading path
  (`CV › Work experience › Senior Engineer — Acme › Billing service`), so one topic per section.
- Keep facts specific: technologies, what you built, results with numbers.
- Write in the third person (the assistant talks about you).
- Never include phone numbers, e-mail or home address. Anything here can be quoted to anyone.
- HTML comments (`<!-- ... -->`) are ignored by the indexer: use them for private notes.
