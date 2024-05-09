import inspect
import os
from pathlib import Path
import sys

from invoke import task

"""
TODO: Add create netkan file from GitHub link
"""


HERE = Path(__file__).parent
NETKAN_DIR = HERE / "NetKAN"
CKAN_DIR = HERE / ".." / "ksp-personal-ckan-meta"
NETKAN_EXE = "netkan.exe"

NETKAN_DIR = NETKAN_DIR.resolve()
CKAN_DIR = CKAN_DIR.resolve()


@task(
    help={
        "github_token": "GitHub API token. Also looks for '.gh-token.txt' file in root directory.",
        "continue_from": "Only generate for projects named after this.",
    }
)
def make_ckan(ctx, github_token=None, continue_from=None):
    """Turn netkan files into (useable) ckan files!"""
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
        try:
            with open(HERE / ".gh-token.txt", "r") as fn:
                GITHUB_TOKEN_STR = fn.read().strip()
                print(
                    f"GITHUB_TOKEN_STR={GITHUB_TOKEN_STR[:3]}[...]{GITHUB_TOKEN_STR[-3:]}"
                )
        except FileNotFoundError:
            GITHUB_TOKEN_STR = ""
            print("No GitHub API token")

    for dirpath, dirnames, filenames in os.walk(NETKAN_DIR):
        # print(dirpath, dirnames, filenames)
        for fn in filenames:
            fn = Path(fn)

            if continue_from and fn.stem < continue_from:
                print(f"    {fn!s} -- skipping!")
                continue

            print()
            print(f"    {fn!s}")
            output_dir = CKAN_DIR / fn.stem
            output_dir.mkdir(exist_ok=True)

            ctx.run(
                f"{NETKAN_EXE} --outputdir {output_dir} --verbose{GITHUB_TOKEN_STR} {NETKAN_DIR / fn}"
            )
    print()
    print("**end**")
    print()
    print("Make sure to push an update to the metadata repo!")


@task
def apply_patches(ctx):
    """Turn patch files into netkan files."""
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
    print()
    print("Make sure to remove the applied patches!")

def input_list(intro="", msg=""):
    """Use input to get multiple items, and return the list."""
    if intro:
        print(intro)

    my_list = []
    while True:
        my_item = input(msg)
        if my_item == "":
            return my_list
        else:
            my_list.append(my_item)

@task
def from_github(ctx, repo=None):
    """Create a .netkan file for a GitHub repo."""

    if repo is None:
        repo = input("GitHub repo? ")

    repo = repo.replace("https://", "")
    repo = repo.replace("github.com/", "")
    repo = repo.rstrip("/")

    print(f'    repo is "{repo}"')

    repo_name = repo.rpartition("/")[-1]

    identifier = input(f"Identifier? [{repo_name}] ")
    if identifier == "":
        identifier = repo_name

    my_license = input("License? ")

    tags = input_list("Tags (enter blank item to end)", " ? ")
    depends = input_list("depends (on what other packages) (enter blank item to end)", " ? ")
    suggests = input_list("suggests (what other packages) (enter blank item to end)", " ? ")
    supports = input_list("supports (what other packages) (enter blank item to end)", " ? ")
    conflicts = input_list("conflicts (with what other packages) (enter blank item to end)", " ? ")
    install_find = input(f"install folder [{repo_name}] ? ")
    if install_find == "":
        install_find = repo_name
    install_to = input("install to: GameData/[] ? ")
    if install_to:
        install_to = "/" + install_to
    source_archive = input("Use Github source archive? [Y/n] ")
    if source_archive in ["n", "no", "N", "No", "NO"]:
        source_archive = False
    else:
        source_archive = True

    my_filename = (NETKAN_DIR / identifier).with_suffix(".netkan")
    with open(my_filename, "w") as fn:
        fn.write(inspect.cleandoc(
            f"""
            spec_version: v1.18
            identifier: {identifier}
            $kref: "#/ckan/github/{repo}"
            license: {my_license}
            $vref: "#/ckan/ksp-avc"
            """
        ))
        fn.write("\n")
        if tags:
            fn.write("tags:\n")
            for tag in tags:
                fn.write(f"  - {tag}\n")
        if depends:
            fn.write("depends:\n")
            for depend in depends:
                fn.write(f"  - name: {depend}\n")
        if suggests:
            fn.write("suggests:\n")
            for suggest in suggests:
                fn.write(f"  - name: {suggest}\n")
        if supports:
            fn.write("supports:\n")
            for support in supports:
                fn.write(f"  - name: {support}\n")
        if conflicts:
            fn.write("conflicts:\n")
            for conflict in conflicts:
                fn.write(f"  - name: {conflict}\n")
        fn.write(inspect.cleandoc(
            f"""
            install:
              - find: {install_find}
                install_to: GameData{install_to}
            """
        ))
        fn.write("\n")
        if source_archive:
            fn.write(inspect.cleandoc(
                """
                x_netkan_github:
                  use_source_archive: true
                """
            ))
            fn.write("\n")
        fn.write("x_via: MinchinWeb's GitHub to NetKan")
        fn.write("\n")

    print()
    print(f'** Written to "{my_filename}". Please confirm details!')
