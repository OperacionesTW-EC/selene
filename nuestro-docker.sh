#! /usr/bin/env bash

if [[ "$BASH_VERSION" =~ ^[0-3] ]];then
    echo "Version de bash '$BASH_VERSION' demasiado viejo.  Necesitas al menos '4.x.x'"
    echo "Si tienes un Mac antiguo, usa homebrew para instalar la ultima version"
    exit 1
fi

project=$(pwd | xargs basename)
docker_cmd=docker
compose_cmd=docker-compose
db_image=${project}_db
backend_image=${project}_backend
ui_image=${project}_ui
default_target_env='local'
target_env=$default_target_env
declare -A operations

usage()
{
    echo Usage:
    echo "     you need at least one of 'clean', 'build', 'up', 'db', 'test', or 'all'"
    echo
    echo "     Examples:"
    echo "       $ $0 clean"
    echo "       $ $0 build"
    echo "       $ $0 prod build"
    echo "       $ $0 up db"
    exit 1
}

cmd()
{
    local function_name=${FUNCNAME[1]}
    local command="$*"
    echo -e "\n########## $function_name ##########\n"
    echo $command

    eval "$command"

    local rc=$?
    if [ "$rc" != 0 ];then
        echo -e "\t'$command' falló con '$rc'"
        echo -e "\ten función '$function_name'"
        exit $rc
    fi
}

exit_on_error()
{
    local function_name=$1
    local rc=$2
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
                [Rr]m-containers | RM-CONTAINERS )
                    operations[CLEAN_CONTAINERS]=1
                    ;;
                [Rr]m-all-images | RM-ALL-IMAGES )
                    operations[CLEAN_ALL_IMAGES]=1
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
                local | ci | qa | uat | prod )
                    target_env=$arg
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

set_compose_file()
{
    if [ "$target_env" == prod ];then
      export COMPOSE_FILE=prod-base.yml:prod-build.yml
    else
      export COMPOSE_FILE=docker-compose.devel.yml
    fi
}

clean_all_containers()
{
    container_ids=$($docker_cmd ps -aq)
    if [ -n "$container_ids"  ]
    then
        echo Removing Old Containers:
        cmd $docker_cmd rm -f $container_ids
        echo
    fi
}

clean_all_images()
{
    image_ids=$($docker_cmd images -aq)
    if [[ -n $image_ids ]]
    then
        echo Removing ALL Images:
        $docker_cmd rmi -f $image_ids
    fi
}

clean_old_pyc_files()
{
  cmd find . -type f -name '*.pyc' -delete
}

clean_image()
{
    image_id=$($docker_cmd images -q $1)
    if [ -n "$image_id"  ]
    then
        echo Removing Image $1:
        cmd $docker_cmd rmi -f $1
        echo
    fi
}

clean_project_images()
{
    for i in $db_image $backend_image $ui_image
    do
        clean_image $i
    done
}

compose_up()
{
    cmd $compose_cmd up -d
}

compose_build()
{
    cmd $compose_cmd build
}

db()
{
    wait_for_compose_up_seconds=3
    sleep $wait_for_compose_up_seconds
    container=${backend_image}_1
    cmd $docker_cmd exec $container python manage.py migrate
    cmd $docker_cmd exec $container python manage.py loaddata user.json
}

run_tests()
{
    cmd $compose_cmd run --rm $backend_service python manage.py test
}
run()
{

    if [ ${operations[CLEAN]} ]; then
        clean_old_pyc_files
        clean_all_containers
        clean_project_images
    fi
    if [ ${operations[CLEAN_CONTAINERS]} ]; then
        clean_all_containers
    fi
    if [ ${operations[CLEAN_ALL_IMAGES]} ]; then
        clean_all_images
    fi
    if [ ${operations[BUILD]} ]; then
        clean_old_pyc_files
        compose_build
    fi
    if [ ${operations[UP]} ]; then
        clean_old_pyc_files
        clean_all_containers
        compose_up
    fi
    if [ ${operations[DB]} ]; then
        db
    fi
    if [ ${operations[TEST]} ]; then
        run_tests
    fi
    if [ ${operations[ALL]} ]; then
        clean_old_pyc_files
        clean_all_containers
        clean_project_images
        compose_build
        compose_up
        db
        # run_tests
    fi
}
parse_args $*
set_compose_file
run
