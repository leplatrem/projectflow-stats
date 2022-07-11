import json
import sys
from collections import Counter


def makefile_sections(content):
	for line in content.splitlines():
		if line.startswith("\t"):
			continue
		if line.startswith("#") or line.startswith("$"):
			continue
		if ":=" in line:
			continue
		if "PHONY" in line:
			continue
		if ":" in line:
			yield line.split(":")[0]


def readme_sections(content):
	for line in content.splitlines():
		if line.startswith("#"):
			yield line.replace("#", "")


def stats_readme(repos):
	count_titles = Counter()
	for repo in repos:
		readme = repo["readme"]
		if not readme:
			continue
		for section in readme_sections(readme):
			count_titles[section] += 1
	return count_titles


def stats_makefile(repos):
	count_sections = Counter()
	for repo in repos:
		makefile = repo["makefile"]
		if not makefile:
			continue
		for section in makefile_sections(makefile):
			count_sections[section] += 1
	return count_sections


def stats_filename(repos, word):
	count_format = Counter()
	for repo in repos:
		for folder, files in repo["files"].items():
			for f in files:
				if word in f.lower():
					count_format[folder[1:] + "/" + f] += 1
	return count_format


if __name__ == "__main__":
	repos = []
	for f in sys.argv[1:]:
		with open(f) as fd:
			repos += json.load(fd)

	print(len(repos), "repositories.")

	print("== README", "=" * 40)
	for c, v in stats_filename(repos, "readme").most_common(20):
		if v < 2:
			continue
		print(f"{c:<18}", v)
	print()

	print("== CHANGELOG", "=" * 40)
	for c, v in stats_filename(repos, "change").most_common(20):
		if v < 2:
			continue
		print(f"{c:<18}", v)
	print()

	print("== Makefile", "=" * 40)
	for c, v in stats_makefile(repos).most_common(20):
		if v < 2:
			continue
		print(f"{c:<18}", v)
	print()

	print("== Readme Sections", "=" * 40)
	for c, v in stats_readme(repos).most_common(20):
		if v < 2:
			continue
		print(f"{c:<18}", v)
	print()
