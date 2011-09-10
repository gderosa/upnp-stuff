# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php or see LICENSE file.
# Copyright 2007-2008 Brisa Team <brisa-develop@garage.maemo.org>

import sys
import time

from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()

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
    c = create()
    c.start()
    reactor.add_after_stop_func(c.stop)
    run_async_function(run, (c, ))
    reactor.main()


def run_interactive(c):
    while True:
        #try:
        #    input_ = raw_input('>>> ').strip()
        #except KeyboardInterrupt, EOFError:
        #    break

        input_ = sys.stdin.readline().strip()

        if input_ == '':
            print
            continue

        elif input_ == 'test':
            print 'I am working!'

        elif input_ == 'list':
            list_devices(devices)

        elif input_ == 'exit':
            break

        elif input_ == 'search':
            c.start_search(600, 'upnp:rootdevice')

        elif input_ == 'stop':
            c.stop_search()

        elif input_.find('MyMethod') == 0:
            device = devices[int(input_.split(' ')[1])]
            k, service = device.services.items()[0]

            response = service.MyMethod(TextIn="In!!")
            print "Return:", response

        elif input_ == 'help':
            print 'Commands available: list, exit, ' \
            'search, stop, help, MyMethod'

    reactor.main_quit()


def run(c):
    c.start_search(600, 'ssdp:all') # async / threaded
    time.sleep(8) # necessary...
    list_devices(devices)
    c.stop_search()
    reactor.main_quit()

if __name__ == '__main__':
    main()
