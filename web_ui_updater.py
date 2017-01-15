"""
web_ui_updater.py
"""
import os
import gossip
from flask import render_template_string
from eva import conf
from eva import scheduler

BACKUP_SINGLE_UPDATE = conf['plugins']['web_ui_updater']['config']['backup_single_update']
BACKUP_ALL_UPDATE = conf['plugins']['web_ui_updater']['config']['backup_all_update']
UPDATE_DISABLED_PLUGINS = conf['plugins']['web_ui_updater']['config']['update_disabled_plugins']

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
UPDATE_PLUGIN_MARKUP = open(DIR_PATH + '/templates/update_plugin.html').read()
UPDATE_ALL_MARKUP = open(DIR_PATH + '/templates/update_all.html').read()
CHECK_FOR_UPDATES_MARKUP = open(DIR_PATH + '/templates/check_for_updates.html').read()
UNDO_PREVIOUS_UPDATE_MARKUP = open(DIR_PATH + '/templates/undo_previous_update.html').read()

@gossip.register('eva.web_ui.start', provides=['web_ui_updater'])
def web_ui_start(app):
    """
    todo
    """
    app.add_url_rule('/plugins/update/<plugin_id>', 'update_plugin', update_plugin)
    app.add_url_rule('/plugins/update-all', 'update_all', update_all)
    app.add_url_rule('/plugins/check-for-updates', 'check_for_updates', check_for_updates)
    app.add_url_rule('/plugins/rollback', 'undo_previous_update', undo_previous_update)

@gossip.register('eva.web_ui_plugins.plugins_columns', provides=['web_ui_updater'])
def web_ui_plugins_plugins_columns(plugins_cols):
    """
    todo
    """
    plugins_cols.append('Status')

@gossip.register('eva.web_ui_plugins.plugins_row', provides=['web_ui_updater'])
def web_ui_plugins_row(plugin_id, row_data):
    """
    todo
    """
    state = conf['plugins']['updater']['module'].get_state(plugin_id)
    if state == conf['plugins']['updater']['module'].BEHIND:
        row_data.append('<a class="btn btn-warning" \
                            href="/plugins/update/%s">Update</a>' %plugin_id)
    else: row_data.append(state)

@gossip.register('eva.web_ui_plugins.pre_plugins_table_markup')
def web_ui_plugins_pre_plugins_table_markup(pre_plugins_table_markup):
    """
    todo
    """
    check_class = 'class="btn btn-success"'
    rollback_class = 'class="btn btn-warning"'
    style = 'style="float: right;"'
    check_href = 'href="/plugins/check-for-updates"'
    rollback_href = 'href="/plugins/rollback"'
    markup = '<div %s><a %s %s>Check For Updates</a> <a %s %s>Undo Last Update</a></div><br />' \
             %(style, check_class, check_href, rollback_class, rollback_href)
    pre_plugins_table_markup.append(markup)

@gossip.register('eva.web_ui_plugins.post_plugins_table_markup')
def web_ui_plugins_post_plugins_table_markup(post_plugins_table_markup): #pylint: disable=C0103
    """
    todo
    """
    _class = 'class="btn btn-info"'
    style = 'style="float: right;"'
    href = 'href="/plugins/update-all"'
    markup = '<a %s %s %s>Update All</a><br />' %(_class, style, href)
    post_plugins_table_markup.append(markup)

def update_plugin(plugin_id):
    """
    todo
    """
    conf['plugins']['updater']['module'].update_plugin(plugin_id, BACKUP_SINGLE_UPDATE)
    plugin_name = conf['plugins'][plugin_id]['info']['name']
    if conf['plugins']['updater']['module'].is_updated(plugin_id):
        success = '%s updated successfully' %plugin_name
        error = None
    else:
        success = None
        error = '%s could not be updated - see logs for more details' %plugin_name
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    return render_template_string(UPDATE_PLUGIN_MARKUP,
                                  plugin_name=plugin_name,
                                  menu_items=menu_items,
                                  success=success,
                                  error=error)

def update_all():
    """
    todo
    """
    update_all_plugins = conf['plugins']['updater']['module'].update_all_plugins
    scheduler.add_job(update_all_plugins,
                      args=(BACKUP_ALL_UPDATE,
                            UPDATE_DISABLED_PLUGINS,
                            True),
                      id='web_ui_updater_update_all')
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    return render_template_string(UPDATE_ALL_MARKUP, menu_items=menu_items)

def check_for_updates():
    """
    todo
    """
    update_check = conf['plugins']['updater']['module'].update_check
    scheduler.add_job(update_check, id='web_ui_updater_update_check')
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    success = 'Note that this is currently \
               <a href="/plugins/configuration/updater">configured</a> \
               to run automatically every %s hours.' \
               %conf['plugins']['updater']['config']['update_check_interval']
    return render_template_string(CHECK_FOR_UPDATES_MARKUP,
                                  menu_items=menu_items,
                                  success=success)

def undo_previous_update():
    """
    todo
    """
    if not conf['plugins']['updater']['module'].rollback_available():
        error = 'Nothing to rollback'
    else:
        error = None
        conf['plugins']['updater']['module'].rollback(reboot=False)
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    return render_template_string(UNDO_PREVIOUS_UPDATE_MARKUP,
                                  menu_items=menu_items,
                                  error=error)
