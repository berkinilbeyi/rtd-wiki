==========================================================================
RISC-V notes
==========================================================================

Need to clone ``riscv-tools``, and fetch the submodule stuff::

  % git clone git@github.com:riscv/riscv-tools.git
  % cd riscv-tools/
  % git submodule update --init --recursive

At this point, the website says, we need gcc 4.8+, so I stow-installed it.
We need to set the install dir and install::

  % export RISCV=$BITS/stowdir/riscv-tools

This complains about gmp stuff. Needed to manually build ``gnu-tools``::

  % cd riscv-gnu-toolchain
  % mkdir build
  % cd build
  % export CPATH=$STOW_PKGS_PREFIX/include
  % export LIBRARY_PATH=$STOW_PKGS_PREFIX/lib
  % ../configure --prefix=$BITS/stowdir/riscv-tools
  % make -j 8

--------------------------------------------------------------------------
Spike notes
--------------------------------------------------------------------------

Debugging with spike is a bit annoying because you have to use the
interactive debugger with `-d` flag::

  % spike -d rv64ui-p-add
  : run 1  # runs one instruction
  : reg 0  # dumps registers for core 0

I went and added a new debug flag `runreg` which runs the program and
dumps the registers::

  % spike -d rv64ui-p-add
  : runreg 5

Really useful is the ability to print CSRs::

  : reg 0 mstatus

--------------------------------------------------------------------------
linux
--------------------------------------------------------------------------

First need to build glibc-enabled `riscv-unknown-linux-gnu-gcc`. Note that
this doesn't seem to work on Mac perhaps due to file system being case
insensitive::

  % cd ricv-gnu-toolchain/build
  % make -j16 linux

If getting an error `LD_LIBRARY_PATH shouldn't contain the current
directory when building glibc`, in my case it was because my
`LD_LIBRARY_PATH` contained a trailing `:`, which apparently was
interpreted as `:.`.

::

  % wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.14.41.tar.xz
  % tar xJf linux-2.13.31.tar.xz
  % cd linux-2.13.31
  % git init
  % git remote add origin https://github.com/riscv/riscv-linux.git
  % git fetch
  % git checkout -f -t origin/master

Generate default config::

  % make ARCH=riscv defconfig

Also can tweak the kernel. Enabled `Early printk` under `Kernel hacking`::

  % make ARCH=riscv menuconfig

Build the kernel::

  % make -j16 ARCH=riscv

Need to get busybox::

  % wget http://busybox.net/downloads/busybox-1.21.1.tar.bz2
  % tar xjf busybox-1.21.1.tar.bz2
  % cd busybox-1.21.1

Generate a configuration with things turned off::

  % make allnoconfig

Then we need to turn on some things in the `.config` file::

  CONFIG_STATIC=y
  CONFIG_CROSS_COMPILER_PREFIX="riscv64-unknown-linux-gnu-"
  CONFIG_FEATURE_INSTALLER=y
  CONFIG_INIT=y
  CONFIG_ASH=y
  CONFIG_ASH_JOB_CONTROL=n
  CONFIG_MOUNT=y
  CONFIG_FEATURE_USE_INITTAB=y
  # enable more goodies VIM, PS, TOP, ECHO, CAT etc.

This is pretty bare, the following is probably better::

  % make defconfig

And change to the following::

  CONFIG_STATIC=y
  CONFIG_CROSS_COMPILER_PREFIX="riscv64-unknown-linux-gnu-"
  CONFIG_FEATURE_INETD_RPC=n

Build::

  % make -j16

Need to create a disk image (of 64MB) (note, this might be too small for
SPEC and stuff, so I created another one of 2GB (2048MB))::

  % cd ../linux-3.14.41
  % dd if=/dev/zero of=root.bin bs=1M count=64
  % mkfs.ext2 -F root.bin

In mounting the disk image, I had trouble to avoid it from being
read-only::

  % chmod o+w root.bin
  % mkdir mnt
  % sudo mount -o loop,rw -t ext2 root.bin mnt
  % mkdir -p bin etc dev lib proc sbin sys tmp usr usr/bin usr/lib usr/sbin

Copy busybox::

  % cd mnt
  % cp ../../busybox-1.21.1/busybox bin

Create `/etc/inittab`::

  ::sysinit:/bin/busybox mount -t proc proc /proc
  ::sysinit:/bin/busybox mount -t tmpfs tmpfs /tmp
  ::sysinit:/bin/busybox mount -o remount,rw /dev/htifblk0 /
  /dev/console::sysinit:/bin/busybox ash

Create a symlink to `busybox` from `/sbin/init`::

  % cd sbin
  % ln -s /bin/busybox init

Then unmount and run::

  % sudo umount mnt
  % spike +disk=root.bin bbl vmlinux

Need to install busybox on the virtual machine the first time around which
will add symlinks for the commands supported::

  # /bin/busybox --install -s

Should turn off the system properly, otherwise the disk might not have the
latest stuff::

  # poweroff -f

If there is ever a corruption in the file system, can use the `fsck.ext2`
tool (on the host, unmounted) to fix it::

  % fsck.ext2 root.bin

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I wanted to be able to run SPEC on the linux image. I created a new SPEC
configuration `riscv-linux` that uses `riscv64-unknown-linux-gnu` target::

  % cd spec
  % . shrc
  % runspec --config=riscv-linux.cfg --loose --size test --tune base --iterations=1 int

This succeeded for all benchmarks except `400.perlbench`.
