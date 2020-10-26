===========================
Python API for Synology DSM
===========================

.. image:: https://travis-ci.org/ProtoThis/python-synology.svg?branch=master
    :target: https://travis-ci.org/ProtoThis/python-synology

.. image:: https://img.shields.io/pypi/v/python-synology.svg
    :alt: Library version
    :target: https://pypi.org/project/python-synology

.. image:: https://img.shields.io/pypi/pyversions/python-synology.svg
    :alt: Supported versions
    :target: https://pypi.org/project/python-synology

.. image:: https://pepy.tech/badge/python-synology
    :alt: Downloads
    :target: https://pypi.org/project/python-synology

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Formated with Black
    :target: https://github.com/psf/black


Installation
============

.. code-block:: bash

    [sudo] pip install python-synology


Usage
=====

You can import the module as `synology_dsm`.


Constructor
-----------

.. code-block:: python

    SynologyDSM(
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        verify_ssl=False,
        timeout=None,
        device_token=None,
        debugmode=False,
    )

``device_token`` should be added when using a two-step authentication account, otherwise DSM will ask to login with a One Time Password (OTP) and requests will fail (see the login section for more details).

Default ``timeout`` is 10 seconds.


Login
------

The library automatically login at first request, but you better use the ``login()`` function separately to authenticate.

It will return a boolean if it successed or faild to authenticate to DSM.

If your account need a two-step authentication (2SA), ``login()`` will raise ``SynologyDSMLogin2SARequiredException``.
Call the function again with a One Time Password (OTP) as parameter, like ``login("123456")`` (better to be a string to handle first zero).
Store the ``device_token`` property so that you do not need to reconnect with password the next time you open a new ``SynologyDSM`` session.


Code exemple
------------

Every API has an ``update()`` function that is needed to get the first data, then the data is cached and updated at the next ``update()`` call.

The ``SynologyDSM`` class can also ``update()`` all APIs at once.

.. code-block:: python

    from synology_dsm import SynologyDSM

    print("Creating Valid API")
    api = SynologyDSM("<IP/DNS>", "<port>", "<username>", "<password>")

    print("=== Information ===")
    api.information.update()
    print("Model:           " + str(api.information.model))
    print("RAM:             " + str(api.information.ram) + " MB")
    print("Serial number:   " + str(api.information.serial))
    print("Temperature:     " + str(api.information.temperature) + " °C")
    print("Temp. warning:   " + str(api.information.temperature_warn))
    print("Uptime:          " + str(api.information.uptime))
    print("Full DSM version:" + str(api.information.version_string))
    print("--")

    print("=== Utilisation ===")
    api.utilisation.update()
    print("CPU Load:        " + str(api.utilisation.cpu_total_load) + " %")
    print("Memory Use:      " + str(api.utilisation.memory_real_usage) + " %")
    print("Net Up:          " + str(api.utilisation.network_up()))
    print("Net Down:        " + str(api.utilisation.network_down()))
    print("--")

    print("=== Storage ===")
    api.storage.update()
    for volume_id in api.storage.volumes_ids:
        print("ID:          " + str(volume_id))
        print("Status:      " + str(api.storage.volume_status(volume_id)))
        print("% Used:      " + str(api.storage.volume_percentage_used(volume_id)) + " %")
        print("--")

    for disk_id in api.storage.disks_ids:
        print("ID:          " + str(disk_id))
        print("Name:        " + str(api.storage.disk_name(disk_id)))
        print("S-Status:    " + str(api.storage.disk_smart_status(disk_id)))
        print("Status:      " + str(api.storage.disk_status(disk_id)))
        print("Temp:        " + str(api.storage.disk_temp(disk_id)))
        print("--")

    print("=== Shared Folders ===")
    api.share.update()
    for share_uuid in api.share.shares_uuids:
        print("Share name:        " + str(api.share.share_name(share_uuid)))
        print("Share path:        " + str(api.share.share_path(share_uuid)))
        print("Space used:        " + str(api.share.share_size(share_uuid, human_readable=True)))
        print("Recycle Bin Enabled: " + str(api.share.share_recycle_bin(share_uuid)))
        print("--")


Download Station usage
--------------------------

.. code-block:: python

    from synology_dsm import SynologyDSM

    api = SynologyDSM("<IP/DNS>", "<port>", "<username>", "<password>")

    if "SYNO.DownloadStation.Info" in api.apis:

        api.download_station.get_info()
        api.download_station.get_config()

        # The download list will be updated after each of the following functions:
        # You should have the right on the (default) directory that the download will be saved, or you will get a 403 or 406 error
        api.download_station.create("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
        api.download_station.pause("dbid_1")
        # Like the other function, you can eather pass a str or a list
        api.download_station.resume(["dbid_1", "dbid_2"])
        api.download_station.delete("dbid_3")

        # Manual update
        api.download_station.update()


Surveillance Station usage
--------------------------

.. code-block:: python

    from synology_dsm import SynologyDSM

    api = SynologyDSM("<IP/DNS>", "<port>", "<username>", "<password>")
    surveillance = api.surveillance_station
    surveillance.update() # First update is required

    # Returns a list of cached cameras available
    cameras = surveillance.get_all_cameras()

    # Assuming there's at least one camera, get the first camera_id
    camera_id = cameras[0].camera_id

    # Returns cached camera object by camera_id
    camera = surveillance.get_camera(camera_id)

    # Returns cached motion detection enabled
    motion_setting = camera.is_motion_detection_enabled

    # Return bytes of camera image
    surveillance.get_camera_image(camera_id)

    # Updates all cameras/motion settings and cahce them
    surveillance.update()

    # Gets Home Mode status
    home_mode_status =  surveillance.get_home_mode_status()

    # Sets home mode - true is on, false is off
    surveillance.set_home_mode(True)


System usage
--------------------------

.. code-block:: python

    from synology_dsm import SynologyDSM

    api = SynologyDSM("<IP/DNS>", "<port>", "<username>", "<password>")
    system = api.system

    # Reboot NAS
    system.reboot()

    # Shutdown NAS
    system.shutdown()

    # Manual update system information
    system.update()

    # Get CPU information
    system.cpu_clock_speed
    system.cpu_cores
    system.cpu_family
    system.cpu_series

    # Get NTP settings
    system.enabled_ntp
    system.ntp_server

    # Get system information
    system.firmware_ver
    system.model
    system.ram_size
    system.serial
    system.sys_temp
    system.time
    system.time_zone
    system.time_zone_desc
    system.up_time

    # Get list of all connected USB devices
    system.usb_dev


Upgrade usage
--------------------------

.. code-block:: python

    from synology_dsm import SynologyDSM

    api = SynologyDSM("<IP/DNS>", "<port>", "<username>", "<password>")
    upgrade = api.upgrade

    # Manual update upgrade information
    upgrade.update()

    # check if DSM update is available
    if upgrade.update_available:
        do something ...

    # get available version string (return None if no update available)
    upgrade.available_version

    # get need of reboot (return None if no update available)
    upgrade.reboot_needed

    # get need of service restarts (return None if no update available)
    upgrade.service_restarts


Credits / Special Thanks
========================
- https://github.com/florianeinfalt
- https://github.com/tchellomello
- https://github.com/Quentame   (Multiple API addition & tests)
- https://github.com/aaska      (DSM 5 tests)
- https://github.com/chemelli74 (2SA tests)
- https://github.com/snjoetw    (Surveillance Station library)
- https://github.com/shenxn     (Surveillance Station tests)
- https://github.com/Gestas     (Shared Folders)

Found Synology API "documentation" on this repo : https://github.com/kwent/syno/tree/master/definitions


Official references
===================

- `Calendar API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Calendar/2.4/enu/Synology_Calendar_API_Guide_enu.pdf>`_

- `Download Station API documentation (2012-2014) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/DownloadStation/All/enu/Synology_Download_Station_Web_API.pdf>`_

- `File Station API documentation (2013-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/FileStation/All/enu/Synology_File_Station_API_Guide.pdf>`_

- `Surveillance Station API documentation (2012-2020) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/SurveillanceStation/All/enu/Surveillance_Station_Web_API.pdf>`_

- `Virtual Machine Manager API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Virtualization/All/enu/Synology_Virtual_Machine_Manager_API_Guide.pdf>`_
