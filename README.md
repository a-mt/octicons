# Octicons webfont

## Retrieve latest SVG

    # Retrieve SVGs
    mkdir tmp
    cd tmp

    npm install octicons

    # Check the version you got
    cd node_modules/octicons/package.json | grep version

    # Get the SVG files
    rm -rf ../run/svg
    cp -r node_modules/octicons/build/svg ../run/svg

    cd ..

## Install dependencies

    sudo apt-get install python-fontforge
    pip2 install templite

## Build SVG webfont containing all SVG files

    /usr/bin/python run > octicons.css