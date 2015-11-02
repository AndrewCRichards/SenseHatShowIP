# SenseHatShowIP
Small program for the Raspberry Pi with Sense Hat: Displays IP address
on the Sense Hat, useful for headless operation esp. for events like
training workshops

## Purpose
The intended usage is as a program that can be included during startup
of a Raspberry Pi with Sense Hat attached, enabling the Pi to announce
its' IP address so that a remote system can use the IP address to
connect to it (using ssh etc). The program logic relies on the target
address in external_IP_and_port being routable, so if you're running
this on a network not connected to the Internet or lacking a default
route you'll need to alter external_IP_and_port to use an address that
the Pi can reach on your network.

It should be helpful for workshops using Raspberry Pis with Sense Hats
allowing the Pis to be used 'headless' via ssh - which is what I wrote
this utility for.

## Usage
Here's how to get this program to run at startup-time on the Pi,

  * Place the program in ``/home/pi`` on the Pi [SD card]
  * Edit ``/etc/rc.local`` (put this line just before the final ``exit 0``),

        python3 /home/pi/sense_hat_show_ip.py 2>/var/log/hatlog.txt

(logging helpful for troubleshooting: If it doesn't work for you,
checkout the contents of ``/var/log/hatlog.txt``).

The above instructions work with the latest (2015-09-24) version of
Raspbian from https://www.raspberrypi.org/downloads/raspbian/ which
already includes the Python libraries used by the program. Note
that the program should work with Python 2.6 upwards or 3.

## Different versions
There are 2 versions of the program using ``pygame`` and ``threading``
libraries respectively.

The initial version I wrote uses ``pygame`` for keyboard monitoring (esp.
the Sense Hat joystick which is mapped to the keyboard) - allowing
the user to press the joystick button to stop the program. I then
wrote a version using threading which is more responsive to the
joystick button (scrolling message stops straightaway) and doesn't
need X to be running on the console. Both versions
are available in the GitHub repository as branches: ``pygame_version``
and ``threading_version``; the default version (``master``) is
``threading_version``.

## License
Gnu Public License v3,
http://www.gnu.org/licenses/gpl-3.0.html
this should also be provided as a text file along with this program;
contact the author if you need a different license.

## Author
Andrew Richards 2015

http://free.acrconsulting.co.uk/
