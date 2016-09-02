==========================================================================
Mercurial tips
==========================================================================

Seems like I'd interact more with the PyPy people, who use mercurial
primarily. So decided it's good to learn the stuff.

--------------------------------------------------------------------------
Building up-to-date version
--------------------------------------------------------------------------

The version on ``brg`` machines is 1.4 (from 2009). The current version is
3.3.1. Seems like a good idea to have a recent build::

  % wget http://mercurial.selenic.com/release/mercurial-3.3.2.tar.gz
  % tar xzf mercurial-3.3.2.tar.gz

Also note that the build system complained about missing ``docutils``. So
I had to ``pip install`` that on the virtual environment::

  % . ~/venvs/python2.7.9/bin/activate
  % pip install docutils

Building was weird, but you need to use ``make install-home`` with the
correct ``$HOME`` to be set up in the environment::

  % cd mercurial-3.3.2
  % HOME=$BITS/stowdir/mercurial-3.3.2 make install-home

--------------------------------------------------------------------------
Some commands
--------------------------------------------------------------------------

Make sure the ``~/.hgrc`` looks like the following. The ``merge`` like
uses the default merging, which is like git's merging for conflicts. It
puts inline ``>>>>>`` and ``<<<<<`` etc. Otherwise it started ``vimdiff``
for me::

  [ui]
  username = Berkin Ilbeyi <berkin@csl.cornell.edu>
  merge = internal:merge

Initialize::

  % hg init

There is no staging area in mercurial. The two most useful commands (each
gives about half the functionality of ``git status``)::

  # just reports files modified etc. if there are no changes, it doesn't
  # print anything. common flags used:
  # ? - file not in repo
  # M - file modified
  # A - file added
  % hg status
  # reports what is the "HEAD". if there are unmerged files, or if the
  # pulled changes from upstream wasn't applied, it reports those
  % hg summary

Add a file that wasn't tracked earlier (note this is not for staging area
as there is none)::

  % hg add <file>

Committing is the same as git sans staging. To allow partial commits (not
interactive, by per-file basis), provide the filename::

  # commits all modified files
  % hg commit
  # commits only files
  % hg commit <files>

If pushing this to upstream for the first time, then there is no way in
mercurial to set ``origin`` with the first push. Instead, need to modify
the project ``.hg/hgrc``::

  [paths]
  default = ssh://hg@bitbucket.org/berkinilbeyi/test

Now, you can push and pull as usual::

  % hg push
  % hg pull

``hg pull`` doesn't update the working directory. Need to use::

  % hg update

If there was a conflict, then::

  % hg merge

To view commits (make sure to pipe it to ``less`` or ``head`` because it
prints all of the commits)::

  % hg log | less
  # the following prints the dag of commits, which is cool
  % hg log -G | less

To see the log for a specific revision::

  % hg log -r <rev>

To see the current diff (uncommited) (like ``git show``)::

  % hg diff

You can diff against a revision, and this shows the differences relative
to current tip::

  % hg diff -r <rev>

More useful is you can diff a particular revision against is parent
(predecessor) to see what change was added::

  % hg diff -c <rev>

Also similar to ``git show``::

  % hg export [<rev>]

To branch::

  % hg branch <branchname>

To see all branches::

  % hg branches

To merge back a branch::

  # merges changes made to default branch to this one
  % hg merge default

When there are multiple branches, ``hg push`` pushes *all* branches. For
new branches use::

  % hg push --new-branch

To selectively push a branch (instead of all)::

  % hg push -b <branchname>

Mercurial doesn't support a rebase-based flow out of the box, so use
merge instead... One final note about ignoring files, the ``.hgignore``
also needs specifying the syntax of the file (so that you can also use
regex for it, which sounds a bit overkill)::

  syntax: glob

  *.orig
  .hgignore

To revert a file and remove the changes done to a file (similar to ``git
checkout -- file``), use::

  % hg revert <file>

This command also produces ``<file>.orig`` with the old state of the file.
This is cool I guess...

--------------------------------------------------------------------------
Modules
--------------------------------------------------------------------------

To enable color, need to enable the color module. Add this to
``~/.hgrc``::

  [extensions]
  color = 

To use a pager for things like ``hg log``, we need to enable the pager
module::

  [pager]
  pager = less

  [extensions]
  pager =
  ...

Note that the guides tell to use another command (``pager = LESS='FRX'
less``) but this causes the output of ``less`` to stay on the screen after
it is killed.

--------------------------------------------------------------------------
mq
--------------------------------------------------------------------------

I really like git's staging (index). It's nice to be able to take time to
ensure what you're committing is what you should and don't embarass
yourself with "oops, forgot this" commits. The way to emulate staging in
mercurial seems to be ``mq`` extension (mercurial queues). Useful websites
are http://mercurial.selenic.com/wiki/MqExtension
http://hgbook.red-bean.com/read/mercurial-queues-reference.html and
http://stevelosh.com/blog/2010/08/a-git-users-guide-to-mercurial-queues/ .
Add the following to your extensions::

  [extensions]
  ...
  record =
  mq     =

  [alias]
  qstatus = status --rev -2:.

The ``qstatus`` alias lets you see which files are in the "staging area".
To use, first create a patch with some name::

  % hg qnew <qname>

This seems to add all changes to the queue. You can use ``hg qstatus`` and
``hg status`` which files are staged and which ones aren't respectively.
To see the diff of staged (equivalent to ``git diff --cached``)::

  % hg qdiff

To add a file to staging::

  % hg qrefresh

To remove a file from staging::

  % hg qrefresh -X <exclude file>

Note that unlike git which builds the index as you add, this will add all
the files. You can also selectively add files::

  % hg qefresh -i

Or::

  % hg qrecord

``hg qdiff`` seems to show the diff of all files. To display the diff of
the staged stuff::

  % hg export [qtip]

