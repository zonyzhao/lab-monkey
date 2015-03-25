#!/usr/bin/env python

from common.base import *
from product.connection_adapters.abstract_adapter import SerialControlRegisterSession
from product.connection_adapters.fpga_adapter import FPGAAdapter
from io_ports.io_port_parallel import *


class FPGAParallelAdapter(FPGAAdapter):
    """
    Encapsulates the behavior by which a test board with an FPGA
    interface to the device under test manages orientation targeting and 
    SCR manipulation.
    """

    entity_name = 'fpga_parallel_adapter'
    entity_atts = []

    def __init__(self):
        # Prepare Parent
        super(FPGAParallelAdapter, self).__init__()
        
        # Set abstract properties
        self._type = 'Parallel FPGA'
        self._port = ParallelSocket()
        

    # Connection Management --------------------------


    @staticmethod
    def detect():
        """Trys to connect to the Parallel FPGA and returns True or False if it is able to connect."""
        if not ParallelSocket.detect():
            return False
        else:
            try:
                p = ParallelSocket()
                d = p.read(0)
            except:
                return False
            else:
                return True


    @property
    def state(self):
        """Returns the state of the parallel connection."""
        # TODO: Add in parallel I/O connection check
        if self._connected:
            return 'active'
        else:
            return 'no connection'
   

    def connect(self, package):
        """
        Initializes the FPGA and creates a new session for each SCR in the package
        """
        if self._connected == True:
            #self.log.info('Already connected.')
            pass
        else:
            #self.log.info('CONNECTING via %s' % self._type)
                      
            # Clear any errors
            self._clear_errors()
            
            # Initialize the buffers
            scr_length = package[0].width
            self._set_scr_length(scr_length)
            self._input_buffer  = list(package[0].value)
            self._output_buffer = list(package[0].value)
            
            # Connect the FPGA to the SCR
            self._scr_enable()
    
            # Set global defaults
            self.set_scr_clock_divider('fast')
            
            # Initialize SCR sessions
            for scr in package:
                
                # Validate target
                #if not self._is_valid_target(scr.label):
                #    raise ValueError('Could not create session for %s, the FPGA does not recognize it as a valid target.' % scr.label)
    
                # Create a virtual SCR session to manage state
                self._scr_sessions[scr.label] = SerialControlRegisterSession(scr)
                
                # Calculate and save the number of bytes it will take to represent this scr 
                self._byte_counts[scr.label]  = self._num_bytes(scr.width)
                
                # Set target specific defaults
                self.set_clock_source(scr.label, 'sma')
                       
            # Set connection state
            self._connected = True
            
            # Initialize the buffers to a target
            self._set_target(package[0].label)

   
    
    def test_me(self):

    #    OOOOOOOOOOOOOOOOOOOOOOOOOOOOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    #    Common Block ---------------------------------------------------------------------------------------->Lane 0 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 1 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 2 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 3 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 4 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 5 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 6 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->Lane 7 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->
              #    01234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567012345670123456701234567
              #           0       1       2       3       4       5       6       7       8       9      10      11      12      13      14      15      16      17      18      19      20      21      22      23      24      25      26      27      28      29      30      31      32      33      34      35      36      37      38      39      40      41      42      43      44      45      46      47      48      49      50      51      52      53      54      55      56      57      58      59      60      61      62      63      64      65      66      67      68      69      70      71      72      73      74      75      76      77      78      79      80      81      82      83      84      85      86      87      88      89      90      91      92      93      94      95      96      97      98      99     100     101     102     103     104     105     106     107     108     109     110     111     112     113     114     115     116     117     118     119     120     121     122     123     124     125     126     127     128     129     130     131     132     133     134     135     136     137     138     139     140     141     142     143     144     145     146     147     148     149     150     151     152     153     154     155     156     157     158     159     160     161     162     163     164     165     166     167     168     169     170     171     172     173     174     175     176     177     178     179     180     181     182     183     184     185     186     187     188     189     190     191     192     193     194     195     196     197     198     199     200     201     202     203     204     205     206     207     208     209     210     211     212     213
        
        #default = '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        #default = '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000001111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        default = '000000000000000000000000000010000000000010100000101000010100001010111111101010110010101010101111101010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010000000000000000000010001000000101100010101010101010101010100101010101010101111111110100101111011111010101110101000010101001010100110100000100010010101011100000000000000001010000100010001010100111001010'

        print 'Byte 41: %s' % default[41*8:41*8+8]
        print 'Byte 42: %s' % default[42*8:42*8+8]
        print 'Byte 43: %s' % default[43*8:43*8+8]

        scr_len = len(default)
    #    print 'Send SYS_CLK: %s' % sys_clk[start_bit_index:end_bit_index]
        
        self._write_input_buffer(list(default))        
        self._read_input_buffer(0, scr_len)

        input = ''.join(self._input_buffer)
        print 'inp: %s' % input
    #    self._write_input_buffer(list(sys_clk))
    #    self._read_input_buffer(0, scr_len)
    #    print 'BIB: %s' % ''.join(self._input_buffer)
    #    print 'Input SYS_CLK:\n%s' % ''.join(self._input_buffer[start_bit_index:end_bit_index])

        self._commit_input_buffer()
        self._populate_output_buffer()
        self._read_output_buffer(0, scr_len)
        
        out = ''.join(self._output_buffer)
        print 'out: %s' % out
        
        results = self.package.top.translate_register_string_delta(input, out)
        deltas = results['deltas']
        blocks = deltas.keys()
        blocks.sort()
        for block in blocks:
            print 'Block --------------------------------------- %s' % block
            for reg_key in deltas[block]:
                result = deltas[block][reg_key]
                reg = result['register']
                if reg.direction == 'I':
                    print '%s: %s -> %s' % (reg_key, result['a_value'], result['b_value'])
        
        print 'I: %s' % results['a_scr']
        print 'O: %s' % results['b_scr']
        print 'D: %s' % results['delta_map']
        
        modified = self._modified_byte_indexes(input, out)
        print 'modified: %s' % modified
        
if __name__=='__main__' :
    #from product.package import Package
    #dut = Package.from_txt_file(exepath('../repository/DES_65nm_Fuji.txt'), connect='Parallel FPGA')
    #dut.connection.test_me()
    pass