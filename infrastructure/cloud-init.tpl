#cloud-config
package_update: true
packages:
  - docker.io
  - nginx
  - git

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker azureuser
  - mkdir -p /opt/task-tracker
  - systemctl enable nginx
  - systemctl start nginx