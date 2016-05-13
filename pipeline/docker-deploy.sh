#! /usr/bin/env bash

project=$(pwd | xargs basename)
artifact_name=${project}.tar.gz

# Concentrate external dependencies up here, please! :-)
path_deploy=${PATH_DEPLOY:? "var unset, please export"}
user_deploy=${USER_DEPLOY:? "var unset, please export"}
ip_deploy=${IP_DEPLOY:? "var unset, please export"}

docker_cmd=docker
compose_cmd=docker-compose
ssh_cmd="cmd ssh $user_deploy@$ip_deploy "
scp_cmd="cmd scp "

db_image=${project}_db
backend_image=${project}_backend
ui_image=${project}_ui
base_config=prod-base.yml
build_config=prod-build.yml
up_config=prod-up.yml

usage()
{
    echo Usage:
    echo "     $ $0 [-n|--dry-run][-d|--debug] [function_name...]"
    echo
    echo "     Examples:"
    echo "       $ $0"
    echo "       $ $0 -d -n build"
    echo "       $ $0 copy_artifact decompress_artifact"
}

heading()
{
  echo -e "\n########## $1 ##########\n"
}
cmd()
{
    local function_name=${FUNCNAME[1]}
    local command="$*"

    if [[ -z $no_echo ]]; then
      heading $function_name
      echo $command
    fi

    if [[ -z $dry_run ]]; then
      eval "$command"
      local rc=$?

      if [[ $rc != 0 ]];then
        echo -e "\t'$command' falló con '$rc'"
        echo -e "\ten función '$function_name'"
        exit $rc
      fi
    fi
    unset -v no_echo
  }

get_project_container_ids()
{
    no_echo='true'
    heading $FUNCNAME
    container_ids=$(cmd $compose_cmd -f $base_config -f $build_config ps -q)
    unset -v no_echo
}

clean_project_containers()
{
    get_project_container_ids
    if [[ -n $container_ids ]] # 1st element non-empty?
    then
        echo Removing Old Containers:
        cmd $docker_cmd rm -f $container_ids
        echo
    fi
}

get_project_image_ids()
{
    heading $FUNCNAME
    image_ids=()
    for i in "${our_images[@]}"
    do
      no_echo='true'
      image_ids+=($(cmd $docker_cmd images -q $i)) # append to array
    done
    unset -v no_echo
}

clean_project_images()
{
    get_project_image_ids
    if [[ -n $image_ids ]] # 1st element non-empty?
    then
        cmd $docker_cmd rmi -f "${image_ids[@]}"
    fi
}

set_images_and_services()
{
  our_images=($db_image $backend_image $ui_image)
  our_services=($(echo "${our_images[@]}" | sed -e 's/selene_//g'))
}

compose_build()
{
  cmd $compose_cmd -f $base_config -f $build_config build "${our_services[@]}"
}

clean_build_products()
{
  cmd rm -rfv ${project}*.tar*
}

save_image()
{
    cmd time $docker_cmd save -o $1.tar $1
}

save_images()
{

  for i in "${our_images[@]}"
  do
    save_image $i
  done
}

build_artifact()
{
  cmd tar -cvzf $artifact_name ${project}_*.tar $base_config $up_config config/{ui,db}/prod.env
}

copy_artifact()
{
  $scp_cmd "$artifact_name $user_deploy@$ip_deploy:$path_deploy/$artifact_name"
}

clean_old_artifacts()
{
  $ssh_cmd "rm -rfv $path_deploy/${project}*.tar*"
}

decompress_artifact()
{
  $ssh_cmd "gunzip $path_deploy/$artifact_name"
  $ssh_cmd "tar --directory $path_deploy -xv -f $path_deploy/${project}.tar"
}

load_image()
{
  $ssh_cmd "time $docker_cmd load -i $path_deploy/$1"
}
load_images()
{
  for i in "${our_images[@]}"
  do
    load_image $i.tar
  done
}

launch_containers()
{
  $ssh_cmd "$compose_cmd -f $path_deploy/$base_config -f $path_deploy/$up_config up -d"
}

django_db_migrate()
{
  wait_for_compose_up_seconds=13
  container=${backend_image}_1
  $ssh_cmd "\"sleep $wait_for_compose_up_seconds && $docker_cmd exec $container python manage.py migrate\""
  $ssh_cmd "$docker_cmd exec $container python manage.py loaddata user.json"
}

parse_args()
{
  functions_from_cmd_line=()
  for arg in $@
  do
    case "$arg" in
      -d | --debug )
        PS4=' ${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
        set -x
        ;;
      -n | --dry*run )
        dry_run='true'
        ;;
      * )
        if declare -f $arg > /dev/null; then
          functions_from_cmd_line+=("$arg")
        else
          echo "'$arg' is not a declared function"
          usage
          exit 1
        fi
    esac
  done
}

set_script_variables()
{
  parse_args $*
  set_images_and_services
}

build()
{
  clean_project_containers
  clean_project_images
  compose_build
}

package()
{
  clean_build_products
  save_images
  build_artifact
}

deploy()
{
  clean_old_artifacts
  copy_artifact
  decompress_artifact
  load_images
  launch_containers
  django_db_migrate
}

run()
{
  if [[ $functions_from_cmd_line ]]; then
    for user_cmd in ${functions_from_cmd_line[@]}; do
      $user_cmd
    done
  else
    build
    package
    deploy
  fi
}
set_script_variables $*
run
