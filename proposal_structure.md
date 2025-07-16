# Vocabularies Repo Structure Proposal

First thing to know: moving vocabularies to their own repo is a _breaking_ change that is independent of how this repo itself is structured.
Due to how github pages works, these will be published under https://cfconventions.org/vocabularies/ and cannot be under https://cfconventions.org/Data.
This gives an opportunity to clean some things up and make them more consistent across the lists.

## What is Published
Github pages do not need to be published from the root (/) of the project.
I opted to put everything that is published under /docs since that was a built in default in github itself.
So in this repo, /docs/index.html would be available under https://cfconventions.org/vocabularies/index.html
Notice that "docs" does not appear in the URL.

This choice allows for ancillary files (scripts, github/CI configs, etc..) to exist external to what is published on the website.

## Structure Overview
I decided to split each list into a "current" and "version" directory.
The current directory would have static copies of the xml, and an index.html that contains statically build version of the html.
The version directory has subdirectories that are numbered.

I picked "version" instead of "versions" because it allows for a more naturally sounding URL e.g.: 
https://cfconventions.org/vocabularies/cf-standard-names/version/87/cf-standard-name-table.xml

The standardized region list was converted to this structure.

## Stylesheets
All browsers support rendering XML with XML stylesheets, no static static html rendering will be kept for versions, only the current (more in Updating section)
All the XML files have been updated to reference a static path to their stylesheets.

I have removed the javascript drop down in favor of details/summary elements (except for the standard name table).
These natively support the triangle icons in all browsers and natively implement the click to show definitions functionality.

I have added a "download" link to all the stylesheets, that extracts the rendered DOM and provides it to the user.

Any processing that was being done via a python script or shell command should be moved to the stylesheet and the javascript within it.
(I may have missed some)

# Update Process
For all the "versioned" files:
* Make a new numeric directory
* Add only the updated XML to that directory (make sure it has the stylesheet reference)
* Commit this to github to the new site builds
* Go to the built site and find the XML, the browser will render this as HTML using the stylesheet
* Use the download link to get the static HTML version (this download has its download link stripped)
* Renamed that downloaded file as index.html and replace the index.html correct "current" directory, also replace the xml file with the current xml.
* Commit and publish

Maybe:
* Make a "release" on github with a good tag indicating what has been updated. This will tie a version of the site/files with an exact git commit.

For other documents (e.g. the docs dir):
* Standard PR/CF update process