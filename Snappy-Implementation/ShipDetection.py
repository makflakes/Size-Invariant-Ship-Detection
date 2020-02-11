import snappy
from snappy import ProductIO
from snappy import HashMap
import os, gc
from snappy import GPF
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')

import time
start = time.time()
path = "path into SAR extracted folder"
gc.enable()
output = path  + "/"
print(output)
#Then, read in the Sentinel-1 data product:
sentinel_1 = ProductIO.readProduct(output + "/manifest.safe")
print sentinel_1
pols = ['VH','VV']
for p in pols:
    polarization = p
    # APPLY ORBIT FILE
    parameters = HashMap()
    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', '3')
    parameters.put('continueOnFail', 'false')
    s1_orbit_applied = GPF.createProduct('Apply-Orbit-File', parameters, sentinel_1)
    file_prefix=output + "_orbit_applied_"+polarization
    ProductIO.writeProduct(s1_orbit_applied,file_prefix,'BEAM-DIMAP')
    del parameters
    # LAND-SEA-MASK
    orbit = ProductIO.readProduct(file_prefix + ".dim")
    parameters = HashMap()
    parameters.put('useSRTM', True)
    parameters.put('landMask', True)
    parameters.put('shorelineExtension','10')
    parameters.put('sourceBands', 'Intensity_' + polarization)
    s1_landseamask = result = GPF.createProduct('Land-Sea-Mask', parameters, orbit)
    mask_prefix=output + "_land-sea-mask_"+polarization
    ProductIO.writeProduct(s1_landseamask,mask_prefix,'BEAM-DIMAP')
    del parameters
    # CALIBRATION
    masked = ProductIO.readProduct(mask_prefix + ".dim")
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Intensity_' + polarization)
    parameters.put('selectedPolarisations', polarization)
    #parameters.put('outputImageScaleInDb', True)
    calib_applied = output + "_calibrate_" + polarization
    s1_calibrated = GPF.createProduct("Calibration", parameters, masked)
    ProductIO.writeProduct(s1_calibrated, calib_applied, 'BEAM-DIMAP')
    del parameters
    # ADAPTIVETHRESHOLDING
    calibration = ProductIO.readProduct(calib_applied + ".dim")
    parameters = HashMap()
    parameters.put('targetWindowSizeInMeter','30')
    parameters.put('guardWindowSizeInMeter','500.0')
    parameters.put('backgroundWindowSizeInMeter','800.0')
    parameters.put('pfa','12.5')
    adapt_thresh_prefix = output + "_adapt-thresh_" + polarization
    adapt_thresh = GPF.createProduct("AdaptiveThresholding", parameters, calibration)
    ProductIO.writeProduct(adapt_thresh, adapt_thresh_prefix, 'BEAM-DIMAP')
    del parameters
    # Object-Discrimination
    adaptThreshold = ProductIO.readProduct(adapt_thresh_prefix + ".dim")
    parameters = HashMap()
    parameters.put('minTargetSizeInMeter','30')
    parameters.put('maxTargetSizeInMeter','600')
    objdisc_prefix = output + "_obj-discrimination_" + polarization
    objdisc = GPF.createProduct("Object-Discrimination", parameters, adaptThreshold)
    ProductIO.writeProduct(objdisc, objdisc_prefix, 'BEAM-DIMAP')
    del parameters
    # Write 1
    obj_disc = ProductIO.readProduct(objdisc_prefix + ".dim")
    parameters = HashMap()
    parameters.put('file','${outputproduct1}')
    #parameters.put('formatName','CSV')
    write_1_prefix = output + "_prod_1_" + polarization
    write_1 = GPF.createProduct("Write", parameters, obj_disc)
    ProductIO.writeProduct(write_1, write_1_prefix, 'BEAM-DIMAP')
    del parameters
    # Write 2
    obj_disc = ProductIO.readProduct(objdisc_prefix + ".dim")
    parameters = HashMap()
    parameters.put('file','${outputproduct2}')
    #parameters.put('formatName','Geotiff')
    write_2_prefix = output + "_prod_2_" + polarization
    write_2 = GPF.createProduct("Write", parameters, obj_disc)
    ProductIO.writeProduct(write_2, write_2_prefix, 'GeoTIFF')
    del parameters
