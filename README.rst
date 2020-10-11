Python API for Synology DSM
===========================

|PyPI| |Python Version| |Downloads| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/python-synology.svg
   :target: https://pypi.org/project/python-synology
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/python-synology
   :target: https://pypi.org/project/python-synology
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/python-synology
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/python-synology/latest.svg?label=Read%20the%20Docs
   :target: https://python-synology.readthedocs.io/
   :alt: Read the documentation at https://python-synology.readthedocs.io/
.. |Tests| image:: https://github.com/ProtoThis/python-synology/workflows/Tests/badge.svg
   :target: https://github.com/ProtoThis/python-synology/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/ProtoThis/python-synology/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ProtoThis/python-synology
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |Downloads| image:: https://pepy.tech/badge/python-synology
    :alt: Downloads
    :target: https://pypi.org/project/python-synology


Features
--------

Python API for communication with Synology DSM


Requirements
------------

* TODO


Installation
------------

You can install *Python API for Synology DSM* via pip_ from PyPI_:

.. code:: console

   $ pip install python-synology


Usage
-----

You can import the module as `synology_dsm`.

Constructor
^^^^^^^^^^^

.. code-block:: python

    SynologyDSM(
        dsm_ip,
        dsm_port,
        username,
        password,
        use_https=False,
        timeout=None,
        device_token=None,
        debugmode=False,
    )

``device_token`` should be added when using a two-step authentication account, otherwise DSM will ask to login with a One Time Password (OTP) and requests will fail (see the login section for more details).

Default ``timeout`` is 10 seconds.


Login
^^^^^

The library automatically login at first request, but you better use the ``login()`` function separately to authenticate.

It will return a boolean if it successed or faild to authenticate to DSM.

If your account need a two-step authentication (2SA), ``login()`` will raise ``SynologyDSMLogin2SARequiredException``.
Call the function again with a One Time Password (OTP) as parameter, like ``login("123456")`` (better to be a string to handle first zero).
Store the ``device_token`` property so that you do not need to reconnect with password the next time you open a new ``SynologyDSM`` session.


Code exemple
^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^

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



Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*Python API for Synology DSM* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits / Special Thanks
------------------------

- https://github.com/florianeinfalt
- https://github.com/tchellomello
- https://github.com/Quentame   (Multiple API addition & tests)
- https://github.com/aaska      (DSM 5 tests)
- https://github.com/chemelli74 (2SA tests)
- https://github.com/snjoetw    (Surveillance Station library)
- https://github.com/shenxn     (Surveillance Station tests)
- https://github.com/Gestas     (Shared Folders)

Found Synology API "documentation" on this repo : https://github.com/kwent/syno/tree/master/definitions

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

Official references
-------------------

- `Calendar API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Calendar/2.4/enu/Synology_Calendar_API_Guide_enu.pdf>`_

- `Download Station API documentation (2012-2014) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/DownloadStation/All/enu/Synology_Download_Station_Web_API.pdf>`_

- `File Station API documentation (2013-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/FileStation/All/enu/Synology_File_Station_API_Guide.pdf>`_

- `Surveillance Station API documentation (2012-2020) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/SurveillanceStation/All/enu/Surveillance_Station_Web_API.pdf>`_

- `Virtual Machine Manager API documentation (2015-2019) <https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/Virtualization/All/enu/Synology_Virtual_Machine_Manager_API_Guide.pdf>`_


.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/ProtoThis/hypermodern-python-test/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
