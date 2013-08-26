
#
# Imports some modules.
#

import sublime, sublime_plugin, os, time, locale

#
# Simple class to ask project name.
#

class PromptHeaderCommand(sublime_plugin.WindowCommand):
  def run(self):
   # label = "Type project name: "
    self.window.active_view().run_command("header",  {"project": ""})
    pass

  def on_done(self):
    try:
      self.window.active_view().run_command("header",  {"project": ""})
    except ValueError:
      pass


#
# Main class: create the 42-style header.
#

class HeaderCommand(sublime_plugin.TextCommand):

  #
  # Get comment type according language.
  # Only C / C++ as been test
  #

  def get_comment(self):
    comments = {}

    comments['Default']      = ['  ', '  ', '  ']
    comments['JavaScript']   = ['/**', ' *', ' */']
    comments['CSS']          = ['/**', ' *', ' */']
    comments['C++']          = ['/* ', '/* ', ' */']
    comments['Python']       = ['#', '#', '#']
    comments['CoffeeScript'] = ['#', '#', '#']
    comments['Ruby']         = ['#', '#', '#']
    comments['Makefile']     = ['##', '##', '##']
    comments['Perl']         = ['#!/usr/local/bin/perl -w', '##', '##']
    comments['ShellScript']  = ['#!/bin/sh', '##', '##']
    comments['HTML']         = ['<!--', ' ', '-->']
    comments['LaTeX']        = ['%%', '%%', '%%']
    comments['Lisp']         = [';;', ';;', ';;']
    comments['Java']         = ['//', '//', '//']
    comments['PHP']          = ['#!/usr/local/bin/php\n<?php', '//', '//']
    comments['Jade']         = ['//-', '//-', '//-']
    comments['Stylus']       = ['//', '//', '//']

    return comments[self.view.settings().get('syntax').split('/')[1]]

  #
  # Get file infos.
  #

  def get_file_infos(self):
    full = self.view.file_name().split('/')
    return [full.pop(), '/'.join(full)]    

  #
  # Get email
  #

  def get_mail(self):
    full = "  By: " + os.environ['USER'] + " <" + os.environ['USER'] + "@42.fr>"
    return full.ljust(48)

  #
  # Get date 42-formated (e.g 2013/12/21 23:42:00)
  #

  def get_date(self):

    return time.strftime("%Y/%m/%d %H:%M:%S by")

  #
  # Generate header.
  #


  def generate(self, project):

    header = ""
    comment = self.get_comment()
    f = self.get_file_infos()
    filename = f[0].ljust(50)
    created = "  Created: " + self.get_date() + " " + os.environ['USER']
    updated = "  Updated: " + self.get_date() + " " + os.environ['USER']

    modified_date_region = self.view.find('  Updated: ', 0)
    if modified_date_region:
        header += comment[1] + updated.ljust(50) + " ###   ########.fr      " + comment[2]
    else:
        header += comment[0] + '*'*74 + comment[2] + '\n'
        header += comment[1] + ' '*74 + comment[2] + '\n'
        header += comment[1] + ' '*55                 + ":::      ::::::::  " + comment[2] + '\n'
        header += comment[1] + "  " + filename     + " :+:      :+:    :+:  " + comment[2] + '\n'
        header += comment[1] + ' '*51             + "+:+ +:+         +:+    " + comment[2] + '\n'
        header += comment[1] + self.get_mail() + " +#+  +:+       +#+       " + comment[2] + '\n'
        header += comment[1] + ' '*47         + "+#+#+#+#+#+   +#+          " + comment[2] + '\n'
        header += comment[1] + created.ljust(50) + "  #+#    #+#            " + comment[2] + '\n'
        header += comment[1] + updated.ljust(50) + " ###   ########.fr      " + comment[2] + '\n'
        header += comment[1] + ' '*74 + comment[2] + '\n'
        header += comment[0] + '*'*74 + comment[2] + '\n'

    return header

  #
  # Run command.
  #

  def run(self, edit, project):
    modified_date_region = self.view.find('  Updated: ', 0)
    if modified_date_region:
        line = self.view.line(modified_date_region)
        self.view.replace(edit, line, self.generate(project))
    else:
        self.view.insert(edit, 0, self.generate(project))

    self.view.run_command('save')