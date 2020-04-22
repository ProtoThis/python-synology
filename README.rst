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
        device_token=None,
        debugmode=False,
    )

``device_token`` should be added when using a two-step authentication account, otherwise DSM will ask to login with a One Time Password (OTP) and requests will fail (see the login section for more details).


Login
------

The library automatically login at first request, but you better use the ``login()`` function separately to authenticate.

It will return a boolean if it successed or faild to authenticate to DSM.

If your account need a two-step authentication (2SA), ``login()`` will raise ``SynologyDSMLogin2SARequiredException``.
Call the function again with a One Time Password (OTP) as parameter, like ``login("123456")`` (better to be a string to handle first zero).
Store the ``device_token`` property so that you do not need to reconnect with password the next time you open a new ``SynologyDSM`` session.


Code exemple
------------

.. code-block:: python

    from synology_dsm import SynologyDSM

    print("Creating Valid API")
    api = SynologyDSM("<SynologyIp>", "<SynologyPort>", "<Username>", "<Password>")

    print("=== Information ===")
    print("Model:           " + str(api.information.model))
    print("RAM:             " + str(api.information.ram) + " MB")
    print("Serial number:   " + str(api.information.serial))
    print("Temperature:     " + str(api.information.temperature) + " °C")
    print("Temp. warning:   " + str(api.information.temperature_warn))
    print("Uptime:          " + str(api.information.uptime))
    print("Full DSM version:" + str(api.information.version_string))

    print("=== Utilisation ===")
    print("CPU Load:        " + str(api.utilisation.cpu_total_load) + " %")
    print("Memory Use:      " + str(api.utilisation.memory_real_usage) + " %")
    print("Net Up:          " + str(api.utilisation.network_up()))
    print("Net Down:        " + str(api.utilisation.network_down()))
    
    print("=== Storage ===")
    for volume_id in api.storage.volumes_ids:
        print("ID:          " + str(volume_id))
        print("Status:      " + str(api.storage.volume_status(volume_id)))
        print("% Used:      " + str(api.storage.volume_percentage_used(volume_id)) + " %")

    for disk_id in api.storage.disks_ids:
        print("ID:          " + str(disk_id))
        print("Name:        " + str(api.storage.disk_name(disk_id)))
        print("S-Status:    " + str(api.storage.disk_smart_status(disk_id)))
        print("Status:      " + str(api.storage.disk_status(disk_id)))
        print("Temp:        " + str(api.storage.disk_temp(disk_id)))

Credits / Special Thanks
========================
- https://github.com/florianeinfalt
- https://github.com/tchellomello
- https://github.com/Quentame
- https://github.com/aaska
- https://github.com/chemelli74

Found Synology API "documentation" on this repo : https://github.com/kwent/syno/tree/master/definitions

Official references
===================

- `Calendar API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Calendar/2.4/enu/Synology_Calendar_API_Guide_enu.pdf>`_

- `Download Station API documentation (2012-2014) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/DownloadStation/All/enu/Synology_Download_Station_Web_API.pdf>`_

- `File Station API documentation (2013-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/FileStation/All/enu/Synology_File_Station_API_Guide.pdf>`_

- `Surveillance Station API documentation (2012-2020) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/SurveillanceStation/All/enu/Surveillance_Station_Web_API.pdf>`_

- `Virtual Machine Manager API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Virtualization/All/enu/Synology_Virtual_Machine_Manager_API_Guide.pdf>`_
