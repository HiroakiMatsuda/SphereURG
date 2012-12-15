#!/usr/bin/env python
# -*- Python -*-

"""
 \file SphereURG.py
 \brief This component outputs a three-dimensional distance information by integrating a distance sensor and servo motor
 \date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sphereurg_spec = ["implementation_id", "SphereURG", 
		 "type_name",         "SphereURG", 
		 "description",       "This component outputs a three-dimensional distance information by integrating a distance sensor and servo motor", 
		 "version",           "1.0.0", 
		 "vendor",            "Matsuda Hiroaki", 
		 "category",          "SENSOR", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "0", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

class SphereURG(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class SphereURG
	\brief This component outputs a three-dimensional distance information by integrating a distance sensor and servo motor
	
	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_urg = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._urgIn = OpenRTM_aist.InPort("urg", self._d_urg)
		self._d_servo = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._servoIn = OpenRTM_aist.InPort("servo", self._d_servo)
		self._d_data = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._dataOut = OpenRTM_aist.OutPort("data", self._d_data)


		


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
		self.addInPort("urg",self._urgIn)
		self.addInPort("servo",self._servoIn)
		
		# Set OutPort buffers
		self.addOutPort("data",self._dataOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		self.flag = 0

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
		print('onDeactivated')
	
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		"""
	
		The execution action that is invoked periodically
		former rtc_active_do()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""

		if self._servoIn.isNew():
                                self._d_servo = self._servoIn.read()
                                angle = self._d_servo.data[1]

                                self.flag = 1
                                
                                if self._urgIn.isNew():

                                        if self.flag == 1:
                                
                                                self._d_urg = self._urgIn.read()
                                                                
                                                timestamp = self._d_urg.data[0]
                                                if self._d_urg.data[1] == 1:
                                                        dist = self._d_urg.data[3:]

                                                        self._d_data.data = [timestamp, angle, 1, len(dist)] + dist
                                                        OpenRTM_aist.setTimestamp(self._d_data)
                                                        self._dataOut.write()

                                                elif self._d_urg.data[1] == 2:
                                                        dist_length = self._d_urg.data[2]
                                                        dist = self._d_urg.data[4:dist_length + 4]
                                                        intens = self._d_urg.data[dist_length + 4:]

                                                        self._d_data.data = [timestamp, angle, 2, len(dist), len(intens)] + dist + intens
                                                        OpenRTM_aist.setTimestamp(self._d_data)
                                                        self._dataOut.write()

                                                self.flag = 0

		return RTC.RTC_OK

def SphereURGInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sphereurg_spec)
    manager.registerFactory(profile,
                            SphereURG,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    SphereURGInit(manager)

    # Create a component
    comp = manager.createComponent("SphereURG")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

