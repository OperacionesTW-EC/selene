Vagrant.configure("2") do |config|
  config.vm.provider :virtualbox do |virtualbox|
        # allocate 1024 mb RAM
        virtualbox.customize ["modifyvm", :id, "--memory", "1024"] 
        # allocate max 50% CPU
        #virtualbox.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
  end
  config.vm.box = "hashicorp/precise64"
  
  config.vm.provision :shell, path: "vagrantFiles/paquetes.sh"
  config.vm.provision  "ansible_local" do |ansible|
    ansible.playbook = "vagrantFiles/selene.yml"
  end
  #config.vm.network "private_network", ip: "10.0.0.25"
  config.vm.network :forwarded_port, guest: 5432, host: 5432	
  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.network :forwarded_port, guest: 22, host: 6222

end
