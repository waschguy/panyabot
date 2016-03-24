#!/usr/bin/python
# sendandreceivearguments.py
# Author: Adrien Emery
# Make sure the you have the SendAndReceiveArguments example loaded onto the Arduino
import sys
import serial

from cmdmessenger import CmdMessenger
from serial.tools import list_ports


class SendAndReceiveArguments(object):

    def __init__(self):
        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.baud = 115200
        # this method list is matched with the enumerator type on the Arduino sketch
        # always make sure to have them in the same order.
        self.commands = ['acknowledge',
                         'error',
                         'pin_set_state',
                         'command_result',
                         'lcd_print'
                         ]

        try:
            # try to open the first available usb port
            self.port_name = self.list_usb_ports()[0][0]
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0)
        except (serial.SerialException, IndexError):
            raise SystemExit('Could not open serial port.')
        else:
            print 'Serial port sucessfully opened.'
            self.messenger = CmdMessenger(self.serial_port)
            # attach callbacks
            self.messenger.attach(func=self.on_error, msgid=self.commands.index('error'))
            self.messenger.attach(func=self.on_command_result,
                                  msgid=self.commands.index('command_result'))

            # send a command that the arduino will acknowledge
            self.messenger.send_cmd(self.commands.index('acknowledge'))
            # Wait until the arduino sends an acknowledgement back
            self.messenger.wait_for_ack(ackid=self.commands.index('acknowledge'))
            print 'Edubot Ready'

    def list_usb_ports(self):
        """ Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('usb')]
        return ports

    def on_error(self, received_command, *args, **kwargs):
        """Callback function to handle errors
        """
        print 'Error:', args[0][0]

    def on_command_result(self, received_command, *args, **kwargs):
        """Callback to handle the Pin State Change success state
        """
        print 'State received:', args[0][0]
        print

    def stop(self):
        self.running = False

    def run(self):
        """Main loop to send and receive data from the Arduino
        """
        self.running = True
        while self.running:
            print 'Which command would you like to test? (1-Pin Set, 2-LCD Print) ',
            userchoice = raw_input()
            if (userchoice == "1"):
                print 'Enter Pin Number > ',
                a = raw_input()
                print 'Enter State > ',
                b = raw_input()
                print 'Sending: {}, {}'.format(a, b)
                self.messenger.send_cmd(self.commands.index('pin_set_state'), a, b)
            if (userchoice == "2"):
                print 'Enter LCD String > ',
                c = raw_input()
                print 'Sending: {}'.format(c)
                self.messenger.send_cmd(self.commands.index('lcd_print'), c)

            # Check to see if any data has been received
            self.messenger.feed_in_data()


if __name__ == '__main__':
    send_and_receive_args = SendAndReceiveArguments()

    try:
        print 'Press Ctrl+C to exit...'
        print
        send_and_receive_args.run()
    except KeyboardInterrupt:
        send_and_receive_args.stop()
        print 'Exiting...'