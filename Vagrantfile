Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provision :shell, path: "vagrantFiles/paquetes.sh"
  config.vm.provision  "ansible_local" do |ansible|
    ansible.playbook = "vagrantFiles/selene.yml"
  end
  config.vm.network "private_network", ip: "10.0.0.25"
  config.vm.network :forwarded_port, guest: 5432, host: 5432	

end
