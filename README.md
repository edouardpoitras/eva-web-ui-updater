Web UI Updater
==============

An Eva plugin that adds a way of updating plugins through the Web UI.

## Installation

Can be easily installed through the Web UI by using [Web UI Plugins](https://github.com/edouardpoitras/eva-web-ui-plugins).

Alternatively, add `web_ui_updater` to your `eva.conf` file in the `enabled_plugins` option list and restart Eva.

## Usage

Once enabled, you will see a few more buttons on the `/plugins` page.

#### Check For Updates button

This button fires a job in the background that will check all plugins for updates.
If a plugin requires an update, it will appear in the `Plugins` table (this could take a few minutes depending on the number of plugins to check and your internet connection).

#### Undo Last Update button

This button is used when the user wishes to un-do the previous update.

NOTE: As of version 0.1.0, This only works for the last applied update - you can't undo more than one update at a time.

#### Plugins table

A new column title `Status` will be added to the `Plugins` table. This column will contain one of the following:

* Text that says `Updated` - The plugin is up-to-date.
* A yellow button that says `Update` - Click on it to update the plugin.
* Text that says `Unknown` - No repository information could be found for this plugin.

#### Update All button

This button is used when the user wishes to update all plugins at once.

If something goes wrong, you can try the `Undo Last Update` button to revert all changes.

## Configuration

Default configurations can be changed by adding a `web_ui_updater.conf` file in your plugin configuration path (can be configured in `eva.conf`, but usually `~/eva/configs`).

To get an idea of what configuration options are available, you can take a look at the `web_ui_updater.conf.spec` file in this repository, or view them at `/plugins/configuration/web_ui_updater`.

Here is a breakdown of the available options:

    backup_single_update
        Type: Boolean
        Default: True
        Whether or not to save a full backup when updating a single plugin.
        Note that as of `updater` version 0.1.0 saving a new backup means that you won't have access to the previous backup that was available.
    backup_all_update
        Type: Boolean
        Default: True
        Whether or not to save a full backup when updating all plugins at once.
        You will most likely want this to stay True.
    update_disabled_plugins
        Type: Boolean
        Default: False
        Whether or not to update the disabled plugins when the user hits the `Update All` button.
