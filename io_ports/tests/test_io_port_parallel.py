#!/usr/bin/env python

"""Tests of the ParallelSocket class"""

from common.tests.pyunit_helpers import *
from unittest import TestCase, main

import yaml

from io_ports.io_port_parallel import *

class ParallelSocketTests(TestCase):
    """Tests of the ParallelSocket class"""
    
    FOUND = None
    
    def run(self, result=None):
        """Only run the io port tests when the adapter is detected"""
        if ParallelSocketTests.FOUND == True:
            super(ParallelSocketTests, self).run(result)
        elif ParallelSocket.detect():
            try:
                p = ParallelSocket()
                d = p.read(0)
            except Exception, e:
                # Parallel port found but returned no data.
                ParallelSocketTests.FOUND = False
            else:
                ParallelSocketTests.FOUND = True
                super(ParallelSocketTests, self).run(result)            
        else:
            ParallelSocketTests.FOUND = False
            #print 'FPGAparallelAdapter not detected.'


    def test_read_write(self):
        """Set and retrieve data"""
        
        INIT      = 0x04
        SELECT_IN = 0x08
        
        SI_CSR    = 0x30
        SI_MCTL   = 0x31
        SI_CFG_0  = 0x32
        SI_CFG_1  = 0x33
        SI_ADDR_0 = 0x34
        SI_ADDR_1 = 0x35
        SI_DATA   = 0x36
        SI_CNT_0  = 0x37
        SI_CNT_1  = 0x38
        SI_CSR    = 0x30
        SI_ST     = 0x02
        SI_ERR    = 0x01
        
        # Create Socket
        fpga = ParallelSocket()
               
        # SI_CFG_0
        fpga.write(SI_CFG_0, 0x20)        
        r = fpga.read(SI_CFG_0)
        self.assertEqual(r, 0x20)

        # SI_CFG_1
        fpga.write(SI_CFG_1, 0x0C)
        fpga.write(SI_CFG_1, 0x04)
        r = fpga.read(SI_CFG_1)
        self.assertEqual(r, 0x04)
    
        # SERDES CFG
        fpga.write(3, 0x1)
        r = fpga.read(3)
        self.assertEqual(r, 0x1)
        
        #r = fpga.read(SI_CSR)
    
        #for i in xrange(4):
        #    r = fpga.read(i)
        #    print r
      


if __name__ == '__main__':
    main()