//--------------------------------------------------------------------------
// Copyright (C) 2015-2016 Cisco and/or its affiliates. All rights reserved.
//
// This program is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License Version 2 as published
// by the Free Software Foundation.  You may not use, modify or distribute
// this program under any other version of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
//--------------------------------------------------------------------------
// tcp_ha.h author Ed Borgoyn <eborgoyn@cisco.com>

#ifndef TCP_HA_H
#define TCP_HA_H

#include "main/snort_types.h"
#include "stream/base/stream_ha.h"

//-------------------------------------------------------------------------

class Flow;

class TcpHA : public ProtocolHA
{
public:
    TcpHA() : ProtocolHA(PktType::TCP) { }
    void delete_session(Flow*);
    void create_session(Flow*);
    void deactivate_session(Flow*);

private:
};

class TcpHAManager
{
public:
    static void process_deletion(Flow* flow);
    static void tinit();
    static void tterm();
    static THREAD_LOCAL TcpHA* tcp_ha;
};
#endif

