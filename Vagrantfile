Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provision :shell, path: "vagrantFiles/ansible.sh"
  config.vm.provision  "ansible_local" do |ansible|
    ansible.playbook = "vagrantFiles/postgres.yml"
    ansible.playbook = "vagrantFiles/git.yml"
  end
  config.vm.network "private_network", ip: "10.0.0.25"
  config.vm.network :forwarded_port, guest: 80, host: 4567	

end
