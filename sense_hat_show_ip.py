"""
Simple utility to show IP address on Sense Hat display

The intended usage is as a program that can be included during startup
of a Raspberry Pi with Sense Hat attached, enabling the Pi to announce
its' IP address so that a remote system can use the IP address to
connect to it (using ssh etc). The program logic relies on the target
address (some_external_address) being routable, so if you're running
this on a network not connected to the Internet or lacking a default
route you'll need to alter some_external_address to an address that
the Pi can reach on your network.

It should be helpful for workshops using Raspberry Pis with Sense Hats
allowing the Pis to be used 'headless' via ssh - which is what I wrote
this utility for.

Here's how to get this program to run at startup-time on the Pi,

  * Place the program in ``/home/pi`` on the Pi [SD card]
  * Edit ``/etc/rc.local`` (put this line just before the final ``exit 0``),

    python3 /home/pi/sense_hat_show_ip.py 2>/var/log/hatlog.txt

(logging helpful for troubleshooting: If it doesn't work for you,
checkout the contents of ``/var/log/hatlog.txt``).

The above instructions work with the latest (2015-09-24) version of
Raspbian from https://www.raspberrypi.org/downloads/raspbian/ which
already includes the sense_hat and pygame libraries used by the
program. Note that the program should work with Python 2 or 3.

License: Gnu Public License v3,
http://www.gnu.org/licenses/gpl-3.0.html
this should also be provided as a text file along with this program;
contact the author if you need a different license.

Andrew Richards 2015
http://free.acrconsulting.co.uk/
--------------------------------------------------------------------------
"""

import sys, socket, sense_hat, pygame

sense = sense_hat.SenseHat()


class _IP(object):  # (object) for Python2-compatibility

    @property
    def IP_address(self):
        """Get IP address: Returns either a string containing the IP
        address or the special value None.
        """
        try:
            s = socket.socket(self.socket_family, socket.SOCK_DGRAM)
            s.connect(self.some_external_address)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

    def display_IP_address(self):
        """Print IP address on Sense Hat display"""
        sense.show_message(self.description + ": " + str(self.IP_address))


class IPv4(_IP):
    # I think no actual network communication occurs, so the actual value
    # of some_external_address is moot unless unroutable,
    some_external_address = ('198.41.0.4', 53)  # a.root-servers.net
    socket_family = socket.AF_INET
    description = "IPv4"


class IPv6(_IP):
    # I think no actual network communication occurs, so the actual value
    # of some_external_address is moot unless unroutable,
    some_external_address = ('2001:503:ba3e::2:30', 53)  # a.root-servers.net
    socket_family = socket.AF_INET6
    description = "IPv6"


def stop_requested():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            return True
    return False


def main_loop():
    sense.clear()
    # pygame.display not used, but needed to capture keyboard events
    pygame.display.set_mode((1, 1))
    try:
        while True:
            # Get IP address on each iteration since its value may change
            IPv4().display_IP_address()
            if stop_requested():
                return
            IPv6().display_IP_address()
            if stop_requested():
                return
            # sense.show_message("...Press joystick button to quit...")
            # if stop_requested():
            #    return
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main_loop()
    sense.clear()
