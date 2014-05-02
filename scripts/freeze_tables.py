#!/usr/bin/python
import rospy
from world_state.state import World, Object
from world_state.identification import ObjectIdentification

import world_state.objectmaster as objectmaster

from ros_datacentre.message_store import MessageStoreProxy

from strands_perception_msgs.msg import Table

if __name__ == '__main__':
    ''' Main Program '''
    rospy.init_node("table_freezer")
    
    w = World()
    om =  objectmaster.ObjectMaster()

    # Check that "Table is a type in the object master
    if not om.check_category_exists("Table"):
        rospy.loginfo("Object master doesnt know 'Table' type. Creating it.")
        om.add_category(objectmaster.ObjectCategory("Table"))
    
    tables =  w.get_objects_of_type("Table")
    rospy.loginfo("World state contains %d tables."%len(tables))
    
    message_proxy = MessageStoreProxy(collection="tables")
    table_list = message_proxy.query(Table._type)
    dc_tables = zip(*table_list)[0]
    rospy.loginfo("Message store contains %d tables."%len(dc_tables))

    rospy.loginfo("Freezing all tables")
    for t in dc_tables:
        name = t.table_id
        if w.does_object_exist(name):
            table = w.get_object(name)
#            rospy.loginfo("Table named '%s' already known."%name)
        else:
            rospy.loginfo("Freezing new table: %s"%name)
            table = w.create_object()
            table.name = name
        
        table.add_identification("TableDetection", ObjectIdentification({'Table':
                                                                      1.0}))