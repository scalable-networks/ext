#!/usr/bin/env python
#
# Copyright 2010 Ettus Research LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

########################################################################
# Template for raw text data describing write registers
# name addr[bit range inclusive] default optional enums
########################################################################
WRITE_REGS_TMPL="""\
########################################################################
## Note: offsets given from perspective of data bits (excludes address)
########################################################################
##
########################################################################
## N-Divider MSB (0) Write
########################################################################
frac                  0[7]          1       invalid, frac
n_divider_msb         0[0:6]        0
########################################################################
## N-Divider LSB (1) Write
########################################################################
n_divider_lsb         1[0:7]        0x23
~n_divider            n_divider_lsb, n_divider_msb
########################################################################
## Charge Pump (2) Write
########################################################################
cpmp                  2[6:7]        0
cplin                 2[4:5]        1
f_divider_mmsb        2[0:3]        0x2
########################################################################
## F-Divider MSB (3) Write
########################################################################
f_divider_msb         3[0:7]        0xF6
########################################################################
## F-Divider LSB (4) Write
########################################################################
f_divider_lsb         4[0:7]        0x84 
~f_divider            f_divider_lsb, f_divider_msb, f_divider_mmsb
########################################################################
## XTAL-Divider R-Divider (5) Write
########################################################################
#set $xtal_divider_names = ', '.join(map(lambda x: 'div' + str(x), range(1,9)))
xtal_divider          5[5:7]        0       $xtal_divider_names
r_divider             5[0:4]        1       
########################################################################
## PLL (6) Write
########################################################################
d24                   6[7]          1       div2, div4  ## div2 for LO <= 1125M, div4 > 1125M
cps                   6[6]          1       i_cp_from_icp, i_cp_from_vas
icp                   6[5]          0       i_cp_600ua, i_cp_1200ua
##reserved            6[0:4]        0
########################################################################
## VCO (7) Write
########################################################################
vco                   7[3:7]        0x19
vas                   7[2]          1       disabled, enabled
adl                   7[1]          1       disabled, enabled
ade                   7[0]          1       disabled, enabled
########################################################################
## LPF (8) Write
########################################################################
lp                    8[0:7]        0x4B    ## map(lambda x: "%0.2f"%((4e6 + (x - 12) * 290e3)/1e6), range(255)) in MHz
########################################################################
## Control (9) Write
########################################################################
stby                  9[7]          0       normal, disable_sig_and_synth
##reserved            9[6]          0
pwdn                  9[5]          0       normal, invalid
##reserved            9[4]          0
bbg                   9[0:3]        0       ## Baseband Gain in dB
########################################################################
## Shutdown (0xA) Write
########################################################################
##reserved            0xA[7]        0
pll_shutdown          0xA[6]        0       normal, shutdown
div_shutdown          0xA[5]        0       normal, shutdown
vco_shutdown          0xA[4]        0       normal, shutdown
bb_shutdown           0xA[3]        0       normal, shutdown
rfmix_shutdown        0xA[2]        0       normal, shutdown
rfvga_shutdown        0xA[1]        0       normal, shutdown
fe_shutdown           0xA[0]        0       normal, shutdown
########################################################################
## Test (0xB) Write
########################################################################
cptst                 0xB[5:7]      0
##reserved            0xB[4]        0
turbo                 0xB[3]        1
ld_mux                0xB[0:2]      0       refout=0, invalid
"""

########################################################################
# Template for raw text data describing read registers
# name addr[bit range inclusive] default optional enums
########################################################################
READ_REGS_TMPL="""\
########################################################################
## Status Byte-1 (0xC) Read
########################################################################
por                   0xC[7]        0       read, reset
vasa                  0xC[6]        0       vas_fail, vas_win
vase                  0xC[5]        0       active, inactive
ld                    0xC[4]        0       unlocked, locked
##reserved            0xC[0:3]      0
########################################################################
## Status Byte-2 (0xD) Read
########################################################################
vcosbr                0xD[3:7]      0       ## vco band readback
adc                   0xD[0:2]      0       ool0, lock0, vaslock0, vaslock1, vaslock2, vaslock3, lock1, ool1
"""

########################################################################
# Template for methods in the body of the struct
########################################################################
BODY_TMPL="""\
boost::uint8_t get_reg(boost::uint8_t addr){
    boost::uint8_t reg = 0;
    switch(addr){
    #for $addr in sorted(set(map(lambda r: r.get_addr(), $regs)))
    case $addr:
        #for $reg in filter(lambda r: r.get_addr() == addr, $regs)
        reg |= (boost::uint8_t($reg.get_name()) & $reg.get_mask()) << $reg.get_shift();
        #end for
        break;
    #end for
    }
    return boost::uint8_t(reg);
}

void set_reg(boost::uint8_t addr, boost::uint8_t reg){
    switch(addr){
    #for $addr in sorted(set(map(lambda r: r.get_addr(), $regs)))
    case $addr:
        #for $reg in filter(lambda r: r.get_addr() == addr, $regs)
        $reg.get_name() = $(reg.get_type())((reg >> $reg.get_shift()) & $reg.get_mask());
        #end for
        break;
    #end for
    }
}
"""

SPLIT_REGS_HELPER_TMPL="""\
#for $divname in ['n','f']
void set_$(divname)_divider(boost::uint32_t $divname){
    #for $regname in sorted(map(lambda r: r.get_name(), filter(lambda r: r.get_name().find(divname + '_divider') == 0, $regs)))
    #end for
}
#end for
"""
    #$regname = boost::uint8_t($divname & $regs[regname].get_mask());
    #$divname = boost::uint32_t($divname >> $regs[regname].get_shift());

if __name__ == '__main__':
    import common; common.generate(
        name='max2112_write_regs',
        regs_tmpl=WRITE_REGS_TMPL,
        body_tmpl=BODY_TMPL,
        file=__file__,
    )

    import common; common.generate(
        name='max2112_read_regs',
        regs_tmpl=READ_REGS_TMPL,
        body_tmpl=BODY_TMPL,
        file=__file__,
        append=True,
    )
