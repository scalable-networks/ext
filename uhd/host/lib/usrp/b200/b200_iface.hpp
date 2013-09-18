//
// Copyright 2012-2013 Ettus Research LLC
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#ifndef INCLUDED_B200_IFACE_HPP
#define INCLUDED_B200_IFACE_HPP

#include <stdint.h>
#include <uhd/transport/usb_control.hpp>
#include <uhd/types/serial.hpp> //i2c iface
#include <boost/shared_ptr.hpp>
#include <boost/utility.hpp>
#include "ad9361_ctrl.hpp"

class b200_iface: boost::noncopyable, public virtual uhd::i2c_iface,
                  public ad9361_ctrl_iface_type {
public:
    typedef boost::shared_ptr<b200_iface> sptr;

    /*!
     * Make a b200 interface object from a control transport
     * \param usb_ctrl a USB control transport
     * \return a new b200 interface object
     */
    static sptr make(uhd::transport::usb_control::sptr usb_ctrl);

    //! query the device USB speed (2, 3)
    virtual boost::uint8_t get_usb_speed(void) = 0;

    //! get the current status of the FX3
    virtual boost::uint8_t get_fx3_status(void) = 0;

    //! get the current status of the FX3
    virtual boost::uint16_t get_compat_num(void) = 0;

    //! load a firmware image
    virtual void load_firmware(const std::string filestring, bool force=false) = 0;

    //! reset the FX3
    virtual void reset_fx3(void) = 0;

    //! reset the GPIF state machine
    virtual void reset_gpif(void) = 0;

    //! set the FPGA_RESET line
    virtual void set_fpga_reset_pin(const bool reset) = 0;

    //! load an FPGA image
    virtual boost::uint32_t load_fpga(const std::string filestring) = 0;

    //! send SPI through the FX3
    virtual void transact_spi( unsigned char *tx_data, size_t num_tx_bits, \
            unsigned char *rx_data, size_t num_rx_bits) = 0;
};


#endif /* INCLUDED_B200_IFACE_HPP */
