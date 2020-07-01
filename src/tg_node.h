//
// Created by ZeqiLai on 2020/7/1.
//

#ifndef TOPOLOGYGENERATOR_TG_NODE_H
#define TOPOLOGYGENERATOR_TG_NODE_H

#include "tg_basic.h"

#define TG_MAX_INTERFACE_NUM   10

typedef struct tg_node_s tg_node_t;

typedef struct tg_egde_s{
    char*          edge_name;
    char*          src_ip;
    char*          dst_ip;
    /* link property. */
    uint32_t       uplink_bandwidth;
    uint32_t       downlink_bandwidth;
    uint32_t       uplink_RTT;
    uint32_t       downlink_RTT;
    uint32_t       uplink_lossy;
    uint32_t       downlink_lossy;
    /* end entry. */
    tg_node_t*     src_node;
    tg_node_t*     dst_node;
}tg_edge_t;


typedef struct tg_node_s{
    char*          node_name;
    uint16_t       node_type;
    tg_edge_t*     interface[TG_MAX_INTERFACE_NUM];

}tg_node_t;


#endif //TOPOLOGYGENERATOR_TG_NODE_H
