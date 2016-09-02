==========================================================================
yum sync
==========================================================================

--------------------------------------------------------------------------
Handy yum commands
--------------------------------------------------------------------------

All packages installed::

  % yum list installed

Show all history (including who installed what)::

  % sudo yum history list all

Find which transaction a package was installed::

  % sudo yum history package-list <package_name>

Use ID to get more info about the transaction::

  % sudo yum history info <ID>

--------------------------------------------------------------------------
brg-05 sync (10/20/2015)
--------------------------------------------------------------------------

Current packages::

  VirtualBox-4.3.x86_64
      alternative PyPy cross translation
  debootstrap
      alternative PyPy cross translation, didn't work, delete
  docker-io
      Docker, good to have
  fakeroot
  fakeroot-libs
      alternative PyPy cross translation, didn't work, delete
  glib2-static
      for static building of qemu (alternative PyPy cross translation), delete
  glibc-static
      for building certain cross-compiler toolchains
  lua-alt-getopt
  lua-filesystem
  lua-lxc
  lxc
  lxc-libs
      dependencies for Docker
  openssl-devel
  zlib-devel
      for building CPython from source

Uninstalled::

  debootstrap
  fakeroot
  fakeroot-libs
  glib2-static


