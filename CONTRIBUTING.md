## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owner of this repository before making a change.

Please note we have a [code of conduct](https://github.com/NickolaiBeloguzov/robust-json/blob/master/CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a
   build.
2. Update the [README.md](https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md) with details of changes to the interface, this includes new environment
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the [README.md](https://github.com/NickolaiBeloguzov/robust-json/blob/master/README.md) to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off. Do not merge if you have not got any form of approval.

## Submitting changes

1. Fork this repository
2. Checkout to master branch
3. Pull from origin master
4. Branch into master
5. Raise a PR back into master

Please follow **One Issue - One PR** rune whenever possible.

## Coding conventions

- Imports: absolute
- Indentations: 4 spaces
- Encoding: UTF-8
- Formatting: [Black](https://black.readthedocs.io/en/stable/)
- Naming conventions
  - Functions: lower_case_with_underscores (snake_Case)
  - Variables: lower_case_with_underscores (snake_Case)
  - Booleans:
    - Singular: is_enabled (snake_Case)
    - Plural: are_cached (snake_Case)
  - Modules & Packages: lower_case_with_underscores (snake_Case)
  - Classes: CapWords convention (PascalCase)
