#!/bin/bash

## This Script is meant to create or initialize a PostgreSQL database for use
## with the FoodMunch web scrapers. It will allow the database to store
## information about food recipes for easy retrieval.


FOOD_DB_SETUP_VER="0.1.0"



function print_usage() {
    local err_code=${1-0}

    echo "Usage: postgres_setup.bash"
    echo
    echo "Options:"
    echo
    
    exit $err_code
}



function postgres_setup() {
    if [[ -z $@ ]]; then
        print_usage 1
    fi
    
    while [ ! -z "$1" ]; do
        case "$1" in
            -h|--help)
                print_usage 0
                ;;
            *)
                print_usage 1
                ;;

        esac
        shift
    done
}



postgres_setup $@

