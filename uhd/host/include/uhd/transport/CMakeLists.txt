#
# Copyright 2010-2011 Ettus Research LLC
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


UHD_INSTALL(FILES
    bounded_buffer.hpp
    bounded_buffer.ipp
    buffer_pool.hpp
    if_addrs.hpp
    udp_simple.hpp
    udp_zero_copy.hpp
    usb_control.hpp
    usb_zero_copy.hpp
    usb_device_handle.hpp
    vrt_if_packet.hpp
    zero_copy.hpp
    DESTINATION ${INCLUDE_DIR}/uhd/transport
    COMPONENT headers
)
