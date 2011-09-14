# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php or see LICENSE file.
# Copyright 2007-2008 Brisa Team <brisa-develop@garage.maemo.org>

# modified by Guido De Rosa

import time

from brisa.core.reactors import SelectReactor
reactor = SelectReactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function


devices = []


def on_new_device(dev):
    print 'Got new device:', dev

    if dev.udn not in [d.udn for d in devices]:
        devices.append(dev)


def on_removed_device(udn):
    print 'Device is gone:', udn

    for dev in devices:
        if dev.udn == udn:
            devices.remove(dev)


def create():
    c = ControlPoint()
    c.subscribe('new_device_event', on_new_device)
    c.subscribe('removed_device_event', on_removed_device)
    return c


def list_devices(devices):
    count = 0
    for d in devices:
        print 'Device number: ', count
        print_device(d, 1)
        print
        count += 1

def print_device(dev, indent=1):
    print '\t'*indent, 'UDN (id): ', dev.udn
    print '\t'*indent, 'Name: ', dev.friendly_name
    print '\t'*indent, 'Type: ', dev.device_type
    print '\t'*indent, 'Services: ', dev.services.keys()
    print '\t'*indent, 'Embedded devices: '
    for d in dev.devices.values():
       if d.device_type == 'urn:schemas-upnp-org:device:BinaryLight:1':  
          print_device(d, indent+1)
          print

def list_services(dev):
    count = 0
    for k, serv in dev.services.items():
        print 'Service number: ', count
        print 'Service id: ' + serv.id
        print
        count += 1


def main():
    c = create() # create control point
    c.start()
    reactor.add_after_stop_func(c.stop)
    run_async_function(run, (c, ))
    reactor.main()


def run(c):
    c.start_search(600, 'urn:schemas-micasaverde-com:device:HomeAutomationGateway:1') # async / threaded
    time.sleep(5) # necessary...
    list_devices(devices)

    c.stop_search()
    reactor.main_quit()

if __name__ == '__main__':
    main()
