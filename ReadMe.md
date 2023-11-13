
# Personal NetKan Repo

This is a collection of netkan files, for Kerbal Space Program mods that never
got added to the main netkan repo for whatever reason.

See <https://github.com/MinchinWeb/ksp-personal-ckan-meta> on how to make use
of this information in CKAN.


## Steps Start with a Pull Request

1. Find the pull request. Note the URL. E.g.
   `https://github.com/KSP-CKAN/NetKAN/pull/9112`
2. Add `.patch` at the end of the URL. E.g.
   `https://github.com/KSP-CKAN/NetKAN/pull/9112.patch`
3. Download the patch file.
4. Apply the patch file with git: `git am 9112.patch`

Alternately, place patch files in the root directory of the repo and run
`invoke apply-patches`.

## Converting these to `.ckan` files

1. Download `netkan.exe` from
[here](https://ksp-ckan.s3-us-west-2.amazonaws.com/netkan.exe) (link originally
from [here](https://github.com/KSP-CKAN/CKAN/wiki/Adding-a-mod-to-the-CKAN)).
2. `netkan.exe <identifier>.netkan`

## Semi-Automated Conversion to `.ckan` files

`invoke make-ckan`

(Relies on Python and `invoke` (installable via `pip`))

Assumes that the metadata has been installed into the same root folder as this
repo.

### GitHub Access Token

from here --> <https://github.com/settings/tokens>
