#!/bin/bash

## This Script is meant to create or initialize a PostgreSQL database for use
## with the FoodMunch web scrapers. It will allow the database to store
## information about food recipes for easy retrieval.


FOOD_DB_SETUP_VER="0.1.0"



function create_user() {
    local userToMake="$1"
    echo "Creating user and group ${userToMake}:${userToMake}"
}



function print_usage() {
    local err_code=${1-0}

    echo "Usage: postgres_setup.bash"
    echo
    echo "Options:"
    echo "    --createuser [USERNAME]   Creates a new user account specifically for running the database The default user is 'hammy'."
    echo
    
    exit $err_code
}



function postgres_setup() {
    if [[ -z $@ ]]; then
        print_usage 1
    fi

    local createUser=0
    
    while [ ! -z "$1" ]; do
        case "$1" in
            -h|--help)
                print_usage 0
                ;;
            --createuser)
                createUser=1
                userToMake="$2"
                shift
                ;;
            *)
                print_usage 1
                ;;

        esac
        shift
    done
    

    # Argument Validation
    if [ $createUser -ne 0 ]; then
        local userToMake="${userToMake:-hammy}"
        echo "Creating user ${userToMake}"
    fi

    # Script Execution
    set -euo pipefail
    
    if [ $createUser -ne 0 ]; then
        create_user "$userToMake"
    fi

    
}



postgres_setup $@

