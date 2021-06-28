from avaspec import * 


dev_handle = 0
pixels = 4096
wavelength = [0.0] * 4096


# stored data from the spectrometer
spectraldata = [0.0] * 4096
darkData = [0.0] * 4096
refData = [0.0] * 4096
transData = [0.0] * 4096
reflectData = [0.0] * 4096

# configuration data
max = 0
integration_time = 1
averages = 2
stopscanning = True
first = True
measureType = MeasConfigType()
identity = AvsIdentityType()
deviceConfig = DeviceConfigType()

# what plot are you currently on
visGraph = 0