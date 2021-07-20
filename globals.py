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
integration_time = 1
averages = 2
stopscanning = True
first = True
measureType = MeasConfigType()
identity = AvsIdentityType()
deviceConfig = DeviceConfigType()

# what plot are you currently on
visGraph = 0

# continuous
continuous = False
config = False

# wavelength range
low = 21
high = pixels - 22