
Download and install ruby::

  % cd ruby
  % wget https://cache.ruby-lang.org/pub/ruby/2.3/ruby-2.3.1.tar.gz
  % tar xzf ruby-2.3.1.tar.gz
  % mkdir build
  % cd build
  % ../configure --prefix=$BITS/stowdir/ruby-2.3.1
  % make -j15
  % make install
  % cd ~/install/stow-pkgs/x86_64-centos6/pkgs
  % ln -s $BITS/stowdir/ruby-2.3.1
  % stow ruby-2.3.1

Follow the Jekyll instructions:
https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/::

  % gem install bundler jekyll

After this, need to re-stow because the new files aren't tracked.

  % cd ~/install/stow-pkgs/x86_64-centos6/pkgs
  % stow ruby-2.3.1
 
Create a new directory::

  % cd $BITS/misc
  % mkdir test-site
  % cd test-site

Create a file called Gemfile and put the following::

  source 'https://rubygems.org'
  gem 'github-pages', group: :jekyll_plugins
  
Do installation::

  % bundle install

Generate local files::

  % bundle exec jekyll new . --force




--------------------------------------------------------------------------
instructions for realms:
--------------------------------------------------------------------------

Create a new virtualenv, then ``pip install realms-wiki``. This complained
because ``lber.h`` couldn't be found. Check which package to install using
``yum whatprovides "*/lber.h"``, and we need ``openldap-devel-XXX``.
Yum-installed this (and its dependency ``cyrus-sasl``) on ``brg-05``.
