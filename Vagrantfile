PROJECT_NAME = "webapp"
SRC_DIR = "/home/vagrant/#{PROJECT_NAME}/src/backend/src"

Vagrant.require_version ">= 2.0.1"
Vagrant.configure(2) do |config|

  config.vm.hostname = PROJECT_NAME
  config.vm.box = "ubuntu/xenial64"

  config.vm.network :private_network, ip: "192.168.12.32"
  config.vm.synced_folder "./src", SRC_DIR

  config.vm.provider :virtualbox do |vb|
    vb.name = PROJECT_NAME
    vb.memory = "2096"
    vb.cpus = 2
    vb.gui = false
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/site.yml"
    ansible.inventory_path = "ansible/vagrant.ini"
    ansible.host_key_checking = false
    ansible.galaxy_roles_path = 'ansible/galaxy_roles'
    ansible.limit = "*"
  end
end