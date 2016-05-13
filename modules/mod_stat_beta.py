from libs.module import *
from libs.correl import *


class mod_stat_beta(CANModule):
    name = "Service discovery and statistic"

    help = """ """
    
    def do_init(self, params):
        self.all_frames = []
        self._cmdList['s'] = ["Show all fields", 0, "", self.show_fields, True]
        self.subnet = Subnet(lambda stream: Separator(SeparatedMessage.builder))

    def show_fields(self, zd):
        str = ""
        str += len(self.subnet._devices)
        for key, value in self.subnet._devices.items():
            str += "ECU: " + str(key) + ", INDEXES: " + str(value._indexes())
        return str

    # Effect (could be fuzz operation, sniff, filter or whatever)
    def do_effect(self, can_msg, args):
        if can_msg.CANData:
            print("X: "+str(can_msg.CANFrame))
            self.subnet.process(can_msg.CANFrame) # ADD NEW CAN MESSAGE
        return can_msg
