==========================================================================
Pi Notes
==========================================================================

It was straightforward to image the SD card using the directions on the
website
(http://www.raspberrypi.org/documentation/installation/installing-images/mac.md).
Once booted, it showed "Raspberry Pi Software Configuration Tool
(raspi-config)", where you can change password, boot environment (GUI vs
command line), overclocking etc.

For the jitviewer, we need to use the desktop environment.

Also the default keyboard layout is EN-UK. To fix it run the following
(although it didn't fix it, maybe needs a reboot?)::

  % sudo dpkg-reconfigure keyboard-configuration

--------------------------------------------------------------------------
Network
--------------------------------------------------------------------------

We need to download additional software, so we need to enable network
connectivity. For this, the MAC address needs to be registered with the
sysadmins. As a temporary solution, I tried changing the MAC address
through ``ifconfig``, but it complained that the device is busy even
though I did a ``ifconfig down``. Another solution is to add the following
to the line in ``/boot/cmdline.txt``::

  ...elevator=deadline smsc95xx.macaddr=a8:20:66:47:f9:27 rootwait

The original MAC address was b8:27:eb:a6:9d:0f. The solution worked and
the network is working.

--------------------------------------------------------------------------
jitviewer
--------------------------------------------------------------------------

Install mercurial::

  % sudo apt-get install mercurial

Download pypy source (not on mercurial because it takes a very long time::

  % mkdir pypy
  % cd ~/pypy
  % wget https://bitbucket.org/pypy/pypy/downloads/pypy-2.2.1-src.tar.bz2
  % tar xjf pypy-2.2.1-src.tar.bz2

Clone jitviewer::

  % hg clone https://bitbucket.org/pypy/jitviewer

Install virtualenv and create a new one::

  % sudo apt-get install python-virtualenv
  % mkdir ~/venvs
  % cd ~/venvs
  % virtualenv --python=`which pypy` --no-site-packages pypy-2.2.1
  % . pypy-2.2.1/bin/activate

Install jitviewer and requirements::

  % cd ~/pypy/jitviewer
  % pip install -r requirements.txt

Export the pypy source to the ``PYTHONPATH``::

  % cd ~/pypy/pypy-2.2.1-src
  % export PYTHONPATH=`pwd`

Generating the log first and then running the jitviewer didn't seem to
show the assembly. Running the code directly from jitviewer works::

  % cd ~/pypy/test-pypy
  % jitviewer.py -c test-loop.py

The jitviewer can be seen locally in browser on address
``128.84.224.243:5000``.

--------------------------------------------------------------------------
Backup notes
--------------------------------------------------------------------------

When I had to reformat the Pi, I wanted to back up certain things.
However, plugging in the SD card to Mac did not allow me to access the
files. For this to work, I had to install OSXFUSE (needs to be installed
with "MacFUSE Compatibility Layer" (http://osxfuse.github.io/) and
fuse-ext2 (http://sourceforge.net/projects/fuse-ext2/). Then I could
access the files normally.

--------------------------------------------------------------------------
New Pi and BeagleBone
--------------------------------------------------------------------------

BeagleBone

default u/n: debian p/w: temppwd (changed this to L* and created berkin
username)
6c:ec:eb:68:ec:12 128.84.224.135

Pi 2
b8:27:eb:42:87:31 128.84.224.128

ZedBoard
00:0a:35:00:01:22

