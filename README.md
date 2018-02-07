# https://styleguide.adhoc.team/ - the Ad Hoc Style guide

## Introduction 0️⃣

[`https://styleguide.adhoc.team/`](https://styleguide.adhoc.team/) is a
[Jekyll](https://jekyllrb.com/) site.

## Installation 📦

1. **Install Ruby.** The website is a Jekyll site. Jekyll requires
Ruby, version 2.0 or newer.

1. **Install bundler.** Do: `gem install bundler`

1. **Checkout the source.** Do: `git checkout
git@github.com:adhocteam/styleguide.git`

1. **Install Jekyll and its dependencies.** Do: `cd
styleguide && bundle install`

## Rebuilding the site locally 🔨

1. **Run Jekyll**. Do: `bundle exec jekyll build`. The generated site
will be in the `_site` directory. You can browse that directory using
something like `python -m SimpleHTTPServer` and going to
`http://localhost:8000/`, or you can do `bundle exec jekyll serve`
instead of `build` and go to `http://localhost:4000/`. This will keep
a persistent process around and rebuild the site when source files
change, too.

## Publishing the site 📤

The workflow for publishing the site is: commit changes to the source
code with git, create a pull request on the GitHub project, get it
reviewed and merged, and then the Codeship CI service will run Jekyll
and push the artifact to an AWS S3 bucket in Ad Hoc’s account. On the
VM instance where the site is served, the content is synced from the
S3 bucket every few minutes, and served with nginx.

1. **Create a new git branch for the changes.** Do: `git checkout -b
your-branch-name`

1. **Make your changes.** Add the blog post, edit a page, change an
image, etc.

1. **Rebuild the site locally and review.**

1. **Commit your changes with git.** Do: `git commit -a -m “useful
commit message here”`

1. **Push your changes to GitHub and open a pull request.** Do: `git
push origin your-branch-name`

1. **Assign another Ad Hoc team member to review your pull request.**

1. **Merge the pull request.** You might need to ask someone with
permission to do that.

1. **Refresh `styleguide.adhoc.team` to confirm your change.** It may take 5
minutes for the change to sync.

You’re done! 😃

## Optimizing the svgs

* Install svgo: `npm install -g svgo`
* Optimize all svgs in the repo: `svgo **/*.svg`
