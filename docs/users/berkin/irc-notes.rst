==========================================================================
IRC Notes
==========================================================================

Start up ``irssi``::

  % irssi

It gives a screen with a prompt that says ``[(status)]``. For help, use
``/help``. Connect to a server::

  /server irc.freenode.net

To change nick::

  /nick <new nick>

To connect to a channel::

  /channel #mini-howto

Query about a user::

  /q nick

Private chat::

  /w nick

Changing tabs::

  ctrl-p and ctrl-n

After settings, can save options::

  /save

To allow beeping::

  /set beep_when_window_active ON
  /set beep_when_away ON
  /set beep_msg_level MSGS NOTICES DCC DCCMSGS HILIGHT
  /set bell_beeps ON

This site is useful: https://quadpoint.org/articles/irssi/ .

--------------------------------------------------------------------------
hilight
--------------------------------------------------------------------------

::

  % git clone git@github.com:irssi/scripts.irssi.org.git
  % cp scripts.irssi.org/scripts/hilightwin.pl ~/.irssi/scripts

Note, you can put the scripts under ``~/.irssi/scripts/autorun`` instead
to run them automatically. Then use the following::

  /window new split
  /window name hilight
  /window size 6

Save the layout::

  /layout save

--------------------------------------------------------------------------
vim mode
--------------------------------------------------------------------------

Experimenting with vim mode as described in
http://archlinux.me/w0ng/2012/07/14/vim-mode-in-irssi/ and
http://superuser.com/questions/243625/any-irc-clients-with-vi-key-binds ::

  % cd ~/misc
  % git clone git@github.com:shabble/irssi-scripts.git

We need to put the ``vim-mode`` directory under ``~/.irssi/scripts``::

  % cp -r irssi-scripts/vim-mode ~/.irssi/scripts

Now, load this in ``irssi``::

  /script load vim_mode.pl

This kinda works. You can use ``esc`` or ``ctrl-c`` to go into editing
mode. You can scroll in the history, but can't search (can search in the
commands). To search, need to use the normal method::

  /lastlog <word>

--------------------------------------------------------------------------
Output logs
--------------------------------------------------------------------------

Use the following::

  /set autolog on
  /SET autolog_path ~/irclogs/$tag/$0.%y-%m-%d.log

The logs will be at the specified directory with the day and stuff.

To close a window (channel)::

  /window close

To exit::

  /exit
