#! /usr/bin/env bash

project=selene
artifact_name=${project}.tar.gz

docker_cmd=docker
compose_cmd=docker-compose
ssh_cmd=ssh
scp_cmd=scp

db_image=${project}_db
backend_image=${project}_backend
ui_image=${project}_ui
base_config=prod-base.yml
build_config=prod-build.yml
up_config=prod-up.yml

path_deploy='/opt/admin/selene'
user_deploy=root
ip_deploy=10.71.23.244

heading()
{
  echo -e "\n########## $1 ##########\n"
}
cmd()
{
    # ':' means no-op
    # assign a value if function_name is not set
    : ${function_name:=${FUNCNAME[1]}}

    local command="$*"
    if [ -z "$no_echo" ]; then
      heading $function_name
      echo $command
    fi

    if [ -z "$dry_run" ]; then
      eval "$command"
      local rc=$?

      if [ "$rc" != 0 ];then
        echo -e "\t'$command' falló con '$rc'"
        echo -e "\ten función '$function_name'"
        exit $rc
      fi
    fi
    unset -v function_name
    unset -v no_echo
  }

cmd_remote()
{
  function_name=${FUNCNAME[1]}
  cmd $ssh_cmd $user_deploy@$ip_deploy $1
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
    if [ -n "$container_ids" ] # 1st element non-empty?
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
    if [ -n "$image_ids" ] # 1st element non-empty?
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
  cmd "$scp_cmd $artifact_name $user_deploy@$ip_deploy:$path_deploy/$artifact_name"
}

clean_old_artifacts()
{
  cmd_remote "rm -rfv $path_deploy/${project}*.tar*"
}

decompress_artifact()
{
  cmd_remote "gunzip $path_deploy/$artifact_name"
  cmd_remote "tar --directory $path_deploy -xv -f $path_deploy/${project}.tar"
}

load_image()
{
  cmd_remote "time $docker_cmd load -i $path_deploy/$1"
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
  cmd_remote "$compose_cmd -f $path_deploy/$base_config -f $path_deploy/$up_config up -d"
}

django_db_migrate()
{
  wait_for_compose_up_seconds=13
  sleep $wait_for_compose_up_seconds
  container=${backend_image}_1
  cmd_remote "$docker_cmd exec $container python manage.py migrate"
  cmd_remote "$docker_cmd exec $container python manage.py loaddata user.json"
}

parse_args()
{
  for arg in $@
  do
    case "$arg" in
      -d | --debug | d | debug )
        PS4=' ${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
        set -x
        ;;
      -n | --dry*run | n | dry | dry*run )
        dry_run='true'
        ;;
      [Pp]ackage | PACKAGE )
        package='true'
        ;;
      [Dd]eploy | DEPLOY )
        deploy='true'
        ;;
    esac
  done
  # do both 'package' and 'deploy' if neither are set
  if [[ -z "$package" && -z "$deploy" ]]; then
    package='true'
    deploy='true'
  fi
}

set_script_variables()
{
  parse_args $*
  set_images_and_services
}

package()
{
  clean_project_containers
  clean_project_images
  compose_build
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

set_script_variables $*
# conditionally run package or deploy or both
[ -n "$package" ] && package
[ -n "$deploy" ] && deploy
