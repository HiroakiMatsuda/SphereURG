#!/usr/bin/env python
# -*- Python -*-

"""
 \file SphereURGViewer.py
 \brief ModuleDescription
 \date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import suviewer

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sphereurgviewer_spec = ["implementation_id", "SphereURGViewer", 
		 "type_name",         "SphereURGViewer", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Matsuda Hiroaki", 
		 "category",          "VIEWER", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "0", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

class SphereURGViewer(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class SphereURGViewer
	\brief ModuleDescription
	
	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_data = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._dataIn = OpenRTM_aist.InPort("data", self._d_data)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	def onInitialize(self):
		"""
		
		The initialize action (on CREATED->ALIVE transition)
		formaer rtc_init_entry() 
		
		\return RTC::ReturnCode_t
		
		"""
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("data",self._dataIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		print('onInitialize')
		
		return RTC.RTC_OK
	

	
	def onActivated(self, ec_id):
		"""
	
		The activated action (Active state entry action)
		former rtc_active_entry()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""

		print('onActivated')
	
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		"""
	
		The deactivated action (Active state exit action)
		former rtc_active_exit()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""

		print('onDactivated')
	
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		"""
	
		The execution action that is invoked periodically
		former rtc_active_do()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""

		if self._dataIn.isNew():
                        self.read_data()
	
		return RTC.RTC_OK

	def read_data(self):
                self._d_data = self._dataIn.read()
                return self._d_data.data
	

def SphereURGViewerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sphereurgviewer_spec)
    manager.registerFactory(profile,
                            SphereURGViewer,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    SphereURGViewerInit(manager)

    # Create a component
    comp = manager.createComponent("SphereURGViewer")

def main():
        view = suviewer.Viewer()
        view.plot()   
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.activateManager()
	# Register component
	profile = OpenRTM_aist.Properties(defaults_str=sphereurgviewer_spec)
	mgr.registerFactory(profile,
                            SphereURGViewer,
                            OpenRTM_aist.Delete)
	comp = mgr.createComponent("SphereURGViewer")
	view.get_in_port(comp.read_data)
	mgr.runManager(True)
	view.show()
	

if __name__ == "__main__":
	main()

