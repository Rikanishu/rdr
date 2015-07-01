# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Box
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  config.vm.hostname = "rdr"

  config.vm.network "private_network", ip: "33.33.33.33"

  # Shared folders
  config.vm.synced_folder ".", "/srv"

  # Port forward
  # config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
     vb.customize [
      "modifyvm", :id, 
      "--memory", "256"
    ]
  end

  # Setup
  config.vm.provision :shell, path: "tools/vagrant/init.sh"

end