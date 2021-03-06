# Upgrading from a Previous Release without Migration Support

This page documents the steps required to upgrade the web portal when you have
a previous version of the software install **prior to migration support via
Django South**. Note that this is a special case and will not apply to most
situations (see [doc/RPKI/CA/UI/GUI/Upgrading][1] for the normal upgrade
path). If you have already performed the steps on this page previously, then
it does not apply to your situation.

If you are unsure whether or not you have previously run this command, you can
verify with the following command:

    
    
    $ rpki-manage migrate --list
    
     app
      (*) 0001_initial
      (*) 0002_auto__add_field_resourcecert_conf
      (*) 0003_set_conf_from_parent
      (*) 0004_auto__chg_field_resourcecert_conf
      (*) 0005_auto__chg_field_resourcecert_parent
      ( ) 0006_add_conf_acl
      ( ) 0007_default_acls
    

The migrations are an ordered list. The presence of the asterisk `(*)`
indicates that the migration has already been performed. `( )` indicates that
the specific migration has not yet been applied. In the example above,
migrations 0001 through 0005 have been applied, but 0006 and 0007 have not.

## Sync databases

Execute the following command in a shell. Note that you do not need to be the
_root_ user, any user with permission to read `/etc/rpki.conf` is sufficient.

    
    
    $ rpki-manage syncdb
    

Note that at the end of the `syncdb` output you will see the following
message:

    
    
    Not synced (use migrations):
     - rpki.gui.app
    (use ./manage.py migrate to migrate these)
    

You should **ignore the message about running ./manage.py** since that script
does not exist in our setup.

## Initial Database Migration

For a completely new install, there will not be any existing tables in the
database, and the `rpki-manage migrate` command will create them. However, in
the special situation where you are upgrading from a previous release prior to
the migration support being added, you will already have the tables created,
which will case the initial migration to fail. In order to work around this
problem, we have to tell the migration that the initial step has already been
performed. This is accomplished via the use the `--fake` command line
argument:

    
    
    $ rpki-manage migrate app 0001 --fake
    

Note that this step doesn't actually modify the database, other than to record
that the migration has already taken place.

## Database Migration

Now bring your database up to date with the current release:

    
    
    $ rpki-manage migrate
    

From this point forward you will follow the steps in
[doc/RPKI/CA/UI/GUI/Upgrading][1] each time you upgrade.

## Restart Apache

In order to make Apache use the new version of the software, it must be
restarted:

    
    
    $ apachectl restart
    

   [1]: #_.wiki.doc.RPKI.CA.UI.GUI.Upgrading

