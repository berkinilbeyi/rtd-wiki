--------------------------------------------------------------------------
tmux notes
--------------------------------------------------------------------------

Currently (version 1.9a), there is an issue with tmux where ``swap-pane``
crashes if the source window has a single pane. Seems like this is fixed?
(http://sourceforge.net/p/tmux/tickets/108/). So I tried installing this
version::

  % git clone git://git.code.sf.net/p/tmux/tmux-code tmux-git
  % cd tmux-git
  % ./autogen.sh
  % mkdir build
  % cd build
  % ../configure --prefix=$BITS/stowdir/tmux-git2015-03-31 LDFLAGS="-L$STOW_PKGS_PREFIX/lib" CFLAGS="-I$STOW_PKGS_PREFIX/include"
  % make
  % make install
  % cd $STOW_PKGS_PREFIX/pkgs
  % ln -s $BITS/stowdir/tmux-git2015-03-31
  % stow --delete tmux-1.9a
  % stow tmux-git2015-03-31

