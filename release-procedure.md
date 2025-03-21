*   Tag commit

        git tag -a x.x.x -m 'Version x.x.x'

*   and push to github

        git push origin master --tags

*  Verify the version number is correct

        pixi r get_version
        0.1.22

        # if it contains .dev, you can always override before building with:
        export SETUPTOOLS_SCM_PRETEND_VERSION=0.1.21

*  Upload to PyPI

        rm -rf dist/
        pixi r build
        twine upload dist/*