``visp_apriltag`` documentation
===============================

.. contents:: Table of Contents
  :depth: 3

Introduction
============

The ``visp_apriltag`` furnishes a node that is a wrapper over the ``vpDetectorAprilTag`` class of `ViSP <https://visp-doc.inria.fr/doxygen/visp-daily/classvpDetectorAprilTag.html>`__.
It permits to detect AprilTag and ArUco tags in an image.

The tracker can either be configured using a configuration file (see `BaseTracker documentation <../visp_tracker_common/index.html#related-to-the-tracking>`__ ) or through its parameters (see `Node parameters`_).

The node will publish a ``/<node_name>/tags_info``
topic that will contain information about the detected tags. See `the message definition <../visp_tracker_common/interfaces/msg/AprilTagDetection.html>`__ to see which information
are published.

Prerequisities
==============

Install ROS 2
-------------

Make sure your ROS 2 core environment is installed. Refer to the official
`ROS 2 documentation <https://docs.ros.org/>`__ to get started.

Install ViSP
------------

Please refer to the official installation instructions from the
`ViSP installation tutorials <https://visp-doc.inria.fr/doxygen/visp-daily/tutorial_install.html>`__.

.. Note::

  * Pre-built ViSP packages exist for Ubuntu (``libvisp-dev``) and ROS 2 (``ros2-<distro>-visp``), but they are usually
    built against a reduced number of third-party libraries. Consequently, you might miss advaFnced features required
    to control hardware (e.g., Franka robots), acquire images from RealSense cameras, or leverage the Panda3D
    dependency needed for the ``visp_apriltag`` package.
  * That's why **we strongly recommend building ViSP from source.**
    See `tutorials <https://visp-doc.inria.fr/doxygen/visp-daily/tutorial_install_src.html>`__.
  * After building ViSP from source, remember to set the ``VISP_DIR`` environment variable to your build directory,
    for example:

    .. code-block:: shell

      export VISP_DIR=$VISP_WS/visp-build


How to get and build visp_apriltag
==================================

Here we suppose that you have a ROS 2  workspace in ``~/colcon_ws/`` folder.

  * Clone the repository into your workspace source directory, checking out the branch corresponding to your
    ROS distribution:

    .. code-block:: shell

      cd ~/colcon_ws/src
      git clone -b $ROS_DISTRO https://github.com/lagadic/visp_tk.git
      cd ..

  * Install required ROS 2 dependencies via ``rosdep``:

    .. code-block:: shell

      rosdep update && rosdep install --from-paths src --ignore-src

  * Build the ``visp_apriltag`` package:

    .. code-block:: shell

      colcon build --symlink-install --packages-up-to visp_apriltag

    .. Note::

      If you encounter the following issue:

        .. code-block:: shell

          --- stderr: visp_apriltag
          CMake Error at CMakeLists.txt:46 (find_package):
            By not providing "FindVISP.cmake" in CMAKE_MODULE_PATH this project has
            asked CMake to find a package configuration file provided by "VISP", but
            CMake did not find one.

            Could not find a package configuration file provided by "VISP" (requested
            version 3.7) with any of the following names:

              VISPConfig.cmake
              visp-config.cmake

            Add the installation prefix of "VISP" to CMAKE_PREFIX_PATH or set
            "VISP_DIR" to a directory containing one of the above files.  If "VISP"
            provides a separate development package or SDK, be sure it has been
            installed.

      it means that ViSP is not found. Use ``VISP_DIR`` to point to ``$VISP_WS/visp-build`` folder like:

        .. code-block:: shell

          colcon build --symlink-install --packages-up-to visp_apriltag --cmake-args -DVISP_DIR=$VISP_WS/visp-build


Node parameters
===============

This section will present the different parameters of the node, that exist
in addition to the ones it inherits from the ``visp_tracker_common::BaseTracker`` class.
See `visp_tracker_common`_ documentation.

.. _visp_tracker_common: ../visp_tracker_common/index.html#basetracker-node

Related to the tag detection
----------------------------

- *OPTIONAL* ``tag_family``: if ``config_file`` is not set, this parameter becomes **REQUIRED**. It corresponds to the tag family the node will have to detect. See `ViSP documentation <https://visp-doc.inria.fr/doxygen/visp-daily/classvpDetectorAprilTag.html>`__ for more information.
- *OPTIONAL* ``detection_margin_thresh``: the detection margin threshold. See `ViSP documentation <https://visp-doc.inria.fr/doxygen/visp-daily/classvpDetectorAprilTag.html>`__ for more information.

Related to the pose computation
-------------------------------

- **REQUIRED** ``tag_size_keys``: it corresponds to the list of IDs of the tags for which ``tag_size_values`` will give the size. ``-1`` is a special key that means ``for all IDs that are not specified in this list``.
- **REQUIRED** ``tag_size_values``: it corresponds to the list of dimension of the tag for each IDs specified in ``tag_size_keys``, in meters. The first item of ``tag_size_values`` will be associated to the first ID listed in ``tag_size_keys`` and so on. The size listed at the same position than the ID ``-1`` in ``tag_size_keys`` will be used **for all IDs that are not specified in the** ``tag_size_keys`` **list**. See `ViSP documentation <https://visp-doc.inria.fr/doxygen/visp-daily/classvpDetectorAprilTag.html>`__ for more information.
- *OPTIONAL* ``pose_method``: if ``config_file`` is not set, this parameter becomes **REQUIRED**. It corresponds to the method to use to compute the pose of a tag. See `ViSP documentation <https://visp-doc.inria.fr/doxygen/visp-daily/classvpDetectorAprilTag.html>`__ for more information.
- *OPTIONAL* ``align_z``: if true, the Z-axis will be aligned with the Z-axis of the camera.
- *OPTIONAL* ``id_published``: if set, the node will publish the pose of the tag whose ID corresponds to this attribute
  in the pose topic inherited from the ``visp_tracker_common::BaseTracker`` class.

Related to display
------------------

- *OPTIONAL* ``display_tag``: if true, the tag borders will be displayed.

How to exploit the AprilTag detection?
======================================

When tags are detected in the image, an array of the ``AprilTagDetection`` message is published on the ``/<node_name>/tags_info``
topic:

.. literalinclude:: /_code/msg/AprilTagDetection.msg
  :linenos:

.. Note::

  If the message is not displayed, please refer to `the definition of the message present here. <../visp_tracker_common/interfaces/msg/AprilTagDetection.html>`__

The ``AprilTagDetectionArray`` has one such element for each detected tag.

.. Warning::

  If you are interested in the 3D pose of the tag with regard to the camera, please check the ``is_pose_valid`` field to
  check if the pose could actually be computed.

If you set ``id_published`` to a value different from -1, the pose of the desired ID will be published in the
pose topic inherited from the ``visp_tracker_common::BaseTracker`` class. If you set ``id_published`` to a value
different from -1  and no poses are published, please refer to the `Tips and Tricks: Tag pose not published`_ section.

.. Warning::

  Please keep in mind that the node does not check if several tags with the same ID than ``id_published`` are visible in
  the image. If that situation happens, the pose topic inherited from the ``visp_tracker_common::BaseTracker`` class
  will be filled by both poses alternatively and would not be usable.

Tips and Tricks: Tag pose not published
=======================================

Several clues can show that the poses are not computed:

  - If you set ``display_tag`` to ``true``, the tags borders are displayed but the frame is not projected in the image.
  - In the console, there are some error messages:

    .. code-block:: shell

      $ ros2 launch visp_tk_tutorials apriltag_tracker_live_v4l_launch.py
      ...
      [visp_apriltag_node-2] [INFO] [1790253340.305237753] [tracker_apriltag]: Receive image
      [visp_apriltag_node-2] [WARN] [1790253340.310646522] [tracker_apriltag]: Published RGB camera parameters are incorrect.
      [visp_apriltag_node-2] [WARN] [1790253340.340782250] [tracker_apriltag]: Published RGB camera parameters are incorrect.
      [visp_apriltag_node-2] [WARN] [1790253340.373742210] [tracker_apriltag]: Published RGB camera parameters are incorrect.
  - If you echo the topic ``/tracker_apriltag/tags_info``, you will see:

    .. code-block:: shell

      ...
      is_pose_valid: false
      pose:
          position:
          x: 0.0
          y: 0.0
          z: 0.0
          orientation:
          x: 0.0
          y: 0.0
          z: 0.0
          w: 1.0

It probably means:

  - that your camera is not calibrated. See for instance the documentation of the `camera_calibration package <https://docs.ros.org/en/rolling/p/camera_calibration/doc/tutorial_mono.html>`__ to see how to calibrate your camera.

  - or that you forgot to set the ``rgb_camera_info_topic_name`` parameter to subscribe to the camera parameters required for the pose computation.
