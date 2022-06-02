#!/usr/bin/env python
import linuxcnc
import os
import hal
import hal_glib
import gtk
from gladevcp.persistence import IniFile,widget_defaults,set_debug,select_widgets

class HandlerClass:
	def _on_set_spindle_speed_change(self,hal_pin,data=None):
		#print "pin value changed to: %s" % (hal_pin.get())
		self.builder.get_object('hal_spindle_speed').set_target_value(float(hal_pin.get()))
		self.builder.get_object('hal_spindle_speed').queue_draw() # force a widget redraw

	def __init__(self, halcomp,builder,useropts):
		self.builder = builder
		self.halcomp = halcomp
		self.builder = builder
		self.useropts = useropts

		# hal pin with change callback.
		# When the pin's value changes the callback is executed.
		self.spindle_speed_target = hal_glib.GPin(halcomp.newpin('hal_spindle_speed_target',  hal.HAL_FLOAT, hal.HAL_IN))
		self.spindle_speed_target.connect('value-changed', self._on_set_spindle_speed_change)

		#inifile = linuxcnc.ini(os.getenv("INI_FILE_NAME"))
		#(directory,inifilename) = os.path.split(inifile)
		#tooltablefile = os.path.join(directory,inifile.find("EMCIO", "TOOL_TABLE"))
		#print tooltablefile
		#self.builder.get_object('tooltable_edit').set_filename(tooltablefile)

		self.builder.get_object('tooltable_edit').set_filename("tool.tbl")
		self.builder.get_object('tooltable_edit').set_visible("spxyacuvbw",False)

		#(directory,inifilename) = os.path.split(linuxcnc.ini(os.getenv("INI_FILE_NAME")))
		#(basename,extension) = os.path.splitext(inifilename)
		#self.ini_filename = os.path.join(directory,basename + '-glade.ini')
		#
		#self.defaults = {
			# the following names will be saved/restored as method attributes
			# the save/restore mechanism is strongly typed - the variables type will be derived from the type of the
			# initialization value. Currently supported types are: int, float, bool, string
		#	self.ini.vars : { 'glade_nhits' : 0, 'glade_a': 1.67, 'glade_d': True ,'glade_c' : "a string"},
			# to save/restore all widget's state which might remotely make sense, add this:
			#self.ini.widgets : widget_defaults(builder.get_objects())
			# a sensible alternative might be to retain only all HAL output widgets' state:
		#	self.ini.widgets: widget_defaults(select_widgets(self.builder.get_objects(), hal_only=True,output_only = True)),
		#	}

		#self.ini = IniFile(self.ini_filename,self.defaults,self.builder)
		#self.ini.restore_state(self)


	def on_destroy(self,obj,data=None):
		self.ini.save_state(self)

	def on_unix_signal(self,signum,stack_frame):
		print "on_unix_signal(): signal %d received, saving state" % (signum)
		self.ini.save_state(self)




def get_handlers(halcomp,builder,useropts):
	return [HandlerClass(halcomp,builder,useropts)]



# https://searchcode.com/file/99893375/configs/gladevcp/complex/complex.py

