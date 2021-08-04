from avaspec import * 


dev_handle = 0
pixels = 4096
wavelength = [0.0] * pixels


# stored data from the spectrometer
spectraldata = [0.0] * pixels
darkData = [0.0] * pixels
refData = [0.0] * pixels
transData = [0.0] * pixels
reflectData = [0.0] * pixels

# configuration data
cycle_time = 0.5
integration_time = 1
averages = 2
stopscanning = True
measureType = MeasConfigType()
identity = AvsIdentityType()
deviceConfig = DeviceConfigType()
highRes = False

# what plot you currently on
visGraph = 0

# continuous
continuous = False
config = False

# wavelength range
low = 21
high = pixels - 24

# deciding if certain graphs can be generated
darkTrue = False
refTrue = False