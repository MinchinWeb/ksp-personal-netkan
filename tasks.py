from invoke import task
from pathlib import Path
import os

"""
TODO: Add pickup of GIthub token from file
TODO: Add create netkan file from GitHub link
"""


HERE = Path(__file__).parent
NETKAN_DIR = HERE / 'NetKAN'
CKAN_DIR = HERE / '..' / 'ksp-personal-ckan-meta'
NETKAN_EXE = "netkan.exe"

NETKAN_DIR = NETKAN_DIR.resolve()
CKAN_DIR = CKAN_DIR.resolve()


@task(help={
    "github_token": "GitHub API token",
    "continue_from": "Only generate for projects named after this."
}
)
def make_ckan(ctx, github_token=None, continue_from=None):
    print("**starting**")
    # print(HERE)
    print(f"{NETKAN_DIR=!s}", end=" ")
    if NETKAN_DIR.exists():
        print("(ok)")
    else:
        print("(missing)")
    print(f"{CKAN_DIR=!s}", end=" ")
    if CKAN_DIR.exists():
        print("(ok)")
    else:
        print("(missing)")

    if github_token:
        GITHUB_TOKEN_STR = f" --github-token {github_token}"
    else:
        GITHUB_TOKEN_STR = ""

    for dirpath, dirnames, filenames in os.walk(NETKAN_DIR):
        # print(dirpath, dirnames, filenames)
        for fn in filenames:
            fn = Path(fn)
            print()
            print(f"    {fn!s}")

            if continue_from and fn.stem < continue_from:
                print("        skipping!")
                continue

            output_dir = CKAN_DIR / fn.stem
            output_dir.mkdir(exist_ok=True)

            ctx.run(f"{NETKAN_EXE} --outputdir {output_dir} --verbose{GITHUB_TOKEN_STR} {NETKAN_DIR / fn}")
    print("")
    print("**end**")
    print("")
    print("Make sure to push an update to the metadata repo!")

@task
def apply_patches(ctx):
    print("**starting**")
    print(f"{HERE.resolve()=!s}")
    for dirpath, dirnames, filenames in HERE.resolve().walk():
        for fn in filenames:
            fn = Path(fn)
            if fn.suffix == ".patch":
                print()
                print(f"    {fn!s}")
                
                ctx.run(f"git am {fn}")
    print("**end**")
    print("")
    print("Make sure to remove the applied patches!")
