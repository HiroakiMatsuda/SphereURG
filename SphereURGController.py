#!/usr/bin/env python
# -*- Python -*-

"""
 \file SphereURGController.py
 \brief SERVO
 \date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import time
import ConfigParser as Conf

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
sphereurgcontroller_spec = ["implementation_id", "SphereURGController", 
		 "type_name",         "SphereURGController", 
		 "description",       "SERVO", 
		 "version",           "1.0.0", 
		 "vendor",            "Matsuda Hiroaki", 
		 "category",          "SERVO", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "0", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

class SphereURGController(OpenRTM_aist.DataFlowComponentBase):
	
	"""
	\class SphereURGController
	\brief SERVO
	
	"""
	def __init__(self, manager):
		"""
		\brief constructor
		\param manager Maneger Object
		"""
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_command = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._commandIn = OpenRTM_aist.InPort("command", self._d_command)
		self._d_urg = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._urgOut = OpenRTM_aist.OutPort("urg", self._d_urg)
		self._d_motion = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._motionOut = OpenRTM_aist.OutPort("motion", self._d_motion)
		self._d_on_off = RTC.TimedLongSeq(RTC.Time(0,0),[])
		"""
		"""
		self._on_offOut = OpenRTM_aist.OutPort("on_off", self._d_on_off)
		


		


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
		self.addInPort("command",self._commandIn)
		
		# Set OutPort buffers
		self.addOutPort("urg",self._urgOut)
		self.addOutPort("motion",self._motionOut)
		self.addOutPort("on_off",self._on_offOut)
		
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

		# Read ini file
		self.conf = Conf.SafeConfigParser()
                self.conf.read('ini/sucontrol.ini')
                
		self.servo_id = int(self.conf.get('SERVO', 'id'))
		self.servo_initial_pos = int(self.conf.get('SERVO', 'initial_pos'))
		self.servo_offset = int(self.conf.get('SERVO', 'offset'))
		self.cw_angle = int(self.conf.get('SERVO', 'cw_angle'))
		self.ccw_angle = int(self.conf.get('SERVO', 'ccw_angle'))
		self.move_time = int(self.conf.get('SERVO', 'move_time'))
		self.margin_time = int(self.conf.get('SERVO', 'margin_time'))

                # Calc Move Time
		self.move_time_cw = abs(self.move_time * self.cw_angle / 100)
                self.move_time_ccw = abs(self.move_time * self.ccw_angle / 100)

		# Servo Motor: Torque ON
		self._d_on_off.data = [0, self.servo_id, 1]
                OpenRTM_aist.setTimestamp(self._d_on_off)
                self._on_offOut.write()

                print('Servo: Torque ON')

                # Servo Motor: Move position 0
                self._d_motion.data = [0, self.servo_id,
                                       self.servo_offset + self.servo_initial_pos, 100]
                OpenRTM_aist.setTimestamp(self._d_motion)
                self._motionOut.write()
                print('Servo: Move Initial Position')

                # URG: Measurement start
                self._d_urg.data = [1]
                OpenRTM_aist.setTimestamp(self._d_urg)
                self._urgOut.write()

                time.sleep(2)
                
                print('URG: Measurement Start')

                print('onActivated')
	
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		"""
	
		The deactivated action (Active state exit action)
		former rtc_active_exit()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
		
		# Servo Motor: Torque OFF
		self._d_on_off.data = [0, self.servo_id, 0]
                OpenRTM_aist.setTimestamp(self._d_on_off)
                self._on_offOut.write()

		# URG: Measurement stop
		self._d_urg.data = [0]
                OpenRTM_aist.setTimestamp(self._d_urg)
                self._urgOut.write()

                print('onDeactivated')
	
		return RTC.RTC_OK
	
	def onExecute(self, ec_id):
		"""
	
		The execution action that is invoked periodically
		former rtc_active_do()
	
		\param ec_id target ExecutionContext Id
	
		\return RTC::ReturnCode_t
	
		"""
		if self._commandIn.isNew():
                                self._d_command = self._commandIn.read()
                                if self._d_command.data[0] == 2:
                                        self.cw_angle = self._d_command.data[1]
                                        self.ccw_angle = self._d_command.data[2]
                                        self.move_time = self._d_command.data[3]

                # Servo: Moving CW
                self._d_motion.data = [0, self.servo_id,
                                       self.servo_offset + self.ccw_angle, self.move_time_ccw]
                OpenRTM_aist.setTimestamp(self._d_motion)
                self._motionOut.write()
                time.sleep(self.move_time_ccw / 100.0 + self.margin_time / 1000.0)

                # Servo: Moving CCW
                self._d_motion.data = [0, self.servo_id,
                                       self.servo_offset + self.cw_angle, self.move_time_cw]
                OpenRTM_aist.setTimestamp(self._d_motion)
                self._motionOut.write()
                time.sleep(self.move_time_cw / 100.0 + self.margin_time / 1000.0)
            
	
		return RTC.RTC_OK

def SphereURGControllerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=sphereurgcontroller_spec)
    manager.registerFactory(profile,
                            SphereURGController,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    SphereURGControllerInit(manager)

    # Create a component
    comp = manager.createComponent("SphereURGController")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

