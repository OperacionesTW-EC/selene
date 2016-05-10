#! /usr/bin/env bash

if [[ "$BASH_VERSION" =~ ^[0-3] ]];then
    echo "Version de bash '$BASH_VERSION' demasiado viejo.  Necesitas al menos '4.x.x'"
    echo "Si tienes un Mac antiguo, usa homebrew para instalar la ultima version"
    exit 1
fi

DOCKER=docker
COMPOSE=docker-compose
DB=selene_db
BACKEND=selene_backend
UI=selene_ui
YAML=docker-compose.devel.yml
declare -A operations

usage()
{
    echo Usage:
    echo "     you need at least one of 'clean', 'build', 'up', 'db', 'test', or 'all'"
    echo
    echo "     Examples:"
    echo "       $ $0 clean"
    echo "       $ $0 build"
    echo "       $ $0 up db"
    exit 1
}

exit_on_error()
{
    function_name=$1
    rc=$2
    if [ "$rc" != 0 ];then
        echo "función '$function_name' falló con '$rc'"
        exit $rc
    fi
}

parse_args()
{
    # if no args, set 'all' by default
    if [ "$#" == 0 ]; then
        operations[ALL]=1
    else
        for arg in $@
        do
            case "$arg" in
                [Cc]lean | CLEAN )
                    operations[CLEAN]=1
                    ;;
                [Bb]uild | BUILD )
                    operations[BUILD]=1
                    ;;
                [Uu]p | UP )
                    operations[UP]=1
                    ;;
                [Dd]b | DB )
                    operations[DB]=1
                    ;;
                [Tt]est | TEST )
                    operations[TEST]=1
                    ;;
                [Aa]ll | ALL )
                    operations[ALL]=1
                    ;;
            esac
        done
        # if 'all' included, remove others
        if [ ${operations[ALL]} ]; then
            operations=()
            operations[ALL]=1
        fi
        # if args, but no good ones, raise usage
        if [ "${#operations[@]}" == 0 ];then
            usage
            exit 2
        fi
    fi
}
clean_containers()
{
    container_ids=$($DOCKER ps -aq)
    if [ -n "$container_ids"  ]
    then
        echo Removing Old Containers:
        $DOCKER rm -f $container_ids
        exit_on_error $FUNCNAME $?
        echo
    fi
}

clean_image()
{
    image_id=$($DOCKER images -q $1)
    if [ -n "$image_id"  ]
    then
        echo Removing Image $1:
        $DOCKER rmi -f $1
        exit_on_error $FUNCNAME $?
        echo
    fi
}

clean_images()
{
    for i in $DB $BACKEND $UI
    do
        clean_image $i
        exit_on_error $FUNCNAME $?
    done
}

compose_up()
{
    $COMPOSE -f $YAML up -d
    exit_on_error $FUNCNAME $?
}

compose_build()
{
    $COMPOSE -f $YAML build
    exit_on_error $FUNCNAME $?
}

db()
{
    wait_for_compose_up_seconds=3
    sleep $wait_for_compose_up_seconds
    container=${BACKEND}_1
    $DOCKER exec $container python manage.py migrate
    exit_on_error $FUNCNAME $?
    $DOCKER exec $container python manage.py loaddata user.json
    exit_on_error $FUNCNAME $?
}

run_tests()
{
    $DOCKER exec "Alguien arrégleme por fa"
    exit_on_error $FUNCNAME $?
}
run()
{

    if [ ${operations[CLEAN]} ]; then
        clean_containers
        clean_images
    fi
    if [ ${operations[BUILD]} ]; then
        compose_build
    fi
    if [ ${operations[UP]} ]; then
        clean_containers
        compose_up
    fi
    if [ ${operations[DB]} ]; then
        db
    fi
    if [ ${operations[TEST]} ]; then
        run_tests
    fi
    if [ ${operations[ALL]} ]; then
        clean_containers
        clean_images
        compose_build
        compose_up
        db
        # run_tests
    fi
}
parse_args $*
run
