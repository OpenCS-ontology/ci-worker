import argparse
import os
import yaml
from github import Github
from time import gmtime, strftime

parser = argparse.ArgumentParser(description='Creating files for ontology page')

parser.add_argument('current_release', type=str)
parser.add_argument('repository_name', type=str)
parser.add_argument('output_path', type=str)


def get_releases(repository_name, token):
    G = Github(token)
    repo = G.get_repo(repository_name)
    res = repo.get_releases()
    releases = [r.tag_name[1:] if r.tag_name[0] == 'v' else r.tag_name for r in res]
    return releases


def save_page(yaml_dict, path):
    with open(path, 'w+') as file:
        content = f'---\n{yaml.dump(yaml_dict)}---\n'
        file.write(content)


def main(current_release, repository_name, output_path, token):
    releases = get_releases(repository_name, token)

    if current_release != 'dev':
        version_list_dict = {
            'layout': 'version_list',
            'versions': releases,
            'latest_stable': current_release
        }
        page_dict = {
            'layout': 'page',
            'date': strftime('%d-%m-%Y', gmtime()),
            'version': current_release,
        }
        curr_ver_idx = releases.index(current_release)
        if curr_ver_idx + 1 < len(releases):
            page_dict['previous_version'] = releases[curr_ver_idx + 1]

        save_page(version_list_dict, os.path.join(os.path.join(output_path, 'versions.md')))

    else:
        page_dict = {
            'layout': 'page',
            'date': strftime('%d-%m-%Y', gmtime()),
            'version': 'dev',
            'previous_version': releases[0]
        }

    save_page(page_dict, os.path.join(os.path.join(output_path, 'page.md')))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args.current_release, args.repository_name, args.output_path, os.environ['GITHUB_TOKEN'])
