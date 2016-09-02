==========================================================================
Docker
==========================================================================

--------------------------------------------------------------------------
Installing on BRG servers
--------------------------------------------------------------------------

This is a useful link: https://docs.docker.com/installation/centos/ .
Turns out BRGs are barely sufficient to install docker::

  % cat /etc/*release
  CentOS release 6.6 (Final)
  ...
  % uname -a
  Linux brg-05.ece.cornell.edu 2.6.32-431.5.1.el6.x86_64 #1 SMP Wed Feb 12 00:41:43 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux

We need to enable EPEL repos
(https://fedoraproject.org/wiki/EPEL/FAQ#How_can_I_install_the_packages_from_the_EPEL_software_repository.3F).
This was already enabled, but the command is like following::

  % sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

To ensure docker is not already installed::

  % yum list installed | grep docker

The instructions say that the package name for Docker is ``docker-io``,
not ``docker``. ``docker`` is apparently unrelated and might conflict.
Install ``docker-io``::

  % sudo yum install docker-io

Now should be installed, start the daemon::

  % sudo service docker start

Search for an image::

  % sudo docker search centos

Pull the ``centos`` image::

  % sudo docker pull centos

List downloaded images::

  % sudo docker images

Start a shell::

  % sudo docker run -i -t centos /bin/bash

Check centos and kernel versions::

  # cat /etc/*release
  CentOS Linux release 7.1.1503 (Core)
  ...
  # uname -a
  Linux 7c5a8220cc77 2.6.32-431.5.1.el6.x86_64 #1 SMP Wed Feb 12 00:41:43 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux

The CentOS is newer but the kernel is the same... Every time the image is
modified, you can see the changes::

  % sudo docker ps -l

If you run ``centos`` again these changes are lost. To keep the changes,
you need to commit them (using commit id from above)::

  % sudo docker commit <commit-id> <name>

Now, if you run ``docker images`` again, you can see the new (or modified)
image given by the ``<name>``. You can use that to ensure the changes are
reflected.

--------------------------------------------------------------------------
PyPy cross-translation image
--------------------------------------------------------------------------

Pull ubuntu::

  % sudo docker pull ubuntu

This seems to download the LTS (14.04 trusty) by default, but if not, it's
possible to download some other tag (check out
https://registry.hub.docker.com/_/ubuntu/)::

  % sudo docker pull ubuntu:vivid

When I tried the following, it crashed the server::

  % sudo docker run ubuntu ls Desktop/

Needed packages to ubuntu::

  % sudo docker run -t -i ubuntu /bin/bash
  # apt-get update
  # apt-get install gcc vim git mercurial gcc-arm-linux-gnueabi scratchbox2 debootstrap schroot binfmt-support qemu-system qemu-user-static


This didn't work...

--------------------------------------------------------------------------
KVM
--------------------------------------------------------------------------

::

  % yum search kvm
  % sudo yum install qemu-kvm

--------------------------------------------------------------------------
VirtualBox
--------------------------------------------------------------------------

::

  % wget http://download.virtualbox.org/virtualbox/4.3.28/VirtualBox-4.3-4.3.28_100309_el6-1.x86_64.rpm

To install, you need to copy it somewhere ``root`` can access. If not,
there could be an error like following::

  TypeError: an integer is required
  ...

You can copy it to ``/tmp``::

  % cp VirtualBox-4.3-4.3.28_100309_el6-1.x86_64.rpm /tmp
  % sudo yum install ./VirtualBox-4.3-4.3.28_100309_el6-1.x86_64.rpm

Copy the VM::

  % cd ~/VirtualBox\ VMs/
  % scp -r ubuntu\ 14.04\ lts/ brg-05:/work/bits0/bi45/misc/virtualbox/vms/ubuntu_14.04_lts

Need to register the VM now (help is at ``VBoxManage help``). Note that
you need to provide the absolute path to ``.vbox`` file::

  % VBoxManage registervm /work/bits0/bi45/misc/virtualbox/vms/ubuntu_14.04_lts/ubuntu\ 14.04\ lts.vbox
  % VBoxManage list vms

You can get info about this vm::

  % VBoxManage showvminfo "ubuntu 14.04 lts"

Currently, this VM is in ``saved`` state, and it doesn't let its settings
change in this setting. To resume the VM. This doesn't work without
``--type headless`` flag::

  % VBoxManage startvm "ubuntu 14.04 lts" --type headless

Now it's SSH'able::

  % ssh -p 22022 berkin@localhost
  ..
  % sudo shutdown -h now

Now we can change the name, memory, number of cores etc::

  % VBoxManage modifyvm "ubuntu 14.04 lts" --name "ubuntu14.04"
  % VBoxManage modifyvm ubuntu14.04 --memory 4096
  % VBoxManage modifyvm ubuntu14.04 --cpus 4
  % VBoxManage showvminfo ubuntu14.04

Start::

  % VBoxManage startvm ubuntu14.04 --type headless

Stop::

  % VBoxManage controlvm ubuntu14.04 poweroff



--------------------------------------------------------------------------
PyMTL-Pydgin Image
--------------------------------------------------------------------------

Installed Ubuntu 14.04 LTS. Install guest utils using the VirtualBox guest
additions CD::

  % sudo apt-get install virtualbox-guest-utils

Debian::

  % sudo apt-get install build-essential module-assistant linux-headers-586
  % sudo su
  # cd /media/cdrom0
  # sh VBoxLinuxAdditions.run

Restart and works. Install necessary stuff::

  % sudo apt-get install vim emacs git pypy autoconf


Create 32-bit RedHat machine. Use VMDK for the hard disk to ensure it
splits the images to small chunks. Once booted::

  # vi /etc/sysconfig/network-scripts/ifcfg-eth0
  ...
  ONBOOT=yes
  # service network start

Verify it works::

  % ping www.google.com

Install desktop etc
(http://www.idevelopment.info/data/Unix/Linux/LINUX_AddGNOMEToCentOSMinimalInstall.shtml)::

  # yum -y groupinstall "Desktop" "Desktop Platform" "X Window System" "Fonts"
  # vi /etc/inittab
  (change id:3:initdefault: to id:5:initdefault:)
  # init 6
  (reboot)

Install packages::

  % yum install kernel-devel

  yum-utils
  wget
  vim
  emacs
  stow  (requires epel)
  mercurial (too old)

  more stuff (for newer git):

  asciidoc
  xmlto
  docbook2X

  for python:
  ncurses-devel
  readline-devel

  for pymtl:
  libffi-devel

Need to get ``rpmforge``::

  % wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.i686.rpm
  % sudo rpm --import  http://apt.sw.be/RPM-GPG-KEY.dag.txt
  % rpm -K rpmforge-release-0.5.3-1.el6.rf.i686.rpm
  % sudo rpm -i rpmforge-release-0.5.3-1.el6.rf.i686.rpm

Install necessary stuff::

  % sudo yum --enablerepo rpmforge install dkms
  % sudo yum groupinstall "Development Tools"
  % sudo yum install kernel-devel

Trying the guest additions failed for a long time. Turns out it was due to
the guest additions expected the sources elsewhere. The sources were at
``/usr/src/kernels/2.6.32-504.16.2.el6.i686`` while ``uname -r`` returned
``2.6.32-504.el6.i686``. I just created a symlink::

  % cd /usr/src/kernels
  % sudo ln -s 2.6.32-504.16.2.el6.i686 2.6.32-504.el6.i686

After this, you can install the virtualbox additions::

  % cd /media/VBOXADDITIONS_4.3.20_96996
  % sudo ./VBoxLinuxAdditions.run

EPEL::

  % sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

For growing the disk image, first back up everything. Turns out you can't
grow VMDK images normally. But there is a trick here:
http://stackoverflow.com/questions/11659005/how-to-resize-a-virtualbox-vmdk-file.
Basically, first clone to a VDI image, grow that, and convert back to
vmdk::

  % VBoxManage clonehd pymtl_pydgin.vmdk pymtl_pydgin_cloned.vdi --format vdi
  % VBoxManage modifyhd pymtl_pydgin_cloned.vdi --resize 12288
  % VBoxManage clonehd pymtl_pydgin_cloned.vdi pymtl_pydgin_disk.vmdk --format vmdk --variant Split2G

After this, need to use ``gparted`` or ``parted`` to resize the
partitions. It was tricky to extend the file system. On a recovery console
(through CentOS recovery mode), find out how much more can we grow the
logical space::

  # vgdisplay

Use the amount ``Free PE`` to extend the logical volume::

  # lvextend -l +511 VolGroup/lv_root

After this, might need to do ``pvextend``, not sure. Boot to normal and
extend the filesystem::

  % sudo resize2fs /dev/mapper/VolGroup-lv_root

``virtualenv`` setup::

  % wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.0.3.tar.gz#md5=cd2043ea72448d65dcc54d33744c2214
  (untar and cd)
  % python setup.py install --prefix=$STOW_PKGS_PREFIX/pkgs/virtualenv-13.0.3
  (stow)

Create ``virtualenv`` and install necessary stuff::

  % virtualenv ~/venvs/python-2.7.10
  (activate)
  % pip install git+git://github.com/cornell-brg/pymtl.git
  (python -m pip ... )

Same thing for pypy::

  % virtualenv -p pypy ~/venvs/pypy-2.5.1
  
Disk setup::

  /vm
    VirtualBox install files (win, mac, linux32, linux64)       378 MB
    vm image
  /repos
    pymtl
    pydgin
    maven-xcc
    arm-xcc

  /docs

To copy stuff, don't use normal copy, but ``rsync``::

  % cd /Volumes/PyMTL\ 1/
  % rsync -ah --progress ~/Documents/pymtl_pydgin_tutorial/disk/ .

restore::

  % sudo asr 

